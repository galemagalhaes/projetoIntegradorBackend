from datetime import datetime, timedelta
from flask import jsonify
from flasgger import swag_from
from app.swagger_config import swagger_template
from sqlalchemy import extract
from flask_jwt_extended import jwt_required
from app.models import db, Sale, Receita_total_mes, Client

def init_dashboard_routes(app): 
    @app.route("/dashboard", methods=["GET"])
    @jwt_required()
    @swag_from({
        "tags": ["Dashboard"],
        "summary": "Busca os valores do dashboard",
        "security": [{"Bearer": []}],
        "responses": swagger_template["paths"].get("/dashboard", {}).get("get", {}).get("responses", {})
    })
    def dashboard():
        """Busca os valores do dashboard"""

        total_clients = Client.query.count()

        now = datetime.now()
        current_year = now.year
        current_month = now.month

        total_vendas_mes = Sale.query.filter(
            extract('year', Sale.data) == current_year,
            extract('month', Sale.data) == current_month
        ).count()

        receita_mes_atual = Receita_total_mes.query.filter_by(
            ano=current_year, mes=current_month
        ).first()
        receita_mes_atual_valor = receita_mes_atual.receita_total_mes if receita_mes_atual else 0

        total_vendas_pendentes = Sale.query.filter_by(pendente=True).count()

        grafico = []
        for i in range(11, -1, -1):
            mes_ano = now - timedelta(days=i * 30)  
            ano = mes_ano.year
            mes = mes_ano.month

            receita = Receita_total_mes.query.filter_by(ano=ano, mes=mes).first()
            receita_valor = receita.receita_total_mes if receita else 0

            grafico.append({
                "ano": ano,
                "mes": mes,
                "receita": receita_valor
            })

        return jsonify({
            "total_clients": total_clients,
            "total_vendas_mes": total_vendas_mes,
            "receita_mes_atual": receita_mes_atual_valor,
            "total_vendas_pendentes": total_vendas_pendentes,
            "grafico": grafico
        }), 200
