# config.py

OLLAMA_MODEL = "qwen3:14b"

INPUT_DIR = "data/resumes"
OUTPUT_DIR = "data/output"

RESUME_FILE = f"{INPUT_DIR}/resume.pdf"
JOB_FILE = f"{INPUT_DIR}/job.txt"
RESUME_JSON = f"{OUTPUT_DIR}/resume.json"
MATCH_JSON = f"{OUTPUT_DIR}/match.json"
ANALYZE_JSON = f"{OUTPUT_DIR}/analyze.json"
ANALYSIS_MD = f"{OUTPUT_DIR}/analysis.md"
TAILOR_JSON = f"{OUTPUT_DIR}/tailor.json"
TAILOR_DOCX = f"{OUTPUT_DIR}/tailored_resume.docx"
COVER_LETTER_JSON = f"{OUTPUT_DIR}/cover_letter.json"
COVER_LETTER_DOCX = f"{OUTPUT_DIR}/cover_letter.docx"

USE_CACHED_RESUME = True  # Set to false to override old resume.json
