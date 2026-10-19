
from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = ROOT / "data" / "raw" / "mock_life_insurance_policy.pdf"


def load_pdf(pdf_path: Path = PDF_PATH) -> list[dict]:
    """Extract text and page numbers from a PDF."""
    pages = []

    with fitz.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text,
                })

    return pages


if __name__ == "__main__":
    pages = load_pdf()

    print(f"PDF: {PDF_PATH.name}")
    print(f"Pages extracted: {len(pages)}")

    for page in pages:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"][:500])
