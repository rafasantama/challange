"""
Crossmint Challenge 2: Logo Pattern Creator

This script implements the solution for Challenge 2, which involves:
1. Fetching the goal map from the Crossmint API
2. Parsing the goal map to extract object positions and properties
3. Creating objects in the Megaverse according to the goal map
4. Handling errors and rate limiting
5. Providing progress feedback

The script supports three types of objects:
- POLYANET: Basic object
- SOLOON: Colored object with properties (blue, red, purple, white)
- COMETH: Directional object with properties (up, down, left, right)
"""

import os
import time
import json
from dotenv import load_dotenv
from megaverse.api import MegaverseAPI
from challenge2_goal_parser import parse_goal_map
from megaverse.models import Position, PolyanetObject, SoloonObject, ComethObject

def log_created_object(obj):
    """
    Log a successfully created object to the log file.
    Each object is logged as a JSON line for easy parsing during cleanup.
    
    Args:
        obj (dict): Object information including type, position, and any additional properties
    """
    with open('challenge2_created.log', 'a') as f:
        f.write(json.dumps(obj) + '\n')

def create_objects_from_goal(api: MegaverseAPI, dry_run: bool = False) -> None:
    """
    Create objects in the Megaverse based on the parsed goal map.
    
    Args:
        api: CrossmintAPI instance for making API calls
        objects: List of objects to create, each containing:
            - row: Row position
            - column: Column position
            - type: Object type (POLYANET, SOLOON, COMETH)
            - color: Color for SOLOON (optional)
            - direction: Direction for COMETH (optional)
        dry_run: If True, only print what would be created without making API calls
    
    The function handles rate limiting by adding delays between API calls
    and provides progress feedback through logging.
    """
    print("Fetching goal map...")
    goal_map = api.get_goal_map()
    
    print("Parsing goal map...")
    objects = parse_goal_map(goal_map)
    
    print(f"Found {len(objects)} objects to create")
    
    for i, obj in enumerate(objects, 1):
        position = Position(obj["row"], obj["column"])
        
        if dry_run:
            # Print detailed information about what would be created
            if obj["type"] == "POLYANET":
                print(f"Would create POLYANET at position ({position.row}, {position.column})")
            elif obj["type"] == "SOLOON":
                print(f"Would create {obj['color'].upper()} SOLOON at position ({position.row}, {position.column})")
            elif obj["type"] == "COMETH":
                print(f"Would create {obj['direction'].upper()} COMETH at position ({position.row}, {position.column})")
            continue
            
        try:
            # Create the appropriate type of object with its properties
            if obj["type"] == "POLYANET":
                api.create_polyanet(position)
                print(f"Created POLYANET {i}/{len(objects)} at position ({position.row}, {position.column})")
            elif obj["type"] == "SOLOON":
                api.create_soloon(position, obj["color"])
                print(f"Created {obj['color'].upper()} SOLOON {i}/{len(objects)} at position ({position.row}, {position.column})")
            elif obj["type"] == "COMETH":
                api.create_cometh(position, obj["direction"])
                print(f"Created {obj['direction'].upper()} COMETH {i}/{len(objects)} at position ({position.row}, {position.column})")
                
            # Log successful creation for potential cleanup
            log_created_object(obj)
            time.sleep(0.5)  # Rate limiting to avoid overwhelming the API
        except Exception as e:
            print(f"Error creating {obj['type']} at position ({position.row}, {position.column}): {str(e)}")

def main():
    """
    Main function to execute the Challenge 2 solution.
    
    The function:
    1. Initializes the API client
    2. Fetches the goal map
    3. Parses the goal map into objects
    4. Creates the objects in the Megaverse
    5. Handles any errors that occur during the process
    """
    load_dotenv()
    api = MegaverseAPI()
    create_objects_from_goal(api)

if __name__ == "__main__":
    main() 