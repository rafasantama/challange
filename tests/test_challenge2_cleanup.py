import os
import json
from unittest.mock import Mock
from challenge2_cleanup import cleanup_from_log

def test_cleanup_from_log(tmp_path):
    """
    Test the basic cleanup functionality with retry logic.
    
    This test:
    1. Creates a fake log file with three objects (POLYANET, SOLOON, COMETH)
    2. Mocks the API to fail the SOLOON deletion once then succeed
    3. Verifies that:
       - All objects are attempted to be deleted
       - The SOLOON is retried and eventually succeeds
       - The correct API methods are called with correct positions
    """
    # Prepare a fake log file with test data
    log_entries = [
        {"row": 0, "column": 1, "type": "POLYANET"},
        {"row": 1, "column": 0, "type": "SOLOON", "color": "red"},
        {"row": 1, "column": 2, "type": "COMETH", "direction": "up"},
    ]
    log_file = tmp_path / "challenge2_created.log"
    with open(log_file, 'w') as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + '\n')

    # Mock API with specific behavior for SOLOON deletion
    mock_api = Mock()
    # Make the second deletion fail with a 429 error, then succeed
    mock_api.delete_soloon.side_effect = [
        Exception("429 Client Error: Too Many Requests"),
        None  # Second attempt succeeds
    ]

    # Run cleanup with shorter retry delay for testing
    cleanup_from_log(mock_api, log_file=str(log_file), max_retries=2, retry_delay=0.1)

    # Verify API calls
    assert mock_api.delete_polyanet.call_count == 1
    assert mock_api.delete_soloon.call_count == 2  # Called twice due to retry
    assert mock_api.delete_cometh.call_count == 1

    # Verify correct positions were used
    polyanet_call = mock_api.delete_polyanet.call_args[0][0]
    assert polyanet_call.row == 0 and polyanet_call.column == 1
    soloon_call = mock_api.delete_soloon.call_args[0][0]
    assert soloon_call.row == 1 and soloon_call.column == 0
    cometh_call = mock_api.delete_cometh.call_args[0][0]
    assert cometh_call.row == 1 and cometh_call.column == 2

def test_cleanup_with_failed_deletions(tmp_path):
    """
    Test the cleanup process when some deletions fail permanently.
    
    This test:
    1. Creates a fake log file with two objects
    2. Mocks the API to always fail for SOLOON deletions
    3. Verifies that:
       - The log file is updated to only contain the failed deletion
       - The successful deletion is removed from the log
    """
    # Prepare a fake log file with test data
    log_entries = [
        {"row": 0, "column": 1, "type": "POLYANET"},
        {"row": 1, "column": 0, "type": "SOLOON", "color": "red"},
    ]
    log_file = tmp_path / "challenge2_created.log"
    with open(log_file, 'w') as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + '\n')

    # Mock API that always fails for SOLOON
    mock_api = Mock()
    mock_api.delete_soloon.side_effect = Exception("429 Client Error: Too Many Requests")

    # Run cleanup
    cleanup_from_log(mock_api, log_file=str(log_file), max_retries=2, retry_delay=0.1)

    # Verify log file only contains the failed deletion
    with open(log_file, 'r') as f:
        remaining_entries = [json.loads(line) for line in f.readlines()]
    
    assert len(remaining_entries) == 1
    assert remaining_entries[0]["type"] == "SOLOON"
    assert remaining_entries[0]["row"] == 1
    assert remaining_entries[0]["column"] == 0 