from resume_extractor import ResumeExtractor
from resume_parser import ResumeParser
from utils import save_json


def main():
    parser = ResumeParser()
    extractor = ResumeExtractor()
    resume_text = parser.extract_text("resume.pdf")
    resume = extractor.extract(resume_text)
    save_json(
        resume.model_dump(),
        "resume.json"
    )

    print("Resume analyzed successfully!")
    print("Saved to outputs/resume.json")

if __name__ == "__main__":
    main()