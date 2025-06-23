#!/bin/sh

# Aplica as migrações do banco de dados
echo "Applying database migrations..."
python manage.py migrate

# Coleta os arquivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Inicia o servidor Gunicorn
echo "Starting Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000 --reload
