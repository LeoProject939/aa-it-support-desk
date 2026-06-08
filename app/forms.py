from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError
)

from app.models import User


class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full name",
        validators=[
            DataRequired(message="Full name is required."),
            Length(min=2, max=100)
        ]
    )

    email = StringField(
        "Email address",
        validators=[
            DataRequired(message="Email address is required."),
            Email(message="Enter a valid email address."),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(
                min=10,
                message="Password must be at least 10 characters long."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords must match.")
        ]
    )

    submit = SubmitField("Create account")

    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data.lower()).first()
        if existing_user:
            raise ValidationError("An account with this email already exists.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email address",
        validators=[
            DataRequired(message="Email address is required."),
            Email(message="Enter a valid email address.")
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required.")
        ]
    )

    submit = SubmitField("Log in")


class TicketForm(FlaskForm):
    title = StringField(
        "Ticket title",
        validators=[
            DataRequired(message="Ticket title is required."),
            Length(min=5, max=120)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(message="Description is required."),
            Length(min=10, max=1000)
        ]
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High")
        ],
        validators=[DataRequired(message="Priority is required.")]
    )

    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired(message="Category is required.")]
    )

    submit = SubmitField("Save ticket")


class AdminTicketUpdateForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[
            ("Open", "Open"),
            ("In Progress", "In Progress"),
            ("Resolved", "Resolved"),
            ("Closed", "Closed")
        ],
        validators=[DataRequired(message="Status is required.")]
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High")
        ],
        validators=[DataRequired(message="Priority is required.")]
    )

    submit = SubmitField("Update ticket")


class CommentForm(FlaskForm):
    body = TextAreaField(
        "Comment",
        validators=[
            DataRequired(message="Comment cannot be empty."),
            Length(min=2, max=500)
        ]
    )

    submit = SubmitField("Add comment")