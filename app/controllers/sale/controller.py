from flask import request, jsonify
from flasgger import swag_from
from datetime import datetime
from app.models import db, Sale, Receita_total_mes
from flask_jwt_extended import jwt_required
from app.swagger_config import swagger_template
from app.handler.validacoes import validar_valor, validar_pendente, validar_data

def init_sale_routes(app):
    @app.route("/sale", methods=["POST"])
    @jwt_required()
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Cria uma nova venda",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/sale"]["post"]["parameters"],
        "responses": swagger_template["paths"]["/sale"]["post"]["responses"]
    })
    
    def create_sale():
        """Cria uma nova venda"""
        try:
            data = request.get_json()

            data_obj = validar_data(data.get("data"))
            if not data_obj:
                return jsonify({"error": "Formato de data inválido. Use o formato YYYY-MM-DD."}), 400

            if not validar_valor(data.get("valor")):
                return jsonify({"error": "O valor deve ser um número positivo."}), 400

            pendente = data.get("pendente", True)
            if not validar_pendente(pendente):
                return jsonify({"error": "O campo 'pendente' deve ser um valor booleano (True ou False).    "}), 400

            ano = data_obj.year
            mes = data_obj.month

            new_sale = Sale(
                cliente_id=data["cliente_id"],
                valor=data["valor"],
                data=data_obj,
                pendente=pendente
            )

            db.session.add(new_sale)

            receita_existente = Receita_total_mes.query.filter_by(ano=ano, mes=mes).first()

            if receita_existente:
                receita_existente.receita_total_mes += data["valor"]
            else:
                nova_receita = Receita_total_mes(
                    ano=ano,
                    mes=mes,
                    receita_total_mes=data["valor"]
                )
                db.session.add(nova_receita)

            db.session.commit()

            return jsonify(new_sale.to_dict()), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/sale", methods=["GET"])
    @jwt_required()
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Retorna a lista de vendas",
        "security": [{"Bearer": []}],
        "responses": swagger_template["paths"]["/sale"]["get"]["responses"]
    })
    
    def get_sales():
        """Retorna a lista de vendas"""
        try:
            sales = Sale.query.all()
            return jsonify([sale.to_dict() for sale in sales]), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/sale/<int:id>", methods=["GET"])
    @jwt_required()
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Busca uma venda pelo id",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/sale/{id}"]["get"]["parameters"],
        "responses": swagger_template["paths"]["/sale/{id}"]["get"]["responses"]
    })
    
    def get_sales_by_id(id):
        """Busca uma venda pelo id"""
        try:
            sale = Sale.query.filter_by(id=id).first()
            if not sale:
                return jsonify({"error": "Venda nao encontrada"}), 404
            return jsonify(sale.to_dict()), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/sale/<int:id>", methods=["PUT"])
    @jwt_required()
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Atualiza as informações de uma venda pelo id",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/sale/{id}"]["put"]["parameters"],
        "responses": swagger_template["paths"]["/sale/{id}"]["put"]["responses"]
    })
    
    def update_sale(id):
        """Atualiza as informações de uma venda pelo id"""
        try:
            data = request.get_json()
            sale = Sale.query.filter_by(id=id).first()

            if not sale:
                return jsonify({"error": "Venda não encontrada"}), 404

            if "data" in data:
                data_obj = validar_data(data["data"])
                if not data_obj:
                    return jsonify({"error": "Formato de data inválido. Use o formato YYYY-MM-DD."}),   400
                sale.data = data_obj

            if "valor" in data:
                if not validar_valor(data["valor"]):
                    return jsonify({"error": "O valor deve ser um número positivo."}), 400
                sale.valor = data["valor"]

            if "pendente" in data:
                if not validar_pendente(data["pendente"]):
                    return jsonify({"error": "O campo 'pendente' deve ser um valor booleano (True ou    False)."}), 400
                sale.pendente = data["pendente"]

            if not any(key in data for key in ["data", "pendente", "valor"]):
                return jsonify({"error": "Nenhum campo para atualização fornecido."}), 400

            db.session.commit()
            return jsonify(sale.to_dict()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/sale/<int:id>", methods=["DELETE"])
    @jwt_required()
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Deleta uma venda pelo id",
        "security": [{"Bearer": []}],
        "parameters": swagger_template["paths"]["/sale/{id}"]["delete"]["parameters"],
        "responses": swagger_template["paths"]["/sale/{id}"]["delete"]["responses"]
    })
    
    def delete_sale(id):
        """Deleta uma venda pelo id"""
        try:
            sale = Sale.query.filter_by(id=id).first()
            if not sale:
                return jsonify({"error": "Venda nao encontrada"}), 404

            db.session.delete(sale)
            db.session.commit()
            return jsonify({"message": "Venda deletada com sucesso"}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
