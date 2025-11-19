# Dockerfile para Planificador Médico
# Multistage build para optimizar el tamaño de la imagen

# Etapa 1: Base con Python
FROM python:3.11-slim as base

# Metadatos
LABEL maintainer="Equipo Planificador Médico"
LABEL version="1.0.0"
LABEL description="Sistema de gestión médica y emergencias"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Etapa 2: Instalación de dependencias
FROM base as dependencies

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt requirements-dev.txt ./

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Etapa 3: Desarrollo (incluye herramientas de desarrollo)
FROM dependencies as development

# Instalar dependencias de desarrollo
RUN pip install -r requirements-dev.txt

# Copiar código fuente
COPY . .

# Cambiar permisos al usuario no-root
RUN chown -R appuser:appuser /app
USER appuser

# Puerto por defecto
EXPOSE 5000

# Comando por defecto para desarrollo
CMD ["python", "backend/app.py"]

# Etapa 4: Producción (optimizada)
FROM dependencies as production

# Copiar solo archivos necesarios
COPY src/ ./src/
COPY config/ ./config/
COPY backend/ ./backend/
COPY requirements.txt ./

# Crear directorio para logs
RUN mkdir -p /app/logs

# Cambiar permisos al usuario no-root
RUN chown -R appuser:appuser /app
USER appuser

# Variables de entorno para producción
ENV ENVIRONMENT=production \
    DEBUG=false \
    LOG_LEVEL=INFO

# Puerto por defecto
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando para producción con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "backend.app:create_app()"]