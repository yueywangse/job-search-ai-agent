import streamlit as st

def show_downloads(
    resume_doc: bytes,
    cover_letter_doc: bytes,
) -> None:
    """Render document download buttons."""

    st.subheader("Downloads")

    left, right = st.columns(2)

    with left:

        st.download_button(
            "📄 Download Tailored Resume",
            data=resume_doc,
            file_name="tailored_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    with right:

        st.download_button(
            "📝 Download Cover Letter",
            data=cover_letter_doc,
            file_name="cover_letter.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )