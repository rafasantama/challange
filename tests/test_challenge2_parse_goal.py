import pytest
from megaverse.models import Position
from challenge2_goal_parser import parse_goal_map

def test_parse_goal_map():
    goal_map = {
        "goal": [
            [None, "POLYANET", None],
            ["RED_SOLOON", None, "UP_COMETH"],
            [None, None, None],
        ]
    }
    expected = [
        {"row": 0, "column": 1, "type": "POLYANET"},
        {"row": 1, "column": 0, "type": "SOLOON", "color": "red"},
        {"row": 1, "column": 2, "type": "COMETH", "direction": "up"},
    ]
    result = parse_goal_map(goal_map)
    assert result == expected 

def test_parse_empty_goal():
    """Test parsing an empty goal map."""
    goal_map = {"goal": []}
    objects = parse_goal_map(goal_map)
    assert len(objects) == 0

def test_parse_polyanet():
    """Test parsing a POLYANET object."""
    goal_map = {
        "goal": [
            ["SPACE", "POLYANET", "SPACE"]
        ]
    }
    objects = parse_goal_map(goal_map)
    assert len(objects) == 1
    assert objects[0] == {
        "row": 0,
        "column": 1,
        "type": "POLYANET"
    }

def test_parse_soloon_colors():
    """Test parsing SOLOON objects with different colors."""
    goal_map = {
        "goal": [
            ["SPACE", "BLUE_SOLOON", "SPACE"],
            ["RED_SOLOON", "SPACE", "PURPLE_SOLOON"],
            ["SPACE", "WHITE_SOLOON", "SPACE"]
        ]
    }
    objects = parse_goal_map(goal_map)
    assert len(objects) == 4
    
    # Verify each SOLOON's color
    expected_colors = {
        (0, 1): "blue",
        (1, 0): "red",
        (1, 2): "purple",
        (2, 1): "white"
    }
    
    for obj in objects:
        assert obj["type"] == "SOLOON"
        position = (obj["row"], obj["column"])
        assert position in expected_colors
        assert obj["color"] == expected_colors[position]

def test_parse_cometh_directions():
    """Test parsing COMETH objects with different directions."""
    goal_map = {
        "goal": [
            ["SPACE", "UP_COMETH", "SPACE"],
            ["LEFT_COMETH", "SPACE", "RIGHT_COMETH"],
            ["SPACE", "DOWN_COMETH", "SPACE"]
        ]
    }
    objects = parse_goal_map(goal_map)
    assert len(objects) == 4
    
    # Verify each COMETH's direction
    expected_directions = {
        (0, 1): "up",
        (1, 0): "left",
        (1, 2): "right",
        (2, 1): "down"
    }
    
    for obj in objects:
        assert obj["type"] == "COMETH"
        position = (obj["row"], obj["column"])
        assert position in expected_directions
        assert obj["direction"] == expected_directions[position]

def test_parse_mixed_objects():
    """Test parsing a mix of different object types."""
    goal_map = {
        "goal": [
            ["SPACE", "POLYANET", "BLUE_SOLOON"],
            ["RED_SOLOON", "UP_COMETH", "SPACE"],
            ["POLYANET", "SPACE", "RIGHT_COMETH"]
        ]
    }
    objects = parse_goal_map(goal_map)
    assert len(objects) == 6
    
    # Verify each object's type and properties
    expected_objects = {
        (0, 1): {"type": "POLYANET"},
        (0, 2): {"type": "SOLOON", "color": "blue"},
        (1, 0): {"type": "SOLOON", "color": "red"},
        (1, 1): {"type": "COMETH", "direction": "up"},
        (2, 0): {"type": "POLYANET"},
        (2, 2): {"type": "COMETH", "direction": "right"}
    }
    
    for obj in objects:
        position = (obj["row"], obj["column"])
        assert position in expected_objects
        expected = expected_objects[position]
        assert obj["type"] == expected["type"]
        if "color" in expected:
            assert obj["color"] == expected["color"]
        if "direction" in expected:
            assert obj["direction"] == expected["direction"]

def test_parse_invalid_objects():
    """Test parsing invalid or unknown object types."""
    goal_map = {
        "goal": [
            ["SPACE", "INVALID_OBJECT", "SPACE"],
            ["UNKNOWN_SOLOON", "SPACE", "WRONG_COMETH"],
            ["SPACE", "SPACE", "SPACE"]
        ]
    }
    objects = parse_goal_map(goal_map)
    assert len(objects) == 0  # Invalid objects should be skipped

def test_parse_none_values():
    """Test parsing goal map with None values."""
    goal_map = {
        "goal": [
            ["SPACE", None, "POLYANET"],
            [None, "BLUE_SOLOON", None],
            ["SPACE", "UP_COMETH", "SPACE"]
        ]
    }
    objects = parse_goal_map(goal_map)
    assert len(objects) == 3
    
    # Verify only valid objects are parsed
    expected_positions = {(0, 2), (1, 1), (2, 1)}
    for obj in objects:
        position = (obj["row"], obj["column"])
        assert position in expected_positions 