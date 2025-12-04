from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import get_settings
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.connection = AsyncIOMotorClient(settings.DATABASE_URL)
    app.state.db_client = app.state.connection[settings.DATABASE_NAME]
    yield
    app.state.connection.close()
  

app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
