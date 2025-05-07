import pdfplumber
import re

def extract_toc_entries(pdf):
    """
    Parses the PDF's Table of Contents page to extract (title, page_number) entries.
    Returns a list of tuples.
    """
    toc_entries = []
#    with pdfplumber.open(pdf_path) as pdf:
        # 1. Locate the TOC page by finding "Contents"
    toc_page_index = None
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        if re.search(r'\bContents\b', text):
            toc_page_index = i
            break
    if toc_page_index is None:
        raise RuntimeError("Table of Contents page not found")

    # 2. Parse the TOC lines for "Title ... page"
    lines = pdf.pages[toc_page_index].extract_text().splitlines()
    for line in lines:
        # Match formats like "Section Title ........ 12" or "Section Title    12"
        match = re.match(r'^(.*?)\.{2,}\s*(\d+)$', line) or re.match(r'^(.*?)\s+(\d+)$', line)
        if match:
            title, page_str = match.groups()
            toc_entries.append((title.strip(), int(page_str)))

    return toc_entries

def extract_sections_by_toc(pdf_path):
    """
    Uses the TOC entries to slice the PDF into sections.
    Returns a list of dicts with keys: title, start_page, end_page, text.
    """
    sections = []

    with pdfplumber.open(pdf_path) as pdf:
        try:
            toc = extract_toc_entries(pdf)
            print(f"Extracted TOC: {toc}")

            num_pages = len(pdf.pages)
            print(f"Total pages in PDF: {num_pages}")
            for idx, (title, pg) in enumerate(toc):
                start_idx = pg - 1
                # Determine end index (one before the next section starts)
                if idx + 1 < len(toc):
                    end_idx = toc[idx+1][1] - 2
                else:
                    end_idx = num_pages - 1

                # Aggregate text for this section
                sec_text = ""
                for p in range(start_idx, end_idx + 1):
                    sec_text += pdf.pages[p].extract_text() or ""

                sections.append({
                    "title": title,
                    "start_gpage": start_idx + 1,
                    "end_page": end_idx + 1,
                    "text": sec_text.strip()
                })
                print(f"Extracted section: {title} (pages {start_idx + 1}-{end_idx + 1})")
        finally:
            pdf.close()
    # for sec in sections:
    #     print(f"{sec['title']}  (pages {sec['start_page']}-{sec['end_page']})")
    #     print("section text:", sec['text'][:1000])  # Print first 1000 chars of each section
    
    return sections

# if __name__ == "__main__":
#     #PDF_PATH = "global_card_access_user_guide_cleaned.pdf"
#     sections = extract_sections_by_toc(PDF_PATH)
#     for sec in sections:
#         print(f"{sec['title']}  (pages {sec['start_page']}-{sec['end_page']})")
#         print("section text:", sec['text'][:1000])  # Print first 1000 chars of each section

