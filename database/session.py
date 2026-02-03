from typing import Annotated
from sqlalchemy import create_engine
from sqlmodel import SQLModel,Session
from fastapi import Depends
from .models import Shipment

engine = create_engine(
    url="sqlite:///shipment.db",
    echo=True,
    connect_args={"check_same_thread":False}
    )

def init_db():
    SQLModel.metadata.create_all(bind=engine)

def get_db():
    with Session(engine) as session:
        yield session

session_db = Annotated[Session, Depends(get_db)]