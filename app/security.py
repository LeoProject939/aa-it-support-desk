from functools import wraps

from flask import abort, current_app, flash, redirect, request, session, url_for

from app import db
from app.models import AuditLog, User


def get_current_user():
    """Return the currently logged-in user, if there is one."""
    user_id = session.get("user_id")

    if not user_id:
        return None

    return User.query.get(user_id)


def log_event(event_type, message, user_id=None):
    """Record important security and admin events."""
    audit_log = AuditLog(
        event_type=event_type,
        message=message,
        user_id=user_id,
        ip_address=request.remote_addr
    )

    db.session.add(audit_log)
    db.session.commit()

    current_app.logger.warning("%s - %s", event_type, message)


def login_required(view):
    """Block access to pages that require a logged-in user."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    """Block access to pages that require administrator permissions."""
    @wraps(view)
    def wrapped_view(**kwargs):
        user = get_current_user()

        if not user:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("auth.login"))

        if not user.is_admin():
            log_event(
                "UNAUTHORISED_ADMIN_ACCESS",
                f"User {user.email} attempted to access an admin-only page.",
                user.id
            )
            abort(403)

        return view(**kwargs)

    return wrapped_view


def ticket_owner_or_admin_required(ticket):
    """Check whether the current user owns a ticket or is an admin."""
    user = get_current_user()

    if not user:
        return False

    if user.is_admin():
        return True

    return ticket.user_id == user.id