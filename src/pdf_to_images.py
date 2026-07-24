"""Render every page of a PDF to a PNG image."""
import os
from pdf2image import convert_from_path


def pdf_to_images(pdf_path: str, out_dir: str, dpi: int = 300) -> list[str]:
    """Render pdf_path's pages to PNGs in out_dir. Returns sorted list of paths."""
    os.makedirs(out_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi)
    paths = []
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    for i, page in enumerate(pages, start=1):
        path = os.path.join(out_dir, f"{stem}_page-{i:02d}.png")
        page.save(path, "PNG")
        paths.append(path)
    return paths
