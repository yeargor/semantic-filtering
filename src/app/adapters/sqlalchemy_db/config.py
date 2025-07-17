import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = "5432"
    database: str = "recipe"
    user: str = "postgres"
    password: str = "pleasecomein"

    @property
    def full_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

def load_config() -> DBConfig:
    return DBConfig(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        database=os.getenv("POSTGRES_DB", "recipe"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "123"),
    )
