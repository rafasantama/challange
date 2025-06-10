"""
Goal Map Parser for Crossmint Challenge 2

This module provides functionality to parse the goal map from the Crossmint API
and convert it into a list of objects with their positions and properties.

The goal map represents a grid where each cell can contain:
- POLYANET: Basic object
- SOLOON: Colored object (blue, red, purple, white)
- COMETH: Directional object (up, down, left, right)
- SPACE: Empty cell
- None: Invalid or empty cell

Example goal map format:
{
    "goal": [
        ["SPACE", "BLUE_SOLOON", "SPACE"],
        ["RED_SOLOON", "UP_COMETH", "SPACE"],
        ["SPACE", "POLYANET", "SPACE"]
    ]
}
"""

def parse_goal_map(goal_map):
    """
    Parse the goal map into a list of objects with their positions and properties.
    
    Args:
        goal_map (dict): The goal map from the API containing a 2D grid of objects
        
    Returns:
        list: List of dictionaries containing object information:
            - row: Row position (0-based)
            - column: Column position (0-based)
            - type: Object type (POLYANET, SOLOON, COMETH)
            - color: Color for SOLOON (blue, red, purple, white)
            - direction: Direction for COMETH (up, down, left, right)
            
    Example return value:
    [
        {
            "row": 0,
            "column": 1,
            "type": "SOLOON",
            "color": "blue"
        },
        {
            "row": 1,
            "column": 1,
            "type": "COMETH",
            "direction": "up"
        }
    ]
    """
    objects = []
    for row_idx, row in enumerate(goal_map.get("goal", [])):
        for col_idx, cell in enumerate(row):
            # Skip empty or invalid cells
            if cell is None or cell == "SPACE":
                continue
                
            # Create base object with position
            obj = {"row": row_idx, "column": col_idx}
            
            # Handle POLYANET objects
            if cell == "POLYANET":
                obj["type"] = "POLYANET"
                objects.append(obj)
                
            # Handle SOLOON objects (COLOR_SOLOON format)
            elif cell.endswith("_SOLOON"):
                color = cell.split("_")[0].lower()
                # Validate color
                if color in ["blue", "red", "purple", "white"]:
                    obj["type"] = "SOLOON"
                    obj["color"] = color
                    objects.append(obj)
                    
            # Handle COMETH objects (DIRECTION_COMETH format)
            elif cell.endswith("_COMETH"):
                direction = cell.split("_")[0].lower()
                # Validate direction
                if direction in ["up", "down", "left", "right"]:
                    obj["type"] = "COMETH"
                    obj["direction"] = direction
                    objects.append(obj)
                    
    return objects 