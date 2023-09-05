from pydantic import BaseModel


class Note(BaseModel):
    folder: str
    resource: str
    tag: str
    value: str
