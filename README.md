# Projeto Integrador 2 - Backend

Esse projeto foi desenvolvido na disciplina de PI2, tem como objetivo prover o backend de uma aplicação web, incluindo a API.

O Projeto foi escrito em [Python](https://www.python.org/), conta com a biblioteca [SQLAlchemy](https://www.sqlalchemy.org/) para auxiliar na construção do modelo de banco de dados [PostgreSQL](https://www.postgresql.org/).

Para auxiliar no desenvolvimento, sem necessitar utilizar o frontend nessa fase, foi utilizada a ferramenta [Swagger](https://swagger.io/), que entrega uma interface gráfica para realizar os testes dos endpoints, além da documentação da API. Além disso, foi feito uso da biblioteca [JWT](https://jwt.io/) para garantir a segurança dos endpoints.

O banco de dados está hospedado na plataforma [Tembo](https://tembo.io/) e a aplicação está hospedada na plataforma [Render](https://render.com/)

> As platformas onde estão hospedados o banco e a aplicação, estão sendo utilizadas no modelo gratuito, por isso, o primeiro carregamento pode demorar até 50 segundos ou mais.

Para inicializar a aplicação localmente é utilizado o comando: 

`python -m app.app`

O arquivo `requirements.txt` podem ser encontradas todas as dependências do projeto. Para a criação deste arquivo foi executado o comando:

`pip freeze > requirements.txt`



