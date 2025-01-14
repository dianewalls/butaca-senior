from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def db_config(app):
    turso_database_url = os.environ.get("TURSO_DATABASE_URL")
    turso_auth_token = os.environ.get("TURSO_AUTH_TOKEN")
    db_url = f"sqlite+{turso_database_url}/?authToken={turso_auth_token}&secure=true"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    db.init_app(app)
