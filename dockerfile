FROM python:3.12-slim

# Evitar que Python genere archivos .pyc y forzar salida de logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    pkg-config \
    default-libmysqlclient-dev \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copiar el código del proyecto
COPY . /app/

# Exponer el puerto de Gunicorn
EXPOSE 8001

# Ejecutar migraciones y arrancar el servidor WSGI (reemplaza 'mi_proyecto' por el nombre de tu carpeta de settings)
CMD ["sh", "-c", "python manage.py migrate && gunicorn IngresoMateriaPrima.wsgi:application --bind 0.0.0.0:8001"]