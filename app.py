from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.session import init_db
from api.routes import router

async def lifespan_handler(app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan_handler)
app.include_router(router)
