# main.py
from fastapi import FastAPI
from database import db_engine
from sqlmodel import SQLModel
from routes import auth, protected

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(db_engine)

app.include_router(auth.router)
app.include_router(protected.router)