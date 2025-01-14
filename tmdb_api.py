import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def buscar_pelicula(nombre_pelicula):
    """Busca una película en TMDB."""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": nombre_pelicula}
    response = requests.get(url, params=params)
    return response.json()


def obtener_detalle_pelicula(pelicula_id):
    """Obtiene los detalles de una película por ID."""
    url = f"{BASE_URL}/movie/{pelicula_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def donde_ver_pelicula(pelicula_id):
    """Obtiene los detalles de una película por ID."""
    url = f"{BASE_URL}/movie/{pelicula_id}/watch/providers"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def peliculas_por_estrenar():
    """Obtiene las películas por estrenar."""
    url = f"{BASE_URL}/movie/upcoming"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    return response.json()