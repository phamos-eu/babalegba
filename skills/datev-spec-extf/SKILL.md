---
name: datev-spec-extf
description: Reference spec for the DATEV-Format (EXTF CSV) into DATEV Rechnungswesen — header v700, Buchungsstapel, Debitoren/Kreditoren, Sachkonten and more, with live lookup and a validator. Load from any datev-* skill or for EXTF field questions.
---

# DATEV spec — DATEV-Format (EXTF CSV)

This skill is the **single source of truth for field-level facts** in the phamos DATEV skill family (`datev-customer-discovery`, `datev-export-builder`, `datev-file-reviewer`, `datev-importer`, `datev-functional-advisor`). It does not build anything. It answers "what does DATEV expect in field X", checks files, and keeps itself current.

Two layers:

1. **Stable core (inline below):** rules that have barely changed since header v700 (Oct 2018). Use them directly.
2. **Live lookup:** everything else (rare fields, Wiederkehrende Buchungen, Zahlungsbedingungen, Diverse Adressen, full Debitoren/Kreditoren list), plus a drift check against DATEV's changelog.

**Snapshot:** read from developer.datev.de on **2026-10-20**. The latest changelog entry then was **March 2025** ("improved a few regular expressions"). Buchungsstapel was at format version **13**, last changed **Feb 2024** when field 125 was added.

---

## 1. Freshness check (do this first when building or reviewing)

1. Fetch the spec JSON (section 2) and read page **"Changelog"**.
2. If it shows an entry newer than **March 2025**, tell the user which formats changed. Then read the affected section live and prefer the live content over this file for that section.
3. If the lookup fails, say so plainly and continue on the snapshot. Mark any field-level claim as "per snapshot 2026-10-20".

## 2. Live lookup

The portal (`https://developer.datev.de/de/file-formats`) is a JavaScript app, so plain WebFetch returns an empty shell. Its content comes from a JSON API:

| Format | Endpoint |
|---|---|
| Overview list | `https://developer.datev.de/mediator/strapi/file-formats` |
| DATEV-Format (EXTF) | `https://developer.datev.de/mediator/strapi/file-formats/slug/datev-format` |
| XML-Schnittstelle online | `https://developer.datev.de/mediator/strapi/file-formats/slug/datev-xml-interface-online` |

JSON shape: the root holds the English pages, and `localization` holds the **German** pages, which are the reference. Each page is `fileFormatPages[]: {title, body (HTML), fileFormatPages[] (children)}`.

The German tree for `datev-format`:

- Einstieg
- Zeichensatz
- Formatbeschreibung › Header, Buchungsstapel, Wiederkehrende Buchungen, Debitoren/Kreditoren, Zahlungsbedingungen, Sachkontenbeschriftung, Diverse Adressen
- Musterdaten
- Tools
- Import/Export
- Anhang › Format-Kategorie/Name/Version, Notation für Ausdrücke, Naturalstapel
- Changelog

Field tables are HTML `<table>` elements with the columns `# | Überschrift | Ausdruck | Beschreibung`.

**Order of attempts:**

1. **Direct fetch from the cloud workspace.** This works once `developer.datev.de` is on the org's network allowlist:
   ```bash
   curl -sS https://developer.datev.de/mediator/strapi/file-formats/slug/datev-format -o datev-format.json
   ```
   Parse with `python3 -I`; strip the HTML with a parser rather than regexes.
2. **Fallback: the browser pane** (Claude's built-in browser on the user's computer). Open `https://developer.datev.de/de/file-formats`, then run in the page:
   ```js
   const d = await fetch('/mediator/strapi/file-formats/slug/datev-format').then(r => r.json());
   d.localization.fileFormatPages.map(p => p.title)   // then pull the one page/table you need
   ```
   Pull only the section you need; the whole document is ~360 KB.
3. If both fail, use the snapshot and say so.

Downloads, which need the user's permission before downloading:

- Musterdaten: `https://developer.datev.de/assets/Musterdaten_DATEV_Format_0_7f9322b9cc.zip`
- Prüfprogramm DATEV-Format 2.2.3.0 (Windows): `https://developer.datev.de/assets/Datev_Format_Pruefprogramm_2_2_3_0_76439824cb.zip`

## 3. File structure and technical rules (stable)

