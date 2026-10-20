---
name: datev-export-builder
description: Plan and build ERPNext → DATEV exports (EXTF Buchungsstapel and Stammdaten, plus DUO document packages once available) for a customer on top of the phamos/datev app, configuration-first, with validation gates. Use when setting up, extending or fixing a customer's DATEV export.
---

# DATEV export builder

Build a customer's ERPNext → DATEV export **on top of the phamos/datev app** (`git.phamos.eu/phamos/datev`), solving as much as possible through **configuration**, step by step, with the user approving each step.

Companion skills:

- `datev-customer-discovery`: required input (GitLab issue).
- `datev-spec-extf`: field rules, live spec lookup, validator.
- `datev-spec-xml-online`: DUO document packages (PDF + GUID, optional ledger data).
- `grill-me` and `build-stepwise`: phamos' planning and increment workflow.
- `erpnext-functional-consultant`: before adding any custom field or script.
- `senior-code-reviewer`: before committing.

## Preconditions (check, don't assume)

1. **Discovery issue** exists in the customer's GitLab project and has no open ⛔ blocking item, including the **booking route per voucher type** (EXTF or DUO ledger data, never both). If it is missing or blocked, stop and offer `datev-customer-discovery`.
2. **Spec is current**: run the freshness check from `datev-spec-extf` (and `datev-spec-xml-online` for DUO work).
3. **phamos/datev is read live**: `README.md`, `datev/datev/docs/*.md` (especially `accepted_export_contract.md`, `export_modes.md`, `tax_category_training.md`), `datev/utils/datev_csv.py`, `datev/utils/datev_constants.py`, and the DATEV Settings doctype JSON on branch `develop`. Note the commit you read. The repo is the source of truth; the summary below may be stale.

## What phamos/datev already provides (as of 2026-10; verify live)

Frappe/ERPNext v16. It provides:

- **DATEV Settings** per company: Beraternummer, Mandantennummer, account number length, 9090 against account, 9000 opening account, BU for incoming/outgoing payments, net/gross amount basis.
- **DATEV Mapping**: which document field goes into which DATEV column, per voucher type and direction (Receivable / Payable / Both, with fallback to Both).
- **Consultant Booking** mode. It groups SI/PI/PE/JE into Konto/Gegenkonto/BU rows, following the frozen **accepted export contract**:

  | Voucher | Konto | Gegenkonto | S/H |
  |---|---|---|---|
  | Sales Invoice | Erlöskonto | Debitor | H |
  | Purchase Invoice | Aufwand | Kreditor | S |
  | PE Receive | Bank | Personenkonto | S |
  | PE Pay | Personenkonto | Bank | S |
  | JE sales | Erlöskonto | Debitor | H |
  | JE purchase | Aufwand | Kreditor | S |

  The contract may change only after a new grill round.
