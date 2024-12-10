# Proyecto Base

Este es el proyecto base para el **Taller de desarrollo de una aplicación con IA generativa** del [Diplomado en Inteligencia Artificial Generativa](https://educacioncontinua.uc.cl/programas/diplomado-en-inteligencia-artificial-generativa/) de la PUC.

Tiene lo necesario para comenzar a programar una aplicación web con [Flask](https://flask.palletsprojects.com/en/stable/), y para hacer despliegue de la aplicación en [Render](https://render.com/).

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

## Ejecución

Una vez ya lo instalaste, recuerda activar el Virtual Env:


```sh
source venv/bin/activate
```

Y luego ya puedes ejecutar el proyecto localmente con

```sh
flask run --debug
```

## Agregar a tu propio GitHub

Si descargaste el proyecto con `git clone`, para agregarlo a tu propio repositorio tienes que hacer lo siguiente:

1. [Crear un nuevo repositorio](https://github.com/new) (en blanco).
2. Cambiar la URL del `origin` por la de tu nuevo repositorio: `git remote set-url origin git@github.com:tu-username/tu-nombre-de-repo.git`
3. Listo, ahora puedes subir el código base a tu propio repositorio con `git push -u origin main`
