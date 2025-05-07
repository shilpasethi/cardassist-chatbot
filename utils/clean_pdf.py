import fitz  
import re
import os
import logging
import stat

# Define the logger globally
logger = logging.getLogger(__name__)

def remove_footer_by_margin(doc, footer_margin=80) -> str:
    """
    Removes all text blocks from the bottom 'footer_margin' of each page.
    """
    for page_num, page in enumerate(doc, start=1):
        logger.info(f"\nProcessing Page {page_num}")
        height = page.rect.height
        footer_threshold = height - footer_margin

        blocks = page.get_text("blocks")

        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            text = text.strip()
            if not text:
                continue

            # If block is in the bottom margin
            if y1 > footer_threshold:
                logger.info(f"  Removing block in footer: \"{text}\" (Y1: {y1:.2f})")
                page.add_redact_annot(fitz.Rect(x0, y0, x1, y1), fill=(1, 1, 1))

        # Apply redactions to make removals permanent
        page.apply_redactions()
    return doc

def is_toc_line(text):
    """
    Detect lines that look like TOC entries (e.g., title followed by page number).
    """
    return bool(re.search(r'\.{2,}\s*\d+$', text)) or bool(re.search(r'\s+\d+$', text.strip()))

def is_toc_page(text):
    """
    Determine if a page is likely a TOC based on line patterns (not keywords).
    """
    lines = text.splitlines()
    toc_like_lines = 0

    for line in lines:
        if is_toc_line(line):
            toc_like_lines += 1

    logger.info(f"  TOC-like lines found: {toc_like_lines}")
    return toc_like_lines >= 5  # Threshold: can be adjusted

def has_toc_keyword_in_top_lines(text, num_lines=5):
    """
    Check if any of the top N lines contain TOC-related keywords.
    """
    lines = text.splitlines()[:num_lines]
    for line in lines:
        line_lower = line.strip().lower()
        if "table of contents" in line_lower or line_lower == "contents":
            logger.info(f"  Found TOC keyword in line: '{line}'")
            return True
    return False

def remove_toc(doc, max_pages_to_check=5) -> str:
    """
    Remove likely Table of Contents pages from a PDF.
    """
    pages_to_remove = []

    for i in range(min(len(doc), max_pages_to_check)):
        page = doc[i]
        text = page.get_text()

        logger.info(f"\nAnalyzing Page {i + 1}...")

        if is_toc_page(text):
            logger.info(f"  --> Page {i + 1} likely contains TOC. Marked for removal.")
            pages_to_remove.append(i)
        else:
            logger.info(f"  --> Page {i + 1} does not appear to be TOC.")

    logger.info(f"\nPages marked for removal: {[p + 1 for p in pages_to_remove]}")
    for i in sorted(pages_to_remove, reverse=True):
        doc.delete_page(i)
        logger.info(f"Removed page {i + 1}")
    return doc


def clean_pdf(pdf_path: str) -> str:
    """
    Cleans the PDF by removing footers and optionally TOC pages, 
    and saves the cleaned PDF to a new file. Deletes the destination file if it already exists.

    Args:
        pdf_path (str): Path to the input PDF file.

    Returns:
        str: Path to the cleaned PDF file.
    """
    logger.info(f"Cleaning PDF: {pdf_path}")

    base, ext = os.path.splitext(pdf_path)
    dst_path = f"{base}_clean{ext}"

    # Check if the destination file already exists and delete it
    if os.path.exists(dst_path):
        logger.info(f"File {dst_path} already exists. Deleting it.")
        os.chmod(dst_path, stat.S_IWRITE)  # Ensure the file is writable
        os.remove(dst_path)

    # Open the PDF and process it
    doc = None
    try:
        doc = fitz.open(pdf_path)
        doc = remove_footer_by_margin(doc, footer_margin=80)
        # doc = remove_toc(doc, 5)

        # Save the cleaned PDF
        doc.save(dst_path)
        logger.info(f"Cleaned PDF saved to: {dst_path}")
    finally:
        # Ensure the document is closed
        if doc:
            doc.close()

    return dst_path