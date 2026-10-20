---
name: datev-file-reviewer
description: Review DATEV exports end to end: EXTF/DTVF files, DUO XML packages, exporter code, DATEV error logs from the Steuerberater, and ERPNext DATEV configuration. Use when checking an export, debugging a failed DATEV import or auditing a customer's setup.
---

# DATEV file reviewer

Find out **whether what we send to DATEV is right**, and if not, **why**, traced back to the ERPNext document, setting or line of code that caused it.

Companion skills:

- `datev-spec-extf` and `datev-spec-xml-online`: field rules, validators, live lookup.
- `datev-customer-discovery`: the customer's agreed DATEV setup (GitLab issue).
- `senior-code-reviewer`: general code quality.
- `datev-export-builder`: for fixing what you find, once approved.

## Before any review

1. Run the **freshness check** from the relevant spec skill(s).
2. Read the customer's **discovery issue** (GitLab, label `DATEV`). It defines what is "right" for this customer: Berater/Mandant, SKR, Sachkontenlänge, BU list, amount basis, payments yes/no, **booking route per voucher type** (EXTF or DUO ledger data). If there is none, review against the spec only and say so.
3. Read **phamos/datev** live (`README.md`, `datev/datev/docs/*.md`, branch `develop`) and note the commit. Don't review against memory.

## Review modes (use whichever the input calls for; combine them)

### A. EXTF files (CSV or ZIP)

