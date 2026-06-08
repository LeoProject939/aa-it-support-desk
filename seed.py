from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User, Category, Ticket, Comment, AuditLog

app = create_app()


def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

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
            ),
            Ticket(
                title="Password reset required",
                description="User is locked out after too many login attempts.",
                priority="Low",
                status="Resolved",
                user_id=regular_user.id,
                category_id=categories[2].id
            )
        ]

        db.session.add_all(tickets)
        db.session.commit()

        comment = Comment(
            body="Initial ticket review completed by support team.",
            ticket_id=tickets[1].id,
            user_id=admin.id
        )

        audit_log = AuditLog(
            event_type="SEED_DATA_CREATED",
            message="Sample users, categories and tickets created.",
            user_id=admin.id,
            ip_address="127.0.0.1"
        )

        db.session.add_all([comment, audit_log])
        db.session.commit()

        print("Sample database created successfully.")
        print("Admin login: admin@example.com / AdminPass123!")
        print("User login: user@example.com / UserPass123!")


if __name__ == "__main__":
    seed_database()