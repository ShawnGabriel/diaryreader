#!/usr/bin/env python3
"""Entry point: data/pdfs/*.pdf -> outputs/field_notes.xlsx

Usage:
    python run_pipeline.py                 # process every PDF in PDF_DIR
    python run_pipeline.py notebook1.pdf    # process just this one file
"""
import glob
import os
import sys

from dotenv import load_dotenv

from src.extract import extract_pdf
from src.vlm_client import VLMClient
from src.build_spreadsheet import build_workbook

load_dotenv()

PDF_DIR = os.getenv("PDF_DIR", "data/pdfs")
OUTPUT_XLSX = os.getenv("OUTPUT_XLSX", "outputs/field_notes.xlsx")
CACHE_DIR = os.getenv("CACHE_DIR", "outputs/.cache")
PAGE_DPI = int(os.getenv("PAGE_DPI", "300"))
TMP_IMAGE_DIR = os.path.join(CACHE_DIR, "_page_images")

VLM_BASE_URL = os.environ["VLM_BASE_URL"]
VLM_API_KEY = os.environ["VLM_API_KEY"]
VLM_MODEL = os.environ["VLM_MODEL"]

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts", "extraction_prompt.md")


def main():
    with open(PROMPT_PATH) as f:
        prompt = f.read()

    if len(sys.argv) > 1:
        pdf_paths = sys.argv[1:]
    else:
        pdf_paths = sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf")))

    if not pdf_paths:
        print(f"No PDFs found in {PDF_DIR}. Drop some in there, or pass paths as arguments.")
        return

    client = VLMClient(base_url=VLM_BASE_URL, api_key=VLM_API_KEY, model=VLM_MODEL)

    records_by_source = {}
    for pdf_path in pdf_paths:
        print(f"\n== {pdf_path} ==")
        records = extract_pdf(
            pdf_path, client, prompt,
            dpi=PAGE_DPI, tmp_image_dir=TMP_IMAGE_DIR, cache_dir=CACHE_DIR,
        )
        records_by_source[os.path.basename(pdf_path)] = records
        print(f"  -> {len(records)} waypoint records")

    os.makedirs(os.path.dirname(OUTPUT_XLSX), exist_ok=True)
    build_workbook(records_by_source, OUTPUT_XLSX)
    print(f"\nSaved: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
