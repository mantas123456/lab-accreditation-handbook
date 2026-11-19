"""Build the downloadable template pack.

    templates/src/<id>.md      forms, procedures, checklists -> docs/downloads/<id>.docx (Pandoc)
    templates/sheets/<id>.yml  registers, plans, budgets     -> docs/downloads/<id>.xlsx (openpyxl)

Each source starts with metadata (Markdown front matter, or top-level YAML keys):

    title:        the name shown on the site and in the file
    type:         SOP, form, checklist, record, register, plan, budget, ...
    description:  one sentence for the templates library

Which clauses a template belongs to is set in data/clauses.yml, not here.

After building, it packs every template with a README.txt into
docs/downloads/iso17025-qms-starter-pack.zip, and writes the template count
and zip size to templates/.build/pack.json for the MkDocs hook. Built files
get fixed internal timestamps (SOURCE_DATE_EPOCH, or PACK_DATE below), so the
pack only changes when a template does.

    python scripts/build_templates.py           # rebuild what changed
    python scripts/build_templates.py --force   # rebuild everything
"""

from __future__ import annotations

import copy
import io
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "templates" / "src"
SHEETS = ROOT / "templates" / "sheets"
OUT = ROOT / "docs" / "downloads"
REFERENCE_DOCX = ROOT / "templates" / ".build" / "reference.docx"
PACK = OUT / "iso17025-qms-starter-pack.zip"
PACK_DATA = ROOT / "templates" / ".build" / "pack.json"
CLAUSES = ROOT / "data" / "clauses.yml"
# Timestamp written into every built file and zip entry, so rebuilding an
# unchanged template gives identical bytes. SOURCE_DATE_EPOCH overrides it.
PACK_DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)

SITE = "https://mantas123456.github.io/lab-accreditation-handbook/"
FOOTER = (
    "Lab Accreditation Handbook template · CC BY 4.0 · "
    "Not official guidance; the standard and your accreditation body's documents take priority."
)

TEAL = "00796B"
HEADER_FILL = "E0F2F1"
EXAMPLE_FONT_COLOR = "808080"


# ---------------------------------------------------------------- catalogue


def _front_matter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.S)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def catalog() -> list[dict]:
    """Every template with its id, title, type, description, format and source path."""
    items = []
    for path in sorted(SRC.glob("*.md")):
        meta = _front_matter(path.read_text(encoding="utf-8"))
        items.append({**_meta(meta, path), "format": "docx", "source": path})
    for path in sorted(SHEETS.glob("*.yml")):
        meta = yaml.safe_load(path.read_text(encoding="utf-8"))
        items.append({**_meta(meta, path), "format": "xlsx", "source": path})
    ids = [t["id"] for t in items]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"template ids used twice: {sorted(dupes)}")
    return items


def _meta(meta: dict, path: Path) -> dict:
    missing = [k for k in ("title", "type", "description") if not meta.get(k)]
    if missing:
        raise ValueError(f"{path.relative_to(ROOT)}: missing {', '.join(missing)}")
    return {"id": path.stem, "title": meta["title"], "type": meta["type"], "description": meta["description"]}


def output_path(template: dict) -> Path:
    return OUT / f"{template['id']}.{template['format']}"


# ---------------------------------------------------------------- Word


def _reference_docx() -> Path:
    """Pandoc's default reference document, restyled once with python-docx."""
    script_time = Path(__file__).stat().st_mtime
    if REFERENCE_DOCX.exists() and REFERENCE_DOCX.stat().st_mtime >= script_time:
        return REFERENCE_DOCX
    import pypandoc
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor

    import subprocess

    REFERENCE_DOCX.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [pypandoc.get_pandoc_path(), "-o", str(REFERENCE_DOCX), "--print-default-data-file", "reference.docx"],
        check=True,
    )

    doc = Document(str(REFERENCE_DOCX))
    styles = doc.styles
    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        if name in [s.name for s in styles]:
            f = styles[name].font
            f.name, f.size = "Calibri", Pt(10.5)
    for name, size in (("Title", 20), ("Heading 1", 15), ("Heading 2", 12.5), ("Heading 3", 11)):
        if name in [s.name for s in styles]:
            f = styles[name].font
            f.name, f.size, f.bold = "Calibri", Pt(size), True
            f.color.rgb = RGBColor.from_string(TEAL)
    # Borders on pandoc's "Table" style, so forms print with visible boxes.
    if "Table" in [s.name for s in styles]:
        style_el = styles["Table"].element
        tbl_pr = style_el.find(qn("w:tblPr"))
        if tbl_pr is None:
            tbl_pr = OxmlElement("w:tblPr")
            # tblPr follows pPr/rPr and precedes trPr/tcPr/tblStylePr in a style.
            after = [style_el.find(qn(t)) for t in ("w:trPr", "w:tcPr", "w:tblStylePr")]
            after = [a for a in after if a is not None]
            if after:
                after[0].addprevious(tbl_pr)
            else:
                style_el.append(tbl_pr)
        old = tbl_pr.find(qn("w:tblBorders"))
        if old is not None:
            tbl_pr.remove(old)
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "0"), ("w:color", "999999")):
                el.set(qn(k), v)
            borders.append(el)
        # Schema order inside tblPr: ... tblInd, tblBorders, shd, tblLayout, tblCellMar, tblLook.
        later = [tbl_pr.find(qn(t)) for t in ("w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook")]
        later = [x for x in later if x is not None]
        if later:
            later[0].addprevious(borders)
        else:
            tbl_pr.append(borders)
    footer = doc.sections[0].footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.text = FOOTER
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in para.runs:
        run.font.size = Pt(7.5)
        run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    doc.save(str(REFERENCE_DOCX))
    return REFERENCE_DOCX


