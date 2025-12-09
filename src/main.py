from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import get_settings
import uvicorn
from stores.llm.LLMProviderFactory import LLMProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.connection = AsyncIOMotorClient(settings.DATABASE_URL)
    app.state.db_client = app.state.connection[settings.DATABASE_NAME]
    llm_factory = LLMProviderFactory(config=settings)
    app.state.generation_client = llm_factory.get_provider(settings.GENERATION_BACKEND)
    app.state.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)
    app.state.embedding_client = llm_factory.get_provider(settings.EMBEDDING_BACKEND)
    app.state.embedding_client.set_embedding_model(
        settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_MODEL_SIZE
    )
    yield
    app.state.connection.close()
  

app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
