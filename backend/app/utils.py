import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

def load_env():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(BASE_DIR, "../.env")

        load_dotenv(dotenv_path=dotenv_path)
    except:
        load_dotenv()

def create_instance(session: Session, obj):
    """
    Create a new instance of a SQLAlchemy model and add it to the session.
    """
    session.add(obj)
    session.commit()
    session.refresh(obj)

def update_instance(session: Session, obj):
    """
    Update an existing instance of a SQLAlchemy model.
    """
    session.commit()
    session.refresh(obj)