def build_docx(template: dict, out: Path) -> None:
    import pypandoc

    pypandoc.convert_file(
        str(template["source"]),
        "docx",
        format="markdown",
        outputfile=str(out),
        extra_args=["--reference-doc", str(_reference_docx())],
    )


# ---------------------------------------------------------------- Excel


def _styles():
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    thin = Side(style="thin", color="BBBBBB")
    return {
        "header_font": Font(bold=True, color="FFFFFF"),
        "header_fill": PatternFill("solid", fgColor=TEAL),
        "label_fill": PatternFill("solid", fgColor=HEADER_FILL),
        "border": Border(left=thin, right=thin, top=thin, bottom=thin),
        "wrap": Alignment(wrap_text=True, vertical="top"),
        "example_font": Font(italic=True, color=EXAMPLE_FONT_COLOR),
        "title_font": Font(bold=True, size=14, color=TEAL),
        "bold": Font(bold=True),
    }


def _about_sheet(wb, spec: dict) -> None:
    from openpyxl.styles import Font

    st = _styles()
    ws = wb.create_sheet("About", 0)
    ws.column_dimensions["A"].width = 100
    rows = [(spec["title"], st["title_font"]), (spec["description"], None), ("", None), ("How to use", st["bold"])]
    rows += [(f"• {line}", None) for line in spec.get("instructions", [])]
    rows += [
        ("• Rows in grey italics are examples from a made-up lab. Replace or delete them.", None),
        ("", None),
        (FOOTER, Font(size=8, color="808080")),
        (f"Source and guidance: {SITE}", Font(size=8, color="808080")),
    ]
    for i, (text, font) in enumerate(rows, start=1):
        cell = ws.cell(row=i, column=1, value=text)
        cell.alignment = st["wrap"]
        if font:
            cell.font = font


def _table_sheet(wb, sheet: dict) -> None:
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    st = _styles()
    ws = wb.create_sheet(sheet["name"])
    cols = sheet["columns"]
    n_rows = sheet.get("rows", 50)
    examples = sheet.get("examples", [])
    last = 1 + max(n_rows, len(examples))

    for j, col in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=col["header"])
        cell.font, cell.fill, cell.alignment, cell.border = st["header_font"], st["header_fill"], st["wrap"], st["border"]
        ws.column_dimensions[get_column_letter(j)].width = col.get("width", 16)
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "B2" if sheet.get("freeze_first_column") else "A2"

    for i in range(2, last + 1):
        example = examples[i - 2] if i - 2 < len(examples) else None
        for j, col in enumerate(cols, start=1):
            cell = ws.cell(row=i, column=j)
            cell.border, cell.alignment = st["border"], st["wrap"]
            if "formula" in col:
                cell.value = col["formula"].format(r=i)
            elif example is not None and j - 1 < len(example):
                cell.value = example[j - 1]
            if example is not None:
                cell.font = st["example_font"]
            if col.get("format") == "date":
                cell.number_format = "yyyy-mm-dd"
            elif col.get("format") == "percent":
                cell.number_format = "0%"
            elif col.get("format"):
                cell.number_format = col["format"]

    for j, col in enumerate(cols, start=1):
        letter = get_column_letter(j)
        if col.get("choices"):
            dv = DataValidation(type="list", formula1='"' + ",".join(col["choices"]) + '"', allow_blank=True)
            dv.error, dv.errorTitle = "Choose a value from the list.", "Not in the list"
            ws.add_data_validation(dv)
            dv.add(f"{letter}2:{letter}{last}")
        if col.get("format") == "date" and "formula" not in col:
            dv = DataValidation(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True)
            dv.error = "Enter a date, for example 2026-03-14."
            ws.add_data_validation(dv)
            dv.add(f"{letter}2:{letter}{last}")

    for rule in sheet.get("highlights", []):
        fill = PatternFill("solid", fgColor=rule.get("color", "FFCDD2"))
        rng = f"A2:{get_column_letter(len(cols))}{last}"
        ws.conditional_formatting.add(rng, FormulaRule(formula=[rule["formula"]], fill=fill))

    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{last}"
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToHeight = 0


