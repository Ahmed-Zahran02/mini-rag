from typing import Optional
from fastapi import FastAPI
from fastapi.routing import APIRouter
from routes import base
from routes import data


app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)
