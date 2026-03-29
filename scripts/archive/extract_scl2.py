import pdfplumber
import sys

def extract_pages(path, pages_range, chars=1500):
    with pdfplumber.open(path) as pdf:
        total = len(pdf.pages)
        sys.stdout.buffer.write(f"\n{'='*70}\nFILE: {path} | TOTAL: {total}\n".encode('utf-8'))
        for i in pages_range:
            if i < total:
                text = pdf.pages[i].extract_text()
                if text and len(text.strip()) > 30:
                    out = f"\n--- Page {i+1} ---\n{text[:chars]}\n"
                    sys.stdout.buffer.write(out.encode('utf-8', errors='replace'))

# siemens SCL.PDF - S7-300/400 era SCL reference (academic thesis)
extract_pages("siemens SCL.PDF", range(6, 50), chars=1200)
