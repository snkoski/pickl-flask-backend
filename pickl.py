from app import create_app, db
from app.models import Game, Team, User, Vote

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Game': Game, 'Team': Team, 'User': User, 'Vote': Vote}