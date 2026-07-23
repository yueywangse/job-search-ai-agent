import streamlit as st

from ui.downloads import show_downloads

def show_results(result) -> None:
    """Render the pipeline results."""

    st.success("Application documents generated successfully.")

    st.divider()

    st.header("Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall Match",
            f"{result.match.match_percentage:.1f}%",
        )

    with col2:
        st.metric(
            "Matching Skills",
            len(result.match.matching_skills),
        )

    with col3:
        st.metric(
            "Missing Skills",
            len(result.match.missing_skills),
        )

    st.divider()

    left, right = st.columns(2)

    with left:
        with st.expander(
            "Matching Skills",
            expanded=True,
        ):
            for skill in result.match.matching_skills:
                st.markdown(f"- ✅ {skill}")

    with right:
        with st.expander(
            "Missing Skills",
            expanded=True,
        ):
            for skill in result.match.missing_skills:
                st.markdown(f"- ⚠️ {skill}")

    st.divider()

    analysis_tab, resume_tab, cover_tab = st.tabs(
        [
            "Analysis",
            "Resume",
            "Cover Letter",
        ]
    )

    with analysis_tab:

        st.subheader("Summary")

        st.write(result.analysis.summary)

    with resume_tab:
        resume = result.tailored_resume

        st.subheader("Professional Summary")
        st.write(resume.professional_summary)

        st.divider()

        st.subheader("Skills")
        st.write(" • ".join(resume.skills))

        st.divider()

        st.subheader("Experience")

        for job in resume.work_experience:

            st.markdown(f"### {job.title}")
            st.write(f"*{job.company} | {job.location}*")
            st.caption(job.dates)

            for bullet in job.bullet_points:
                st.markdown(f"- {bullet}")

        st.divider()

        st.subheader("Projects")

        for project in resume.projects:

            st.markdown(f"### {project.title}")

            for bullet in project.bullet_points:
                st.markdown(f"- {bullet}")

        st.divider()

        st.subheader("Education")

        for education in result.resume.education:

            st.markdown(f"**{education.degree}**")
            st.write(f"{education.university} | {education.date}")

    with cover_tab:

        st.subheader("Cover Letter")

        cover_letter = "\n\n".join(
            [
                result.cover_letter.greeting,
                result.cover_letter.opening,
                *result.cover_letter.body,
                result.cover_letter.closing,
                result.cover_letter.signature,
            ]
        )

        st.text(cover_letter)

    st.divider()

    show_downloads(
        st.session_state["resume_doc"],
        st.session_state["cover_letter_doc"],
    )