import pdfplumber

# Deep-dive into Sterowniki_PLC.pdf - general PLC concepts 
# and siemens SCL.PDF - SCL reference
# Looking for technical facts to compare with Q&A

def extract_pages(path, pages_range):
    with pdfplumber.open(path) as pdf:
        total = len(pdf.pages)
        print(f"\n{'='*70}")
        print(f"FILE: {path} | TOTAL PAGES: {total}")
        for i in pages_range:
            if i < total:
                text = pdf.pages[i].extract_text()
                if text and len(text.strip()) > 30:
                    print(f"\n--- Page {i+1} ---")
                    print(text[:2000])

# Sterowniki_PLC.pdf: pages about PROFINET, scan cycle, I/O modules
extract_pages("Sterowniki_PLC.pdf", range(0, 30))
