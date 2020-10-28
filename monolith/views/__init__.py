import operator
from .home import home
from .auth import auth
from .users import users
from .restaurants import restaurants
from .operators import operators
from .health_authorities import authorities


blueprints = [home, auth, users, restaurants, operators, authorities]
