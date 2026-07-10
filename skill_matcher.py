from match import MatchResult
from resume import Resume
from job import Job

class SkillMatcher:

    def match(
        self,
        resume: Resume,
        job: Job
    ) -> MatchResult:
        resume_skills = {
            skill.lower()
            for skill in resume.skills
        }
        job_skills = {
            skill.lower()
            for skill in job.required_skills
        }
        matching = sorted(
            resume_skills & job_skills
        )
        missing = sorted(
            job_skills - resume_skills
        )
        extra = sorted(
            resume_skills - job_skills
        )
        
        if len(job_skills) == 0:
            score = 100.0
        else:
            score = (
                len(matching)
                / len(job_skills)
            ) * 100

        return MatchResult(
            match_percentage=round(score, 1),
            matching_skills=matching,
            missing_skills=missing,
            extra_skills=extra
        )