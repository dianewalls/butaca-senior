import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_bcrypt import Bcrypt

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


bcrypt = Bcrypt(app)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        favorite_movie = request.form.get("favorite_movie") or ''
        favorite_genre = request.form.get("favorite_genre") or ''
        
        if password != confirm_password:
            return render_template("register.html", error="Las contraseñas no coinciden.")
        
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template("register.html", error="El correo electrónico ya está registrado.")
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            email=email, 
            password=hashed_password, 
            pelicula_favorita=favorite_movie, 
            genero_favorito=favorite_genre
        )
        
        db.session.add(new_user)
        db.session.commit()
        flash("Muy bien! ya tienes tu usuario y contraseña. Por favor, inicia sesión con tus credenciales para ingresar.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        logout_user()
        
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return render_template("login.html", error="El correo electrónico no está registrado.")
        
        if not bcrypt.check_password_hash(user.password, password):
            return render_template("login.html", error="Contraseña incorrecta.")
        
        login_user(user)
        return redirect(url_for("chat", user_id=user.id))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("landing.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("landing.html")

    email = request.form.get("email")

    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        user = User(email=email)
        message = Message(
            content="Hola! Soy Butaca Senior, un recomendador de películas vintage. ¿En qué te puedo ayudar?",
            author="assistant",
            user=user,
        )
        db.session.add(user)
        db.session.add(message)
        db.session.commit()

    return redirect(url_for("chat", user_id=user.id))


@app.route('/password', methods=['POST'])
@login_required
def password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not bcrypt.check_password_hash(current_user.password, current_password):
            return render_template('password.html', error='La contraseña actual es incorrecta.')

        if new_password != confirm_new_password:
            return render_template('password.html', error='Las contraseñas no coinciden.')

        hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        current_user.password = hashed_new_password
        db.session.commit()
        flash('Tu contraseña ha sido actualizada exitosamente. Haz login nuevamente.')
        return redirect(url_for('login'))
    
    return redirect(url_for('password'))


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    
    if current_user.is_authenticated:
        user = current_user
    else:
        return render_template("error.html", error_message="No tienes permiso para ver este chat.")

    user_id = user.id

    if request.method == "GET":
        return render_template("chat.html", messages=user.messages, user_id=user_id, username=user.email)

    intent = request.form.get("intent")

    if intent==user.email:
        return redirect(url_for("profile", user_id=user_id))

    intents = {
        "Quiero tener suerte": "Recomiéndame una película",
        "Terror": "Recomiéndame una película de terror",
        "Acción": "Recomiéndame una película de acción",
        "Comedia": "Recomiéndame una película de comedia",
        "Enviar": request.form.get("message"),
    }

    if intent in intents:
        user_message = intents[intent]

        # Guardar nuevo mensaje en la BD
        db.session.add(Message(content=user_message, author="user", user=user))
        db.session.commit()

        content = """
                Eres un chatbot llamado 'Butaca Senior' especializado en recomendar películas estrenadas antes de 1990. 
                Tu tarea es ofrecer recomendaciones breves y concisas, asegurándote de no repetir ninguna película. 
                Cada recomendación debe incluir el año de estreno y el rating en IMDb.
                """
        
        if user.genero_favorito:
            content+= f"Ten en cuenta que el género favorito de la persona es {user.genero_favorito}"
        if user.pelicula_favorita:
            content+= f" y su película favorita es {user.pelicula_favorita}"
            
        print(content)
            
        messages_for_llm = [
            {
                "role": "system",
                "content": content,
            }
        ]

        for message in user.messages:
            messages_for_llm.append(
                {
                    "role": message.author,
                    "content": message.content,
                }
            )

        chat_completion = client.chat.completions.create(
            messages=messages_for_llm, model="gpt-4o", temperature=1
        )

        model_recommendation = chat_completion.choices[0].message.content
        db.session.add(
            Message(content=model_recommendation, author="assistant", user=user)
        )
        db.session.commit()

        return render_template("chat.html", messages=user.messages, user_id=user.id, username=user.email)


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    if current_user.is_authenticated:
        user = current_user
    else:
        return redirect(url_for("landing"))

    return render_template("profile.html", 
                           username=user.email, 
                           pelicula_favorita=user.pelicula_favorita, 
                           genero_favorito=user.genero_favorito)


@app.route("/preferences", methods=["GET","POST"])
@login_required
def preferences():
    
    if current_user.is_authenticated:
        user = current_user
    else:
        return redirect(url_for("landing"))
    
    if request.method == "GET":
        return render_template("preferences.html",
                               username=user.email, 
                               pelicula_favorita=user.pelicula_favorita, 
                               genero_favorito=user.genero_favorito)

    pelicula_favorita = request.form.get("pelicula_favorita")    
    genero_favorito = request.form.get("genero_favorito")
    
    if pelicula_favorita:
        user.pelicula_favorita = pelicula_favorita
    if genero_favorito:
        user.genero_favorito = genero_favorito

    db.session.commit()

    flash("Tus preferencias han sido actualizadas exitosamente.")
    return render_template("profile.html", 
                           username=user.email, 
                           pelicula_favorita=user.pelicula_favorita, 
                           genero_favorito=user.genero_favorito)