# Tepmplate CORS 
from pydantic_settings import BaseSettings
from typing import List

class Origins(BaseSettings):
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost",
        "http://127.0.0.1"
    ]

origins = Origins()
