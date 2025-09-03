from typing import Optional
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env
from routes import base  # it needs the .env variables

app = FastAPI()
app.include_router(base.base_router)
