from dataclasses import dataclass


@dataclass
class MessageDTO:
    data: str

@dataclass
class MessageResultDTO:
    data: str