# Uncertainty budget layout. The tests in tests/ rely on these cells.
UB_FIRST, UB_LAST = 6, 25  # component rows
UB_CELLS = {"value": "C28", "coverage": "C29", "fixed_k": "C30", "u_c": "C32", "v_eff": "C33", "k": "C34", "U": "C35", "U_rel": "C36"}


def _uncertainty_budget(wb, spec: dict) -> None:
    from openpyxl.styles import Font
    from openpyxl.worksheet.datavalidation import DataValidation

    st = _styles()
    ws = wb.create_sheet("Budget")
    ws["A1"] = "Uncertainty budget"
    ws["A1"].font = st["title_font"]
    ws["A2"] = "Measurand:"
    ws["B2"] = "e.g. Moisture content of wood pellets as received, % (m/m), oven drying at 105 °C"
    ws["B2"].font = st["example_font"]
    ws["A3"] = "Method, version, date, prepared by:"
    headers = [
        ("Source of uncertainty", 34), ("Value", 10), ("Distribution", 13), ("k (normal only)", 9),
        ("Sensitivity c", 10), ("Degrees of freedom (blank = infinite)", 13), ("Unit", 9),
        ("Divisor", 9), ("Standard uncertainty u", 12), ("Contribution |c|·u", 12),
        ("Share of variance", 10), ("Welch–Satterthwaite term", 12),
    ]
    from openpyxl.utils import get_column_letter

    for j, (h, w) in enumerate(headers, start=1):
        c = ws.cell(row=5, column=j, value=h)
        c.font, c.fill, c.alignment, c.border = st["header_font"], st["header_fill"], st["wrap"], st["border"]
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[5].height = 45
    ws.freeze_panes = "B6"

    examples = spec.get("examples", [])
    for r in range(UB_FIRST, UB_LAST + 1):
        ex = examples[r - UB_FIRST] if r - UB_FIRST < len(examples) else None
        if ex:
            for j, v in enumerate(ex, start=1):
                ws.cell(row=r, column=j, value=v).font = st["example_font"]
        ws[f"H{r}"] = (
            f'=IF(A{r}="","",IF(C{r}="normal",IF(D{r}="",1,D{r}),IF(C{r}="rectangular",SQRT(3),'
            f'IF(C{r}="triangular",SQRT(6),IF(C{r}="u-shaped",SQRT(2),NA())))))'
        )
        ws[f"I{r}"] = f'=IF(A{r}="","",ABS(B{r})/H{r})'
        ws[f"J{r}"] = f'=IF(A{r}="","",ABS(IF(E{r}="",1,E{r}))*I{r})'
        ws[f"K{r}"] = f'=IF(A{r}="","",J{r}^2/{UB_CELLS["u_c"]}^2)'
        ws[f"L{r}"] = f'=IF(OR(A{r}="",F{r}=""),0,J{r}^4/F{r})'
        for j in range(1, 13):
            cell = ws.cell(row=r, column=j)
            cell.border = st["border"]
            if j >= 8:
                cell.fill = st["label_fill"]
        ws[f"I{r}"].number_format = ws[f"J{r}"].number_format = "0.0000"
        ws[f"K{r}"].number_format = "0.0%"

    dv = DataValidation(type="list", formula1='"normal,rectangular,triangular,u-shaped"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"C{UB_FIRST}:C{UB_LAST}")

    rng = lambda col: f"{col}{UB_FIRST}:{col}{UB_LAST}"  # noqa: E731
    summary = [
        ("value", "Result y (needed only for the relative uncertainty)", spec.get("example_value")),
        ("coverage", "Coverage probability", 0.95),
        ("fixed_k", "Fixed k (optional; leave blank to use v_eff)", None),
        (None, "", None),
        ("u_c", "Combined standard uncertainty u_c", f"=SQRT(SUMSQ({rng('J')}))"),
        ("v_eff", "Effective degrees of freedom v_eff", f'=IF(SUM({rng("L")})=0,"infinite",{UB_CELLS["u_c"]}^4/SUM({rng("L")}))'),
        ("k", "Coverage factor k", (
            f'=IF({UB_CELLS["fixed_k"]}<>"",{UB_CELLS["fixed_k"]},IF({UB_CELLS["v_eff"]}="infinite",'
            f'_xlfn.NORM.S.INV(0.5+{UB_CELLS["coverage"]}/2),_xlfn.T.INV.2T(1-{UB_CELLS["coverage"]},{UB_CELLS["v_eff"]})))'
        )),
        ("U", "Expanded uncertainty U = k · u_c", f'={UB_CELLS["k"]}*{UB_CELLS["u_c"]}'),
        ("U_rel", "Relative expanded uncertainty U / |y|", f'=IF({UB_CELLS["value"]}="","",{UB_CELLS["U"]}/ABS({UB_CELLS["value"]}))'),
    ]
    row = 28
    for key, label, value in summary:
        ws.cell(row=row, column=1, value=label).font = st["bold"] if key in ("U",) else Font()
        if key:
            cell = ws.cell(row=row, column=3, value=value)
            cell.border = st["border"]
            if key in ("u_c", "v_eff", "k", "U", "U_rel"):
                cell.fill = st["label_fill"]
            if key == "value" and value is not None:
                cell.font = st["example_font"]
            assert f"C{row}" == UB_CELLS[key], (key, row)
        row += 1
    ws[UB_CELLS["coverage"]].number_format = "0%"
    ws[UB_CELLS["U_rel"]].number_format = "0.00%"
    for key in ("u_c", "U"):
        ws[UB_CELLS[key]].number_format = "0.0000"
    ws[UB_CELLS["v_eff"]].number_format = ws[UB_CELLS["k"]].number_format = "0.00"
    ws[UB_CELLS["U"]].font = st["bold"]

    notes = [
        "Value: for normal, a standard uncertainty (or an expanded one with its k in column D); for the other distributions, the half-width a.",
        "Divisors: rectangular √3, triangular √6, u-shaped √2. Sensitivity c is 1 when the source is already in the units of the result.",
        "Same calculation as labqc.uncertainty.combine for independent inputs. Excel rounds degrees of freedom down to a whole number in "
        "T.INV.2T, so k can be very slightly larger than labqc's.",
    ]
    for i, n in enumerate(notes, start=38):
        ws.cell(row=i, column=1, value=n).alignment = st["wrap"]
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=12)
        ws.row_dimensions[i].height = 30


