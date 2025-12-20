from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from helpers import get_settings
from routes import base, data, nlp
from stores.llm import LLMProviderFactory
from stores.llm.templates import TemplateParser
from stores.vectordb import VectorDBFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.connection = AsyncIOMotorClient(settings.DATABASE_URL)
    app.state.db_client = app.state.connection[settings.DATABASE_NAME]
    llm_factory = LLMProviderFactory(config=settings)
    vector_db_factory = VectorDBFactory(config=settings)
    ## llm
    app.state.generation_client = llm_factory.get_provider(settings.GENERATION_BACKEND)
    # app.state.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)
    app.state.embedding_client = llm_factory.get_provider(settings.EMBEDDING_BACKEND)
    # app.state.embedding_client.set_embedding_model(
    #     settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_MODEL_SIZE
    # )
    # # vector db
    app.state.vectordb_client = vector_db_factory.create(settings.VECTORDB_TYPE)
    if app.state.vectordb_client is not None:
        app.state.vectordb_client.connect()
    ## template parser
    app.state.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )
    yield
    app.state.connection.close()


app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
