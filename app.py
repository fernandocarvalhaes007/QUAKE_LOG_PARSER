from flask import Flask, request, jsonify
from log_parser import read_game_kills_from_file, report
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/games', methods=['POST'])
def parse_log():
    try:
        # Check if the request is JSON
        if not request.is_json:
            raise ValueError(f"Request content-type must be application/json, got {request.content_type} instead")

        file_path = request.json.get('file_path', 'games.log')
        read_game = read_game_kills_from_file(file_path)
        game_reports = report(read_game)
        return game_reports, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        app.logger.error(f"Error parsing log: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
