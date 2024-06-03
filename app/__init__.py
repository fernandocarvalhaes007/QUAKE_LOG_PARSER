from flask import Flask
import logging

def create_app():
    app = Flask(__name__)
    
    # Configurações adicionais
    app.config.from_pyfile('../config.py')
    
    # Registro dos blueprints
    from app.controllers.default import app as default_app
    app.register_blueprint(default_app)

    # Configurar o logger
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app

app = create_app()
