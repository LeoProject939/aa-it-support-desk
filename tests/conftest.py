import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import Category, Ticket, User


@pytest.fixture
def app():
    test_app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key"
    })

    with test_app.app_context():
        db.create_all()

        admin = User(
            full_name="Test Admin",
            email="admin@test.com",
            password_hash=generate_password_hash("AdminPass123!"),
            role="admin"
        )

        user = User(
            full_name="Test User",
            email="user@test.com",
            password_hash=generate_password_hash("UserPass123!"),
            role="user"
        )

        category = Category(
            name="Network",
            description="Network and VPN issues"
        )

        db.session.add_all([admin, user, category])
        db.session.commit()

        ticket = Ticket(
            title="VPN connection issue",
            description="Unable to connect to the VPN from home.",
            priority="High",
            status="Open",
            user_id=user.id,
            category_id=category.id
        )

        db.session.add(ticket)
        db.session.commit()

        yield test_app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, email="user@test.com", password="UserPass123!"):
    return client.post(
        "/auth/login",
        data={
            "email": email,
            "password": password
        },
        follow_redirects=True
    )