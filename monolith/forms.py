from monolith.models import precautions
from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    display = ["email", "password"]


class UserForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    firstname = f.StringField("firstname", validators=[DataRequired()])
    lastname = f.StringField("lastname", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    dateofbirth = f.DateField("dateofbirth", format="%d/%m/%Y")
    display = ["email", "firstname", "lastname", "password", "dateofbirth"]


class OperatorForm(UserForm):
    # TODO validate fiscal code in a good proper way
    fiscal_code = f.StringField("fiscalcode", validators=[DataRequired()])
    display = [
        "email",
        "firstname",
        "lastname",
        "password",
        "dateofbirth",
        "fiscal_code",
    ]


class AuthorityForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    name = f.StringField("name", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    country = f.StringField("country", validators=[DataRequired()])
    state = f.StringField("state", validators=[DataRequired()])
    city = f.StringField("city", validators=[DataRequired()])
    lat = f.DecimalField("latitude", validators=[DataRequired()])
    lon = f.DecimalField("longitude", validators=[DataRequired()])

    display = ["email", "name", "password", "country", "state", "city", "lat", "lon"]


class CreateRestaurantForm(FlaskForm):
    name = f.StringField("name", validators=[DataRequired()])
    latitude = f.FloatField("latitude", validators=[DataRequired()])
    longitude = f.FloatField("longitude", validators=[DataRequired()])
    phone = f.IntegerField("phone", validators=[DataRequired()])
    display = ["name", "latitude", "longitude", "phone"]

class CreateTableForm(FlaskForm):
    name = f.StringField("name", validators=[DataRequired()])
    seats = f.IntegerField("seats", validators=[DataRequired()])
    display = ["name", "seats"]