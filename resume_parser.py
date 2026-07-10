import re
from pypdf import PdfReader

class ResumeParser:
    def extract_text(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text = re.sub(r"[ \t]+", " ", text)
                text = re.sub(r"\n{3,}", "\n\n", text)
                pages.append(text.strip())

        return "\n\n".join(pages)