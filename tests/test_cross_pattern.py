import pytest
from unittest.mock import Mock, patch
from megaverse.api import MegaverseAPI
from megaverse.patterns import PatternGenerator
from megaverse.models import Position, PolyanetObject

def test_cross_pattern_generation():
    """Test that the cross pattern is generated correctly."""
    objects = PatternGenerator.generate_cross()
    
    # Verify we have the correct number of objects (13 for the cross)
    assert len(objects) == 13
    
    # Verify all objects are POLYanets
    assert all(isinstance(obj, PolyanetObject) for obj in objects)
    
    # Verify the positions form the expected cross
    center = 11 // 2
    distances = [2, 3, 4]
    expected_positions = set()
    for dist in distances:
        expected_positions.add((center - dist, center - dist))  # Top-left
        expected_positions.add((center + dist, center + dist))  # Bottom-right
        expected_positions.add((center - dist, center + dist))  # Top-right
        expected_positions.add((center + dist, center - dist))  # Bottom-left
    expected_positions.add((center, center))  # Center
    positions = {(obj.position.row, obj.position.column) for obj in objects}
    assert positions == expected_positions

@pytest.fixture
def mock_api():
    """Create a mock API for testing."""
    api = Mock(spec=MegaverseAPI)
    return api

def test_create_cross_pattern(mock_api):
    """Test the creation of the cross pattern through the API."""
    from challenge1_cross import create_cross_pattern
    
    # Call the function
    create_cross_pattern(mock_api)
    
    # Verify the API was called 13 times (once for each POLYanet)
    assert mock_api.create_astral_object.call_count == 13
    
    # Verify each call was made with a POLYanet
    for call in mock_api.create_astral_object.call_args_list:
        obj = call.args[0]
        assert isinstance(obj, PolyanetObject)

@patch('challenge1_cross.MegaverseAPI')
def test_main_function(mock_api_class):
    """Test the main function execution."""
    from challenge1_cross import main
    
    # Configure the mock
    mock_api = Mock()
    mock_api_class.return_value = mock_api
    
    # Call main
    result = main()
    
    # Verify the result
    assert result == 0
    
    # Verify API was initialized and create_cross_pattern was called
    mock_api_class.assert_called_once()
    assert mock_api.create_astral_object.call_count == 13

def test_error_handling(mock_api):
    """Test error handling during pattern creation."""
    from challenge1_cross import create_cross_pattern
    
    # Configure the mock to raise an exception
    mock_api.create_astral_object.side_effect = Exception("API Error")
    
    # Call the function - it should not raise an exception
    create_cross_pattern(mock_api)
    
    # Verify the API was called
    assert mock_api.create_astral_object.call_count == 13 