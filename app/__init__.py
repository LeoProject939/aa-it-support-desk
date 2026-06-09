from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    """Create/configure the AA - Support Desk App."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app import models
    from app.admin_routes import admin
    from app.auth_routes import auth
    from app.ticket_routes import tickets

    app.register_blueprint(auth)
    app.register_blueprint(tickets)
    app.register_blueprint(admin)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html"), 500

    return app