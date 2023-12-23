
from flask import Blueprint

from .team import team


race = Blueprint('race', __name__, url_prefix='/race')
race.register_blueprint(team)


