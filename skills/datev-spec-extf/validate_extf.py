"""DATEV-Format (EXTF) validator: header v700 + Buchungsstapel core fields.

Usage: python3 -I validate_extf.py EXTF_Buchungsstapel.csv

Regexes follow the DATEV notation (\\w = [a-zA-Z0-9_], hence re.ASCII).
An empty field means "not provided" and is skipped, except in the header,
where every field is checked. Extend BUCHUNG with rules from the live spec
when a customer uses more fields. See SKILL.md for the meaning of each field
and for the known quirks (BU-Schluessel #9 is a warning, not an error).
"""
import re
import sys

HEADER = {
    1: r'^"(EXTF|DTVF)"$', 2: r"^700$", 3: r"^(16|20|21|46|48|65)$",
    4: r'^"(Buchungsstapel|Wiederkehrende Buchungen|Debitoren/Kreditoren|Kontenbeschriftungen|Zahlungsbedingungen|Diverse Adressen)"$',
    5: r"^(2|3|4|5|13)$",
    6: r"^20\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(2[0-3]|[01]\d)[0-5]\d[0-5]\d{4}$",
    7: r"^$", 8: r'^"\w{0,2}"$', 9: r'^"\w{0,25}"$', 10: r'^("\w{0,25}")?$',
    11: r"^(\d{4,6}|\d{7})$", 12: r"^\d{1,5}$",
    13: r"^20\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$", 14: r"^[4-8]$",
    15: r"^(20\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))?$",
    16: r"^(20\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))?$",
    17: r'^("[\w.\-/ ]{0,30}")?$', 18: r'^("([A-Z]{2}){0,2}")?$', 19: r"^[12]?$",
    20: r"^(0|30|40|50|64)?$", 21: r"^(0|1)?$", 22: r'^("[A-Z]{3}")?$',
    23: r"^$", 24: r'^("")?$', 25: r"^$", 26: r"^$", 27: r'^"(\d{2}){0,2}"$',
    28: r"^\d{0,4}$", 29: r"^$", 30: r'^("")?$', 31: r'^(".{0,16}")?$',
}
DDMMYYYY = r"^(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])20\d{2}$"
BUCHUNG = {
    1: r"^(?!0{1,10},00)\d{1,10},\d{2}$", 2: r'^"(S|H)"$', 3: r'^"[A-Z]{3}"$',
    4: r"^[1-9]\d{0,3},\d{2,6}$", 5: r"^(?!0{1,10},00)\d{1,10},\d{2}$", 6: r'^"[A-Z]{3}"$',
    7: r"^(?!0{1,9}$)\d{1,9}$", 8: r"^(?!0{1,9}$)\d{1,9}$", 9: r'^"\d{4}"$',
    10: r"^(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])$",
    11: r'^"[\w$&%*+\-/]{0,36}"$', 12: r'^"[\w$&%*+\-/]{0,36}"$',
    13: r"^[1-9]\d{0,7},\d{2}$", 14: r'^".{0,60}"$', 15: r"^(0|1)$",
    37: r'^"[\w ]{0,36}"$', 38: r'^"[\w ]{0,36}"$', 40: r'^".{0,15}"$',
    41: r"^\d{2},\d{2}$", 42: r'^"(I|K|P|S)"$', 96: r'^"[A-Z]{2}"$',
    114: r"^(0|1)$", 115: DDMMYYYY, 116: DDMMYYYY, 117: DDMMYYYY,
    119: r"^\d{1,2},\d{2}$", 120: r'^"[A-Z]{2}"$', 125: r"^\d{1,9}$",
}
WARN_ONLY = {9}  # BU-Schluessel: spec says 4 digits, real files use short keys


def split_fields(line):
    """Split one DATEV line on ';' outside quotes and keep the quotes."""
    out, buf, inq, i = [], "", False, 0
    while i < len(line):
        c = line[i]
        if inq and c == '"' and line[i + 1:i + 2] == '"':
            buf += '""'
            i += 2
            continue
        if c == '"':
            inq = not inq
        if c == ";" and not inq:
            out.append(buf)
            buf = ""
        else:
            buf += c
        i += 1
    out.append(buf)
    return out


def check(fields, rules, label, errors, warns, skip_empty=True, warn_only=()):
    for no, rx in rules.items():
        val = fields[no - 1] if no <= len(fields) else ""
        if skip_empty and val in ("", '""') and not re.fullmatch(rx, val, re.ASCII):
            continue
        if not re.fullmatch(rx, val, re.ASCII):
            (warns if no in warn_only else errors).append(f"{label} field {no}: {val!r} !~ {rx}")


def validate(path):
    raw = open(path, "rb").read()
    errors, warns = [], []
    if raw.startswith(b"\xef\xbb\xbf"):
        text = raw[3:].decode("utf-8")
        warns.append("UTF-8 BOM: only manual import / extf-files API accept Unicode (not KrStaPv)")
    else:
        text = raw.decode("cp1252")
    if b"\r\n" not in raw or re.search(rb"(?<!\r)\n", raw):
        errors.append("line endings must be CRLF")
    lines = text.split("\r\n")
    while lines and lines[-1] == "":
        lines.pop()
    head = split_fields(lines[0])
    check(head, HEADER, "header", errors, warns, skip_empty=False)
    rows = lines[2:]
    if head[2] == "21":
        if len(rows) > 99999:
            errors.append(f"{len(rows)} rows > 99,999 per Buchungsstapel")
        for n, line in enumerate(rows, start=3):
            f = split_fields(line)
            if len(f) != 125:
                errors.append(f"line {n}: {len(f)} fields, expected 125")
            check(f, BUCHUNG, f"line {n}", errors, warns, warn_only=WARN_ONLY)
    return errors, warns


if __name__ == "__main__":
    errs, wrns = validate(sys.argv[1])
    print("\n".join(["ERROR " + e for e in errs] + ["WARN  " + w for w in wrns]) or "OK")
    sys.exit(1 if errs else 0)
