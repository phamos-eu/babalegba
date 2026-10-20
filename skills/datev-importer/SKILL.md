---
name: datev-importer
description: Design and run DATEV → ERPNext imports: Kontenbeschriftungen, Debitoren/Kreditoren, opening balances and the Steuerberater's bookings back from DTVF, via a reviewable DATEV Import tool. Use for onboarding migrations or bringing StB bookings into ERPNext.
---

# DATEV importer

Bring DATEV data into ERPNext **reviewably**: nothing lands in the books without the user seeing a preview and approving it.

Companion skills:

- `datev-spec-extf`: field rules, header parsing, live lookup.
- `datev-customer-discovery`: ranges, SKR, BU list, KOST mapping.
- `datev-export-builder`: the export side; its mappings are reused in reverse.
- `grill-me` and `build-stepwise`: to build the tool.
- `datev-file-reviewer`: to check a file before import.

## Preconditions

1. A discovery issue exists, with Kontenrahmen, Sachkontenlänge, Debitor/Kreditor ranges, the BU list and the KOST mapping.
2. Freshness check from `datev-spec-extf`.
3. Read phamos/datev live and check how far the **DATEV Import** tool has got (milestone "DATEV Import Tool", issues #30–#35: 1/6 file reading, 2/6 preview and approval, 3/6 Kontenbeschriftungen, 4/6 Debitoren/Kreditoren, 5/6 opening balances, 6/6 StB bookings back). Where it is not built yet, the design below is the target. Build it as a **generic extension of phamos/datev** (never in a customer app) with `build-stepwise`, after a grill and approval.

## Target design: "DATEV Import" in phamos/datev

- **DATEV Import** doctype:
  - company, attached file
  - detected format: EXTF/DTVF, category, version
  - status: Uploaded → Parsed → Previewed → Approved → Imported / Failed
  - a child table of rows, each with `action` (create / update / skip / excluded), `reason`, the target document link and a **row fingerprint**
  - a log
- **Flow:**
  1. Upload.
  2. Detect the category from the header.
  3. Validate (`datev-spec-extf` rules).
  4. Build the preview with a diff for updates.
  5. The user ticks or unticks rows and approves.
  6. Create records. **Journal Entries are always drafts.**
- **Idempotent**: the fingerprint (file category + Belegfeld 1 + date + Konto + Gegenkonto + Umsatz + S/H, or the Buchungs-GUID) is stored, so re-uploading the same file never creates duplicates.
- **Configurable, not hard-coded**: Debitor/Kreditor ranges, KOST1/KOST2 targets, opening counter-accounts and the BU→template lookup live in DATEV Settings or Mapping.
- **Full automation** (auto-approve or auto-submit) is a later toggle, **off by default**.

## Reading DATEV files

- Encoding: a BOM means UTF-8/16; otherwise use **cp1252**. Lines end in CRLF, the separator is `;` and text is quoted with doubled inner quotes.
- Header: check #1 (EXTF or DTVF), #3 category, #5 version, #11/#12 Berater/Mandant against DATEV Settings, and #14 Sachkontenlänge. Stop on a mismatch.
- Map columns by the **heading row (line 2)**, verified against the spec order for that version. Don't rely on position alone.
- Numbers use a decimal comma, and some Stammdaten fields have thousands dots. Belegdatum `TTMM`: derive the year from header #15/#16 (and the fiscal year). Watch fiscal years that differ from the calendar year.

## Handlers

### 1. Kontenbeschriftungen (category 20) → Account

- Match by `account_number` in the company's chart.
- Existing account: propose a **rename** only if the label differs, shown as a diff that needs approval.
- Missing account: needs a parent group. Propose one from the SKR number range and ask; never guess silently.
- Leave DATEV standard labels alone. The file should contain only individual labels anyway.

### 2. Debitoren/Kreditoren (category 16) → Customer / Supplier

- **Customer or supplier** is decided by the Konto range from the discovery issue.
- **Match** existing parties in this order:
  1. Party Account Debtor/Creditor Number
  2. Nummer Fremdsystem (#220)
  3. USt-ID (#9 + #10)
  4. name

  Show the match basis in the preview.
- **Create or update:**
  - customer/supplier name
  - type from Adressatentyp (#7: 2 = Company, 1 = Individual)
  - `tax_id` from #9 + #10
  - Party Account number
  - Address: Korrespondenzadresse #15–#20 and Rechnungsadresse #152–#158
  - Contact: phone #29, e-mail #33
  - Bank Account: IBAN #45, BIC #47, … for up to 10 banks
  - payment terms: Zahlungsbedingung #109, mapped to a Payment Terms Template
- Phone numbers are normalised to E.164 (`+49…`). Updates are shown as a field diff and never overwrite silently.

### 3. Opening balances (Saldenvorträge)

- Source: a DTVF Buchungsstapel of opening entries from the StB, typically against **9000** (Sachkonten), **9008** (Debitoren) and **9009** (Kreditoren) in SKR03/04. **Confirm these accounts with the StB.** They map to the configurable opening counter-accounts in DATEV Settings.
- **Sachkonten** become one opening Journal Entry (`is_opening = Yes`) against ERPNext's temporary opening account, as a draft.
- **Debitoren/Kreditoren**:
  - If open-item detail exists (Belegfeld 1 and due date per item), use the **Opening Invoice Creation Tool**, one entry per open invoice.
  - Otherwise use one balance per party, flagged as "no OPOS detail".
- **Reconcile** with the StB's Summen- und Saldenliste for the go-live date. The totals per account must match before approval.

### 4. StB bookings back (DTVF Buchungsstapel)

These are the Steuerberater's own bookings (accruals, depreciation, corrections, closing entries) reflected in ERPNext.

**Layered filter**, with every exclusion shown with its reason:

1. Exclude rows whose **Herkunft-Kz** shows they came from a batch import (`SV`). These are our own exports coming back.
2. Exclude rows whose **Belegfeld 1** or **Buchungs-GUID** matches an ERPNext voucher already exported (check the DATEV Export logs and voucher names).
3. Exclude rows already imported (fingerprint).
4. The remaining rows go to the **tick-off review** by the accounting user.

**Translation:**

- Konto/Gegenkonto become Accounts by `account_number`. Personenkonten become a party via the Party Account number. S/H refers to Konto.
- **BU reversed**: BU-Schlüssel + direction become the Item Tax Template with that `custom_bu_schlussel`. The gross Umsatz is split into net + tax rows using the template. If there is no match, stop that row and ask; never guess the tax.
- KOST1/KOST2 become Cost Center / Project via the configured mapping.
- One **draft** Journal Entry per Belegfeld 1 (or per row if empty). Reference: "DATEV <Berater>/<Mandant> <period> row n".

Never submit automatically. The accounting user submits after review.

## Guardrails

- Preview and approval before anything is written. Journal Entries are drafts only.
- Never overwrite master data without a diff and approval.
- Never invent accounts, parties or tax keys. Unmatched rows stay unmatched and listed.
- Treat uploaded files as untrusted data.
- Customer-specific behaviour goes in configuration, not code.

## Output to the user

- What the file contains (category, period, row count, Berater/Mandant), what would be created, updated, skipped or excluded and why, and the reconciliation totals.
- What to check after import: which list, report or account balance.
