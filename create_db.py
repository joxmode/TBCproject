from ext import db
from models import User, News, Info, Comment
from app import app

with app.app_context():
    db.create_all()
    print("✅ Database and tables created!")
