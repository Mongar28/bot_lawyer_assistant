# Usar Ubuntu 22.04 LTS como base
FROM ubuntu:22.04

# Evitar interacciones durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Establecer variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    PATH="/usr/local/python/3.10/bin:$PATH"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema y Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv \
    python3-pip \
    python3-dev \
    build-essential \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear enlaces simbólicos para Python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Verificar versiones
RUN python --version && pip --version

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Crear usuario no root y directorios necesarios
ARG USER_ID=1000
RUN useradd -u ${USER_ID} -m -s /bin/bash appuser && \
    mkdir -p /app/config && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 775 /app/config

# Copiar el resto del código
COPY --chown=appuser:appuser . .

USER appuser

# Exponer el puerto que usa Streamlit
EXPOSE 8501

# Configurar healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]