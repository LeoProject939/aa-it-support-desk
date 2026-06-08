from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    """Create/configure the AA - Support Desk App."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app import models

    @app.route("/")
    def home():
        return "AA IT Support Desk is running."

    return app