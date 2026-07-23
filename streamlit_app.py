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
        completed_steps = []

        def update_progress(message: str, percent: int):
            completed_steps.append(message)

            lines = []

            for step in completed_steps[:-1]:
                lines.append(f"✓ {step}")

            if completed_steps:
                lines.append(f"⏳ {completed_steps[-1]}")

            status.markdown("\n".join(lines))
            progress.progress(percent)

        resume = pipeline.load_resume(
            str(temp_resume),
            progress_callback=update_progress,
        )

        st.session_state.agent_state = pipeline.create_session(
            resume,
            job_description,
        )

        st.session_state.result = None
        st.session_state.pop("resume_doc", None)
        st.session_state.pop("cover_letter_doc", None)
        st.session_state.pop("pending_prompt", None)

        st.session_state.agent_state.add_assistant_message(
            "I've loaded your resume and the job description. "
            "Tell me what you'd like to improve—whether it's tailoring your resume, "
            "generating or revising a cover letter, or making further edits to either document."
        )

        progress.empty()
        status.empty()

        st.rerun()
        
if st.session_state.result is not None:
    show_results(st.session_state.result)

if st.session_state.agent_state:

    if st.sidebar.button("New Session", disabled="pending_prompt" in st.session_state):
        st.session_state.agent_state = None
        st.session_state.result = None
        st.session_state.pop("resume_doc", None)
        st.session_state.pop("cover_letter_doc", None)
        st.session_state.pop("pending_prompt", None)
        st.rerun()
        
    chat_container = st.container(
        height=500,
        border=True
    )

    with chat_container:
        for message in st.session_state.agent_state.messages:
            with st.chat_message(message.role):
                st.markdown(message.content)
                
        if "pending_prompt" in st.session_state:
            with st.chat_message("assistant"):
                st.markdown("_Thinking..._")

    if "pending_prompt" in st.session_state:
        st.chat_input(
            "Generating response...",
            disabled=True,
        )
        
        progress = st.progress(0)
        status = st.empty()
        completed_steps = []

        def update_progress(message: str, percent: int):
            completed_steps.append(message)

            lines = []

            for step in completed_steps[:-1]:
                lines.append(f"✓ {step}")

            if completed_steps:
                lines.append(f"⏳ {completed_steps[-1]}")

            status.markdown("\n".join(lines))
            progress.progress(percent)

        result = pipeline.chat(
            st.session_state.agent_state,
            st.session_state.pending_prompt,
            progress_callback=update_progress
        )

        st.session_state.result = result

        tailored_resume = Path(TAILOR_DOCX)
        if tailored_resume.exists():
            st.session_state.resume_doc = tailored_resume.read_bytes()

        cover_letter = Path(COVER_LETTER_DOCX)
        if cover_letter.exists():
            st.session_state.cover_letter_doc = cover_letter.read_bytes()

        del st.session_state.pending_prompt

        progress.empty()
        status.empty()

        st.rerun()
    else:
        prompt = st.chat_input("How can I help?")

        if prompt:
            st.session_state.agent_state.add_user_message(prompt)
            st.session_state.pending_prompt = prompt
            st.rerun()