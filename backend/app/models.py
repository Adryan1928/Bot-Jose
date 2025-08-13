from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, unique=True)
    name = Column(String, nullable=True)
    last_received_message = Column(String, nullable=True)
    last_sent_message = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)


    def __init__(self, number, is_active=True):
        self.number = number
        self.is_active = is_active

class Choices(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"))
    is_right = Column(Boolean, default=False)

    def __init__(self, question_id, text, is_right=False):
        self.question_id = question_id
        self.text = text
        self.is_right = is_right


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)

    def __init__(self, question):
        self.question = question
