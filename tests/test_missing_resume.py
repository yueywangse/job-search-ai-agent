import pytest

from services import ResumeParser

def test_missing_resume():
    parser = ResumeParser()

    with pytest.raises(FileNotFoundError):
        parser.extract_text("missing.pdf")