- File name prefix **`EXTF_`**, extension `.csv`, e.g. `EXTF_Buchungsstapel.csv`. `EXTF` means 3rd-party software; `DTVF` means a file exported by a DATEV app, so we **write EXTF** and may **read DTVF**.
- Line 1 is the **header** (metadata). Line 2 holds the **column headings** of the format. Lines 3 to n are the **data rows**.
- Separator `;`. Every line ends with **CR/LF**.
- **Text fields are always in double quotes**. A quote inside a text is doubled (`""`). Control characters (line breaks!) are not allowed inside text.
- Numbers are not quoted. The decimal separator is a **comma** (`99,99`) and there are no thousands separators. Exception: a few Debitoren/Kreditoren fields such as Kreditlimit (`1.123.123.123`) and Mahnlimit (`12.123,12`).
- Dates inside data rows are **TTMM** (Belegdatum) or **TTMMJJJJ**. Header dates are **YYYYMMDD**. The header timestamp is `YYYYMMDDHHMMSSFFF`.
- **Encoding:** the default is **ISO-8859-1 / CodePage 1252**. Unicode (UTF-8/16/32) is accepted **only with a BOM**, and **only** for manual import in DATEV Rechnungswesen or via the API `accounting:extf-files`. **KrStaPv.exe does not support Unicode.** Practical rule: write **`cp1252`**, not `latin_1`. `latin_1` has no `€` and silently turns it into `?`.
- **Volume limit:** at most **99,999 bookings per Buchungsstapel file**. Stammdaten files have no limit.
- **One file per booking period** is DATEV's recommendation. A batch must lie inside **one fiscal year**.
- Empty optional field: write nothing (`;;`). For text fields, `""` is also accepted.

## 4. Header (line 1), version 700 — all 31 fields

DATEV regex notation: `\w` = `[a-zA-Z0-9_]` only (no umlauts), and `{0,n}` means optional. Fields marked **B** apply only to *Bewegungsdaten* (Buchungsstapel, Wiederkehrende Buchungen) and stay empty for Stammdaten.

| # | Field | Rule | Notes |
|---|---|---|---|
| 1 | Kennzeichen | `"EXTF"` \| `"DTVF"` | We write EXTF |
| 2 | Versionsnummer | `700` | |
| 3 | Formatkategorie | 16 \| 20 \| 21 \| 46 \| 48 \| 65 | 16 Debitoren/Kreditoren, 20 Sachkontenbeschriftungen, 21 Buchungsstapel, 46 Zahlungsbedingungen, 48 Diverse Adressen, 65 Wiederkehrende Buchungen |
| 4 | Formatname | quoted name | `"Buchungsstapel"`, `"Debitoren/Kreditoren"`, `"Kontenbeschriftungen"`, `"Zahlungsbedingungen"`, `"Diverse Adressen"`, `"Wiederkehrende Buchungen"` |
| 5 | Formatversion | number | Buchungsstapel **13**, Debitoren/Kreditoren **5**, Kontenbeschriftungen **3**, Zahlungsbedingungen **2**, Diverse Adressen **2**, Wiederkehrende **4** |
| 6 | Erzeugt am | `YYYYMMDDHHMMSSFFF` | 17 digits, e.g. `20240130140440439` |
| 7 | Importiert | empty | |
| 8 | Herkunft | `"\w{0,2}"` | e.g. `"RE"`; replaced by `SV` on import |
| 9 | Exportiert von | `"\w{0,25}"` | **No `@ . -` or spaces**, so an e-mail address is invalid. Use a cleaned user name |
| 10 | Importiert von | `"\w{0,25}"` | Normally empty |
| 11 | Beraternummer | 4–7 digits | 1001–9999999 |
| 12 | Mandantennummer | 1–5 digits | 1–99999 |
| 13 | WJ-Beginn | `YYYYMMDD` | Start of the fiscal year |
| 14 | Sachkontenlänge | 4–8 | **Must equal the Mandant's setting in DATEV** |
| 15 | Datum von | `YYYYMMDD` | **B**: start of the batch period |
| 16 | Datum bis | `YYYYMMDD` | **B**: end of the batch period |
| 17 | Bezeichnung | `"[\w.-/ ]{0,30}"` | **B**: batch label, max 30, e.g. `Rechnungsausgang 02/2024` |
| 18 | Diktatkürzel | `"([A-Z]{2}){0,2}"` | Quoted, uppercase |
| 19 | Buchungstyp | 1 \| 2 | **B**: 1 = Finanzbuchführung (default), 2 = Jahresabschluss |
| 20 | Rechnungslegungszweck | 0 \| 30 \| 40 \| 50 \| 64 | **B**: 0 = independent (default) |
| 21 | Festschreibung | 0 \| 1 | **B**: **DATEV default = 1 (locked)!** Our default is **0**; see the guardrails in `datev-export-builder` |
| 22 | WKZ | `"[A-Z]{3}"` | **B**: e.g. `"EUR"` |
| 23 | reserviert | empty | |
| 24 | Derivatskennzeichen | `""` | |
| 25–26 | reserviert | empty | |
| 27 | Sachkontenrahmen | `"(\d{2}){0,2}"` | e.g. `"03"` (SKR03), `"04"` (SKR04) |
| 28 | ID Branchenlösung | `\d{0,4}` | |
| 29 | reserviert | empty | |
| 30 | reserviert | `""` | |
| 31 | Anwendungsinformation | `".{0,16}"` | Free processing tag, e.g. `02/2024` |

