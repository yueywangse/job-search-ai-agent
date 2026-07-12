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

RESUME_TAILOR_PROMPT = """
You are an expert technical resume writer.

Tailor the supplied resume for the target job description.

Follow the provided JSON schema exactly.

Rules

Truthfulness
------------
- Return only valid JSON.
- Never invent or exaggerate experience, projects, skills, responsibilities, or accomplishments.
- Preserve all companies, job titles, employment dates, education, and factual information.
- Preserve the original meaning of every accomplishment.
- Never add responsibilities, technologies, metrics, or accomplishments that are not already supported by the resume.

Tailoring
---------
- Rewrite bullet points only by rephrasing, reordering, or emphasizing existing information.
- Do not introduce terminology that implies experience the resume does not explicitly support.
- Rewrite the professional summary only if doing so improves relevance to the target job. Otherwise preserve the original summary.
- Reorder skills so the most relevant skills appear first.
- Use the supplied match analysis to determine which existing experience and accomplishments should be emphasized.
- Do not attempt to address resume gaps by inventing or implying experience that is not present.
- Only rewrite sections when doing so improves relevance.
- Leave already effective content unchanged.
- Preserve the number of work experiences and projects. Do not remove or combine entries.
- When in doubt, preserve the original wording rather than making unnecessary changes.
- Preserve the original order of work experiences and projects unless reordering is explicitly requested.

Resume Quality
--------------
- Improve ATS compatibility through clear wording and appropriate emphasis, not keyword stuffing.
- Preserve readability and maintain a natural, professional resume.
- Preserve quantified accomplishments and metrics.
- Do not remove important accomplishments simply because they are not directly related to the job.

Skills
------
- The returned skills list must contain exactly the same skills as the original resume.
- Do not add, remove, rename, merge, or split skills.

Resume

{resume}

Job Description

{job}

Match Analysis

{analysis}
"""