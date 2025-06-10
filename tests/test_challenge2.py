"""
Test suite for Challenge 2 implementation.
Tests the creation of objects from the goal map and error handling.
"""

import pytest
from unittest.mock import Mock, patch
from challenge2 import create_objects_from_goal

def test_create_objects_from_goal():
    # Mock API and its methods
    mock_api = Mock()
    mock_api.get_goal_map.return_value = {
        "goal": [
            [None, "POLYANET", None],
            ["RED_SOLOON", None, "UP_COMETH"],
            [None, None, None],
        ]
    }
    
    # Test dry run
    create_objects_from_goal(mock_api, dry_run=True)
    
    # Verify API was not called for creation
    assert not mock_api.create_polyanet.called
    assert not mock_api.create_soloon.called
    assert not mock_api.create_cometh.called
    
    # Test actual creation
    create_objects_from_goal(mock_api, dry_run=False)
    
    # Verify API was called correctly
    assert mock_api.create_polyanet.call_count == 1
    assert mock_api.create_soloon.call_count == 1
    assert mock_api.create_cometh.call_count == 1
    
    # Verify the correct positions were used
    polyanet_call = mock_api.create_polyanet.call_args[0][0]
    assert polyanet_call.row == 0
    assert polyanet_call.column == 1
    
    soloon_call = mock_api.create_soloon.call_args
    assert soloon_call[0][0].row == 1
    assert soloon_call[0][0].column == 0
    assert soloon_call[0][1] == "red"  # color is the second positional argument
    
    cometh_call = mock_api.create_cometh.call_args
    assert cometh_call[0][0].row == 1
    assert cometh_call[0][0].column == 2
    assert cometh_call[0][1] == "up"  # direction is the second positional argument

def test_error_handling():
    # Mock API that raises an exception
    mock_api = Mock()
    mock_api.get_goal_map.side_effect = Exception("API Error")
    
    # Test that the function handles the error gracefully
    create_objects_from_goal(mock_api)
    # If we get here without an exception, the error was handled correctly 