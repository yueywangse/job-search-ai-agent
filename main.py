from resume_extractor import ResumeExtractor
from resume_parser import ResumeParser
from utils import save_json
from config import RESUME_FILE, RESUME_JSON


def main():
    parser = ResumeParser()
    extractor = ResumeExtractor()
    resume_text = parser.extract_text(RESUME_FILE)
    resume = extractor.extract(resume_text)
    save_json(
        resume.model_dump(),
        RESUME_JSON
    )

    print("Resume analyzed successfully!")
    print("Saved to outputs/resume.json")

if __name__ == "__main__":
    main()