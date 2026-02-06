"""
Test script for resume_to_json parsing.
Usage: python3 test.py <resume_name.pdf>
  - Reads the PDF from this same directory (backend/services/)
  - Passes extracted text through the same prompt as resume_to_json
  - Saves output to test.txt
"""
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pypdf import PdfReader
from services.resume_to_json import parse_resume_to_json


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test.py <resume_name.pdf>")
        sys.exit(1)

    pdf_name = sys.argv[1]
    services_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(services_dir, pdf_name)

    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)

    print(f"📄 Reading PDF: {pdf_name}")
    resume_text = extract_text_from_pdf(pdf_path)

    if not resume_text.strip():
        print("⚠️  No text extracted from PDF (might be image-based).")
        sys.exit(1)

    print(f"📝 Extracted {len(resume_text)} characters. Sending to AI...")
    result = parse_resume_to_json(resume_text)

    output_path = os.path.join(services_dir, "test.txt")
    with open(output_path, "w") as f:
        f.write(json.dumps(result, indent=4))

    print(f"✅ Output saved to {output_path}")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