Valid examples (from DATEV):

```
"EXTF";700;21;"Buchungsstapel";13;20240130140440439;;"RE";"";"";29098;55003;20240101;4;20240101;20240831;"Buchungsstapel";"WD";1;0;0;"EUR";;"";;;"03";;;"";""
"EXTF";700;16;"Debitoren/Kreditoren";5;20240130140659583;;"RE";"";"";29098;55003;20240101;4;;;"";"";;;;"";;"";;;"03";;;"";""
```

## 5. Buchungsstapel (category 21, format version 13, 125 columns)

### 5.1 Column headings (line 2), exact order

```
Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;WKZ Umsatz;Kurs;Basis-Umsatz;WKZ Basis-Umsatz;Konto;Gegenkonto (ohne BU-Schlüssel);BU-Schlüssel;Belegdatum;Belegfeld 1;Belegfeld 2;Skonto;Buchungstext;Postensperre;Diverse Adressnummer;Geschäftspartnerbank;Sachverhalt;Zinssperre;Beleglink;Beleginfo - Art 1;Beleginfo - Inhalt 1;Beleginfo - Art 2;Beleginfo - Inhalt 2;Beleginfo - Art 3;Beleginfo - Inhalt 3;Beleginfo - Art 4;Beleginfo - Inhalt 4;Beleginfo - Art 5;Beleginfo - Inhalt 5;Beleginfo - Art 6;Beleginfo - Inhalt 6;Beleginfo - Art 7;Beleginfo - Inhalt 7;Beleginfo - Art 8;Beleginfo - Inhalt 8;KOST1 - Kostenstelle;KOST2 - Kostenstelle;Kost-Menge;EU-Land u. UStID (Bestimmung);EU-Steuersatz (Bestimmung);Abw. Versteuerungsart;Sachverhalt L+L;Funktionsergänzung L+L;BU 49 Hauptfunktionstyp;BU 49 Hauptfunktionsnummer;BU 49 Funktionsergänzung;Zusatzinformation - Art 1;Zusatzinformation- Inhalt 1;Zusatzinformation - Art 2;Zusatzinformation- Inhalt 2;Zusatzinformation - Art 3;Zusatzinformation- Inhalt 3;Zusatzinformation - Art 4;Zusatzinformation- Inhalt 4;Zusatzinformation - Art 5;Zusatzinformation- Inhalt 5;Zusatzinformation - Art 6;Zusatzinformation- Inhalt 6;Zusatzinformation - Art 7;Zusatzinformation- Inhalt 7;Zusatzinformation - Art 8;Zusatzinformation- Inhalt 8;Zusatzinformation - Art 9;Zusatzinformation- Inhalt 9;Zusatzinformation - Art 10;Zusatzinformation- Inhalt 10;Zusatzinformation - Art 11;Zusatzinformation- Inhalt 11;Zusatzinformation - Art 12;Zusatzinformation- Inhalt 12;Zusatzinformation - Art 13;Zusatzinformation- Inhalt 13;Zusatzinformation - Art 14;Zusatzinformation- Inhalt 14;Zusatzinformation - Art 15;Zusatzinformation- Inhalt 15;Zusatzinformation - Art 16;Zusatzinformation- Inhalt 16;Zusatzinformation - Art 17;Zusatzinformation- Inhalt 17;Zusatzinformation - Art 18;Zusatzinformation- Inhalt 18;Zusatzinformation - Art 19;Zusatzinformation- Inhalt 19;Zusatzinformation - Art 20;Zusatzinformation- Inhalt 20;Stück;Gewicht;Zahlweise;Forderungsart;Veranlagungsjahr;Zugeordnete Fälligkeit;Skontotyp;Auftragsnummer;Buchungstyp;USt-Schlüssel (Anzahlungen);EU-Land (Anzahlungen);Sachverhalt L+L (Anzahlungen);EU-Steuersatz (Anzahlungen);Erlöskonto (Anzahlungen);Herkunft-Kz;Buchungs GUID;KOST-Datum;SEPA-Mandatsreferenz;Skontosperre;Gesellschaftername;Beteiligtennummer;Identifikationsnummer;Zeichnernummer;Postensperre bis;Bezeichnung SoBil-Sachverhalt;Kennzeichen SoBil-Buchung;Festschreibung;Leistungsdatum;Datum Zuord. Steuerperiode;Fälligkeit;Generalumkehr (GU);Steuersatz;Land;Abrechnungsreferenz;BVV-Position;EU-Land u. UStID (Ursprung);EU-Steuersatz (Ursprung);Abw. Skontokonto
```

