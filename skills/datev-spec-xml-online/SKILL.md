---
name: datev-spec-xml-online
description: Reference spec for the DATEV XML-Schnittstelle online (document packages to DATEV Unternehmen online): document.xml, ledger XML, XSD v6.0 rules, limits, live lookup and validation. Load from any datev-* skill or for DUO XML questions.
---

# DATEV spec — XML-Schnittstelle online (DUO document packages)

This skill is the field-level source of truth for **sending documents (Belege) and optional booking data to DATEV Unternehmen online (DUO)**. It is the companion of `datev-spec-extf` and is used by `datev-export-builder`, `datev-file-reviewer`, `datev-customer-discovery` and `datev-functional-advisor`.

**Snapshot:** read from developer.datev.de and the official XSD files on **2026-10-20**. Interface version **6.0** (latest changelog entry: **March 2023**, `base1/paymentOrder` added).

## 1. Freshness check and live lookup

- The spec JSON lives at `https://developer.datev.de/mediator/strapi/file-formats/slug/datev-xml-interface-online`. German pages are under `localization.fileFormatPages`:
  - DATEV XML-Schnittstelle online
  - Einstieg
  - Zeichensatz
  - Formatbeschreibung › Verwaltungsdatendatei, Belegsatzdatendatei
  - Werkzeuge
  - XSD-Files
  - Musterdateien
  - Import-/Export
  - Changelog
  - Hilfe
