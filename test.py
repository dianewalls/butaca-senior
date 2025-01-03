from db import db
from app import app
from models import User

with app.app_context():
    db.create_all()

    email = "ddd111111111111111@ddd.com"

    # Corrected query to fetch the user by email
    user = db.session.query(User).filter_by(email=email).first()
    if user:
        print(user.email)
        print(user.id)
    else:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        print(user.email)
        print(user.id)
