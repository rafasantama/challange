from typing import List, Dict, Tuple
from .models import Position, PolyanetObject, SoloonObject, ComethObject, AstralObject

class PatternGenerator:
    @staticmethod
    def generate_cross(size: int = 11) -> List[AstralObject]:
        """
        Generate a cross pattern of POLYanets.
        The cross will be centered in a size x size grid.
        The pattern will be an X shape with POLYanets at specific distances from the center.
        """
        if size % 2 == 0:
            raise ValueError("Size must be odd to create a centered cross")

        center = size // 2
        objects = []

        # Define the distances from center for each arm of the X
        distances = [2, 3, 4]  # This creates the correct X pattern

        # Create POLYanets for each distance
        for dist in distances:
            # Top-left to bottom-right diagonal
            objects.append(PolyanetObject(Position(center - dist, center - dist)))  # Top-left
            objects.append(PolyanetObject(Position(center + dist, center + dist)))  # Bottom-right

            # Top-right to bottom-left diagonal
            objects.append(PolyanetObject(Position(center - dist, center + dist)))  # Top-right
            objects.append(PolyanetObject(Position(center + dist, center - dist)))  # Bottom-left

        # Add the center point
        objects.append(PolyanetObject(Position(center, center)))

        return objects

    @staticmethod
    def generate_logo() -> List[AstralObject]:
        """
        Generate the Crossmint logo pattern.
        This pattern includes POLYanets, SOLoons, and ComETHs.
        """
        objects = []

        # First, let's get the goal map to understand the pattern
        api = MegaverseAPI()
        goal_map = api.get_goal_map()

        # Parse the goal map and create objects accordingly
        for row_idx, row in enumerate(goal_map.get("goal", [])):
            for col_idx, cell in enumerate(row):
                if cell is None:
                    continue

                position = Position(row_idx, col_idx)
                
                if cell == "POLYANET":
                    objects.append(PolyanetObject(position))
                elif cell.startswith("SOLOON"):
                    color = cell.split("_")[1].lower()
                    objects.append(SoloonObject(position, color))
                elif cell.startswith("COMETH"):
                    direction = cell.split("_")[1].lower()
                    objects.append(ComethObject(position, direction))

        return objects 