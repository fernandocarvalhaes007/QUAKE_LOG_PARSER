from log_parser import read_game_kills, report
import json

def test_read_game_kills():
    log_data = """
    20:34 InitGame: \\sv_floodprotect\\1\\g_synchronousClients\\0\\...
    20:37 Kill: 1022 2 22: <world> killed Player2 by MOD_TRIGGER_HURT
    20:38 Kill: 2 3 7: Player1 killed Player3 by MOD_ROCKET
    """
    expected_result = {
        'game_1': {
            'total_kills': 2,
            'players': {'Player1', 'Player2', 'Player3'},
            'kills': {'Player1': 1, 'Player2': -1},
            'kills_by_means': {'MOD_TRIGGER_HURT': 1, 'MOD_ROCKET': 1}
        }
    }
    assert read_game_kills(log_data) == expected_result

def test_report():
    read_game = {
        'game_1': {
            'total_kills': 2,
            'players': {'Player1', 'Player2'},
            'kills': {'Player1': 1, 'Player2': -1},
            'kills_by_means': {'MOD_ROCKET': 2}
        }
    }
    expected_report = json.dumps({
        'game_1': {
            'total_kills': 2,
            'players': ['Player1', 'Player2'],
            'kills': {'Player1': 1, 'Player2': -1}
        }
    }, indent=4)
    assert report(read_game) == expected_report
