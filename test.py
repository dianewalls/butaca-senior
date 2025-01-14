from db import db
from app import app
from models import User
from sqlalchemy import text

from flask_bcrypt import Bcrypt

with app.app_context():
    db.create_all()

    bcrypt = Bcrypt(app)

    email = "inf.rpino@gmail.com"
    password = 'hola'
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    #get all users
    users = db.session.query(User).all()
    
    for user in users:
        user.password = hashed_password
        db.session.commit()
        print(f"Password for user {user.email} updated successfully.")

    # Corrected query to fetch the user by email
    #user = db.session.query(User).filter_by(email=email).first()
    #if user:
    #    print(user.email)
    #    print(user.id)
    #else:
    #    user = User(email=email, password='1234')
    #    db.session.add(user)
    #    db.session.commit()
    #    print(user.email)
    #    print(user.id)
