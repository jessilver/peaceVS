<p align="center">
  <img src="Back_end/web/static/images/Full_Logo.svg" alt="PeacVS Logo" width="320"/>
</p>

# PeacVS - Configuração Inicial

Este projeto é composto por dois módulos principais:
- **Back_end**: API desenvolvida em Django
- **Front_end**: Aplicação mobile/web desenvolvida com Ionic + Angular

## Configuração do Back_end (Django)

1. **Acesse a pasta do backend:**
   ```bash
   cd Back_end
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **(Opcional) Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

A API estará disponível em `http://localhost:8000/`.

---

## Configuração do Front_end (Ionic + Angular)


### Em outro terminal, siga os passos abaixo para configurar o frontend:

1. **Acesse a pasta do frontend:**
   ```bash
   cd Front_end
   ```

2. **Instale as dependências do Node.js:**
   ```bash
   npm install
   ```

3. **Acesse a pasta do frontend:**
   ```bash
   cd peaceVSfront
   ```

4. **Instale as dependências do Node.js:**
   ```bash
   npm install
   ```

   > Rode este comando dentro de cada pasta que possuir um arquivo `package.json` relevante para o seu projeto. Neste caso, o principal é rodar em `Front_end/` e em `Front_end/peaceVSfront/`. Mesmo que exista a pasta `node_modules`, ainda assim é necessário rodar `npm install` para garantir que todas as dependências estejam corretas e atualizadas.

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   npx ionic serve
   ```

A aplicação estará disponível em `http://localhost:8100/`.

---

## Configuração do Banco de Dados (PostgreSQL via Docker)

1. **Certifique-se de ter o Docker instalado em sua máquina.**

2. **Na raiz do projeto, suba o serviço do banco de dados:**
   ```bash
   docker-compose up -d
   ```
   Isso irá criar e iniciar um container PostgreSQL acessível na porta 5432.

3. **Configurações de acesso:**
   - Usuário: `mainuser`
   - Senha: `123456789`
   - Host: `localhost`
   - Porta: `5432`
   - Banco de dados: (crie um nome, por exemplo, `peacvs_db`)

4. **No Django, configure o banco de dados no arquivo `Back_end/project/settings.py`**
   Exemplo:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'peacvs_db',
           'USER': 'mainuser',
           'PASSWORD': '123456789',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Crie o banco de dados no PostgreSQL (se necessário):**
   Você pode acessar o container e criar o banco manualmente:
   ```bash
   docker exec -it <nome_ou_id_do_container> psql -U mainuser
   CREATE DATABASE peacvs_db;
   \q
   ```
   Ou use uma ferramenta gráfica como DBeaver ou pgAdmin.

6. **Siga os passos normais do Django para aplicar as migrações:**
   ```bash
   python manage.py migrate
   ```

---

## Configuração do .env

1. Copie o arquivo `Back_end/.env-example` para `Back_end/.env`:
   ```bash
   cp Back_end/.env-example Back_end/.env
   ```
2. Edite o arquivo `.env` com as variáveis do seu ambiente (banco de dados, secret key, CORS, etc).
3. Nunca versionar o `.env` no git. Use sempre o `.env-example` como modelo para novos ambientes.

---

## Observações
- O frontend consome a API do backend via HTTP. Certifique-se de que ambos estejam rodando.
- Ajuste as URLs de API nos arquivos de ambiente do Angular (`src/environments/environment.ts`) conforme necessário.
- Não esqueça de configurar o CORS no Django para permitir requisições do frontend.

---

Se tiver dúvidas, consulte a documentação de cada framework ou abra uma issue.
