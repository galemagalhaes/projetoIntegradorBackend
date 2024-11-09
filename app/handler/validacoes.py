import re
from datetime import datetime

def validar_nome(nome):
        return bool(re.match(r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]{3,}$", nome.strip()))
    
def validar_email(email):
        return re.match(r"^(?!.*\.\.)[a-zA-Z0-9]+(?:[._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$", email)
    
def validar_telefone(telefone):
    return re.match(r'^\d{11}$', telefone)

def validar_cpf(cpf: str) -> bool:
    """Valida o CPF fornecido"""
    
    # Remove caracteres não numericos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se o CPF tem 11 digitos
    if len(cpf) != 11:
        return False
    
    # Verifica se o CPF não é uma sequência de numeros iguais
    if cpf == cpf[0] * len(cpf):
        return False
    
    # Validação dos dois digitos verificadores
    def calcular_digito(cpf, peso):
        soma = sum(int(cpf[i]) * peso[i] for i in range(len(peso)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Calcula o primeiro digito verificador
    peso_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    digito_1 = calcular_digito(cpf[:9], peso_1)
    
    # Calcula o segundo digito verificador
    peso_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    digito_2 = calcular_digito(cpf[:10], peso_2)
    
    # Compara os digitos calculados com os digitos informados
    return cpf[-2:] == f'{digito_1}{digito_2}'

def validar_senha(senha):
        return 6 <= len(senha) <= 8
    

def validar_data(data_str):
    """Valida se a data está no formato correto YYYY-MM-DD."""
    try:
        return datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def validar_valor(valor):
    """Verifica se o valor é um número positivo."""
    if isinstance(valor, (int, float)) and valor > 0:
        return True
    return False

def validar_pendente(pendente):
    """Verifica se o campo 'pendente' é um valor booleano."""
    return isinstance(pendente, bool)
