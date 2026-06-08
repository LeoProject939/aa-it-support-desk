import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration for the Flask IT Desk Ticket application."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///supportdesk.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False