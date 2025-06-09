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

## Observações
- O frontend consome a API do backend via HTTP. Certifique-se de que ambos estejam rodando.
- Ajuste as URLs de API nos arquivos de ambiente do Angular (`src/environments/environment.ts`) conforme necessário.
- Não esqueça de configurar o CORS no Django para permitir requisições do frontend.

---

Se tiver dúvidas, consulte a documentação de cada framework ou abra uma issue.
