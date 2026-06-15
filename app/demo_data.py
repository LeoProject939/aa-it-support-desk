from werkzeug.security import generate_password_hash

from app import db
from app.models import AuditLog, Category, Ticket, User


def create_demo_data():
    """Create demo records if the database is empty."""
    if User.query.first():
        return

    admin = User(
        full_name="Admin User",
        email="admin@example.com",
        password_hash=generate_password_hash("AdminPass123!"),
        role="admin"
    )

    regular_user = User(
        full_name="Regular User",
        email="user@example.com",
        password_hash=generate_password_hash("UserPass123!"),
        role="user"
    )

    db.session.add_all([admin, regular_user])
    db.session.commit()

    categories = [
        Category(
            name="Laptop",
            description="Laptop, hardware or device issues"
        ),
        Category(
            name="Network",
            description="Wi-Fi, VPN or connection issues"
        ),
        Category(
            name="Account Access",
            description="Password, login or permission issues"
        ),
        Category(
            name="Business Application Support",
            description="Support for internal business applications and system errors"
        ),
        Category(
            name="Software Installation",
            description="Software requests, installation problems and application updates"
        ),
        Category(
            name="Other",
            description="Can't find what you're looking for"
        )
    ]

    db.session.add_all(categories)
    db.session.commit()

    tickets = [
        Ticket(
            title="Unable to connect to VPN",
            description="VPN fails when trying to connect from home.",
            priority="High",
            status="Open",
            user_id=regular_user.id,
            category_id=categories[1].id
        ),
        Ticket(
            title="Laptop running slowly",
            description="Laptop takes a long time to start and open apps.",
            priority="Medium",
            status="In Progress",
            user_id=regular_user.id,
            category_id=categories[0].id
        )
    ]

    db.session.add_all(tickets)

    audit_log = AuditLog(
        event_type="DEMO_DATA_CREATED",
        message="Demo users, categories and tickets created.",
        user_id=admin.id,
        ip_address="127.0.0.1"
    )

    db.session.add(audit_log)
    db.session.commit()