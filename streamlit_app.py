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

@st.cache_resource
def get_pipeline() -> ApplicationPipeline:
    return ApplicationPipeline()

pipeline = get_pipeline()

if "agent_state" not in st.session_state:
    st.session_state.agent_state = None

if "result" not in st.session_state:
    st.session_state.result = None

show_sidebar()
show_layout()

if st.session_state.agent_state is None:
    resume_file, job_description, initialize = show_form()

    if initialize:
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

        def update_progress(message: str, percent: int):
            status.write(message)
            progress.progress(percent)

        resume = pipeline.load_resume(
            str(temp_resume),
            progress_callback=update_progress
        )

        st.session_state.agent_state = pipeline.create_session(resume, job_description)
        st.session_state.result = None
        st.session_state.pop("resume_doc", None)
        st.session_state.pop("cover_letter_doc", None)

        st.session_state.agent_state.add_assistant_message("I've loaded your resume and the job description. I can tailor your resume, generate a cover letter, explain my recommendations, or answer questions about the job. What would you like to do?")

        progress.empty()
        status.empty()

        st.rerun()
            
if st.session_state.agent_state:
    if st.sidebar.button("New Session"):
        st.session_state.agent_state = None
        st.session_state.result = None
        st.session_state.pop("resume_doc", None)
        st.session_state.pop("cover_letter_doc", None)
        st.rerun()
        
    for message in st.session_state.agent_state.messages:
        with st.chat_message(message.role):
            st.markdown(message.content)
            
    prompt = st.chat_input("How can I help?")

    if prompt:

        progress = st.progress(0)
        status = st.empty()

        def update_progress(message: str, percent: int):
            status.write(message)
            progress.progress(percent)

        result = pipeline.chat(
            st.session_state.agent_state,
            prompt,
            progress_callback=update_progress
        )

        st.session_state.result = result

        tailored_resume = Path(TAILOR_DOCX)
        if tailored_resume.exists():
            st.session_state.resume_doc = tailored_resume.read_bytes()

        cover_letter = Path(COVER_LETTER_DOCX)
        if cover_letter.exists():
            st.session_state.cover_letter_doc = cover_letter.read_bytes()

        progress.empty()
        status.empty()

        st.rerun()

if st.session_state.result is not None:
    show_results(st.session_state.result)