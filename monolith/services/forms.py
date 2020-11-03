from wtforms.fields.core import StringField
from monolith.services.auth import authority_required
from sys import displayhook
from wtforms import widgets
from wtforms.fields.html5 import DateField, EmailField, IntegerField
from monolith.models.precautions import Precautions
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from monolith import db
import wtforms as f
from wtforms.validators import DataRequired, Length, NumberRange, Email


class LoginForm(FlaskForm):
    email = f.StringField("Email", validators=[DataRequired()])
    password = f.PasswordField("Password", validators=[DataRequired()])
    display = ["email", "password"]


class UserForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    firstname = f.StringField("firstname", validators=[DataRequired()])
    lastname = f.StringField("lastname", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    dateofbirth = DateField("dateofbirth", validators=[DataRequired()])
    display = ["email", "firstname", "lastname", "password", "dateofbirth"]


# TODO Validators are missing?
class OperatorForm(UserForm):
    # TODO validate fiscal code in a good proper way
    fiscal_code = f.StringField("Fiscal Code", validators=[DataRequired()])
    display = [
        "email",
        "firstname",
        "lastname",
        "password",
        "dateofbirth",
        "fiscal_code",
    ]


class AuthorityForm(FlaskForm):
    email = f.StringField("Email", validators=[DataRequired()])
    name = f.StringField("Name", validators=[DataRequired()])
    password = f.PasswordField("Password", validators=[DataRequired()])
    phone = f.IntegerField("Phone", validators=[DataRequired()])
    country = f.StringField("Country", validators=[DataRequired()])
    state = f.StringField("State", validators=[DataRequired()])
    city = f.StringField("City", validators=[DataRequired()])
    # TODO adding validators here causes two fails in the tests
    lat = f.DecimalField("Latitude", validators=[DataRequired()])
    lon = f.DecimalField("Longitude", validators=[DataRequired()])

    display = ["email", "name", "password", "country", "state", "city", "lat", "lon"]


def precautions_choices():
    return db.session.query(Precautions)


class MultiCheckboxField(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CreateRestaurantForm(FlaskForm):
    name = f.StringField("Name", validators=[DataRequired()])
    lat = f.FloatField(
        "latitude",
        validators=[
            DataRequired(),
            NumberRange(-90, 90, "Latitude must be between -90 and 90"),
        ],
    )
    lon = f.FloatField(
        "Longitude",
        validators=[
            DataRequired(),
            NumberRange(-180, 180, "Longitude must be between -180 and 180"),
        ],
    )
    phone = f.IntegerField("Phone", validators=[DataRequired()])
    time_of_stay = f.RadioField(
        "Time of stay",
        choices=[("30", "30 minutes"), ("90", "1:30 hour"), ("180", "3 hours")],
        validators=[DataRequired()],
    )
    prec_measures = MultiCheckboxField(
        "Precautions",
        get_label="name",
        query_factory=precautions_choices,
    )
    display = ["name", "lat", "lon", "phone", "time_of_stay", "prec_measures"]


class CreateTableForm(FlaskForm):
    name = f.StringField("Name", validators=[DataRequired()])
    seats = f.IntegerField(
        "Seats",
        validators=[
            DataRequired(),
            NumberRange(
                0, 20, "The number of seats for each table must be between 0 and 20"
            ),
        ],
    )
    display = ["name", "seats"]


class MarkSsnForm(FlaskForm):
    # TODO Custom validator to check if ssn is valid
    duration = IntegerField(
        "Duration",
        validators=[
            DataRequired(message="This field must be a number."),
            NumberRange(
                min=1, max=60, message="The duration must be between 1 and 60."
            ),
        ],
    )
    ssn = f.StringField(
        "SSN",
        validators=[DataRequired()],
        render_kw={"placeholder": "RSSMRA00A01H501C"},
    )
    submit = f.SubmitField("Mark")
    display = ["duration", "ssn", "submit"]


class MarkEmailForm(FlaskForm):
    duration = IntegerField(
        "Duration",
        validators=[
            DataRequired(message="This field must be a number."),
            NumberRange(
                min=1, max=60, message="The duration must be between 1 and 60."
            ),
        ],
    )
    email = f.StringField(
        "Email",
        validators=[DataRequired(), Email(message="Insert a valid email address.")],
        render_kw={"placeholder": "example@mail.com"},
    )
    submit = f.SubmitField("Mark")
    display = ["duration", "email", "submit"]


class MarkPhoneNumberForm(FlaskForm):
    duration = IntegerField(
        "Duration",
        validators=[
            DataRequired(message="This field must be a number."),
            NumberRange(
                min=1, max=60, message="The duration must be between 1 and 60."
            ),
        ],
    )
    phone_number = f.StringField(
        "Phone number",
        validators=[DataRequired("This field must be a valid phone number")],
        render_kw={"placeholder": "333 3339999"},
    )
    submit = f.SubmitField("Mark")
    display = ["duration", "phone_number", "submit"]


class ReviewForm(FlaskForm):
    rating = IntegerField(
        "Your rating",
        validators=[
            DataRequired(),
            NumberRange(
                min=1, max=5, message="The number of stars must be between 1 and 5"
            ),
        ],
    )
    message = f.TextAreaField("Your review", validators=[Length(min=30, message="The review should be at least of 30 characters.")])
