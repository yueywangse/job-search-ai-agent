import streamlit as st

def show_form(
    existing_resume: bytes | None = None,
    existing_resume_name: str | None = None
):
    """Render the application setup form."""

    with st.form("setup"):
        left, right = st.columns([1, 2])

        with left:
            if existing_resume is not None:
                st.success(f"Using existing resume:\n{existing_resume_name}")

                new_resume = st.file_uploader(
                    "Upload a different resume (optional)",
                    type=["pdf"]
                )

                if new_resume is not None:
                    resume_bytes = new_resume.getvalue()
                    resume_name = new_resume.name
                else:
                    resume_bytes = existing_resume
                    resume_name = existing_resume_name

            else:
                resume_file = st.file_uploader(
                    "Resume",
                    type=["pdf"]
                )

                if resume_file is not None:
                    resume_bytes = resume_file.getvalue()
                    resume_name = resume_file.name
                else:
                    resume_bytes = None
                    resume_name = None

        with right:
            job = st.text_area("Job Description", height=350)

        initialize = st.form_submit_button("Start Session", type="primary")

    return resume_bytes, resume_name, job, initialize