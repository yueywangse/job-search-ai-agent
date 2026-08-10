INTERVIEW_QUESTIONS_PROMPT = """
Generate interview questions for the candidate based on the job,
resume, and resume-job analysis.

Focus on questions that are actually relevant to the target role
and the candidate's experience.

Generate:
- 4 technical questions
- 3 behavioral questions
- 3 role-specific questions

Do not invent experience or skills that are not present in the resume.

Resume:
{resume}

Job:
{job}

Analysis:
{analysis}

Tailored Resume:
{tailored_resume}
"""