swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Autenticação, Gerenciamento de Usuários, Clientes e Vendas",
        "description": "API para autenticação, gerenciamento de usuários, clientes e vendas.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
    "Bearer": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "Insira o token JWT com o prefixo 'Bearer '"
        }
    },
    "paths": {
        "/login": {
            "post": {
                "summary": "Autentica um usuário e gera um token JWT",
                "tags": ["Autenticação"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Credenciais do usuário para autenticação",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["email", "senha"],
                            "properties": {
                                "email": {"type": "string", "description": "E-mail do usuário"},
                                "senha": {"type": "string", "description": "Senha do usuário"}
                                },
                            },
                        },
                ],
                "responses": {
                    "200": {
                        "description": "Token gerado com sucesso",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "access_token": {"type": "string", "description": "Token JWT"}
                            }
                        }
                    },
                    "401": {"description": "E-mail ou senha incorretos"}
                }
            }
        },
        "/user": {
            "post": {
                "summary": "Cria um novo usuário",
                "tags": ["Usuário"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Dados do novo usuário",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["nome", "email", "senha"],
                            "properties": {
                                "nome": {"type": "string", "description": "Nome do usuário"},
                                "email": {"type": "string", "description": "E-mail do usuário"},
                                "senha": {"type": "string", "description": "Senha do usuário"}
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Usuário criado com sucesso"},
                    "400": {"description": "Erro: Email já cadastrado"}
                }
            },
            "get": {
                "summary": "Retorna a lista de usuários",
                "tags": ["Usuário"],
                "security": [
                {
                    "Bearer": []
                }
            ],
                "responses": {
                    "200": {
                        "description": "Lista de usuários",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "nome": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "/user/{email}": {
            "get": {
                "summary": "Busca um usuário pelo email",
                "tags": ["Usuário"],
                "security": [
                {
                    "Bearer": []
                }
            ],
                "parameters": [
                    {"in": "path", "name": "email", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "Usuário encontrado"},
                    "404": {"description": "Usuário não encontrado"}
                }
            },
            "put": {
                "summary": "Atualiza as informações de um usuário pelo email",
                "tags": ["Usuário"],
                "security": [
                {
                    "Bearer": []
                }
            ],                
                "parameters": [
                    {"in": "path", "name": "email", "required": True, "type": "string"},
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Dados atualizados do usuário",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nome": {"type": "string"},
                                "senha": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Usuário atualizado com sucesso"},
                    "404": {"description": "Usuário não encontrado"}
                }
            },
            "delete": {
                "summary": "Deleta um usuário pelo email",
                "tags": ["Usuário"],
                "security": [
                {
                    "Bearer": []
                }
            ],                
                "parameters": [
                    {"in": "path", "name": "email", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "Usuário deletado com sucesso"},
                    "404": {"description": "Usuário não encontrado"}
                }
            }
        },
        "/client": {
            "post": {
                "summary": "Cria um novo cliente",
                "tags": ["Cliente"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Dados do novo cliente",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["cpf", "nome", "email", "telefone"],
                            "properties": {
                                "cpf": {"type": "string", "description": "CPF do cliente"},
                                "nome": {"type": "string", "description": "Nome do cliente"},
                                "email": {"type": "string", "description": "E-mail do cliente"},
                                "telefone": {"type": "string", "description": "Telefone do cliente"}
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Cliente criado com sucesso"},
                    "400": {"description": "Erro: CPF já cadastrado"}
                }
            },
            "get": {
                "summary": "Retorna a lista de clientes",
                "tags": ["Cliente"],
                "responses": {
                    "200": {
                        "description": "Lista de clientes",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "cpf": {"type": "string"},
                                    "nome": {"type": "string"},
                                    "email": {"type": "string"},
                                    "telefone": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "/client/{cpf}": {
            "get": {
                "summary": "Busca um cliente pelo CPF",
                "tags": ["Cliente"],
                "parameters": [
                    {"in": "path", "name": "cpf", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "Cliente encontrado"},
                    "404": {"description": "Cliente não encontrado"}
                }
            },
            "put": {
                "summary": "Atualiza as informações de um cliente pelo CPF",
                "tags": ["Cliente"],
                "parameters": [
                    {"in": "path", "name": "cpf", "required": True, "type": "string"},
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Dados atualizados do cliente",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nome": {"type": "string"},
                                "email": {"type": "string"},
                                "telefone": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Cliente atualizado com sucesso"},
                    "404": {"description": "Cliente não encontrado"}
                }
            },
            "delete": {
                "summary": "Deleta um cliente pelo CPF",
                "tags": ["Cliente"],
                "parameters": [
                    {"in": "path", "name": "cpf", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "Cliente deletado com sucesso"},
                    "404": {"description": "Cliente não encontrado"}
                }
            }
        },
        "/sale": {
            "post": {
                "summary": "Cria uma nova venda",
                "tags": ["Vendas"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Dados da venda",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["data", "cliente_id", "valor", "pendente"],
                            "properties": {
                                "data": {"type": "string", "description": "Data da venda"},
                                "cliente_id": {"type": "number", "description": "ID do cliente"},
                                "valor": {"type": "number", "description": "Valor da venda"},
                                "pendente": {"type": "boolean", "description": "Status da venda"}
                            }
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Venda criada com sucesso"},
                    "400": {"description": "Erro: ID de venda já cadastrado"}
                }
            },
            "get": {
                "summary": "Retorna a lista de vendas",
                "tags": ["Vendas"],
                "responses": {
                    "200": {
                        "description": "Lista de vendas",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "data": {"type": "string"},
                                    "cliente": {"type": "string"},
                                    "valor": {"type": "number"},
                                    "pendente": {"type": "boolean"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "/sale/{id}": {
            "get": {
                "summary": "Busca uma venda pelo ID",
                "tags": ["Vendas"],
                "parameters": [
                    {"in": "path", "name": "id", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "Venda encontrada"},
                    "404": {"description": "Venda não encontrada"}
                }
            },
            "put": {
                "summary": "Atualiza as informações de uma venda pelo ID",
                "tags": ["Vendas"],
                "parameters": [
                    {"in": "path", "name": "id", "required": True, "type": "string"},
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Dados atualizados da venda",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "data": {"type": "string", "description": "Data da venda"},
                                "pendente": {"type": "boolean", "description": "Status da venda"},
                                "valor": {"type": "number", "description": "Valor da venda"}
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Venda atualizada com sucesso"},
                    "404": {"description": "Venda não encontrada"}
                }
            },
            "delete": {
                "summary": "Deleta uma venda pelo ID",
                "tags": ["Vendas"],
                "parameters": [
                    {"in": "path", "name": "id", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "Venda deletada com sucesso"},
                    "404": {"description": "Venda não encontrada"}
                }
            }
        },
        "/dashboard": {
            "get": {
                "summary": "Busca os valores do dashboard",
                "tags": ["Dashboard"],
                "responses": {
                    "200": {
                        "description": "Dados do dashboard recuperados com sucesso",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "total_clients": {"type": "integer", "description": "Total de clientes cadastrados"},
                                "total_vendas_mes": {"type": "integer", "description": "Total de vendas no mês atual"},
                                "receita_mes_atual": {"type": "number", "format": "float", "description": "Receita total do mês atual"},
                                "total_vendas_pendentes": {"type": "integer", "description": "Total de vendas pendentes"},
                                "grafico": {
                                    "type": "array",
                                    "description": "Dados de receita dos últimos 12 meses",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "ano": {"type": "integer", "description": "Ano"},
                                            "mes": {"type": "integer", "description": "Mês"},
                                            "receita": {"type": "number", "format": "float", "description": "Receita do mês"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Erro ao recuperar os dados do dashboard"}
                }
            }
        }
    }
}
