import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    LOG_FILE_PATH = os.path.join(BASE_DIR, 'app/data/games.log')

config = Config()