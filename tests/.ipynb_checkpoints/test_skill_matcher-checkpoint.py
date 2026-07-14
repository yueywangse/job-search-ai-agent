from models import Job, Resume
from services import SkillMatcher

def make_resume() -> Resume:
    return Resume(
        name="Test",
        email="test@test.com",
        phone="123",
        linkedin="",
        github="",
        professional_summary="",
        years_experience=5,
        education=[],
        skills=["Python", "SQL", "Git"],
        work_experience=[],
        projects=[],
    )


def make_job() -> Job:
    return Job(
        title="ML Engineer",
        company="Test",
        location="Remote",
        required_skills=["Python", "Git", "AWS"],
        preferred_skills=[],
        responsibilities=[],
        qualifications=[],
    )

def test_skill_match():
    result = SkillMatcher().match(
        make_resume(),
        make_job(),
    )

    assert result.match_percentage == 66.7