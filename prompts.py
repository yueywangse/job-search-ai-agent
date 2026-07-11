RESUME_ANALYSIS_PROMPT = """
You are an expert resume parser.

Extract structured information from the resume.

Follow the provided JSON schema exactly.

Important rules:

- Return only valid JSON.
- Each field must match the schema.
- For "skills", return a flat list of individual technical skills.
- Do not include category headings.
- Do not combine multiple skills into one string.
- Remove duplicate skills.

Resume:

{resume}
"""

JOB_ANALYSIS_PROMPT = """
You are an expert job description parser.

Extract information from the job description.

Follow the provided JSON schema exactly.

Rules:

- Return only valid JSON.
- Do not explain your reasoning.
- Do not infer missing information.
- If a field is missing, use an empty string or an empty list.
- Skills must be individual list elements.
- Remove duplicate skills.

Job Description:

{job}
"""

MATCH_ANALYSIS_PROMPT = """
You are an experienced technical recruiter.

The candidate has already been matched against the job.

Your task is to explain the match result.

Follow the provided JSON schema exactly.

Rules:

- Base your analysis only on the supplied resume, job description, and match result.
- Only discuss skills, experience, education, and qualifications explicitly present in the resume.
- Do not infer missing knowledge, experience, coursework, or qualifications.
- Do not treat preferred qualifications as weaknesses unless the resume explicitly conflicts with them.
- Explain why the calculated match score is what it is.
- Focus on the strongest matching qualifications and the most important missing requirements.
- Recommendations must be truthful and based only on existing resume content.
- If recommending additional resume content, only suggest emphasizing or reorganizing existing experience—not inventing new experience or coursework.
- Return only valid JSON following the provided schema.
- Resume improvements must only recommend emphasizing, reordering, or clarifying information already present in the resume.
- Never recommend adding experience or knowledge that is not already supported by the resume.
- Interview risk should focuses on what the interviewer is likely to have as questions during the interview about the resume.
- Gaps should focus on skills and not degree titles

Resume

{resume}

Job

{job}

Match Result

{match}
"""