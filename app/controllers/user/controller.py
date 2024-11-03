from flask import request, jsonify
from flasgger import swag_from
from werkzeug.security import generate_password_hash
from app.models import db, User
# from flask_jwt_extended import jwt_required
from app.swagger_config import swagger_template

def init_user_routes(app):
    @app.route("/user", methods=["POST"])
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Cria um novo usuário",
        "parameters": swagger_template["paths"]["/user"]["post"]["parameters"],
        "responses": swagger_template["paths"]["/user"]["post"]["responses"]
    })
    def create_user():
        """Cria um novo usuário"""
        data = request.get_json()
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email já cadastrado"}), 400
        
        hashed_password = generate_password_hash(data["senha"])
        new_user = User(nome=data["nome"], email=data["email"], senha=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    
    @app.route("/user", methods=["GET"])
    # @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Retorna a lista de usuários",
        "responses": swagger_template["paths"]["/user"]["get"]["responses"]
        })
    def get_users():
        """Retorna a lista de usuários"""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    
    @app.route("/user/<string:email>", methods=["GET"])
    # @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Busca um usuário pelo email",
        "parameters": swagger_template["paths"]["/user/{email}"]["get"]["parameters"],
        "responses": swagger_template["paths"]["/user/{email}"]["get"]["responses"]
        })
    def get_users_by_email(email):
        """Busca um usuário pelo email"""
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(user.to_dict()), 200
    
    @app.route("/user/<string:email>", methods=["PUT"])
    # @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Atualiza as informações de um usuário pelo email",
        "parameters": swagger_template["paths"]["/user/{email}"]["put"]["parameters"],
        "responses": swagger_template["paths"]["/user/{email}"]["put"]["responses"]
        })
    def update_user(email):
        """Atualiza as informações de um usuário pelo email"""
        data = request.get_json()
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        if "nome" in data:
            user.nome = data["nome"]

        if "senha" in data:
            user.senha = generate_password_hash(data["senha"])
            
        db.session.commit()
        return jsonify(user.to_dict()), 200
    
    @app.route("/user/<string:email>", methods=["DELETE"])
    # @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Deleta um usuário pelo email",
        "parameters": swagger_template["paths"]["/user/{email}"]["delete"]["parameters"],
        "responses": swagger_template["paths"]["/user/{email}"]["delete"]["responses"]
        })
    def delete_user(email):
        """Deleta um usuário pelo email"""
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado com sucesso"})