- **BU-Schlüssel** on the Item Tax Template; direction is chosen via Tax Category (`… Ust` for customers, `… Vst` for suppliers).
- **Fallthrough**: ungroupable vouchers are exported against 9090, usually with a blank BU, for the StB to review.
- **DATEV Export** doctype (one ZIP per period, logged; a re-export asks for confirmation), the `/desk/datev` page, and the **DATEV** preview report.
- Custom fields shipped as fixtures (DATEV Account No, BU-Schlüssel, Debtor/Creditor Number on Party Account, …).
- Planned, check the milestones before assuming: Festschreibung setting and period lock (#25), header/encoding fixes (#28), draft vouchers in test exports (#29), DATEV Import tool (milestone "DATEV Import Tool"), DUO document packages and Beleglink (milestone "DUO xml").

## Workflow

### 1. Fit-gap (plain language)

Walk the discovery issue and classify each requirement:

| Requirement | Solution | Type | What the user will see/test |
|---|---|---|---|
| e.g. SKR04, Sachkonten 4-digit | DATEV Settings: account length 4 | Config | Header shows `4` / `"04"` |
| e.g. EU deliveries with USt-ID | Tax Category `EU Ust` + Item Tax Template with StB's BU | Config | Preview row has BU + #40 USt-ID |
| e.g. KOST1 from Cost Center | DATEV Mapping column or generic extension | Config / Generic MR | KOST1 filled in preview |

Order of preference:

1. **Config**: Settings, Mapping, Tax Category, Item Tax Template, Party Account, DUO document mapping.
2. **Generic extension to phamos/datev** (MR): a new *setting* rather than code paths per customer. No hard-coding.
3. **Customer app**: only for truly customer-specific behaviour. Never put customer logic into phamos/datev.

Present the table to the user and wait for approval before any change.

### 2. Plan increments (`build-stepwise`)

Each increment must be small, testable and understandable for the accounting user. A typical order:

1. Settings + master data.
2. Sales Invoices.
3. Purchase Invoices.
4. Payments.
5. Journal Entries.
6. Stammdaten files.
7. Special cases (EU/§13b/Anzahlungen).
8. DUO documents (if the customer uses the XML package).

Where automation is possible (e.g. auto-filling DATEV account numbers on save), make it a **toggle in DATEV Settings**, not a forced behaviour. Grill the plan (`grill-me`) and get explicit approval before any code.

### 3. Configure

Guide the user through the configuration in non-technical words, with what to check afterwards in the DATEV preview report. Write configuration records only after approval. Prefer showing the user where to click over changing a production site silently.

### 4. Extend (only if config can't cover it)

- Frappe/ERPNext standards. Custom fields go in fixtures. Everything configurable; no customer constants in code.
- Use `erpnext-functional-consultant` before adding fields or scripts.
- Tests for every grouping and orientation rule, plus a validator test (below).
- Run `senior-code-reviewer` before committing. MRs get a good description and a **testing plan**, and are scoped narrowly. Work locally unless the user says to push.

### 5. Validate: the three gates (all required before "done")

1. **Regex self-check.** Generate an export for the sample month and run the `datev-spec-extf` validator (`validate_extf.py`) on every CSV; validate DUO XML against the XSD (`datev-spec-xml-online`). Add both as automated tests. Also check:
   - Belegdatum lies within the batch period, and the batch lies within one fiscal year.
   - Account lengths: Personenkonto = Sachkontenlänge + 1.
   - Exactly 125 fields per Buchungsstapel row; at most 99,999 rows per file.
   - CP1252 encoding (not `latin_1`), CRLF line endings.
   - Header #9 is `\w` only (no e-mail address); #17 is at most 30 characters.
2. **Steuerberater test import.** The StB imports the sample month into a **test Mandant** (and a test DUO client for packages) and confirms Konto, Gegenkonto, BU and tax amounts. Record the result in the discovery issue.
3. **Accounting user sign-off.** The customer's accounting user compares the DATEV preview report for the sample month with their expectations and signs off. Record it in the issue.

## Hard rules (always)

- **Never invent BU-Schlüssel, account numbers or account mappings.** They come from the StB (via the discovery issue). If missing, export with a visible gap (blank BU / 9090) and list it, or stop and ask.
- **One file per period**, never more than **99,999 rows** per Buchungsstapel file. Split if needed.
- **Never send test files to the productive Mandant.**

## Settings-driven behaviour (not hard rules)

Implement these as options in **DATEV Settings**. If phamos/datev does not have them yet, propose a generic MR:

| Setting | Default | Purpose |
|---|---|---|
| **Festschreibung** | **0** (not locked) | Header #21 (and row #114 left empty or 0). Set to 1 only when the StB explicitly wants it. DATEV's own default is 1! |
| **Submitted vouchers only** | **On** | When off (implementation/testing only), drafts are included. The file and the DATEV Export record must be clearly marked as TEST (e.g. Bezeichnung `TEST …`, file name suffix) |

## DATEV pitfalls to check in every build

- **S/H refers to Konto (#7)**, and Umsatz is always positive.
- **Gross vs net**: with BU-Schlüssel or Automatikkonten, DATEV normally expects **gross** Umsatz. Confirm with the StB and set amount basis accordingly.
- **Payments double-booked**: if the StB also books bank data, don't export Payment Entries.
- **Invoices double-booked**: if a voucher type is routed to DUO ledger data, it must not be in the Buchungsstapel.
- **Belegfeld 1**: ERPNext names like `ACC-SINV-2026-00001` are fine. Spaces, dots and umlauts are not. Keep it the OPOS key (invoice number).
- **Buchungstext** at most 60 characters, **Bezeichnung** at most 30. Strip line breaks from texts. Double any quotes.
- **Encoding cp1252**: `€` breaks under `latin_1`.
- **Cancelled and amended vouchers**: exclude cancelled GL entries. Agree with the StB how corrections of already-exported periods are delivered (delta batch vs re-export).
- **Personenkonto** from the Party Account (Debtor/Creditor Number) per company. Fallback: the receivable/payable account. Make sure the StB knows which.
- **Header Sachkontenlänge** must equal the Mandant's setting, or the whole import fails.

## Output to the user at each step

- What will change, in plain words (no code unless asked).
- Where to test it: which page or report, which voucher, which expected DATEV row.
- What is still open, with a pointer to the discovery issue.
