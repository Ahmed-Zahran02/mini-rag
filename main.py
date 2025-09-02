from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome_message(x: Optional[str] = "ahmed"):
    return {"Hello": x}
