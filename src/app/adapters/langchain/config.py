from dataclasses import dataclass


@dataclass
class LLMConfig:
    project: str
    location: str = "us-central1"