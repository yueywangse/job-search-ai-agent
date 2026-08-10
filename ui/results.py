import streamlit as st

from pathlib import Path
from ui.downloads import show_downloads
from utils.resume_diff import get_resume_changes
from config import COVER_LETTER_DOCX, TAILOR_DOCX

def show_results(result, pipeline) -> None:
    """Render the pipeline results."""

    st.success("Application documents generated successfully.")

    st.divider()

    st.header("Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall Match",
            f"{result.match.match_percentage:.1f}%"
        )

    with col2:
        st.metric(
            "Matching Skills",
            len(result.match.matching_skills)
        )

    with col3:
        st.metric(
            "Missing Skills",
            len(result.match.missing_skills)
        )

    st.divider()

    left, right = st.columns(2)

    with left:
        with st.expander(
            "Matching Skills",
            expanded=True
        ):
            for skill in result.match.matching_skills:
                st.markdown(f"- ✅ {skill}")

    with right:
        with st.expander(
            "Missing Skills",
            expanded=True
        ):
            for skill in result.match.missing_skills:
                st.markdown(f"- ⚠️ {skill}")

    st.divider()

    analysis_tab, resume_tab, cover_tab, interview_tab  = st.tabs(
        [
            "Analysis",
            "Resume",
            "Cover Letter",
            "Interview Prep"
        ]
    )

    with analysis_tab:
        st.subheader("Summary")

        st.write(result.analysis.summary)

    with resume_tab:
        resume = result.tailored_resume
        
        changes = get_resume_changes(
            result.resume,
            result.tailored_resume
        )
        
        changed_experience = [
            item
            for item in changes["experience"]
            if item["changed"]
        ]
        
        changed_projects = [
            item
            for item in changes["projects"]
            if item["changed"]
        ]

        total_changes = (
            int(changes["skills_changed"])
            + len(changed_experience)
            + len(changed_projects)
        )

        st.subheader("Changes from Original Resume")
        
        if (
            st.session_state.agent_state.tailored_resume is not None
            and st.session_state.agent_state.previous_tailored_resume is not None
        ):
            if st.button("↩ Undo Last Resume Edit"):
                result = pipeline.undo_resume(
                    st.session_state.agent_state
                )

                st.session_state.result = result

                tailored_resume = Path(TAILOR_DOCX)
                if tailored_resume.exists():
                    st.session_state.resume_doc = tailored_resume.read_bytes()

                cover_letter = Path(COVER_LETTER_DOCX)
                if cover_letter.exists():
                    st.session_state.cover_letter_doc = cover_letter.read_bytes()

                st.rerun()

        if total_changes:
            st.caption(f"{total_changes} change(s) from the original resume")

            if changes["skills_changed"]:
                st.markdown(
                    "🟢 **Skills** — reordered"
                )

            if changed_experience:
                st.markdown(
                    f"🟢 **Experience** — "
                    f"{len(changed_experience)} position(s) updated"
                )

            if changed_projects:
                st.markdown(
                    f"🟢 **Projects** — "
                    f"{len(changed_projects)} project(s) updated"
                )

        else:
            st.write("No changes were made to the resume.")

        for item in changed_experience:
            with st.expander(
                f"{item['title']} — {item['company']}"
            ):
                st.markdown("🔵 **Original**")

                for bullet in item["original_bullets"]:
                    st.markdown(f"- {bullet}")

                st.markdown("🟢 **Tailored**")

                for bullet in item["tailored_bullets"]:
                    st.markdown(f"- {bullet}")

        for item in changed_projects:
            with st.expander(item["title"]):
                st.markdown("**Original**")

                for bullet in item["original_bullets"]:
                    st.markdown(f"- {bullet}")

                st.markdown("**Tailored**")

                for bullet in item["tailored_bullets"]:
                    st.markdown(f"- {bullet}")

        st.divider()

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
        
        if (
            st.session_state.agent_state.cover_letter is not None
            and st.session_state.agent_state.previous_cover_letter is not None
        ):
            if st.button("↩ Undo Last Cover Letter Edit"):
                result = pipeline.undo_cover_letter(
                    st.session_state.agent_state
                )

                st.session_state.result = result

                tailored_resume = Path(TAILOR_DOCX)
                if tailored_resume.exists():
                    st.session_state.resume_doc = tailored_resume.read_bytes()

                cover_letter = Path(COVER_LETTER_DOCX)
                if cover_letter.exists():
                    st.session_state.cover_letter_doc = cover_letter.read_bytes()

                st.rerun()

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
        
    with interview_tab:
        st.subheader("Interview Preparation")

        if result.interview_questions is None:
            st.info(
                "No interview questions have been generated yet. "
                "Ask the agent to generate interview questions."
            )
        else:
            questions = result.interview_questions
            
            total_questions = (
                len(questions.technical)
                + len(questions.behavioral)
                + len(questions.role_specific)
            )

            st.caption(f"{total_questions} questions generated")

            st.markdown("### Technical Questions")

            if questions.technical:
                for i, question in enumerate(
                    questions.technical,
                    start=1,
                ):
                    with st.expander(
                        f"{i}. {question}"
                    ):
                        st.write(question)
            else:
                st.write("No technical questions generated.")

            st.divider()

            st.markdown("### Behavioral Questions")

            if questions.behavioral:
                for i, question in enumerate(
                    questions.behavioral,
                    start=1,
                ):
                    with st.expander(
                        f"{i}. {question}"
                    ):
                        st.write(question)
            else:
                st.write("No behavioral questions generated.")

            st.divider()

            st.markdown("### Role-Specific Questions")

            if questions.role_specific:
                for i, question in enumerate(
                    questions.role_specific,
                    start=1,
                ):
                    with st.expander(
                        f"{i}. {question}"
                    ):
                        st.write(question)
            else:
                st.write("No role-specific questions generated.")

    st.divider()

    show_downloads(
        st.session_state["resume_doc"],
        st.session_state["cover_letter_doc"],
    )