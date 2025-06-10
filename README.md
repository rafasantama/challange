# Crossmint Megaverse Challenge

This project implements solutions for the Crossmint Megaverse Challenge, focusing on creating and managing astral objects (POLYANETs, SOLOONs, and COMETHs) in a grid-based universe.

## Project Structure

```
.
├── megaverse/                 # Core package for Megaverse functionality
│   ├── __init__.py           # Package initialization
│   ├── api.py                # API client for Crossmint API
│   ├── models.py             # Data models for astral objects
│   └── patterns.py           # Pattern generation utilities
├── challenge1_cross.py       # Solution for Challenge 1 (Cross Pattern)
├── challenge2.py             # Main script for Challenge 2
├── challenge2_goal_parser.py # Goal map parsing for Challenge 2
├── challenge2_cleanup.py     # Cleanup utility for Challenge 2
├── tests/                    # Test suite
│   ├── test_challenge2.py
│   ├── test_challenge2_cleanup.py
│   ├── test_challenge2_parse_goal.py
│   └── test_cross_pattern.py
└── goal.json                 # Goal map for Challenge 2
```

## Features

### Challenge 1: Cross Pattern
- Creates a cross pattern using POLYANETs
- Configurable size and center position
- Includes cleanup functionality

### Challenge 2: Logo Pattern
- Fetches and parses goal map from Crossmint API
- Creates objects with specific properties:
  - POLYANET: Basic object
  - SOLOON: Colored objects (blue, red, purple, white)
  - COMETH: Directional objects (up, down, left, right)
- Includes error handling and rate limiting
- Provides cleanup functionality with retry logic
- Comprehensive test suite

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd crossmint-challenge
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your Crossmint API credentials:
```
CANDIDATE_ID=your_candidate_id
```

## Usage

### Challenge 1: Cross Pattern
```bash
python challenge1_cross.py
```

### Challenge 2: Logo Pattern
```bash
# Create objects
python challenge2.py

# Clean up objects
python challenge2_cleanup.py
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Implementation Details

### API Client (`megaverse/api.py`)
- Handles all API interactions with Crossmint
- Implements rate limiting and error handling
- Supports creation and deletion of all object types

### Goal Parser (`challenge2_goal_parser.py`)
- Parses the goal map from the API
- Extracts object types and properties
- Validates object properties (colors, directions)

### Cleanup Utility (`challenge2_cleanup.py`)
- Removes created objects
- Implements retry logic for rate limits
- Maintains a log of created objects for cleanup

## Error Handling

The project includes comprehensive error handling:
- API rate limiting (429 errors)
- Invalid object properties
- Network errors
- Invalid goal map data

## Testing Strategy

The test suite covers:
- Goal map parsing
- Object creation and deletion
- Error handling
- Edge cases
- Property validation

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 