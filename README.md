# Proyecto ButacaSenior

Aplicación web que cuenta con un chatbot de estilo vintage que recomienda películas clásicas. Pensada para usuarios de 30 a 70 años que disfrutan del cine atemporal, la interfaz es minimalista y enfocada a la información, con una estética sobria y pocas imágenes.

Esta basada en [Flask](https://flask.palletsprojects.com/en/stable/), y para hacer despliegue de la aplicación en [Render](https://render.com/). Como base de datos se ocupa [Turso](https://turso.tech/) y se conecta a  [The Movie Database (TMDB) API](https://developer.themoviedb.org/docs/getting-started) para obtener el IMDB e información de proveedores de streaming.

## Instrucciones de instalación

Una vez descargado el proyecto, crear Virtual environment:

```sh
python3 -m venv venv
```

Activarlo:

```sh
source venv/bin/activate
```

Instalar dependencias:

```sh
pip install -r requirements.txt
```

## Configuración de variables de entorno

Antes de ejecutar el proyecto, es necesario configurar las variables de entorno. Para ello, sigue estos pasos:

1. Copia el archivo `.env.sample` y renómbralo como `.env`:

   ```sh
   cp .env.sample .env
   ```

2. Completa las siguientes variables de entorno con las claves necesarias, registrándote en los servicios correspondientes:

   - **TURSO_DATABASE_URL** y **TURSO_AUTH_TOKEN**: Obtén estas credenciales registrándote en [Turso](https://turso.tech/) y creando una base de datos.
   - **OPENAI_API_KEY**: Regístrate en [OpenAI](https://platform.openai.com/signup/) y genera una clave de API.
   - **TMDB_API_TOKEN** y **TMDB_API_KEY**: Regístrate en [The Movie Database (TMDB)](https://developer.themoviedb.org/docs/getting-started) y crea una cuenta para obtener tus credenciales.

3. Guarda los cambios y asegúrate de que el archivo `.env` no se suba al repositorio (está incluido en `.gitignore`).

4. Inicializa la base de datos ejecutando el siguiente comando:

   ```sh
   python seed.py
   ```

   Esto poblará la base de datos con la información inicial necesaria para el funcionamiento del chatbot.

## Ejecución

Una vez ya lo instalaste, recuerda activar el Virtual Env:

```sh
source venv/bin/activate
```

Y luego ya puedes ejecutar el proyecto localmente con:

```sh
flask run --debug
```

