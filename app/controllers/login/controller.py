from flask import request, jsonify
from flasgger import swag_from
from app.swagger_config import swagger_template
from werkzeug.security import check_password_hash
from app.models import User
import jwt
import datetime

def init_login_routes(app):
    @app.route("/login", methods=["POST"])
    @swag_from({
        "tags": ["Autenticação"],
        "summary": "Autentica um usuário e gera um token JWT",
        "parameters": swagger_template["paths"].get("/login", {}).get("post", {}).get("parameters", []),
        "responses": swagger_template["paths"].get("/login", {}).get("post", {}).get("responses", {})
    })

    def login():
        """Autentica um usuário e gera um token JWT"""
        data = request.get_json()
        user = User.query.filter_by(email=data.get("email")).first()

        if user and check_password_hash(user.senha, data.get("senha")):
            token = jwt.encode({
                "sub": user.id, 
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
                }, str(app.config["JWT_SECRET_KEY"]), algorithm="HS256")
            return jsonify(access_token=token), 200
        
        return jsonify({"msg": "Email ou senha incorretos"}), 401