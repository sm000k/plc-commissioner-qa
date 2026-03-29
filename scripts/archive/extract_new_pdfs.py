import pdfplumber
import os

pdfs = [
    r"btc.pl-podstawy_programowania_sterownikow_s7_1200_w_jezyku_scl-tomasz_gilewski (2).pdf",
    r"siemens SCL.PDF",
    r"Sterowniki_PLC.pdf",
    r"Simatic-s7-1200-w-zadaniach (1)\Simatic-s7-1200-w-zadaniach.pdf",
    r"Simatic-s7-1200-w-zadaniach_LAD_Zaawansowany (3)\Simatic-s7-1200-w-zadaniach_LAD_Zaawansowany.pdf",
]

for pdf_path in pdfs:
    print(f"\n{'='*70}")
    print(f"FILE: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total = len(pdf.pages)
            print(f"PAGES: {total}")
            # Extract first 6 pages for overview
            for i, page in enumerate(pdf.pages[:6]):
                text = page.extract_text()
                if text:
                    print(f"\n--- Page {i+1} ---")
                    print(text[:1200])
    except Exception as e:
        print(f"ERROR: {e}")
