"""
Crossmint Challenge 2: Cleanup Utility

This script provides functionality to clean up objects created during Challenge 2.
It reads a log file of created objects and deletes them from the Megaverse.

Features:
- Reads object creation log
- Deletes objects in reverse order
- Handles rate limiting with retries
- Maintains a log of failed deletions for retry
- Provides progress feedback
"""

import os
import json
import time
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from megaverse.api import MegaverseAPI
from megaverse.models import Position

def cleanup_from_log(api: MegaverseAPI, log_file: str = 'challenge2_created.log', max_retries: int = 3, retry_delay: float = 1.0):
    """
    Clean up objects from the Megaverse based on the log file.
    
    This function:
    1. Reads the log file containing objects to delete
    2. Attempts to delete each object with retry logic for rate limits
    3. Updates the log file to only contain failed deletions for retry
    
    Args:
        api (MegaverseAPI): API client for interacting with the Megaverse
        log_file (str): Path to the log file containing objects to delete
        max_retries (int): Maximum number of retry attempts for each deletion
        retry_delay (float): Delay in seconds between retry attempts
    """
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Log file '{log_file}' not found. Nothing to clean up.")
        return
    
    print(f"Found {len(lines)} objects to clean up.")
    failed_deletions = []  # Track objects that failed to delete
    
    for i, line in enumerate(lines, 1):
        obj = json.loads(line)
        position = Position(obj["row"], obj["column"])
        
        # Try deletion with retry logic
        success = False
        for attempt in range(max_retries):
            try:
                # Delete the appropriate type of object
                if obj["type"] == "POLYANET":
                    api.delete_polyanet(position)
                elif obj["type"] == "SOLOON":
                    api.delete_soloon(position)
                elif obj["type"] == "COMETH":
                    api.delete_cometh(position)
                print(f"Deleted {obj['type']} {i}/{len(lines)} at position ({position.row}, {position.column})")
                success = True
                break
                
            except Exception as e:
                # Handle rate limit errors specifically
                if "429" in str(e):  # Too Many Requests
                    if attempt < max_retries - 1:
                        print(f"Rate limit hit, waiting {retry_delay} seconds before retry...")
                        time.sleep(retry_delay)
                        continue
                print(f"Error deleting {obj['type']} at position ({position.row}, {position.column}): {str(e)}")
                break
        
        # If deletion failed after all retries, add to failed_deletions
        if not success:
            failed_deletions.append(obj)
        
        time.sleep(0.2)  # Rate limiting between different objects
    
    # Update log file based on deletion results
    if failed_deletions:
        print(f"\nFailed to delete {len(failed_deletions)} objects. Updating log file for retry...")
        # Write only failed deletions back to the log file
        with open(log_file, 'w') as f:
            for obj in failed_deletions:
                f.write(json.dumps(obj) + '\n')
        print(f"Log file updated. Run cleanup again to retry failed deletions.")
    else:
        print("\nAll objects successfully deleted. Clearing log file.")
        open(log_file, 'w').close()

def main():
    """
    Main function to execute the cleanup process.
    
    The function:
    1. Initializes the API client
    2. Reads the log of created objects
    3. Deletes the objects
    4. Handles any errors that occur during the process
    """
    load_dotenv()
    api = MegaverseAPI()
    cleanup_from_log(api)

if __name__ == "__main__":
    main() 