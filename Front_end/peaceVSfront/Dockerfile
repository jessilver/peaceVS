# Estágio 1: Build da aplicação
FROM node:20-alpine as build

WORKDIR /app

# Copia os arquivos de dependência e instala
COPY package*.json ./
RUN npm install

# Copia o restante dos arquivos da aplicação
COPY . .

# Build da aplicação para produção
# O output será em /app/www
RUN npm run build


# Estágio 2: Servidor Nginx para servir os arquivos estáticos
FROM nginx:1.25-alpine

# Copia os arquivos buildados do estágio anterior
COPY --from=build /app/www /usr/share/nginx/html

# Copia a configuração customizada do Nginx (se necessário)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
