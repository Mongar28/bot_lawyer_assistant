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
    # Create directories with proper ownership from the start
    mkdir -p /app/config /app/credentials && \
    touch /app/config/verification_codes.yaml && \
    # Set ownership in a single layer
    chown -R appuser:appuser /app && \
    # Set directory permissions
    find /app -type d -exec chmod 755 {} \; && \
    # Set specific permissions for config and credentials directories
    chmod 777 /app/config && \
    chmod 777 /app/credentials && \
    chmod 666 /app/config/verification_codes.yaml && \
    # Verify permissions were set correctly
    ls -la /app/config /app/credentials

# Copiar el resto del código
COPY --chown=appuser:appuser . .

USER appuser

# Asegurar permisos después de copiar y verificar
RUN find /app -type d -exec chmod 755 {} \; && \
    chmod 777 /app/config && \
    chmod 777 /app/credentials && \
    chmod 666 /app/config/verification_codes.yaml && \
    # Verify final permissions
    ls -la /app/config /app/credentials

# Exponer el puerto que usa Streamlit
EXPOSE 8501

# Configurar healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para ejecutar la aplicación con permisos forzados
CMD ["sh", "-c", "chmod 777 /app/config && chmod 666 /app/config/verification_codes.yaml && streamlit run app.py --server.address 0.0.0.0"]