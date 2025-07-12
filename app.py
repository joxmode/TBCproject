from flask import Flask
from ext import db, login_manager
from routes import main
from models import User
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "SADNABUKA213YAJ82Y1SJ21212ASA1488AS1161HEILWASA21"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor 
def inject_user():
    return dict(current_user=current_user)

app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
