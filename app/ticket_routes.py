from flask import Blueprint, abort, flash, redirect, render_template, url_for

from app import db
from app.forms import CommentForm, TicketForm
from app.models import Category, Comment, Ticket
from app.security import (
    get_current_user,
    login_required,
    log_event,
    ticket_owner_or_admin_required
)

tickets = Blueprint("tickets", __name__, url_prefix="/tickets")


def load_category_choices(form):
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(category.id, category.name) for category in categories]


@tickets.route("/")
@login_required
def list_tickets():
    user = get_current_user()

    if user.is_admin():
        user_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        user_tickets = Ticket.query.filter_by(user_id=user.id).order_by(
            Ticket.created_at.desc()
        ).all()

    return render_template("tickets/list.html", tickets=user_tickets)


@tickets.route("/new", methods=["GET", "POST"])
@login_required
def create_ticket():
    form = TicketForm()
    load_category_choices(form)

    if form.validate_on_submit():
        user = get_current_user()

        ticket = Ticket(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            priority=form.priority.data,
            category_id=form.category_id.data,
            user_id=user.id
        )

        db.session.add(ticket)
        db.session.commit()

        flash("Ticket created successfully.", "success")
        return redirect(url_for("tickets.list_tickets"))

    return render_template("tickets/create.html", form=form)


@tickets.route("/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if not ticket_owner_or_admin_required(ticket):
        user = get_current_user()
        log_event(
            "UNAUTHORISED_TICKET_ACCESS",
            f"User {user.email} attempted to view ticket {ticket.id}.",
            user.id
        )
        abort(403)

    form = CommentForm()

    if form.validate_on_submit():
        user = get_current_user()

        comment = Comment(
            body=form.body.data.strip(),
            ticket_id=ticket.id,
            user_id=user.id
        )

        db.session.add(comment)
        db.session.commit()

        flash("Comment added successfully.", "success")
        return redirect(url_for("tickets.view_ticket", ticket_id=ticket.id))

    return render_template("tickets/view.html", ticket=ticket, form=form)


@tickets.route("/<int:ticket_id>/edit", methods=["GET", "POST"])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    user = get_current_user()

    if not ticket_owner_or_admin_required(ticket):
        log_event(
            "UNAUTHORISED_TICKET_EDIT",
            f"User {user.email} attempted to edit ticket {ticket.id}.",
            user.id
        )
        abort(403)

    if not user.is_admin() and ticket.status in ["Resolved", "Closed"]:
        flash("Resolved or closed tickets cannot be edited by regular users.", "error")
        return redirect(url_for("tickets.view_ticket", ticket_id=ticket.id))

    form = TicketForm(obj=ticket)
    load_category_choices(form)

    if form.validate_on_submit():
        ticket.title = form.title.data.strip()
        ticket.description = form.description.data.strip()
        ticket.priority = form.priority.data
        ticket.category_id = form.category_id.data

        db.session.commit()

        flash("Ticket updated successfully.", "success")
        return redirect(url_for("tickets.view_ticket", ticket_id=ticket.id))

    return render_template("tickets/edit.html", form=form, ticket=ticket)