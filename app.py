from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('landing.html')
    
    email = request.form.get('email')
    
    user = User(email=email)
    
    user_db = db.session.query(user).first()
    print(user_db)
    if user_db:
        return render_template('chat.html', messages=user_db.messages)
    
    message = Message(content="Hola! Soy Butaca Senior, un recomendador de películas vintage. ¿En qué te puedo ayudar?", author="assistant", user=user)

    db.session.add(user)
    db.session.add(message)
    db.session.commit()
    print(email)
    
    return render_template('chat.html', messages=user.messages)



@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user = db.session.query(User).first()
    print(user)

    if request.method == 'GET':
        return render_template('chat.html', messages=user.messages)

    intent = request.form.get('intent')
    profile = request.form.get('profile')
    print(profile)

    intents = {
        'Quiero tener suerte': 'Recomiéndame una película',
        'Terror': 'Recomiéndame una película de terror',
        'Acción': 'Recomiéndame una película de acción',
        'Comedia': 'Recomiéndame una película de comedia',
        'Enviar': request.form.get('message')
    }

    if intent in intents:
        user_message = intents[intent]

        # Guardar nuevo mensaje en la BD
        db.session.add(Message(content=user_message, author="user", user=user))
        db.session.commit()

        messages_for_llm = [{
            "role": "system",
            "content": "Eres un chatbot que recomienda películas, te llamas 'Butaca Senior'. Tu rol es responder recomendaciones de peliculas estrenadas antes de 1990, de manera breve y concisa. No repitas recomendaciones. Tus respuestas deben incluir el rating IMDB asi como el año de estreno.",
        }]

        for message in user.messages:
            messages_for_llm.append({
                "role": message.author,
                "content": message.content,
            })

        chat_completion = client.chat.completions.create(
            messages=messages_for_llm,
            model="gpt-4o",
            temperature=1
        )

        model_recommendation = chat_completion.choices[0].message.content
        db.session.add(Message(content=model_recommendation, author="assistant", user=user))
        db.session.commit()

        return render_template('chat.html', messages=user.messages)


@app.route('/profile')
def user():
    user = db.session.query(User).first()
    print(user)
    return render_template('profile.html', username=user.email)
