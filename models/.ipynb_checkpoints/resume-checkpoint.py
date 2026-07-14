from pydantic import BaseModel

class Education(BaseModel):
    """An education entry on a resume."""
    
    degree: str
    university: str
    date: str

class Experience(BaseModel):
    """A work experience entry on a resume."""
    
    company: str
    location: str
    title: str
    dates: str
    bullet_points: list[str]

class Project(BaseModel):
    """A project included on a resume."""
    
    title: str
    bullet_points: list[str]

class Resume(BaseModel):
    """Structured representation of a candidate's resume."""
    
    name: str
    email: str
    phone: str
    linkedin: str
    github: str
    education: list[Education]
    skills: list[str]
    work_experience: list[Experience]
    projects: list[Project]
    years_experience: int