from flask import Flask
from flasgger import Swagger
from .models import db, DATABASE_URI, TRACK_MODIFICATIONS
from .controllers import init_login_routes, init_user_routes, init_client_routes, init_sale_routes
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = TRACK_MODIFICATIONS

    app.config["JWT_SECRET_KEY"] = "smsDsadkm23547dssfrgt@" #altere para sua chave secreta
    jwt = JWTManager(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    swagger = Swagger(app)

    init_login_routes(app)
    init_user_routes(app)
    init_client_routes(app)
    init_sale_routes(app)

    @app.route("/")
    def home():
        return "head", 200
    return app