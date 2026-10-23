import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from jobagent import ROOT

MAX_PDF_BYTES = int(2.5 * 1024 * 1024)
RESUME_FILENAME = "Harshal_Shinoy_Thachapully_Resume.pdf"


def render_resume(packet: Path, out_dir: Path) -> Path:
    """Compile a resume packet to PDF with Typst. Returns the PDF path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / RESUME_FILENAME
    packet_in_root = "/" + str(packet.resolve().relative_to(ROOT))
    subprocess.run(
        [
            "typst", "compile", "--root", str(ROOT),
            str(ROOT / "profile" / "resume.typ"), str(pdf),
            "--input", f"packet={packet_in_root}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return pdf


@dataclass
class PdfCheck:
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def pdf_text(pdf: Path) -> str:
    if shutil.which("pdftotext") is None:
        raise RuntimeError("pdftotext not found; install poppler-utils")
    result = subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True)
    return result.stdout


def check_pdf(pdf: Path, packet: Path) -> PdfCheck:
    """ATS round-trip: size limit, and every bullet extractable as text in reading order."""
    check = PdfCheck()
    size = pdf.stat().st_size
    if size > MAX_PDF_BYTES:
        check.errors.append(f"PDF is {size} bytes; Greenhouse limit is {MAX_PDF_BYTES}")

    text = _normalize(pdf_text(pdf))
    data = yaml.safe_load(packet.read_text())
    bullets = [b["text"] for job in data.get("experience", []) for b in job.get("bullets", [])]
    bullets += [b["text"] for proj in data.get("projects", []) for b in proj.get("bullets", [])]

    last = -1
    for bullet in bullets:
        pos = text.find(_normalize(bullet))
        if pos == -1:
            check.errors.append(f"bullet not extractable as text: {bullet[:60]}...")
        elif pos < last:
            check.errors.append(f"bullet out of reading order: {bullet[:60]}...")
        else:
            last = pos
    return check
