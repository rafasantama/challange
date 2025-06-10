import os
import requests
from typing import Optional, List
from .models import AstralObject, Position, PolyanetObject, SoloonObject, ComethObject

class MegaverseAPI:
    BASE_URL = "https://challenge.crossmint.io/api"

    def __init__(self, candidate_id: Optional[str] = None):
        self.candidate_id = candidate_id or os.getenv("CANDIDATE_ID")
        if not self.candidate_id:
            raise ValueError("Candidate ID must be provided either through constructor or CANDIDATE_ID environment variable")

    def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> requests.Response:
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.request(method, url, json=data)
        response.raise_for_status()
        return response

    def create_polyanet(self, position: Position) -> None:
        """Create a POLYanet at the specified position."""
        data = {
            "row": position.row,
            "column": position.column,
            "candidateId": self.candidate_id
        }
        self._make_request("POST", "polyanets", data)

    def delete_polyanet(self, position: Position) -> None:
        """Delete a POLYanet at the specified position."""
        data = {
            "row": position.row,
            "column": position.column,
            "candidateId": self.candidate_id
        }
        self._make_request("DELETE", "polyanets", data)

    def create_soloon(self, position: Position, color: str) -> None:
        """Create a SOLoon at the specified position with the given color."""
        data = {
            "row": position.row,
            "column": position.column,
            "color": color,
            "candidateId": self.candidate_id
        }
        self._make_request("POST", "soloons", data)

    def delete_soloon(self, position: Position) -> None:
        """Delete a SOLoon at the specified position."""
        data = {
            "row": position.row,
            "column": position.column,
            "candidateId": self.candidate_id
        }
        self._make_request("DELETE", "soloons", data)

    def create_cometh(self, position: Position, direction: str) -> None:
        """Create a ComETH at the specified position with the given direction."""
        data = {
            "row": position.row,
            "column": position.column,
            "direction": direction,
            "candidateId": self.candidate_id
        }
        self._make_request("POST", "comeths", data)

    def delete_cometh(self, position: Position) -> None:
        """Delete a ComETH at the specified position."""
        data = {
            "row": position.row,
            "column": position.column,
            "candidateId": self.candidate_id
        }
        self._make_request("DELETE", "comeths", data)

    def cleanup_polyanets(self, positions: List[Position]) -> None:
        """Delete multiple POLYanets at the specified positions."""
        for position in positions:
            try:
                self.delete_polyanet(position)
                print(f"Deleted POLYanet at position ({position.row}, {position.column})")
            except Exception as e:
                print(f"Error deleting POLYanet at position ({position.row}, {position.column}): {str(e)}")

    def get_goal_map(self) -> dict:
        """Get the goal map for the current challenge phase."""
        response = self._make_request("GET", f"map/{self.candidate_id}/goal")
        return response.json()

    def create_astral_object(self, obj: AstralObject) -> None:
        """Create any type of astral object."""
        if isinstance(obj, PolyanetObject):
            self.create_polyanet(obj.position)
        elif isinstance(obj, SoloonObject):
            self.create_soloon(obj.position, obj.color)
        elif isinstance(obj, ComethObject):
            self.create_cometh(obj.position, obj.direction)
        else:
            raise NotImplementedError(f"Creation of {type(obj).__name__} not implemented yet") 