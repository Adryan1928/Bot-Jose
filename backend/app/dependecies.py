from sqlalchemy.orm import sessionmaker
from database import db

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session_ = Session()
        yield session_
    finally:
        session_.close()