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