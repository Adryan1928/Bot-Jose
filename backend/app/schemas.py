from pydantic import BaseModel
from typing import Optional

class MessageSchema(BaseModel):
    message: str
    number: str

    class Config:
        from_attributes = True

class ChoiceSchema(BaseModel):
    text: str
    is_right: bool

class QuestionSchema(BaseModel):
    question: str
    choices: list[ChoiceSchema]

    class Config:
        from_attributes = True