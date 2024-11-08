from flask import request, jsonify
from flasgger import swag_from
from app.models import db, Client
from flask_jwt_extended import jwt_required
from app.swagger_config import swagger_template

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
        data = request.get_json()
        if Client.query.filter_by(cpf=data["cpf"]).first():
            return jsonify({"error": "CPF já cadastrado"}), 400
        
        new_client = Client(cpf=data["cpf"], nome=data["nome"], email=data["email"], telefone=data["telefone"])
        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.to_dict()), 201
    
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
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients]), 200
    
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
        client = Client.query.filter_by(cpf=cpf).first()
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        return jsonify(client.to_dict()), 200
    
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
        data = request.get_json()
        client = Client.query.filter_by(cpf=cpf).first()
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        if "email" in data:
            client.email = data["email"]

        if "nome" in data:
            client.nome = data["nome"]

        if "telefone" in data:
            client.telefone = data["telefone"]
            
        db.session.commit()
        return jsonify(client.to_dict()), 200
    
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
        client = Client.query.filter_by(cpf=cpf).first()
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Cliente deletado com sucesso"})