BUILDERS = {"uncertainty_budget": _uncertainty_budget}


def build_xlsx(template: dict, out: Path) -> None:
    from openpyxl import Workbook

    spec = yaml.safe_load(template["source"].read_text(encoding="utf-8"))
    wb = Workbook()
    wb.remove(wb.active)
    _about_sheet(wb, spec)
    if spec.get("builder"):
        BUILDERS[spec["builder"]](wb, spec)
    for sheet in spec.get("sheets", []):
        _table_sheet(wb, copy.deepcopy(sheet))
    wb.active = 1 if len(wb.sheetnames) > 1 else 0
    wb.properties.title = template["title"]
    wb.properties.creator = "Lab Accreditation Handbook"
    wb.save(str(out))


# ---------------------------------------------------------------- reproducible output


def build_date() -> datetime:
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    return datetime.fromtimestamp(int(epoch), tz=timezone.utc) if epoch else PACK_DATE


def _zip_time() -> tuple[int, int, int, int, int, int]:
    return build_date().timetuple()[:6]


def normalise_ooxml(path: Path) -> None:
    """Give a .docx or .xlsx fixed entry timestamps and document dates.

    Word and Excel files are zip archives. Pandoc and openpyxl stamp the
    current time on every entry and in docProps/core.xml, so two builds of
    the same source differ. This rewrites both with build_date().
    """
    stamp = build_date().strftime("%Y-%m-%dT%H:%M:%SZ")
    with zipfile.ZipFile(path) as src:
        entries = [(info, src.read(info)) for info in src.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as dst:
        for info, data in entries:
            if info.filename == "docProps/core.xml":
                data = re.sub(
                    rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)",
                    lambda m: m.group(1) + stamp.encode() + m.group(2),
                    data,
                )
            out = zipfile.ZipInfo(info.filename, date_time=_zip_time())
            out.compress_type = zipfile.ZIP_DEFLATED
            out.external_attr = 0o644 << 16
            dst.writestr(out, data, compresslevel=9)
    path.write_bytes(buf.getvalue())


# ---------------------------------------------------------------- template pack


