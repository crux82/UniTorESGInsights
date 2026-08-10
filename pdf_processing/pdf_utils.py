import os
import re
import csv
import fitz

def get_cnt(text):
    cnt = 0
    for word in text.split():
        if word.isalpha():
            cnt += 1
    return cnt

# Function to extract text from a page including text
def extract_text(page) -> str:
    page_blocks = page.get_text('blocks', sort=False, flags=fitz.TEXTFLAGS_SEARCH & fitz.TEXT_DEHYPHENATE & ~fitz.TEXT_PRESERVE_IMAGES)

    page_text = ''
    for block in page_blocks:
        block_text = block[4]  # STRUCTURE: (x0, y0, x1, y1, text, block_no, block_type)

        # a) Remove starting and ending whitespaces
        block_text = block_text.replace('\n', ' ').strip()
        page_text += block_text + '\n'

    # b) Add full stop in different "sentences" --> e.g., improved readability \n In 2021 the company will ..
    page_text = re.sub(pattern=r'([a-zA-Z0-9 ])(\n+)([A-Z])', repl=r'\1. \2\3', string=page_text)

    # b) Remove the new line in the middle of a sentence --> e.g., improved readability \n of the code
    page_text = re.sub(pattern=r'([^.])(\n)([^A-Z])', repl=r'\1 \3', string=page_text)

    # c) Remove duplicated white spaces --> e.g., improved  readability
    page_text = re.sub(pattern=r' +', repl=' ', string=page_text)

    # Save the page text in the document text --> pages separated by two new lines
    page_text = re.sub(pattern=r'\n{3,}', repl=r'\n\n\n', string=page_text)

    return page_text.strip()

def process_pdf(pdf_path, csv_path):
    # Set to store unique paragraphs
    unique_paragraphs = set()
    #paragraph_counter = 0  # <-- new counter whole doc

    doc = fitz.open(pdf_path)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Doc_name","Page_num","Paragraph_num","Paragraph_content","Paragraph_length"
        ])
        writer.writeheader()

        for p in range(len(doc)):
            page = doc.load_page(p)
            text = extract_text(page)
            paragraph_counter = 0  # <-- new counter per page

            # Split the page content into separate paragraphs
            paragraphs = text.strip().split('\n')
            MIN_WORD_CNT = 20
            for idx, paragraph in enumerate(paragraphs):
                # Check if paragraph content is not empty and length is greater than 10
                word_count = get_cnt(paragraph)
                if word_count > MIN_WORD_CNT:
                    # Check if paragraph is unique
                    if paragraph not in unique_paragraphs:
                        # Add paragraph to set of unique paragraphs
                        unique_paragraphs.add(paragraph)
                        paragraph_counter += 1  # increment only when valid
                        # Write the paragraph content and its word count to the CSV file
                        writer.writerow({
                            "Doc_name": os.path.basename(pdf_path),
                            "Page_num": p+1,
                            "Paragraph_num": paragraph_counter,  # <-- reset-based numbering "Paragraph_num": idx,
                            "Paragraph_content": paragraph,
                            "Paragraph_length": word_count,
                        })

def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    paths = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        p = f"/tmp/page_{i}.png"
        pix.save(p)
        paths.append(p)

    return paths