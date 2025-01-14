from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message, Prompt
import tmdb_api

load_dotenv()

client = OpenAI()
app = Flask(__name__)
bootstrap = Bootstrap5(app)
db_config(app)


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


@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_id = request.args.get("user_id")
    user = db.session.query(User).filter_by(id=user_id).first()

    if request.method == "GET":
        return render_template("chat.html", messages=user.messages, user_id=user_id)

    intent = request.form.get("intent")

    if intent == "Modificar perfil":
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
                Eres un chatbot llamado 'Butaca Senior' especializado en películas estrenadas antes de 1990. 
                Tu tarea es ofrecer recomendaciones breves y concisas, asegurándote de no repetir ninguna película. 
                Cada recomendación debe incluir el año de estreno y el rating en IMDb.
                
                Extrae la siguiente información del prompt si es que está disponible:
                
                - Nombre de la pelicula a consultar
                - Si la pregunta es específica o no
                - Año de estreno (sólo si está en el prompt)
                - Compañia que la produjo (se puede obtener si no está en el prompt)
                - Si es vintage o no (se puede obtener si no está en el prompt)
                
                Agrega esa info a los datos de prompt del usuario.
                """
        
        if user.genero_favorito:
            content+= f"Ten en cuenta que el género favorito de la persona es {user.genero_favorito}"
        if user.pelicula_favorita:
            content+= f" y su película favorita es {user.pelicula_favorita}"
            
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

        chat_completion = client.beta.chat.completions.parse(
            messages=messages_for_llm,
            model="gpt-4o", 
            temperature=1,
            response_format=Prompt
        )
        
        movie = chat_completion.choices[0].message.parsed.movie
        is_vintage  = chat_completion.choices[0].message.parsed.is_vintage
        is_specific = chat_completion.choices[0].message.parsed.is_specific
        
        if is_specific or not is_vintage:
            movie_info = tmdb_api.buscar_pelicula(movie) if movie else ''
            movie_id = movie_info["results"][0]["id"] if movie_info else ''
            movie_details = tmdb_api.obtener_detalle_pelicula(movie_id) if movie_id else ''
            movie_provider = tmdb_api.donde_ver_pelicula(movie_id) if movie_id else ''
            upcoming = tmdb_api.peliculas_por_estrenar()
        
            content += f"""
                Para responder con mayor precisión, utiliza la siguiente información:
                {movie_info}
                {movie_details}
                {movie_provider}
                {upcoming}
                """
        
        messages_for_llm[0]["content"] = content
        
        model_recommendation = client.chat.completions.create(
            model="gpt-4o",
            messages=messages_for_llm,
            temperature=1.0,
            response_format={"type": "text"},
        ).choices[0].message.content
        
        db.session.add(
            Message(content=model_recommendation, author="assistant", user=user)
        )
        db.session.commit()

        return render_template("chat.html", messages=user.messages, user_id=user.id)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    
    user_id = request.args.get("user_id")
    
    user = db.session.query(User).filter_by(id=user_id).first()
    
    if request.method == "GET":
        return render_template("profile.html", 
                               username=user.email, 
                               pelicula_favorita=user.pelicula_favorita, 
                               genero_favorito=user.genero_favorito)

    
    intent = request.form.get("intent")
    
    if intent == "Volver al chat":
        return redirect(url_for("chat", user_id=user.id))
    # Handle POST request to update profile values
    
    pelicula_favorita = request.form.get("pelicula_favorita")    
    genero_favorito = request.form.get("genero_favorito")
    
    # Update the user's profile with new values if they exist
    if pelicula_favorita:
        user.pelicula_favorita = pelicula_favorita
    if genero_favorito:
        user.genero_favorito = genero_favorito

    # Commit changes to the database
    db.session.commit()

    # After saving, redirect or render the updated profile page
    return render_template("profile.html", 
                           username=user.email, 
                           pelicula_favorita=user.pelicula_favorita, 
                           genero_favorito=user.genero_favorito)