def _clauses_by_template() -> dict[str, list[str]]:
    data = yaml.safe_load(CLAUSES.read_text(encoding="utf-8"))
    out: dict[str, list[str]] = {}
    for c in data["clauses"]:
        for tid in c.get("templates", []):
            out.setdefault(tid, []).append(f"{c['number']} {c['title']}")
    return out


def pack_readme(templates: list[dict]) -> str:
    """README.txt for the zip: licence, credit, warning, and every file with its clauses."""
    clauses = _clauses_by_template()
    lines = [
        "ISO/IEC 17025 QMS starter pack",
        "Lab Accreditation Handbook",
        "=" * 30,
        "",
        f"{len(templates)} editable Word and Excel templates for a small testing or",
        "calibration lab working towards ISO/IEC 17025:2017 accreditation.",
        "",
        f"Guidance for every template: {SITE}",
        f"All templates online: {SITE}template-library/",
        "",
        "ADAPT BEFORE USE",
        "----------------",
        "A template is a starting point. Make it match how your lab actually",
        "works, and check it against your accreditation body's rules. An",
        "assessor will notice a form copied without thought. This is not",
        "official guidance; the standard and your accreditation body's",
        "documents take priority.",
        "",
        "LICENCE",
        "-------",
        "Creative Commons Attribution 4.0 International (CC BY 4.0),",
        "https://creativecommons.org/licenses/by/4.0/",
        "You may use, adapt and share these templates, also commercially, if",
        "you give credit. Suggested credit line:",
        "",
        f'  "Based on templates from the Lab Accreditation Handbook ({SITE}),',
        '   CC BY 4.0."',
        "",
        "FILES",
        "-----",
    ]
    for t in templates:
        name = output_path(t).name
        supports = "; ".join(clauses.get(t["id"], [])) or "preparing for assessment (Start here)"
        lines += ["", name, f"  {t['title']} ({t['type']}, {'Word' if t['format'] == 'docx' else 'Excel'})",
                  f"  {t['description']}", f"  Clauses: {supports}"]
    return "\r\n".join(lines) + "\r\n"


def pack_bytes(templates: list[dict]) -> bytes:
    """The zip, built in memory: fixed file order, timestamps and permissions."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        files = [("README.txt", pack_readme(templates).encode("utf-8"))]
        files += [(output_path(t).name, output_path(t).read_bytes()) for t in templates]
        for name, data in files:
            info = zipfile.ZipInfo(name, date_time=_zip_time())
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data, compresslevel=9)
    return buf.getvalue()


def write_pack(quiet: bool = False) -> dict:
    """Write the zip and pack.json, only where their content changed."""
    templates = sorted(catalog(), key=lambda t: output_path(t).name)
    data = pack_bytes(templates)
    if not PACK.exists() or PACK.read_bytes() != data:
        PACK.write_bytes(data)
        if not quiet:
            print(f"packed {PACK.relative_to(ROOT)} ({len(templates)} templates, {len(data) // 1024} KB)")
    info = {
        "count": len(templates),
        "zip": f"downloads/{PACK.name}",
        "bytes": len(data),
        "files": [output_path(t).name for t in templates],
    }
    text = json.dumps(info, indent=2) + "\n"
    PACK_DATA.parent.mkdir(parents=True, exist_ok=True)
    if not PACK_DATA.exists() or PACK_DATA.read_text(encoding="utf-8") != text:
        PACK_DATA.write_text(text, encoding="utf-8")
    return info


# ---------------------------------------------------------------- driver


def build(force: bool = False, quiet: bool = False) -> list[Path]:
    """Build every template whose output is missing or older than its source or this script,
    then refresh the zip pack."""
    OUT.mkdir(parents=True, exist_ok=True)
    script_time = Path(__file__).stat().st_mtime
    built = []
    for t in catalog():
        out = output_path(t)
        stale = force or not out.exists() or out.stat().st_mtime < max(t["source"].stat().st_mtime, script_time)
        if not stale:
            continue
        (build_docx if t["format"] == "docx" else build_xlsx)(t, out)
        normalise_ooxml(out)
        built.append(out)
        if not quiet:
            print(f"built {out.relative_to(ROOT)}")
    known = {output_path(t).name for t in catalog()} | {PACK.name}
    for old in OUT.iterdir():
        if old.is_file() and old.name not in known:
            old.unlink()
            if not quiet:
                print(f"removed {old.relative_to(ROOT)}")
    write_pack(quiet=quiet)
    return built


if __name__ == "__main__":
    built = build(force="--force" in sys.argv)
    print(f"{len(built)} template(s) built")
