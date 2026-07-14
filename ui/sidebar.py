import streamlit as st

def show_sidebar() -> None:
    """Render the application sidebar."""

    with st.sidebar:

        st.header("Settings")

        st.success("Qwen3:14B")

        st.caption("Version 1.0")

        st.divider()

        st.write(
            "Upload a resume, paste a job description, and generate tailored application documents."
        )