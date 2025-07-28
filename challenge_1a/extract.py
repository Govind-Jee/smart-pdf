# In extract.py
import fitz  # This is the PyMuPDF library
import operator

def extract_pdf_outline(pdf_path):
    """
    Extracts title and headings from a PDF by analyzing font properties.
    """
    doc = fitz.open(pdf_path)
    font_counts = {}

    # 1. First, loop through the document to find all font sizes and styles
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"])
                        font_counts[size] = font_counts.get(size, 0) + 1
    
    # 2. Sort fonts by how often they appear. The least common are usually headings.
    sorted_fonts = sorted(font_counts.items(), key=operator.itemgetter(1), reverse=True)
    
    # 3. Assume the top 3-4 largest and least frequent fonts are headings
    # This logic is more robust than just checking font size, as advised in the PDF [cite: 94]
    try:
        h1_size = sorted_fonts[-1][0]
        h2_size = sorted_fonts[-2][0]
        h3_size = sorted_fonts[-3][0]
    except IndexError: # Fallback for very simple PDFs
        h1_size, h2_size, h3_size = 20, 16, 14

    title = ""
    outline = []
    
    # 4. Second loop to actually pull out the text based on our identified heading sizes
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue

                        size = round(span["size"])
                        
                        # A simple way to find the title
                        if page_num == 1 and size == h1_size and not title:
                            title = text

                        # Create the heading list
                        if size == h1_size:
                            outline.append({"level": "H1", "text": text, "page": page_num})
                        elif size == h2_size:
                            outline.append({"level": "H2", "text": text, "page": page_num})
                        elif size == h3_size:
                            outline.append({"level": "H3", "text": text, "page": page_num})

    # 5. Format the final dictionary to be converted to JSON, as required [cite: 43]
    return {"title": title, "outline": outline}