import streamlit as st

from .session import clear_session

def show_layout() -> None:
    """Render the application header."""

    st.title("🤖 Job Search AI Agent")

    st.caption(
        "Generate ATS-optimized resumes and personalized cover letters using a local LLM."
    )

    left, right = st.columns([1, 6])

    with left:

        if st.button(
            "🗑️ Clear",
            use_container_width=True,
        ):
            clear_session()

    st.divider()