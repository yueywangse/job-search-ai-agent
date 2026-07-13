from pydantic import BaseModel

class Education(BaseModel):
    degree: str
    university: str
    date: str

class Experience(BaseModel):
    company: str
    location: str
    title: str
    dates: str
    bullet_points: list[str]

class Project(BaseModel):
    title: str
    bullet_points: list[str]

class Resume(BaseModel):
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