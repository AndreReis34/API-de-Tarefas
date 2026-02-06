# API para Controle de Tarefas (To-Do)

Esta API foi desenvolvida com o objetivo de treinar o desenvolvimento de APIs REST,
incluindo autenticação com JWT, CRUD de tarefas, filtros e paginação.

Também foi desenvolvido um Front-End para consumir esta API:

👉 [Gerenciador de Tarefas – Front-End](https://github.com/AndreReis34/Gerente-de-Tarefas-Front-End)
---

## Tecnologias utilizadas
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Flask JWT Extended
- SQLite (padrão)
- Gunicorn

---

## Como rodar o projeto

### 1️⃣ Clonar o repositório
```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>
```
----------

### 2️⃣ Criar e ativar ambiente virtual (Linux)

```bash
python -m venv .venv
source .venv/bin/activate
```
----------

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

----------

### 4️⃣ Configurações importantes

Se for rodar localmente com Front-End separado, configure o CORS no arquivo `app.py`.

Para mais detalhes, consulte a documentação:  
👉 [https://pypi.org/project/flask-cors/](https://pypi.org/project/flask-cors/)


----------

### 5️⃣ Criar o banco de dados (migrations)

```bash
flask --app app db init
flask --app app db migrate -m "init"
flask --app app db upgrade
```

----------

### 6️⃣ Rodar a aplicação

#### Ambiente local (desenvolvimento)

```bash
flask --app  run
```

#### Ambiente de produção

```bash
gunicorn wsgi:app
```

_______
## Rotas da API

### Autenticação

-   `POST /auth/register`  
    Registra um novo usuário.
    
-   `POST /auth/login`  
    Realiza login e retorna um token JWT.
    

----------

### Tarefas (JWT obrigatório)

-   `GET /tasks`  
    Lista as tarefas do usuário autenticado.  
    **Parâmetros opcionais:**  
    `status`, `q`, `sort`, `order`, `page`, `per_page`
    
-   `POST /tasks`  
    Cria uma nova tarefa.
    
-   `PUT /tasks/:id`  
    Atualiza os dados da tarefa.
    
-   `PUT /tasks/:id/toggle`  
    Alterna o status da tarefa (`pendente` ↔ `concluída`).
    
-   `DELETE /tasks/:id`  
    Remove a tarefa.
    

----------
