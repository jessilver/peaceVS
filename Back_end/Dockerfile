# Dockerfile para backend Django
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# Copia o script de entrypoint e o torna executável
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Define o entrypoint que será executado quando o container iniciar
ENTRYPOINT ["/app/entrypoint.sh"]
