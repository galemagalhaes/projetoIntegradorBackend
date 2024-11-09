from flask import Flask
from flasgger import Swagger
from .models import db, TRACK_MODIFICATIONS
from .controllers import init_login_routes, init_user_routes, init_client_routes, init_sale_routes, init_dashboard_routes
from flask_jwt_extended import JWTManager
from .swagger_config import swagger_template
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Permite CORS para todas as origens
    CORS(app)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = TRACK_MODIFICATIONS

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    Swagger(app, template=swagger_template)

    init_login_routes(app)
    init_user_routes(app)
    init_client_routes(app)
    init_sale_routes(app)
    init_dashboard_routes(app)

    @app.route("/")
    def home():
        return "head", 200
    return app