import functools
from flask import session, g, request, redirect, url_for
from flask_login import current_user
from monolith.models import User, HealthAuthority, Operator
from functools import wraps

from monolith import login_manager


def operator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = current_user.is_authenticated
        if not authenticated:
            return redirect("/operator_login")
        elif session["role"] != "operator":
            return login_manager.unauthorized()
            # need to implement logic for logout maybe? or templated error page
            pass
        return f(*args, **kwargs)

    return decorated_function


def authority_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = current_user.is_authenticated
        if not authenticated:
            return redirect("/authority_login")
        elif session["role"] != "authority":
            return login_manager.unauthorized()
            # need to implement logic for logout maybe? or templated error page
            pass
        return f(*args, **kwargs)

    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = current_user.is_authenticated
        if not authenticated:
            return redirect("/login")
        elif session["role"] != "user":
            return login_manager.unauthorized()
        return f(*args, **kwargs)

    return decorated_function


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)

    return _admin_required


@login_manager.user_loader
def load_user(user_id):
    if session["role"] == "user":
        user = User.query.get(user_id)
    elif session["role"] == "operator":
        user = Operator.query.get(user_id)
    elif session["role"] == "authority":
        user = HealthAuthority.query.get(user_id)

    if user is not None:
        user._authenticated = True
    return user
