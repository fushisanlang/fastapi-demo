# database.py
from sqlmodel import SQLModel, create_engine, Session
from config import DATABASE_URL

db_engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(db_engine) as session:
        yield session
