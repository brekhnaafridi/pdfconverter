#!/usr/bin/env python3
"""
PDF Converter - a small command-line tool.

Install:
    pip install pillow pymupdf reportlab
    (Word/PowerPoint/Excel -> PDF also needs LibreOffice installed: https://www.libreoffice.org)

Usage examples:
    python pdf_converter.py img2pdf photo1.jpg photo2.png -o photos.pdf
    python pdf_converter.py txt2pdf notes.txt -o notes.pdf
    python pdf_converter.py office2pdf report.docx            # .docx .doc .pptx .xlsx ...
    python pdf_converter.py pdf2img file.pdf --dpi 200 --format png
    python pdf_converter.py pdf2txt file.pdf
    python pdf_converter.py merge a.pdf b.pdf -o merged.pdf
    python pdf_converter.py split file.pdf --pages 1-3 -o first3.pdf
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


# ---------- helpers ----------
def die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def check_files(paths):
    for p in paths:
        if not Path(p).is_file():
            die(f"file not found: {p}")


def parse_pages(spec, total):
    """'1-3,5' -> [0,1,2,4] (zero-based)."""
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            start = int(a) if a else 1
            end = int(b) if b else total
            pages.extend(range(start - 1, end))
        else:
            pages.append(int(part) - 1)
    for p in pages:
        if p < 0 or p >= total:
            die(f"page {p + 1} is out of range (document has {total} pages)")
    return pages


# ---------- converters ----------
def img2pdf(args):
    from PIL import Image

    check_files(args.inputs)
    images = []
    for path in args.inputs:
        img = Image.open(path)
        if img.mode in ("RGBA", "P", "LA"):
            bg = Image.new("RGB", img.size, "white")
            rgba = img.convert("RGBA")
            bg.paste(rgba, mask=rgba.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
        images.append(img)
    out = args.output or "output.pdf"
    images[0].save(out, save_all=True, append_images=images[1:])
    print(f"Created {out} ({len(images)} page(s))")


def txt2pdf(args):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    check_files(args.inputs)
    src = Path(args.inputs[0])
    out = args.output or str(src.with_suffix(".pdf"))
    text = src.read_text(encoding="utf-8", errors="replace")

    c = canvas.Canvas(out, pagesize=A4)
    width, height = A4
    margin, font, size, lead = 50, "Helvetica", 11, 14
    max_chars = int((width - 2 * margin) / (size * 0.5))
    y = height - margin
    c.setFont(font, size)

    for raw in text.splitlines() or [""]:
        # simple word wrap
        lines, line = [], ""
        for word in raw.split(" "):
            if len(line) + len(word) + 1 <= max_chars:
                line = f"{line} {word}".strip()
            else:
                lines.append(line)
                line = word
        lines.append(line)
        for ln in lines:
            if y < margin:
                c.showPage()
                c.setFont(font, size)
                y = height - margin
            c.drawString(margin, y, ln)
            y -= lead
    c.save()
    print(f"Created {out}")


def office2pdf(args):
    check_files(args.inputs)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        die("LibreOffice not found. Install it from https://www.libreoffice.org")
    outdir = Path(args.output or ".")
    outdir.mkdir(parents=True, exist_ok=True)
    for path in args.inputs:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(outdir), path],
            check=True,
        )
        print(f"Converted {path} -> {outdir / (Path(path).stem + '.pdf')}")


def pdf2img(args):
    import fitz  # PyMuPDF

    check_files(args.inputs)
    src = Path(args.inputs[0])
    outdir = Path(args.output or f"{src.stem}_images")
    outdir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(src)
    zoom = args.dpi / 72
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        dest = outdir / f"page_{i:03d}.{args.format}"
        pix.save(dest)
    print(f"Saved {len(doc)} image(s) to {outdir}/")


def pdf2txt(args):
    import fitz

    check_files(args.inputs)
    src = Path(args.inputs[0])
    out = args.output or str(src.with_suffix(".txt"))
    doc = fitz.open(src)
    text = "\n\n".join(page.get_text() for page in doc)
    Path(out).write_text(text, encoding="utf-8")
    if not text.strip():
        print("Warning: no text found. The PDF may be scanned (needs OCR).")
    print(f"Created {out}")


def merge(args):
    import fitz

    check_files(args.inputs)
    out = args.output or "merged.pdf"
    merged = fitz.open()
    for path in args.inputs:
        with fitz.open(path) as doc:
            merged.insert_pdf(doc)
    merged.save(out)
    print(f"Created {out} ({len(merged)} pages)")


def split(args):
    import fitz

    check_files(args.inputs)
    src = Path(args.inputs[0])
    doc = fitz.open(src)
    pages = parse_pages(args.pages, len(doc))
    out = args.output or f"{src.stem}_extract.pdf"
    new = fitz.open()
    for p in pages:
        new.insert_pdf(doc, from_page=p, to_page=p)
    new.save(out)
    print(f"Created {out} ({len(pages)} pages)")


# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Simple PDF converter")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_):
        p = sub.add_parser(name, help=help_)
        p.add_argument("inputs", nargs="+", help="input file(s)")
        p.add_argument("-o", "--output", help="output file or folder")
        p.set_defaults(func=fn)
        return p

    add("img2pdf", img2pdf, "images (jpg/png/...) -> one PDF")
    add("txt2pdf", txt2pdf, "text file -> PDF")
    add("office2pdf", office2pdf, "Word/PowerPoint/Excel -> PDF (needs LibreOffice)")
    p = add("pdf2img", pdf2img, "PDF -> images, one per page")
    p.add_argument("--dpi", type=int, default=150)
    p.add_argument("--format", choices=["png", "jpg"], default="png")
    add("pdf2txt", pdf2txt, "PDF -> text file")
    add("merge", merge, "merge several PDFs into one")
    p = add("split", split, "extract pages from a PDF")
    p.add_argument("--pages", required=True, help="e.g. 1-3,5")

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
