from services import ResumeParser

def test_resume_parser():
    parser = ResumeParser()

    text = parser.extract_text(
        "tests/data/resume.pdf"
    )

    assert "Python" in text