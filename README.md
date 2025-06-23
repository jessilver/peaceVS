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
   ```bash
   docker exec -it <nome_ou_id_do_container> psql -U mainuser
   CREATE DATABASE peacvs_db;
   \q
   ```

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

## Como rodar o projeto com Docker

### 1. Build e subida dos containers

Execute na raiz do projeto:

```bash
docker compose build
docker compose up -d
```

Acesse o backend em: http://localhost:8000/web/

### 2. Rodar comandos dentro do container backend

Para acessar o terminal do backend:

```bash
docker exec -it peacetvs-backend-1 bash
```

Ou para rodar um comando Django direto (exemplo: migrate):

```bash
docker exec -it peacetvs-backend-1 python manage.py migrate
```

### 3. Rodar seeders ou coletar estáticos

```bash
docker exec -it peacetvs-backend-1 python manage.py collectstatic --noinput
docker exec -it peacetvs-backend-1 python manage.py seed
```

### 4. Parar os containers

```bash
docker compose down
```

---

Essas instruções garantem que qualquer desenvolvedor consiga rodar, debugar e executar comandos administrativos no backend Django via Docker.

## Observações
- O frontend consome a API do backend via HTTP. Certifique-se de que ambos estejam rodando.
- Ajuste as URLs de API nos arquivos de ambiente do Angular (`src/environments/environment.ts`) conforme necessário.
- Não esqueça de configurar o CORS no Django para permitir requisições do frontend.

npx ionic sync android
npx ionic run android
