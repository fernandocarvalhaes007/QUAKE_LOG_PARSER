import re
import collections
from collections import OrderedDict
import json

GAME_REGEX = re.compile(r".*InitGame.*")
KILL_REGEX = re.compile(r".*Kill:.*:(.*) killed (.*) by (.*)")

def read_game_kills_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            log_data = file.read()
            return read_game_kills(log_data)
    except Exception as e:
        raise RuntimeError(f"Failed to read log file: {str(e)}")

def read_game_kills(log_data):
    game_count = 1
    read_game = OrderedDict()

    for line in log_data.split('\n'):
        if GAME_REGEX.match(line):
            game = f"game_{game_count}"
            read_game[game] = {
                'total_kills': 0,
                'players': set(),
                'kills': collections.defaultdict(int),
                'kills_by_means': collections.defaultdict(int)
            }
            game_count += 1
        if KILL_REGEX.match(line):
            insert_value_per_game(line, read_game[game])
                
    return read_game

def insert_value_per_game(line, read_game):
    kill = KILL_REGEX.match(line)
    killer = kill.group(1).strip()
    victim = kill.group(2).strip()
    weapon = kill.group(3).strip()
    
    read_game['total_kills'] += 1

    if killer != "<world>":
        read_game['players'].add(killer)
        read_game['kills'][killer] += 1
    else:
        read_game['kills'][victim] -= 1
    
    read_game['players'].add(victim)
    read_game['kills_by_means'][weapon] += 1

def report(read_game):
    game_reports = OrderedDict()
    for game_num, game_values in read_game.items():
        game_report = OrderedDict()
        game_report['total_kills'] = game_values['total_kills']
        game_report['players'] = sorted(list(game_values['players']))
        game_report['kills'] = dict(game_values['kills'])
        game_reports[game_num] = game_report
    
    return json.dumps(game_reports, indent=4)
