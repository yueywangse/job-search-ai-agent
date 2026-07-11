# config.py

OLLAMA_MODEL = "qwen3:14b"

INPUT_DIR = "data/resumes"
OUTPUT_DIR = "data/output"

RESUME_FILE = f"{INPUT_DIR}/resume.pdf"
RESUME_JSON = f"{OUTPUT_DIR}/resume.json"
MATCH_JSON = f"{OUTPUT_DIR}/match.json"
ANALYZE_JSON = f"{OUTPUT_DIR}/analyze.json"

USE_CACHED_RESUME = True # Set to false to override old resume.json