"""Regression test for Unicode Greek text in pdf-maker."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from pdf_maker import NewPDF


def test_greek_round_trip(tmp_path):
    output = Path(r"C:\Users\Young\Downloads") / "greek.pdf"
    expected = "Greek: α β γ δ θ λ μ π σ φ χ ψ ω Δ Ω"
    pdf = NewPDF(filepath=str(output))
    pdf.text(page=1, x=72, y=700, text=expected)
    pdf.save()
    print(pdf.filepath)

    extracted = subprocess.check_output(["pdftotext", str(output), "-"])
    assert expected in extracted.decode("utf-8")


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as directory:
        test_greek_round_trip(Path(directory))
    print("Greek Unicode PDF test passed")
