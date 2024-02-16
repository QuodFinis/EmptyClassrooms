from app import app, db
from app.models import User, Room, Comment, Schedule

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Room': Room, 'Comment': Comment, 'Schedule': Schedule}