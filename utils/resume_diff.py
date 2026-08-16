from models import Resume, TailoredResume

def count_changed_items(
    original: list[str],
    tailored: list[str]
) -> int:
    """Count bullet points that differ between two lists."""

    changed = 0

    for original_item, tailored_item in zip(original, tailored):
        if original_item != tailored_item:
            changed += 1

    changed += abs(len(original) - len(tailored))

    return changed


def get_resume_changes(
    original: Resume,
    tailored: TailoredResume
) -> dict:
    """Compare the original and tailored resumes."""

    changes = {
        "skills_changed": original.skills != tailored.skills,
        "experience": [],
        "projects": []
    }

    # Build lookup tables for LLM-generated explanations
    experience_reasons = {
        reason.item: reason.reason
        for reason in tailored.change_reasons
        if reason.section == "work_experience"
    }

    project_reasons = {
        reason.item: reason.reason
        for reason in tailored.change_reasons
        if reason.section == "project"
    }

    for original_job, tailored_job in zip(
        original.work_experience,
        tailored.work_experience,
    ):
        changed_bullets = (original_job.bullet_points != tailored_job.bullet_points)

        experience_key = (f"{tailored_job.company} - {tailored_job.title}")

        changes["experience"].append({
            "title": tailored_job.title,
            "company": tailored_job.company,
            "changed": changed_bullets,
            "original_bullets": original_job.bullet_points,
            "tailored_bullets": tailored_job.bullet_points,
            "reason": experience_reasons.get(experience_key, "")
    })

    for original_project, tailored_project in zip(
        original.projects,
        tailored.projects
    ):
        changed_bullets = (original_project.bullet_points != tailored_project.bullet_points)

        changes["projects"].append({
            "title": tailored_project.title,
            "changed": changed_bullets,
            "original_bullets": original_project.bullet_points,
            "tailored_bullets": tailored_project.bullet_points,
            "reason": project_reasons.get(tailored_project.title, "")
        })

    return changes