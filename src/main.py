from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import get_settings
import uvicorn

app = FastAPI()


@app.on_event("startup")
async def startup():
    settings = get_settings()
    app.state.connection = AsyncIOMotorClient(settings.DATABASE_URL)
    app.state.db_client = app.state.connection[settings.DATABASE_NAME]


app.include_router(base.base_router)
app.include_router(data.data_router)


@app.on_event("shutdown")
async def shutdown():
    if hasattr(app.state, "client"):
        await app.state.client.close()


# app = FastAPI()
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
