from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config  # Importe a configuração

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carregue as configurações do arquivo Config
    db.init_app(app)

    from app.controllers.filmes_controller import filmes_controller
    app.register_blueprint(filmes_controller)

    return app
