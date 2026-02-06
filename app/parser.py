import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def segment_sections(text: str) -> dict:
    sections = {
        "skills": "",
        "experience": "",
        "education": ""
    }

    current_section = None

    for line in text.split("\n"):
        line_lower = line.lower()
        if "skill" in line_lower:
            current_section = "skills"
        elif "experience" in line_lower:
            current_section = "experience"
        elif "education" in line_lower:
            current_section = "education"
        elif current_section:
            sections[current_section] += line + " "

    return sections
