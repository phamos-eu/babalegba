---
name: datev-customer-discovery
description: Run a structured DATEV discovery for an ERPNext customer (Steuerberater setup, SKR, account lengths, tax keys, OPOS, payments, KOST, DUO route) and record it as a GitLab issue. Use before any DATEV export/import work for a customer.
---

# DATEV customer discovery

Find out **how this customer's DATEV world works** before anyone builds or changes an export. The output is a **GitLab issue in the customer's project** that `datev-export-builder`, `datev-file-reviewer` and `datev-importer` rely on.

Mindset: the customer's accounting clerk and their **Steuerberater (StB)** own the truth. Never copy answers from another customer (e.g. Gärtnerei Berger) as facts. Similar customers may be named as *inspiration* only, clearly labelled.

## When to use

- A new customer needs DATEV exports, DUO transfers or imports.
- An existing customer changes Steuerberater, chart of accounts, fiscal year, tax situation (EU, OSS, §13b, …) or its DUO route.
- A builder or reviewer finds no discovery issue, or finds one with open blocking items.

## Process

1. **Find an existing issue first.** Search the customer's GitLab project for an issue labelled `DATEV` / titled `DATEV Discovery`. If one exists, update it rather than duplicating it.
2. **Read before asking.** Collect what the system already shows, and present it as "found in system, please confirm":
   - Company: `chart_of_accounts` (SKR03/SKR04), default currency, fiscal year start, and account number lengths in the CoA.
   - Existing **DATEV Settings** (phamos/datev): Beraternummer, Mandantennummer, account length, 9090 account, payment BUs, net/gross, DUO transfer method and DUO document mapping.
   - Tax Categories, Item Tax Templates (and whether they carry a BU-Schlüssel), Sales/Purchase Taxes templates.
   - Customers/Suppliers: is a Debtor/Creditor Number (Party Account) maintained? What ranges are used?
   - Which vouchers exist in volume: Sales/Purchase Invoice, Payment Entry, Journal Entry, Expense Claim, POS. Do Purchase Invoices and Expense Claims carry the original PDF?
   - Cost Centers / Projects (candidates for KOST1/KOST2).
3. **Grill**, one question at a time, in the order of the sections below. After each answer: summarise it, flag contradictions, and state the recommended position. Questions only the StB can answer go on the **StB question list** instead of being guessed.
4. **Fit-gap against phamos/datev.** For each requirement, mark how it would be covered:
   - **Config**: DATEV Settings, DATEV Mapping, Tax Category, Item Tax Template BU, Party Account number, DUO document mapping.
   - **Generic extension**: an MR to phamos/datev that would benefit every customer.
   - **Customer app**: truly customer-specific.

   Read phamos/datev's `README.md` and `datev/datev/docs/*.md` live from GitLab (`phamos/datev`, branch `develop`). Don't rely on memory.
5. **Write or update the GitLab issue** (template below). Show the draft to the user before creating or updating it.
6. **Hand over.** When no **blocking** item is open, the issue is "ready for build". Suggest `datev-export-builder` (or `datev-importer`).

## Question sections

Mark each answer `✅ confirmed`, `🔎 found in system – confirm`, `❓ open – StB`, `❓ open – customer` or `⛔ blocking`.

### A. People and handoff

- Steuerberater firm, contact person, e-mail. Who at the customer owns accounting?
- How do **bookings** reach DATEV? Options: ZIP by mail or portal to the StB (who imports via Stapelverarbeitung), or automated via the `accounting:extf-files` API.
- Does the customer use **DATEV Unternehmen online (DUO)**? If yes, how do **documents** get there:
  - **Mail**: PDF only, to the DUO upload addresses.
  - **XML package**: PDF + GUID via DATEV Belegtransfer; see `datev-spec-xml-online`.
- Rhythm (monthly? until which working day?) and who triggers the export.

### B. DATEV Mandant master data (StB)

- **Beraternummer** (4–7 digits) and **Mandantennummer** (1–5 digits).
- **Kontenrahmen**: SKR03 / SKR04 / other (SKR14 agriculture → Naturalstapel?). Does it match the ERPNext CoA?
- **Sachkontenlänge** (4–8). Personenkonten are then Sachkontenlänge + 1 digits.
- **Wirtschaftsjahr** start; is it different from the calendar year?
- **Versteuerung**: Soll or Ist? Kleinunternehmer? Special DATEV Branchenlösung?
- Which DATEV version does the StB run? This decides the supported Buchungsstapel format version.

### C. Scope

- Which data goes to DATEV? Buchungsstapel only, or also Stammdaten (Debitoren/Kreditoren, Sachkontenbeschriftungen)?
- Which vouchers: Sales Invoice, Purchase Invoice, Payment Entry, Journal Entry, Expense Claim, POS/cash?
- Go-live date and first period. Opening balances: who books them, and where?

### D. Booking logic (the heart, mostly StB)

