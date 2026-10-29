import sys
for mod in ["pypdf", "pdfplumber", "fitz", "pypdf2"]:
    try:
        __import__(mod)
        print(f"{mod}: available")
    except ImportError:
        print(f"{mod}: NOT available")