Every data row has exactly **125** fields (124 separators).

### 5.2 Core fields (stable, used in nearly every export)

| # | Field | Rule | Meaning / gotchas |
|---|---|---|---|
| 1 | Umsatz | `\d{1,10},\d{2}`, not `0,00` | **Always positive**; the direction comes from #2 |
| 2 | Soll/Haben-Kz | `"S"` \| `"H"` | Refers to **#7 Konto** (not Gegenkonto). Default S |
| 3 | WKZ Umsatz | `"[A-Z]{3}"` | Default = header #22 |
| 4 | Kurs | `[1-9]\d{0,3},\d{2,6}` | Foreign currency only. If #1 is in a foreign currency, also send #4, #5 and #6. `0` is invalid |
| 5 / 6 | Basis-Umsatz / WKZ Basis-Umsatz | as #1 / #3 | Always used together |
| 7 | Konto | 1–9 digits, not all zeros | Sach- or Personenkonto |
| 8 | Gegenkonto (ohne BU) | 1–9 digits | Sach- or Personenkonto. **Personenkonto length = Sachkontenlänge + 1** (e.g. 4 → 5-digit Debitoren/Kreditoren) |
| 9 | BU-Schlüssel | `"\d{4}"` (see quirks) | Tax/control key. **Never invent it; it comes from the Steuerberater** |
| 10 | Belegdatum | `TTMM` | The year comes from the header (the batch must sit in one fiscal year; DATEV states header #13) |
| 11 | Belegfeld 1 | `"[\w$&%*+\-/]{0,36}"` | Invoice/document number, the **OPOS matching key**. **No spaces, umlauts, `.` `,` `;` `:`** |
| 12 | Belegfeld 2 | same | 2nd number, or OPOS info such as a due date `TTMMJJ` |
| 13 | Skonto | `[1-9]\d{0,7},\d{2}` | Payments only; `0` is invalid |
| 14 | Buchungstext | `".{0,60}"` | Max 60 |
| 15 | Postensperre | 0 \| 1 | Dunning/payment block |
| 20 | Beleglink | `".{0,210}"` | Link to the document. For DATEV DMS / Unternehmen online use `"BEDI ""<GUID>"""` (inner quotes doubled) |
| 37 / 38 | KOST1 / KOST2 | `"[\w ]{0,36}"` | Cost centre / cost object. The length must match the KOST setup in DATEV |
| 39 | KOST-Menge | `\d{12},\d{4}` | |
| 40 | EU-Land u. UStID (Bestimmung) | `".{0,15}"` | e.g. `"DE133546770"`. Greece = EL, Northern Ireland = XI |
| 41 | EU-Steuersatz (Bestimmung) | `\d{2},\d{2}` | |
| 42 | Abw. Versteuerungsart | `"I"`/`"K"`/`"P"`/`"S"` | Ist / keine / Pauschal / Soll, when different from the Mandant |
| 43 | Sachverhalt L+L | 1–3 digits, not 0 | §13b UStG cases |
| 96 | Buchungstyp | `"AA"`/`"AG"`/`"AV"`/`"SR"`/`"SU"`/`"SG"`/`"SO"` | Anzahlungen/Schlussrechnung. Used with #95 Auftragsnummer (`".{0,30}"`) |
| 102 | Herkunft-Kz | `"[A-Z]{2}"` | Replaced by SV on import |
| 103 | Buchungs GUID | `".{0,36}"` | Used by DATEV |
| 105 | SEPA-Mandatsreferenz | `".{0,35}"` | Requires #17 Geschäftspartnerbank (3 digits), and vice versa |
| 114 | Festschreibung | 0 \| 1 \| empty | **If any row has 1, the whole batch is locked after import.** Empty = auto-lock per DATEV |
| 115 | Leistungsdatum | `TTMMJJJJ` | Requires #116. Agree with the Steuerberater first |
| 116 | Datum Zuord. Steuerperiode | `TTMMJJJJ` | |
| 117 | Fälligkeit | `TTMMJJJJ` | OPOS only. If used, Belegfeld 2 OPOS info no longer works |
| 118 | Generalumkehr | `"0"`/`"1"` | Text also mentions `G` |
| 119 | Steuersatz | `\d{1,2},\d{2}` | Only for BU keys with rate choice (e.g. 100, 400). Use with #120 |
| 120 | Land | `"[A-Z]{2}"` | ISO country |
| 125 | Abw. Skontokonto | 1–9 digits | Expense account for Skonto; otherwise the Skonto collective account is used |

Other fields, by group (look up live when needed):

- 16–19: OPOS (Diverse Adressnummer, Geschäftspartnerbank, Sachverhalt 31/40, Zinssperre)
- 21–36: Beleginfo Art/Inhalt 1–8 (always as pairs)
- 44–47: L+L Austria / BU 49
- 48–87: Zusatzinformation Art/Inhalt 1–20 (pairs; Art ≤ 20 chars, Inhalt ≤ 210)
- 88–89: Stück/Gewicht (SKR14 only)
- 90–93: kommunal OPOS
- 94: Skontotyp
- 97–101: Anzahlungen
- 104: KOST-Datum
- 106: Skontosperre
- 107–113: Gesellschafter/SoBil
- 121: Abrechnungsreferenz
- 122: BVV-Position
- 123–124: EU (Ursprung)

## 6. Debitoren/Kreditoren (category 16, format version 5, 254 columns)

Rules for import:

- An address, communication data or bank data sent in the file is **created or updated**.
- Up to 10 bank connections are matched by bank number.
- A Bankleitzahl `0` **deletes** the bank connection, but only if that option is enabled in the Stapelverarbeitung.

Core fields:

| # | Field | Rule |
|---|---|---|
| 1 | Konto | Personenkonto, **Sachkontenlänge + 1** digits |
| 2 | Name (Unternehmen) | `".{0,50}"` |
| 4 / 5 | Name / Vorname (natürliche Person) | `".{0,30}"` each |
| 6 | Name (keine Angabe) | `".{0,50}"` |
| 7 | Adressatentyp | `"0"` keine Angabe, `"1"` natürliche Person, `"2"` Unternehmen (default) |
| 8 | Kurzbezeichnung | `".{0,15}"` |
| 9 / 10 | EU-Land / EU-UStID | `"\w{0,2}"` / `".{0,13}"` (USt-ID **without** country prefix in #10) |
| 15 | Adressart | `"STR"`/`"PF"`/`"GK"` |
| 16 / 17 | Straße / Postfach | `".{0,36}"` / `".{0,10}"` |
| 18 / 19 / 20 | PLZ / Ort / Land | `"\d{0,10}"` (digits only!) / `".{0,30}"` / `"[A-Z]{2}"` (mandatory outside DE) |
| 29 / 33 / 35 | Telefon / E-Mail / Internet | `".{0,60}"` |
| 41–49 | Bank 1: BLZ, Bankbezeichnung, Kontonummer, Länderkennz., **IBAN (#45, ≤34)**, Leerfeld, **SWIFT (#47, ≤11)**, Abw. Kontoinhaber, Kennz. Hauptbankverbindung | Banks 2–5 continue in 52–95, banks 6–10 in 165–219 |
| 99 | Kundennummer | `".{0,15}"` |
| 100 | Steuernummer | `".{0,20}"` |
| 101 | Sprache | 1 de, 4 fr, 5 en, 10 es, 19 it |
| 105 | Diverse-Konto | 0/1 |
| 108 | Kreditlimit (Debitor) | `[\d.]{0,13}` (**with thousands dots**) |
| 109 | Zahlungsbedingung | `\d{0,3}` (number of a Zahlungsbedingung in DATEV) |
| 110 / 111 | Fälligkeit Tage / Skonto % (Debitor) | |
| 112–120 | Kreditoren-Ziele/Skonti | |
| 152–164 | Rechnungsadresse (separate from the Korrespondenzadresse) | |
| 220 | Nummer Fremdsystem | `".{0,15}"`: **our ERPNext ID**; overwritten when DATEV uses centralised business partners |
| 222–231 | SEPA-Mandatsreferenz 1–10 | |
| 245 | Status | 0 aktiv, 1 inaktiv |

Column headings (line 2) and all remaining fields (dunning, interest, individual fields 1–15, …) come from the **live lookup** or the Musterdaten. Never guess the heading strings.

## 7. Sachkontenbeschriftungen (category 20, format name "Kontenbeschriftungen", version 3)

| # | Field | Rule |
|---|---|---|
| 1 | Konto | 1–9 digits (per Sachkontenlänge) |
| 2 | Kontenbeschriftung | `".{0,40}"` |
| 3 | Sprach-ID | `"de-DE"` \| `"en-GB"` (see quirks) |
| 4 | Kontenbeschriftung lang | `".{0,300}"` |

DATEV recommends sending **only individually labelled accounts**. Standard SKR labels are maintained by DATEV and should not be overwritten.

## 8. Other categories (live lookup for fields)

| Cat. | Name | Version | Note |
|---|---|---|---|
| 65 | Wiederkehrende Buchungen | 4 | Starts with B1 (Belegfeld-1 handling: 1 fixed ≤36, 2 = ≤34 + 2 auto digits, 3 = auto numbering); EUR only |
| 46 | Zahlungsbedingungen | 2 | |
| 48 | Diverse Adressen | 2 | OPOS one-off addresses |
| 44 | Textschlüssel | 2 | Appendix only |
| 66 | Natural-Stapel | 2 | Agriculture (SKR14): Textschlüssel, Art, Stück, Gewicht, Beleg, Datum TTMM, … 15 fields |

Version history of Buchungsstapel:

- **v13**: Feb 2024, added #125
- **v12**: Jun 2021, added #123–124 (EU Ursprung)
- **v11**: Jan 2021, added #121–122

Older DATEV installations may need lower versions; check against the DATEV version the Steuerberater runs.

## 9. Import/export channels

- **Import:**
  - Manual: DATEV Rechnungswesen › Stapelverarbeitung
  - Automated: `KrStaPv.exe` (no Unicode)
  - Online API: `accounting:extf-files` (via the DATEV Rechenzentrum)
- **Export from DATEV:**
  - Manual: Rechnungswesen › Export › DATEV-Format
  - Automated: `KRExport.exe`

  These produce **DTVF** files, which `datev-importer` reads.

## 10. Known quirks in DATEV's own spec (flag them; don't silently "fix")

- **BU-Schlüssel #9:** the current regex says exactly 4 digits (`"\d{4}"`), but many real exports (including phamos/datev) use short keys such as `"9"`, and DATEV's sample leaves it empty. Treat non-4-digit keys as a **warning**, not an error, and let the Steuerberater's test import decide. Record the outcome here once known.
- Header **#5** regex lists `2|4|5|13`, but Kontenbeschriftungen is version **3**. Header **#4** regex says "Kontenbeschriftungen" while the page title says "Sachkontenbeschriftung".
- Sachkonten **Sprach-ID**: the regex says `en-EN`, the description says `en-GB`.
- **Generalumkehr #118**: the regex allows `"0"`/`"1"`, the text mentions `G`.
- DATEV's sample data contains a malformed Buchungstext (`" "Normalabschr..." "`). Don't copy it.
- `\w` in the DATEV notation means ASCII only. Use `re.ASCII` in Python.

## 11. Validator (regex self-check)

`validate_extf.py` in this skill folder checks:

- CP1252 (or a BOM), CRLF line endings
- the 31 header fields
- the Buchungsstapel core fields above, and exactly 125 fields per row
- the 99,999-row limit

Run it with `python3 -I validate_extf.py <file>`. It exits 1 on errors and prints `ERROR` / `WARN` lines. Use it as the basis for unit tests in exporter apps, and extend its `BUCHUNG` rules with live-looked-up fields when a customer uses more of them.

Beyond regexes, these are business checks for the reviewer/builder:

- Belegdatum lies within header #15–#16.
- Konto/Gegenkonto lengths fit the Sachkontenlänge (Personenkonto = +1).
- Each row's account numbers exist in the Mandant's chart.
- Beleginfo and Zusatzinformation come in complete pairs.
- #17 and #105 are filled together.
- #115 comes with #116.