- **⛔ Booking route per voucher type**: is each voucher type booked from the **EXTF Buchungsstapel** or from **DUO ledger data** (XML package with booking data, StB books in DUO)? A voucher type must **never** go both ways, or it is booked twice. The app has no technical guard for this; this answer is the guard. The default is EXTF for all bookings, with DUO receiving documents only (Beleglink).
- **OPOS**: does the StB keep open items per Debitor/Kreditor? If yes, Belegfeld 1 = invoice number (charset rules!) and individual Personenkonten are needed. If no, are collective accounts acceptable?
- **Personenkonten numbering**: ranges (DATEV standard with 4-digit Sachkonten: Debitoren 10000–69999, Kreditoren 70000–99999). Who assigns them: ERPNext or the StB? Are existing numbers to be migrated?
- **Revenue/expense accounts**: does the ERPNext account number = the DATEV account? Any mapping needed?
- **Tax**: which BU-Schlüssel per tax situation, *or* Automatikkonten (no BU needed)? Get the **list from the StB**. Never guess.
- **Amount basis**: does the StB expect **gross** Umsatz with BU/Automatik (DATEV standard) or net? This maps to the phamos/datev net/gross setting.
- **Payments**: should ERPNext export Payment Entries, or does the StB book the bank from DATEV bank data (Bankdaten-Service)? ⚠ Both at once means **double-booked payments**. This is ⛔ blocking until answered.
- **Skonto** handling (Skonto field vs. separate booking; Abw. Skontokonto?).
- **Special cases**: EU deliveries/purchases (USt-ID), OSS, §13b reverse charge, foreign currency, down payments (Anzahlungen/Schlussrechnung), credit notes, cancellations (omit vs. Generalumkehr).
- **Corrections after export**: how does the StB want late corrections? A new batch with only the delta, or a full re-export after deleting the batch in DATEV?

### E. Optional DATEV features

- **KOST1/KOST2**: used? Mapped from Cost Center / Project? KOST length in DATEV?
- **Festschreibung**: does the StB want batches locked on import? (phamos default: 0 = not locked.)
- **DUO details** (if XML package):
  - Which doctypes carry a PDF (print format or original attachment)?
  - Invoice folder names and Kassenkontonummer / Kassenbezeichnung as configured in DUO.
  - Repository folders (Kategorie / Ordner / Register).
  - Is ledger data wanted (route B), and for which types?
  - Who uploads with DATEV Belegtransfer, and do they have a DATEV SmartCard/login?
- **Leistungsdatum** (#115/#116): only if the StB asks.
- **Stammdaten sync**: is Nummer Fremdsystem (#220) used to carry the ERPNext ID?

### F. Test and acceptance

- Is there a **test Mandant** at the StB for test imports, and a test DUO client?
- Which **sample month** is the reference? Who signs off on the customer side (accounting user) and on the StB side?
- Implementation phase: should draft vouchers be exportable for testing (phamos/datev "submitted vouchers only" switched off)? Test files must never go into the productive Mandant.

## GitLab issue template

Title: `DATEV Discovery – <Company>`. Labels: `DATEV`, `Discovery`.

```markdown
## Context
Customer: … | Company: … | Steuerberater: … (contact) | Prepared by: … | Date: …
Bookings handoff: … | DUO: no / Mail / XML package | Rhythm: …

## DATEV Mandant
| Item | Value | Status |
|---|---|---|
| Beraternummer | | |
| Mandantennummer | | |
| Kontenrahmen | | |
| Sachkontenlänge / Personenkontenlänge | | |
| WJ-Beginn | | |
| Versteuerung (Soll/Ist) | | |
| DATEV version at StB | | |

## Scope
- [ ] Buchungsstapel – vouchers: …
- [ ] Debitoren/Kreditoren
- [ ] Sachkontenbeschriftungen
- [ ] DUO documents – doctypes: …

## Booking route per voucher type (⛔ never both)
| Voucher type | Booked via EXTF | Booked via DUO ledger data | PDF to DUO |
|---|---|---|---|

## Booking logic
OPOS: … | Personenkonten ranges: … | Amount basis: gross/net | Payments exported: yes/no (bank data at StB?)
### Tax keys (from StB)
| Tax situation | ERPNext Tax Category / Item Tax Template | Erlös-/Aufwandskonto | BU-Schlüssel | Source |
|---|---|---|---|---|
### Special cases
EU/OSS/§13b/foreign currency/Anzahlungen/credit notes/cancellations/corrections: …

## Optional features
KOST1/KOST2: … | Festschreibung: … | DUO folders/Kasse: … | Leistungsdatum: …

## Fit-gap vs phamos/datev (version/commit read: …)
| Requirement | Covered by | Notes |
|---|---|---|
| | Config / Generic MR / Customer app | |

## Open questions
### For the Steuerberater
- [ ] …
### For the customer
- [ ] …
### ⛔ Blocking
- [ ] …

## Test & acceptance
Test Mandant: … | Test DUO: … | Sample month: … | Sign-off customer: … | Sign-off StB: …
```

## Quality bar

- Every value is either confirmed (with its source) or listed as an open question. Nothing is assumed.
- Tax keys, account mappings and the booking route carry their **source** (StB e-mail or meeting, date).
- The issue is understandable by a functional consultant and by the customer's accounting user, with no code in it.
- Before writing to GitLab, show the draft and get approval.
