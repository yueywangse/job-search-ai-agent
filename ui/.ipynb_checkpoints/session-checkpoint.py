import streamlit as st

def clear_session() -> None:
    """Clear the current Streamlit session."""

    st.session_state.clear()

    st.rerun()