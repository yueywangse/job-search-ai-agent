import streamlit as st

def show_form():
    """Render the upload form."""

    with st.form("generator"):

        left, right = st.columns([1, 2])

        with left:

            resume = st.file_uploader(
                "Resume",
                type=["pdf"],
            )

        with right:

            job = st.text_area(
                "Job Description",
                height=350,
            )

        submitted = st.form_submit_button(
            "Generate",
            type="primary",
        )

    return resume, job, submitted