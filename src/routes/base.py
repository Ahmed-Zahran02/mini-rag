import os
from sys import api_version
from fastapi import FastAPI, APIRouter

base_router = APIRouter(prefix="/v1", tags=["v1"])


@base_router.get("/")
def welcome_message():
    # get the env variables
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return {
        "APPName": app_name,
        "APPVersion": app_version,
    }
