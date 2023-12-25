
from flask import Blueprint

from .team import team
from .member import member


race = Blueprint('race', __name__, url_prefix='/race')
race.register_blueprint(team)
race.register_blueprint(member)


