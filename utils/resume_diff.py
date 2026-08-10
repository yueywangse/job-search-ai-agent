from models import Resume, TailoredResume

def get_resume_changes(
    original: Resume,
    tailored: TailoredResume,
) -> dict:
    """Compare the original and tailored resumes."""

    changes = {
        "skills_changed": original.skills != tailored.skills,
        "experience": [],
        "projects": []
    }

    for original_job, tailored_job in zip(
        original.work_experience,
        tailored.work_experience
    ):
        changed_bullets = (original_job.bullet_points != tailored_job.bullet_points)

        changes["experience"].append({
            "title": tailored_job.title,
            "company": tailored_job.company,
            "changed": changed_bullets,
            "original_bullets": original_job.bullet_points,
            "tailored_bullets": tailored_job.bullet_points
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
            "tailored_bullets": tailored_project.bullet_points
        })

    return changes