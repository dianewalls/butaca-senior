from db import db
from app import app
from models import User, Message

with app.app_context():
    db.create_all()

    user = User(email="user@example.org", password="password")
    message = Message(
        content="Hola! Soy Butaca Senior, un recomendador de películas vintage. ¿En qué te puedo ayudar?",
        author="assistant",
        user=user,
    )

    db.session.add(user)
    db.session.add(message)
    db.session.commit()

    print("Usuario y Mensaje creado!")
