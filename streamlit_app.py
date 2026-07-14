from pathlib import Path

import streamlit as st

from config import COVER_LETTER_DOCX, TAILOR_DOCX
from services import ApplicationPipeline
from ui import (
    show_form,
    show_layout,
    show_results,
    show_sidebar,
)

st.set_page_config(
    page_title="Job Search AI Agent",
    layout="wide",
)

pipeline = ApplicationPipeline()

show_sidebar()
show_layout()

resume_file, job_description, generate = show_form()

if generate:

    if resume_file is None:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    temp_resume = Path("data/input/uploaded_resume.pdf")
    temp_resume.parent.mkdir(parents=True, exist_ok=True)
    temp_resume.write_bytes(resume_file.getbuffer())

    progress = st.progress(0)
    status = st.empty()

    def update_progress(message: str, percent: int) -> None:
        status.write(message)
        progress.progress(percent)

    resume = pipeline.load_resume(
        str(temp_resume),
        progress_callback=update_progress,
    )

    result = pipeline.run(
        resume,
        job_description,
        progress_callback=update_progress,
    )

    st.session_state["result"] = result
    st.session_state["resume_doc"] = Path(TAILOR_DOCX).read_bytes()
    st.session_state["cover_letter_doc"] = Path(COVER_LETTER_DOCX).read_bytes()

    progress.empty()
    status.empty()

if "result" in st.session_state:
    show_results(st.session_state["result"])