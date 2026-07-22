import streamlit as st


def show_form():
    """Render the application setup form."""

    with st.form("setup"):

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

        initialize = st.form_submit_button(
            "Start Session",
            type="primary",
        )

    return resume, job, initialize