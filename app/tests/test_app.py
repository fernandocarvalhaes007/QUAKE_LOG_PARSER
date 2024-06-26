import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_parse_log_success(client, mocker):
    mock_read_game_kills_from_file = mocker.patch('app.models.log_parser.read_game_kills')
    mock_report = mocker.patch('app.models.log_parser.report')

    mock_read_game_kills_from_file.return_value = {
        'game_1': {
            'total_kills': 2,
            'players': {'Player1', 'Player2'},
            'kills': {'Player1': 1, 'Player2': -1},
            'kills_by_means': {'MOD_ROCKET': 2}
        }
    }
    mock_report.return_value = json.dumps({
        'game_1': {
            'total_kills': 2,
            'players': ['Player1', 'Player2'],
            'kills': {'Player1': 1, 'Player2': -1}
        }
    })

    headers = {'Content-Type': 'application/json'}
    response = client.post('/games', data=json.dumps({'file_path': 'app/data/games.log'}), headers=headers)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    expected_data = {
        'game_1': {
            'total_kills': 2,
            'players': ['Player1', 'Player2'],
            'kills': {'Player1': 1, 'Player2': -1}
        }
    }
    assert json.loads(response.data) == expected_data

def test_parse_log_failure(client, mocker):
    mock_read_game_kills_from_file = mocker.patch('app.models.log_parser.read_game_kills')
    mock_read_game_kills_from_file.side_effect = Exception('Failed to read log file')

    headers = {'Content-Type': 'application/json'}
    response = client.post('/games', data=json.dumps({'file_path': 'app/data/games.log'}), headers=headers)
    assert response.status_code == 500
    assert response.content_type == 'application/json'
    expected_data = {'error': 'Failed to read log file: Failed to read log file'}
    assert json.loads(response.data) == expected_data
