import os

class Config:
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'games.log')

config = Config()
