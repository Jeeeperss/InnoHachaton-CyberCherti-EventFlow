from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerConfig(BaseModel):
    ps_dsn: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/eventflow"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
    )
    db: WorkerConfig = WorkerConfig()

settings = Settings()