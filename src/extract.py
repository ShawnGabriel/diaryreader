"""Extract structured waypoint records from every page of a PDF,
caching per-page results so re-runs don't re-pay for unchanged pages."""
import hashlib
import json
import os

from tqdm import tqdm

from src.pdf_to_images import pdf_to_images
from src.vlm_client import VLMClient


def _page_hash(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def extract_pdf(pdf_path: str, client: VLMClient, prompt: str, dpi: int,
                 tmp_image_dir: str, cache_dir: str) -> list[dict]:
    os.makedirs(cache_dir, exist_ok=True)
    image_paths = pdf_to_images(pdf_path, tmp_image_dir, dpi=dpi)

    all_records = []
    source_name = os.path.basename(pdf_path)
    for image_path in tqdm(image_paths, desc=f"Pages in {source_name}"):
        h = _page_hash(image_path)
        cache_path = os.path.join(cache_dir, f"{h}.json")

        if os.path.exists(cache_path):
            with open(cache_path) as f:
                records = json.load(f)
        else:
            try:
                records = client.extract_page(image_path, prompt)
            except ValueError as e:
                print(f"  [WARN] {e}")
                records = []
            with open(cache_path, "w") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)

        for r in records:
            r["_source_file"] = source_name
            r["_source_page"] = os.path.basename(image_path)
        all_records.extend(records)

    return all_records
