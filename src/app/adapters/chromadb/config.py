from dataclasses import dataclass


@dataclass
class ChromaConfig:
    host: str = "localhost",
    port: int = 8000