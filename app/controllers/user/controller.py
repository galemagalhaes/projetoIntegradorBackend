from flask import request, jsonify
from flasgger import swag_from
from werkzeug.security import generate_password_hash
from app.models import db, User
from flask_jwt_extended import jwt_required
from app.swagger_config import swagger_template
from app.handler.validacoes import validar_email, validar_nome, validar_senha

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
        try:
            data = request.get_json()
            
            if "nome" not in data or not validar_nome(data["nome"]):
                return jsonify({"error": "O campo 'nome' e obrigatorio e deve conter apenas letras e no mínimo 3 caracteres"}), 400

            if "email" not in data or not validar_email(data["email"]):
                return jsonify({"error": "O campo 'email' e obrigatorio e deve ter um formato valido"}), 400

            if "senha" not in data or not validar_senha(data["senha"]):
                return jsonify({"error": "O campo 'senha' e obrigatorio e deve ter entre 6 e 8 caracteres"}), 400

            if User.query.filter_by(email=data["email"]).first():
                return jsonify({"error": "Email ja cadastrado"}), 400

            hashed_password = generate_password_hash(data["senha"])
            new_user = User(nome=data["nome"], email=data["email"], senha=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
        except Exception as e:
            return jsonify({"error": f"Ocorreu um erro ao criar o usuario: {str(e)}"}), 500

    @app.route("/user", methods=["GET"])
    @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Retorna a lista de usuários",
        "security": [{"Bearer": []}],
        "responses": swagger_template["paths"]["/user"]["get"]["responses"]
    })
    def get_users():
        """Retorna a lista de usuários"""
        try:
            users = User.query.all()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify({"error": f"Ocorreu um erro ao buscar os usuarios: {str(e)}"}), 500

    @app.route("/user/<string:email>", methods=["GET"])
    @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Busca um usuário pelo email",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/user/{email}"]["get"]["parameters"],
        "responses": swagger_template["paths"]["/user/{email}"]["get"]["responses"]
    })
    def get_users_by_email(email):
        """Busca um usuário pelo email"""
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({"error": "Usuario nao encontrado"}), 404
            return jsonify(user.to_dict()), 200
        except Exception as e:
            return jsonify({"error": f"Ocorreu um erro ao buscar o usuario: {str(e)}"}), 500

    @app.route("/user/<string:email>", methods=["PUT"])
    @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Atualiza as informações de um usuário pelo email",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/user/{email}"]["put"]["parameters"],
        "responses": swagger_template["paths"]["/user/{email}"]["put"]["responses"]
    })
    def update_user(email):
        """Atualiza as informações de um usuário pelo email"""
        try:
            data = request.get_json()
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({"error": "Usuario nao encontrado"}), 404
            
            if "nome" in data:
                if not data["nome"].strip():
                    return jsonify({"error": "O campo 'nome' nao pode estar vazio"}), 400
                user.nome = data["nome"]

            if "senha" in data:
                if not validar_senha(data["senha"]):
                    return jsonify({"error": "O campo 'senha' e obrigatorio e deve ter entre 6 e 8 caracteres"}), 400
                user.senha = generate_password_hash(data["senha"])
                
            db.session.commit()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            return jsonify({"error": f"Ocorreu um erro ao atualizar o usuario: {str(e)}"}), 500

    @app.route("/user/<string:email>", methods=["DELETE"])
    @jwt_required()
    @swag_from({
        "tags": ["Usuário"],
        "summary": "Deleta um usuário pelo email",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/user/{email}"]["delete"]["parameters"],
        "responses": swagger_template["paths"]["/user/{email}"]["delete"]["responses"]
    })
    def delete_user(email):
        """Deleta um usuário pelo email"""
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({"error": "Usuario nao encontrado"}), 404
            
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Usuario deletado com sucesso"})
        except Exception as e:
            return jsonify({"error": f"Ocorreu um erro ao deletar o usuario: {str(e)}"}), 500
