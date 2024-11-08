from flask import request, jsonify
from flasgger import swag_from
from datetime import datetime
from app.models import db, Sale, Receita_total_mes
from app.swagger_config import swagger_template

def init_sale_routes(app):
    @app.route("/sale", methods=["POST"])
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Cria uma nova venda",
        "parameters": swagger_template["paths"]["/sale"]["post"]["parameters"],
        "responses": swagger_template["paths"]["/sale"]["post"]["responses"]
    })
    def create_sale():
        """Cria uma nova venda"""
        data = request.get_json()

    # Converte a string de data para objeto datetime.date
        data_obj = datetime.strptime(data["data"], "%Y-%m-%d").date()
        ano = data_obj.year
        mes = data_obj.month

        # Cria a nova venda
        new_sale = Sale(
            cliente_id=data["cliente_id"],
            valor=data["valor"],
            data=data_obj,
            pendente=data.get("pendente", True)
        )

        # Adiciona a venda ao banco
        db.session.add(new_sale)

        # Verifica se já existe um registro para o ano e mês na tabela receita_total
        receita_existente = Receita_total_mes.query.filter_by(ano=ano, mes=mes).first()

        if receita_existente:
            # Se existir, soma o valor da venda ao valor existente
            receita_existente.receita_total_mes += data["valor"]
        else:
            # Se não existir, cria uma nova entrada para o ano e mês com o valor da venda
            nova_receita = Receita_total_mes(
                ano=ano,
                mes=mes,
                receita_total_mes=data["valor"]
            )
            db.session.add(nova_receita)

        # Salva as mudanças no banco de dados
        db.session.commit()

        return jsonify(new_sale.to_dict()), 201

    @app.route("/sale", methods=["GET"])
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Retorna a lista de vendas",
        "responses": swagger_template["paths"]["/sale"]["get"]["responses"]
    })
    def get_sales():
        """Retorna a lista de vendas"""
        sales = Sale.query.all()
        return jsonify([sale.to_dict() for sale in sales]), 200

    @app.route("/sale/<int:id>", methods=["GET"])
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Busca uma venda pelo id",
        "parameters": swagger_template["paths"]["/sale/{id}"]["get"]["parameters"],
        "responses": swagger_template["paths"]["/sale/{id}"]["get"]["responses"]
    })
    def get_sales_by_id(id):
        """Busca uma venda pelo id"""
        sale = Sale.query.filter_by(id=id).first()
        if not sale:
            return jsonify({"error": "Venda não encontrada"}), 404
        return jsonify(sale.to_dict()), 200

    @app.route("/sale/<int:id>", methods=["PUT"])
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Atualiza as informações de uma venda pelo id",
        "parameters": swagger_template["paths"]["/sale/{id}"]["put"]["parameters"],
        "responses": swagger_template["paths"]["/sale/{id}"]["put"]["responses"]
    })
    def update_sale(id):
        """Atualiza as informações de uma venda pelo id"""
        data = request.get_json()
        sale = Sale.query.filter_by(id=id).first()
        if not sale:
            return jsonify({"error": "Venda não encontrada"}), 404
        
        if "data" in data:
            sale.data = datetime.strptime(data["data"], "%Y-%m-%d").date()
        
        if "pendente" in data:
            sale.pendente = data["pendente"]

        if "valor" in data:
            sale.valor = data["valor"]
            
        db.session.commit()
        return jsonify(sale.to_dict()), 200

    @app.route("/sale/<int:id>", methods=["DELETE"])
    @swag_from({
        "tags": ["Vendas"],
        "summary": "Deleta uma venda pelo id",
        "parameters": swagger_template["paths"]["/sale/{id}"]["delete"]["parameters"],
        "responses": swagger_template["paths"]["/sale/{id}"]["delete"]["responses"]
    })
    def delete_sale(id):
        """Deleta uma venda pelo id"""
        sale = Sale.query.filter_by(id=id).first()
        if not sale:
            return jsonify({"error": "Venda não encontrada"}), 404
        
        db.session.delete(sale)
        db.session.commit()
        return jsonify({"message": "Venda deletada com sucesso"})
