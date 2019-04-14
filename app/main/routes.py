from app import db
from app.models import Game, Team, User, Vote
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return "Hello World :)"