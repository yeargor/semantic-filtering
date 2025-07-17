import os
from dataclasses import dataclass


@dataclass
class LLMConfig:
    project: str
    credentials: str
    location: str = "us-central1"

def load_config() -> LLMConfig:
    return LLMConfig(
        project=os.getenv("GCP_PROJECT"),
        location=os.getenv("GCP_LOCATION", "us-central1"),
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    )