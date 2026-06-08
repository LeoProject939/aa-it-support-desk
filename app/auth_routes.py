from flask import Blueprint, flash, redirect, render_template, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import LoginForm, RegisterForm
from app.models import User
from app.security import log_event

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            full_name=form.full_name.data.strip(),
            email=form.email.data.lower().strip(),
            password_hash=generate_password_hash(form.password.data),
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            session.clear()
            session["user_id"] = user.id
            session["role"] = user.role
            session["full_name"] = user.full_name

            flash("Login successful.", "success")

            if user.is_admin():
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("tickets.list_tickets"))

        log_event(
            "FAILED_LOGIN",
            f"Failed login attempt for email: {email}"
        )
        flash("Invalid email or password.", "error")

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))