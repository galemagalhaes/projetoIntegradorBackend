from flask import request, jsonify
from flasgger import swag_from
from app.models import db, Client
from flask_jwt_extended import jwt_required
from app.swagger_config import swagger_template
from app.handler.validacoes import validar_email, validar_nome, validar_cpf, validar_telefone

def init_client_routes(app):
    @app.route("/client", methods=["POST"])
    @jwt_required()
    @swag_from({
        "tags": ["Cliente"],
        "summary": "Cria um novo cliente",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/client"]["post"]["parameters"],
        "responses": swagger_template["paths"]["/client"]["post"]["responses"]
    })
    def create_client():
        """Cria um novo cliente"""
        try:
            data = request.get_json()
            
            if not validar_cpf(data["cpf"]):
                return jsonify({"error": "CPF invalido"}), 400
            
            if "nome" not in data or not validar_nome(data["nome"]):
                return jsonify({"error": "O campo 'nome' e obrigatorio e deve conter apenas letras e no mínimo 3 caracteres"}), 400

            if "email" not in data or not validar_email(data["email"]):
                return jsonify({"error": "O campo 'email' e obrigatorio e deve ter um formato valido"}), 400
            
            if not validar_telefone(data["telefone"]):
                return jsonify({"error": "O numero de telefone deve conter entre 10 e 11 digitos numericos."}), 400
            
            if Client.query.filter_by(cpf=data["cpf"]).first():
                return jsonify({"error": "CPF ja cadastrado"}), 400
            
            new_client = Client(
                cpf=data["cpf"], 
                nome=data["nome"], 
                email=data["email"], 
                telefone=data["telefone"]
            )
            
            db.session.add(new_client)
            db.session.commit()
            return jsonify(new_client.to_dict()), 201
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/client", methods=["GET"])
    @jwt_required()
    @swag_from({
        "tags": ["Cliente"],
        "summary": "Retorna a lista de clientes",
        "security": [{"Bearer": []}],
        "responses": swagger_template["paths"]["/client"]["get"]["responses"]
    })
    def get_clients():
        """Retorna a lista de clientes"""
        try:
            clients = Client.query.all()
            return jsonify([client.to_dict() for client in clients]), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/client/<string:cpf>", methods=["GET"])
    @jwt_required()
    @swag_from({
        "tags": ["Cliente"],
        "summary": "Busca um cliente pelo cpf",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/client/{cpf}"]["get"]["parameters"],
        "responses": swagger_template["paths"]["/client/{cpf}"]["get"]["responses"]
    })
    def get_clients_by_cpf(cpf):
        """Busca um cliente pelo cpf"""
        try:
            client = Client.query.filter_by(cpf=cpf).first()
            if not client:
                return jsonify({"error": "Cliente nao encontrado"}), 404
            return jsonify(client.to_dict()), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/client/<string:cpf>", methods=["PUT"])
    @jwt_required()
    @swag_from({
        "tags": ["Cliente"],
        "summary": "Atualiza as informações de um cliente pelo cpf",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/client/{cpf}"]["put"]["parameters"],
        "responses": swagger_template["paths"]["/client/{cpf}"]["put"]["responses"]
    })
    def update_client(cpf):
        """Atualiza as informações de um cliente pelo cpf"""
        try:
            data = request.get_json()
            client = Client.query.filter_by(cpf=cpf).first()

            if not client:
                return jsonify({"error": "Cliente nao encontrado"}), 404
            
            if "nome" in data:
                if not validar_nome(data["nome"]):
                    return jsonify({"error": "O campo 'nome' deve conter apenas letras e no minimo 3 caracteres"}), 400
                client.nome = data["nome"]
            
            if "email" in data:
                if not validar_email(data["email"]):
                    return jsonify({"error": "O campo 'email' deve ter um formato valido"}), 400
                client.email = data["email"]

            if "telefone" in data:
                if not validar_telefone(data["telefone"]):
                    return jsonify({"error": "O numero de telefone deve conter entre 10 e 11 digitos numericos."})
                client.telefone = data["telefone"]

            db.session.commit()
            return jsonify(client.to_dict()), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/client/<string:cpf>", methods=["DELETE"])
    @jwt_required()
    @swag_from({
        "tags": ["Cliente"],
        "summary": "Deleta um cliente pelo cpf",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/client/{cpf}"]["delete"]["parameters"],
        "responses": swagger_template["paths"]["/client/{cpf}"]["delete"]["responses"]
    })
    def delete_client(cpf):
        """Deleta um cliente pelo cpf"""
        try:
            client = Client.query.filter_by(cpf=cpf).first()
            if not client:
                return jsonify({"error": "Cliente nao encontrado"}), 404

            db.session.delete(client)
            db.session.commit()
            return jsonify({"message": "Cliente deletado com sucesso"}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
