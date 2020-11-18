from .home import home
from .auth import auth
from .users import users
from .restaurants import restaurants
from .operators import operators
from .health_authorities import authorities
from .marks import marks
from .profile import me

blueprints = [
    home,
    me,
    auth,
    users,
    restaurants,
    operators,
    authorities,
    marks,
]
