import pdfplumber

# Extract from siemens SCL.PDF - SCL language reference
# and btc.pl SCL book - S7-1200 SCL specific
# Focus on technically relevant content

def extract_pages(path, pages_range, chars=1500):
    with pdfplumber.open(path) as pdf:
        total = len(pdf.pages)
        print(f"\n{'='*70}")
        print(f"FILE: {path} | TOTAL PAGES: {total}")
        for i in pages_range:
            if i < total:
                text = pdf.pages[i].extract_text()
                if text and len(text.strip()) > 30:
                    print(f"\n--- Page {i+1} ---")
                    print(text[:chars])

# siemens SCL.PDF - all pages for full reference
extract_pages("siemens SCL.PDF", range(6, 50), chars=1200)
