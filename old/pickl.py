from app import app, db
from app.models import User, Team, Game, Vote

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Team': Team, 'Game': Game, 'Vote': Vote}