- Fetch it the same way as `datev-spec-extf` section 2: `curl` from the cloud workspace once `developer.datev.de` is allowlisted, otherwise via the browser pane with `fetch()` in the page.
- Check **Changelog**. An entry newer than March 2023 means re-reading the affected part live and preferring it over this file.
- **The XSD files are authoritative**, not the prose. Download them before building or reviewing (the user's permission is needed for downloads):
  - XSDs: `https://developer.datev.de/assets/XSD_3c866dbe96.zip` contains `Document_v060.xsd`, `Document_types_v060.xsd`, `Belegverwaltung_online_ledger_import_v060.xsd`, `Belegverwaltung_online_ledger_types_v060.xsd`, plus the legacy `…invoice_v060.xsd` and `…types_v060.xsd`.
  - Samples:
    - `https://developer.datev.de/assets/accounts_Payable_Ledger_Eingangsrechnungen_7_8ce161174e.zip`
    - `https://developer.datev.de/assets/accounts_Receivable_Ledger_Ausgangsrechnungen_2_2061bc8391.zip`
    - `https://developer.datev.de/assets/cash_Ledger_067be9d707.zip`

## 2. What it is for, and what not

**Use for** (into DUO, from where the StB can pass data on to Rechnungswesen):

- invoice data with or without PDFs into the Rechnungsbücher (incoming and outgoing)
- cash data with or without receipts into the Kassenbuch
- **PDFs with a GUID for archiving only** in Belege online, to link from EXTF bookings (Beleglink `BEDI`)
- SEPA/DTAUS files to split collective payments

**Not for:**

- pure G/L bookings (account to account, e.g. payments)
- master data (Debitoren/Kreditoren)
- some §13b cases

Use the **DATEV-Format (EXTF)** for those. DATEV itself says: if the data is meant for Rechnungswesen, check the DATEV-Format first.

**Import only.** DATEV apps never export this format.

## 3. phamos usage patterns (agreed design, see phamos/datev milestone "DUO xml")

- **Route A (default): documents only.** The package holds PDF + GUID (`document` with `File` extensions). Bookings go via EXTF, and each EXTF row carries Beleglink #20 = `"BEDI ""<GUID>"""`.
- **Route B (per company): documents + ledger data.** Sales/Purchase Invoices and cash also carry ledger XML, and the StB books from DUO. Those vouchers **must not** also be in the EXTF Buchungsstapel. This is agreed in discovery; there is no technical guard.
- Only doctypes with a real PDF are covered (Sales Invoice, Purchase Invoice, Expense Claim, POS). Ledger lines are grouped **per account and tax rate**.
- Packages are built per period on the DATEV page and uploaded with DATEV Belegtransfer. An API upload is planned for later.

## 4. Document package

- A **ZIP file** (local route) or a **job ID** (API route) containing:
  - exactly one `document.xml`
  - 0..n ledger XML files
  - the document files (PDF etc.)
  - optionally SEPA files
- **No nested folders** in the ZIP; all files sit in the root.
- **Limits:**
  - package technical maximum 465 MB, **recommended ≤ 100 MB**
  - each file ≤ **20 MB**
  - `document` elements per `document.xml`: **1–4,999** per the XSD (the prose says 5,000; respect 4,999)
  - `extension` per document: 1–50
- **File names: ASCII only** (a GUID is ideal). Other characters break processing.
- Allowed file types for `File`: PDF, XML, TIF, TIFF, BMP, CSV, DOC, DOCX, GIF, JPEG, JPG, ODS, ODT, PKCS7, PNG, RTF, TXT, XLS, XLSX.

## 5. Character set (all XML files)

- **UTF-8 only.** Content is checked against an allow-list:
  - letters and digits
  - `§@€`
  - common punctuation, tab and line breaks
  - Latin-1 Supplement (umlauts, ß, …)
  - CJK and Hangul ranges

  Anything else (emoji, some typographic quotes or dashes) is rejected, so sanitise free texts.
- Use precomposed Unicode (NFC). Escape `< > & " '` as `&lt; &gt; &amp; &quot; &apos;`.
- **Element order must follow the XSD exactly.** Empty elements or attributes are rejected; omit them instead.

## 6. document.xml (Verwaltungsdatendatei, `Document_v060.xsd`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<archive xmlns="http://xml.datev.de/bedi/tps/document/v06.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xml.datev.de/bedi/tps/document/v06.0 Document_v060.xsd"
         version="6.0" generatingSystem="ERPNext">
  <header><date>2026-02-02T10:15:00</date></header>
  <content>
    <document guid="0b6f6a0e-3c1d-4b7e-9a51-2f1c7d9e4a10" type="2">
      <extension xsi:type="accountsReceivableLedger" datafile="0b6f6a0e-3c1d-4b7e-9a51-2f1c7d9e4a10.xml">
        <property key="1" value="2026-01"/>
        <property key="3" value="Ausgangsrechnungen"/>
      </extension>
      <extension xsi:type="File" name="0b6f6a0e-3c1d-4b7e-9a51-2f1c7d9e4a10.pdf"/>
      <repository>
        <level id="1" name="ERPNext"/>
        <level id="2" name="Ausgangsrechnungen 2026"/>
        <level id="3" name="01 Januar"/>
      </repository>
    </document>
  </content>
</archive>
```

| Element / attribute | Rule (XSD) | Notes |
|---|---|---|
| `archive@version` | `6.0` | required |
| `archive@generatingSystem` | 1–40 chars | software name |
| `archive@guid` | UUID | optional |
| `header/date` | xsd:dateTime **without timezone** (`2026-02-02T10:15:00`) | required |
| `header/description` | 1–255 | optional |
| `header/consultantNumber`, `clientNumber`, `clientName` | 1000–9999999 / 0–99999 / ≤36 | **Don't use.** DATEV asks for them at transfer anyway; values here only get in the way |
| `header/repository` | as below | optional default folder |
| `content/document` | 1–4,999 | one per business document |
| `document@guid` | UUID `8-4-4-4-12` hex | stores the document under this ID in DUO, and is the target of the EXTF Beleglink. **Needs a `File` extension** |
| `document@type` | `1` = Belegkreis Rechnungseingang, `2` = Rechnungsausgang | optional |
| `document@processID` | `1` / `2` | **Quirk:** the XSD says 1 = buchungsrelevant, 2 = archivierungsrelevant; the prose says 1 = into the Posteingang (repository ignored, only without data XML), 2 = into the repository. Test with the StB before relying on it |
| `document/description` | 1–40 | optional |
| `document/keywords` | 1–255 | note |
| `document/extension` | 1–50 | see below |
| `document/repository` | `level` 1–3 with `@id` 1/2/3 and `@name` 1–30 chars | 1 Kategorie, 2 Ordner, 3 Register. DATEV recommends a constant level-1 name per software. Default when omitted: Buchführung / `IMPORT JJJJ RE` (or RA, KASSE) / `MM Monatsname` |

**`extension@xsi:type`:**

| Type | Attribute | Properties |
|---|---|---|
| `accountsPayableLedger` | `datafile` | key 1 = invoice month `JJJJ-MM`; key 3 = invoice folder (default "Eingangsrechnungen"). 1–2 properties |
| `accountsReceivableLedger` | `datafile` | key 1 = month; key 3 = folder (default "Ausgangsrechnungen") |
| `cashLedger` | `datafile` | key 1 = month, key 2 = Kassenkontonummer (e.g. 1000), key 3 = Kassenbezeichnung (default "Kasse"). The prose says only keys 2 or 3 for cash; check the samples |
| `File` | `name` | none; the document file itself |
| `SEPAFile` | `name` | none |
| `Invoice` | `datafile` | legacy invoice format |

Folder names, Kassenkontonummer and Kassenbezeichnung are **configured by the customer in DUO**. Make them settings, never constants.

## 7. Ledger XML (Belegsatzdatendatei, `Belegverwaltung_online_ledger_import_v060.xsd`)

One file per invoice, or per cash day/transaction.

```xml
<LedgerImport xmlns="http://xml.datev.de/bedi/tps/ledger/v060" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xml.datev.de/bedi/tps/ledger/v060 Belegverwaltung_online_ledger_import_v060.xsd"
  version="6.0" generator_info="phamos" generating_system="ERPNext"
  xml_data="Kopie nur zur Verbuchung berechtigt nicht zum Vorsteuerabzug">
  <consolidate consolidatedAmount="326.00" consolidatedDate="2026-01-05" consolidatedInvoiceId="ACC-SINV-2026-00001" consolidatedCurrencyCode="EUR">
    <accountsReceivableLedger> … </accountsReceivableLedger>
  </consolidate>
</LedgerImport>
```

Root and consolidate:

| Item | Rule |
|---|---|
| `@version` | `6.0` |
| `@generator_info` | company that generated it, 1–40 (required) |
| `@generating_system` | 1–40 |
| `@xml_data` | fixed note, `[0-9a-zA-Z. _]{1,60}`. Use DATEV's text exactly: `Kopie nur zur Verbuchung berechtigt nicht zum Vorsteuerabzug` |
| `consolidate` (1) | holds 1–5,000 lines of **one** type: `accountsPayableLedger` \| `accountsReceivableLedger` \| `cashLedger` |
| `@consolidatedAmount` | required; decimal with dot, 2 decimals, may be negative/zero; = sum of the lines |
| `@consolidatedDate` | required; `YYYY-MM-DD` |
| `@consolidatedInvoiceId` | `[a-zA-Z0-9$%&*+\-/]{0,36}` |
| `@consolidatedCurrencyCode` | required; ISO 4217 |
| `@consolidatedDeliveryDate` | required if `deliveryDate` is used in base1 |
| `@consolidatedOrderId` | `[a-zA-Z0-9$%&*+\-./]{1,30}`; required if `orderId` is used |

**`base` fields (all line types), in this order:**

| Field | Rule | Meaning |
|---|---|---|
| `date` | `YYYY-MM-DD`, required | Belegdatum |
| `amount` | required, ±0.01–9999999999.99, **dot**, 2 decimals, ≠ 0 | gross recommended; negative for credit notes / cash out |
| `discountAmount` | 0.01–99999999.99 | Skontobetrag 1 |
| `accountNo` | 1–999999999 | Sachkonto (4–8 digits per Mandant) |
| `buCode` | 0–9999 (number, unquoted) | BU-Schlüssel. **From the StB, never invented** |
| `costAmount` | 0.0001…, 4 decimals | KOST-Menge |
| `costCategoryId` / `costCategoryId2` | ≤36, no leading/trailing space | KOST1 / KOST2 |
| `tax` | 0.00–99.99 | tax rate % |
| `information` | 1–120 | free text |

**`base1` (incoming/outgoing invoices) adds, in this order:**

| Field | Rule | Meaning |
|---|---|---|
| `currencyCode` | required, ISO 4217 | |
| `invoiceId` | required, `[a-zA-Z0-9$%&*+\-/]{0,36}` | invoice number. **No spaces, dots or underscores** (ERPNext `ACC-SINV-2026-00001` is fine) |
| `bookingText` | 1–60 (XSD; the prose says 30) | |
| `typeOfReceivable` | 1–10 | Forderungsart (kommunal) |
| `ownVatId` | `[0-9a-zA-Z. _]{1,15}` | own USt-ID (OSS) |
| `shipFromCountry` | ISO 3166 alpha-2 | OSS |
| `partyId` | 1–15 | customer/supplier number on the document |
| `paidAt` | date | stamps the document "bezahlt" |
| `internalInvoiceId` | `[a-zA-Z0-9$%&*+\-/]{1,12}` | |
| `vatId` | `[0-9a-zA-Z. _]{1,15}` | partner USt-ID |
| `shipToCountry` | alpha-2 | OSS |
| `exchangeRate` | 0.000001–9999.999999, 6 decimals | |
| `bankCode`, `bankAccount`, `bankCountry` | ≤10 digits / ≤30 / alpha-2 | legacy bank data |
| `iban` | `[A-Z]{2}\d\d[A-Za-z0-9]{11,30}` | |
| `swiftCode` | 8 or 11 | BIC |
| `accountName` | 1–40 | |
| `paymentConditionsId` | 9–999 | DATEV Zahlungsbedingung |
| `paymentOrder` | boolean | tick "create Lastschrift/Überweisung" |
| `discountPercentage`, `discountPaymentDate`, `discountAmount2`, `discountPercentage2`, `discountPaymentDate2` | | Skonto 1/2 |
| `dueDate` | date | due without Skonto |
| `bpAccountNo` | 10000–999999999 | Personenkonto |
| `deliveryDate` | date | Leistungsdatum (requires `consolidatedDeliveryDate`) |
| `orderId` | as consolidatedOrderId | e.g. PayPal transaction (requires `consolidatedOrderId`) |

Then, per type:

- `accountsReceivableLedger`: `customerName` (1–50), `customerCity` (1–30)
- `accountsPayableLedger`: `supplierName` (1–50), `supplierCity` (1–30)

**`cashLedger`** = `base` + `currencyCode` (**EUR only**) + optional `invoiceId` + **required** `bookingText` (1–60).

**Granularity** is the software maker's choice: line, product group, tax rate, or total. phamos uses **one line per account and tax rate** (same as the EXTF Consultant Booking).

## 8. Validation

Keep the six XSD files together in one folder (the types files are included), and validate every generated file:

```python
from lxml import etree

def validate(xml_path, xsd_path):
    schema = etree.XMLSchema(etree.parse(xsd_path))
    doc = etree.parse(xml_path)
    if not schema.validate(doc):
        return [f"{e.line}: {e.message}" for e in schema.error_log]
    return []

# document.xml   -> Document_v060.xsd
# ledger files   -> Belegverwaltung_online_ledger_import_v060.xsd
```

Also check what the XSD cannot:

- the character allow-list
- ASCII file names
- every `datafile`/`name` exists in the ZIP and every file in the ZIP is referenced
- the sum of the lines = `consolidatedAmount`
- the size limits
- `guid` uniqueness

DATEV's own **Prütool for XSD validation** (help-center doc 1070393) only checks syntax. A clean result does not guarantee the import into a customer's DUO works; a test upload does.

## 9. Transfer

- **DATEV Belegtransfer** (free app, `https://www.datev.de/belegtransfer`): the user uploads the ZIP. It needs a DATEV SmartCard or login with rights and at least "DATEV Sicherheitspaket compact".
- **Online API `accounting:dxso-jobs`**: request a job ID, upload the files, poll the status. It needs DATEV developer registration and OAuth.
- Help: `schnittstellenberatung@datev.de` and the DATEV Schnittstellenberatung booking calendar.

## 10. Known quirks

- `processID` meaning differs between the XSD and the prose (see section 6).
- `bookingText` is 60 in the XSD and 30 in the prose. Stay ≤ 30 if the StB's view truncates; the XSD allows 60.
- Maximum documents per package: 4,999 (XSD) vs 5,000 (prose).
- Header Berater/Mandant fields exist but DATEV advises against them.
- The legacy `Invoice` format still works but is only published as XSD. Use `ledger` for new work.
