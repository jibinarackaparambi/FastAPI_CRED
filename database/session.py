from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel,Session
from fastapi import Depends

from .models import Shipment
from config import db_settings

engine = create_async_engine(
    url= db_settings.POSTGRES_URL,
    echo=True,
    # connect_args={"check_same_thread":False}
    )

async def init_db():
    # SQLModel.metadata.create_all(bind=engine)
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_db():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

session_db = Annotated[AsyncSession, Depends(get_db)]