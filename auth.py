from flask import g, redirect, url_for
from models import db, User

def authenticate_user(app):
    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            g.user = User.query.get(session['user_id'])

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('index'))