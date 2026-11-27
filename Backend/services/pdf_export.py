import io
import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    try:
        from weasyprint import HTML
    except (ImportError, OSError):
        return _render_with_edge(html_docs)

    documents = [HTML(string=html).render() for html in html_docs.values()]
    pages = [page for document in documents for page in document.pages]
    return documents[0].copy(pages).write_pdf()


def _render_with_edge(html_docs: dict[str, str]) -> bytes:
    from PyPDF2 import PdfWriter

    edge = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))
    edge = edge / "Microsoft" / "Edge" / "Application" / "msedge.exe"
    if os.name != "nt" or not edge.is_file():
        raise RuntimeError("PDF export requires WeasyPrint or Microsoft Edge on Windows.")

    writer = PdfWriter()
    with TemporaryDirectory(prefix="ats-report-") as folder:
        work_dir = Path(folder)
        for index, html in enumerate(html_docs.values()):
            source = work_dir / f"report-{index}.html"
            target = source.with_suffix(".pdf")
            source.write_text(html, encoding="utf-8")
            subprocess.run(
                [
                    str(edge),
                    "--headless",
                    "--disable-gpu",
                    "--disable-background-networking",
                    "--no-first-run",
                    "--no-pdf-header-footer",
                    f"--user-data-dir={work_dir / 'profile'}",
                    f"--print-to-pdf={target}",
                    source.as_uri(),
                ],
                capture_output=True,
                check=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            writer.append(io.BytesIO(target.read_bytes()))

    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()
