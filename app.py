from flask import Flask, render_template
from config import Config
from models import db, User
from routes import register_routes
from auth import authenticate_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Create initial admin user
    if not User.query.filter_by(username='root').first():
        admin = User(username='root')
        admin.set_password('chebbi.exe')
        db.session.add(admin)
        db.session.commit()

register_routes(app)
authenticate_user(app)

if __name__ == '__main__':
    app.run(debug=True)