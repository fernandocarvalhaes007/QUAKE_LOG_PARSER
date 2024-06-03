from flask import Blueprint, jsonify, request, current_app
from ..models.log_parser import read_game_kills_from_file, report
import logging

app = Blueprint('default', __name__)

# Create a logger for the Blueprint
logger = logging.getLogger('quake_log_parser')
logger.setLevel(logging.INFO)

@app.route('/games', methods=['POST'])
def parse_log():
    try:
        # Check if the request is JSON
        if not request.is_json:
            raise ValueError(f"Request content-type must be application/json, got {request.content_type} instead")

        # Use the configured log file path
        file_path = current_app.config.get('LOG_FILE_PATH', 'app/data/games.log')
        read_game = read_game_kills_from_file(file_path)
        game_reports = report(read_game)
        return game_reports, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Error parsing log: {e}")
        return jsonify({'error': str(e)}), 500
