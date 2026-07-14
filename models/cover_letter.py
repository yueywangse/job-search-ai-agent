from pydantic import BaseModel


class CoverLetter(BaseModel):
    greeting: str
    opening: str
    body: list[str]
    closing: str
    signature: str