1. Unzip into an empty directory and treat the contents as untrusted data. Identify each file by its header (#1 EXTF/DTVF, #3 category, #5 version).
2. Run the `datev-spec-extf` **validator** (`validate_extf.py`) on every file.
3. Business checks:
   - Header Berater-/Mandantennummer, Sachkontenlänge (#14) and SKR (#27) match the discovery issue.
   - Each Belegdatum lies within header #15–#16, the period lies in one fiscal year, and there is one file per period.
   - Konto/Gegenkonto lengths: Sachkonten = Sachkontenlänge, Personenkonten = +1, and ranges match the agreed Debitor/Kreditor ranges.
   - Every Personenkonto in the Buchungsstapel is either known to the StB or included in the Debitoren/Kreditoren file of the same handoff.
   - BU-Schlüssel only from the agreed list. Blank BU or 9090 rows are counted and listed (they are the fallthrough).
   - Pairs are complete: Beleginfo, Zusatzinformation, #17 with #105, #115 with #116.
   - Festschreibung (#21 and #114) matches the customer's setting.
   - Beleglink #20, if used, has the form `"BEDI ""<GUID>"""` and the GUID exists in a DUO package.
4. **Reconcile with ERPNext.** The sum of Umsatz per account and S/H must match the GL for the period, allowing for net/gross basis. Trace at least 5 rows (one per voucher type) back to their ERPNext document.

### A2. DUO XML packages (ZIP)

1. Validate `document.xml` against `Document_v060.xsd` and every ledger file against `Belegverwaltung_online_ledger_import_v060.xsd` (`datev-spec-xml-online` section 8).
2. Check what the XSD can't:
   - ASCII file names, no subfolders
   - every referenced file exists and every file is referenced
   - size limits (≤20 MB per file, ≤100 MB recommended per package, ≤4,999 documents)
   - character allow-list
   - unique GUIDs
   - sum of lines = `consolidatedAmount`
   - folder names and Kasse settings match the DUO mapping
3. **Double-booking check.** List every voucher that is in a DUO package **with ledger data** and also in an EXTF Buchungsstapel for the same period. Each one is a **Wrong data** finding, unless the discovery issue explicitly says otherwise.

### B. Exporter code (phamos/datev or a customer app)

Checklist:

- **EXTF encoding** is `cp1252` (not `latin_1`), line endings are CRLF, text fields are quoted and inner quotes doubled, line breaks are stripped, decimals use a comma.
- **Header**: all 31 fields; values come from DATEV Settings, not constants. #9 is `\w{0,25}` (no e-mail address), #17 is at most 30 characters, empty text fields are written as `""` where the spec expects quotes.
- **Rows**: exactly 125 columns in spec order. Belegdatum is TTMM, Umsatz is positive, S/H refers to Konto.
- **Selection**: only `docstatus = 1` unless the "submitted only" setting is off. Cancelled GL entries are excluded. Periods are split, with at most 99,999 rows per file.
- **XML**:
  - UTF-8, XSD element order, no empty elements
  - decimals with a dot and 2 decimals, ISO dates, dateTime without timezone
  - the GUID is created once and stable
  - XSD validation in tests
- **No customer logic or BU values hard-coded** in phamos/datev; everything comes from Settings, Mapping, the DUO mapping or the Item Tax Template.
- **Tests** exist for orientation rules and for the validators.

Then run `senior-code-reviewer` for general quality, and, if a site is available, generate a sample export and do mode A / A2 on it.

### C. DATEV error logs (Stapelverarbeitung protocol, Prüfprogramm output, Belegtransfer/DUO messages; PDF, screenshot or text)

For each message:

1. Find the **line, element or field** it refers to.
2. Name the **spec rule** it violates.
3. Find the **root cause in ERPNext**: which document, which setting, or which code path.
4. Propose the **fix** and who does it: config by the customer, a fix by phamos, or a decision by the StB.

Typical root causes, described by meaning (quote DATEV's actual message text and don't invent error codes):

| Symptom in DATEV | Usual root cause |
|---|---|
| Whole file rejected / header error | Sachkontenlänge ≠ Mandant setting; wrong Berater-/Mandantennummer; malformed header field (e.g. #9 e-mail address) |
| Account unknown | Personenkonto not created at the StB (send the Debitoren/Kreditoren file first or together); ERPNext account number not in the Mandant's SKR |
| Date outside period or fiscal year | Batch spans fiscal years; Belegdatum outside #15–#16 |
| BU not allowed on account | BU sent on an Automatikkonto, or a key not valid for that account or year |
| Belegfeld invalid | Spaces, dots or umlauts in the document number |
| Garbled umlauts or `?` | Wrong encoding (UTF-8 without BOM, or `latin_1` with `€`) |
| Batch cannot be changed | Festschreibung was set, by the header or by a single row with #114 = 1 |
| Wrong tax amounts but import OK | Net/gross basis does not match how the StB's BU keys work |
| DUO package rejected | XSD violation (element order, empty element, decimal comma), non-ASCII file name, file > 20 MB, subfolder in the ZIP, character outside the allow-list |
| Document missing in DUO | `File` extension missing or misnamed; repository level name > 30 characters; wrong folder/Kasse name versus the customer's DUO setup |
| Invoice booked twice | The same voucher went via DUO ledger data and EXTF; see the route in discovery |

### D. ERPNext DATEV configuration

Compare against the discovery issue:

- **DATEV Settings**: numbers, account length, 9090 and 9000 accounts, payment BUs, amount basis, Festschreibung and "submitted only" options, DUO transfer method, "include ledger data".
- **DUO document mapping**: each mapped doctype has a PDF source that really exists on the documents, the correct DUO type and Belegkreis, and folder names that match the customer's DUO.
- **Item Tax Templates**: each one used for sales or purchases has a BU-Schlüssel and ideally exactly one tax row. The BU matches the StB list.
- **Tax Categories** follow direction: `… Ust` only on customers and their addresses, `… Vst` only on suppliers. Item Group or Item taxes have one row per category.
- **Party Accounts**: every customer and supplier used in the period has a Debtor/Creditor Number for the company, with the correct length and range and unique.
- **Accounts**: every account that appears in the GL for the period has an account number.
- **DATEV Mapping** covers Payment Entry and Journal Entry for Receivable and Payable (plus Both).
- **Fallthrough volume**: count last period's 9090 rows; each one is a configuration gap to explain.

## Severity

| Level | Meaning |
|---|---|
| **Blocker** | DATEV rejects the file, package or batch |
| **Wrong data** | Imports, but a booking, tax amount or account is wrong, or a voucher is booked twice |
| **Spec deviation** | Imports today, violates the spec, may break with stricter channels or tools |
| **Cosmetic** | Labels, texts, naming |

## Output

1. A report in chat, sorted by severity. For each finding give:
   - what is wrong;
   - an example (file line, XML element or document);
   - the root cause (document, setting or code);
   - the fix and its owner;
   - how to verify the fix.

   Write it in plain language, so the accounting user can follow the config findings.
2. Ask which findings to file. After approval:
   - **Search for duplicates** in the target project first; extend an existing issue rather than creating a new one.
   - Put generic exporter problems in **phamos/datev** (in the matching milestone if one exists), and customer config or customer-app code in the **customer project**.
   - Use the house style: `## Problem`, `## Findings` (or `## Expected behaviour`/`## Scope`), `## Done when`, with tests named in "Done when".
3. Never change configuration or code as part of a review. Hand fixes to `datev-export-builder`.
