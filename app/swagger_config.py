swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Autenticação e Gerenciamento de Usuários",
        "description": "API para autenticação e gerenciamento de usuários.",
        "version": "1.0.0"
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
                            }
                        }
                    }
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
                "parameters": [
                    {"in": "path", "name": "email", "required": True, "type": "string"}
                ],
                "responses": {
                    "200": {"description": "Usuário deletado com sucesso"},
                    "404": {"description": "Usuário não encontrado"}
                }
            }
        }
    }
}
