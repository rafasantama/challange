import pytest
from unittest.mock import Mock, patch
from challenge2_goal_parser import parse_goal_map

def test_parse_goal_map_from_api():
    # Mocked goal map as returned by the API
    goal_map = {
        "goal": [
            [None, "POLYANET", None],
            ["SOLOON_RED", None, "COMETH_UP"],
            [None, None, None],
        ]
    }
    expected = [
        {"row": 0, "column": 1, "type": "POLYANET"},
        {"row": 1, "column": 0, "type": "SOLOON", "color": "red"},
        {"row": 1, "column": 2, "type": "COMETH", "direction": "up"},
    ]

    # Patch MegaverseAPI.get_goal_map to return our mocked goal_map
    with patch('megaverse.api.MegaverseAPI.get_goal_map', return_value=goal_map):
        from megaverse.api import MegaverseAPI
        api = MegaverseAPI(candidate_id="dummy")
        result = parse_goal_map(api.get_goal_map())
        assert result == expected 