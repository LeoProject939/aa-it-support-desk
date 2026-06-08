from flask import Blueprint, flash, redirect, render_template, url_for

from app import db
from app.forms import AdminTicketUpdateForm
from app.models import AuditLog, Ticket, User
from app.security import admin_required, login_required, log_event

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@login_required
@admin_required
def dashboard():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    users = User.query.order_by(User.created_at.desc()).all()
    audit_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()

    return render_template(
        "admin/dashboard.html",
        tickets=tickets,
        users=users,
        audit_logs=audit_logs
    )


@admin.route("/tickets/<int:ticket_id>/update", methods=["GET", "POST"])
@login_required
@admin_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = AdminTicketUpdateForm(obj=ticket)

    if form.validate_on_submit():
        ticket.status = form.status.data
        ticket.priority = form.priority.data

        db.session.commit()

        log_event(
            "ADMIN_TICKET_UPDATED",
            f"Ticket {ticket.id} was updated by an administrator."
        )

        flash("Ticket updated successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/update_ticket.html", form=form, ticket=ticket)


@admin.route("/tickets/<int:ticket_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    db.session.delete(ticket)
    db.session.commit()

    log_event(
        "ADMIN_TICKET_DELETED",
        f"Ticket {ticket_id} was deleted by an administrator."
    )

    flash("Ticket deleted successfully.", "success")
    return redirect(url_for("admin.dashboard"))