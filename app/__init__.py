from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv
import os


db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


    db.init_app(app)
    migrate.init_app(app, db)

    # IMPORT INSIDE FUNCTION (IMPORTANT FIX)
    from app.api.profiles import profiles_bp
    from app.models.profile import BusinessProfile

    app.register_blueprint(profiles_bp)

    @app.route("/")
    def home():
        return "API is working"

    return app