from dataclasses import dataclass


@dataclass
class ConsumerConfig:
    topics: list[str] = "localhost:29092"
    consumer_group_id: str = "default"
    bootstrap_servers: list[str] = "localhost:29092"
