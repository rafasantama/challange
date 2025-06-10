from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class Position:
    row: int
    column: int

@dataclass
class Polyanet:
    position: Position

@dataclass
class Soloon:
    position: Position
    color: str

@dataclass
class Cometh:
    position: Position
    direction: str

class AstralObject:
    def __init__(self, position: Position):
        self.position = position

    def to_api_payload(self, candidate_id: str) -> dict:
        return {
            "row": self.position.row,
            "column": self.position.column,
            "candidateId": candidate_id
        }

class PolyanetObject(AstralObject):
    def to_api_payload(self, candidate_id: str) -> dict:
        return super().to_api_payload(candidate_id)

class SoloonObject(AstralObject):
    def __init__(self, position: Position, color: Literal["blue", "red", "purple", "white"]):
        super().__init__(position)
        self.color = color

    def to_api_payload(self, candidate_id: str) -> dict:
        payload = super().to_api_payload(candidate_id)
        payload["color"] = self.color
        return payload

class ComethObject(AstralObject):
    def __init__(self, position: Position, direction: Literal["up", "down", "left", "right"]):
        super().__init__(position)
        self.direction = direction

    def to_api_payload(self, candidate_id: str) -> dict:
        payload = super().to_api_payload(candidate_id)
        payload["direction"] = self.direction
        return payload 