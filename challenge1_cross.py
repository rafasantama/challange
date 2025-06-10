import os
import time
from dotenv import load_dotenv
from megaverse.api import MegaverseAPI
from megaverse.patterns import PatternGenerator
from megaverse.models import Position

def create_cross_pattern(api: MegaverseAPI) -> None:
    """Create the cross pattern for Challenge 1."""
    print("Creating cross pattern...")
    objects = PatternGenerator.generate_cross()
    
    print(f"Creating {len(objects)} POLYanets...")
    for i, obj in enumerate(objects, 1):
        try:
            api.create_astral_object(obj)
            print(f"Created POLYanet {i}/{len(objects)} at position ({obj.position.row}, {obj.position.column})")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error creating POLYanet at position ({obj.position.row}, {obj.position.column}): {str(e)}")

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize API client
    api = MegaverseAPI()
    
    try:
        create_cross_pattern(api)
        print("Cross pattern creation completed!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 