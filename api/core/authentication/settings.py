from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

class TokenTransport(BaseModel):
    bearer_token_url: str = "/login"

class Settings(BaseSettings):
    api: TokenTransport = TokenTransport()

settings = Settings()