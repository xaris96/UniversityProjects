from pathlib import Path
import textwrap

from fpdf import FPDF


def sanitize(text: str) -> str:
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def add_wrapped_line(pdf: FPDF, text: str) -> None:
    safe = sanitize(text)
    if safe == "":
        pdf.ln(6)
        return

    max_chars = 95 if pdf.font_family.lower() == "courier" else 115
    wrapped = textwrap.wrap(
        safe,
        width=max_chars,
        replace_whitespace=False,
        drop_whitespace=False,
        break_long_words=True,
        break_on_hyphens=False,
    )
    if not wrapped:
        wrapped = [" "]

    for segment in wrapped:
        pdf.cell(0, 6, segment, new_x="LMARGIN", new_y="NEXT")


def build_pdf(md_path: Path, pdf_path: Path) -> None:
    lines = md_path.read_text(encoding="utf-8").splitlines()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    in_code = False
    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            in_code = not in_code
            pdf.ln(1)
            continue

        if in_code:
            pdf.set_font("Courier", size=9)
            add_wrapped_line(pdf, line if line else " ")
            continue

        if line.startswith("# "):
            pdf.set_font("Helvetica", style="B", size=16)
            add_wrapped_line(pdf, line[2:].strip())
            pdf.ln(1)
            continue

        if line.startswith("## "):
            pdf.set_font("Helvetica", style="B", size=13)
            add_wrapped_line(pdf, line[3:].strip())
            pdf.ln(0.5)
            continue

        if line.startswith("### "):
            pdf.set_font("Helvetica", style="B", size=11)
            add_wrapped_line(pdf, line[4:].strip())
            continue

        if line.startswith("#### "):
            pdf.set_font("Helvetica", style="B", size=10)
            add_wrapped_line(pdf, line[5:].strip())
            continue

        pdf.set_font("Helvetica", size=10)
        if line.startswith("- "):
            add_wrapped_line(pdf, "* " + line[2:])
        else:
            add_wrapped_line(pdf, line if line else " ")

    pdf.output(str(pdf_path))


if __name__ == "__main__":
    src = Path("Proj2_Mongo_report.md")
    dst = Path("Proj2_Mongo_report.pdf")
    build_pdf(src, dst)
    print(f"PDF rebuilt: {dst}")
