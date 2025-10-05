import os
from fastapi import FastAPI, APIRouter, Depends
from helpers import Settings, get_settings

base_router = APIRouter(prefix="/v1")


@base_router.get("/")
async def welcome():
    return {"Hello Ahmed"}
