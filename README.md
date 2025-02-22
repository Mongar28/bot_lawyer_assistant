# Temis - Asistente Legal Virtual 👩‍⚖️

Temis es un asistente virtual inteligente diseñado para gestionar citas y consultas con el Dr. Saul. Utilizando tecnología de punta en procesamiento de lenguaje natural, ofrece una interfaz conversacional profesional y segura para la programación y consulta de citas legales, brindando una experiencia personalizada y eficiente. Si bien este asistente cumple con un proposito particular, puede configurar para adapatarse a otro tipo de consultas o citas.

## 🎯 Objetivos del Proyecto

- Automatizar y optimizar la gestión de citas legales
- Proporcionar atención 24/7 a consultas básicas
- Reducir tiempos de espera y mejorar la experiencia del cliente
- Mantener un registro organizado de las consultas y citas

## 🌟 Características Principales

- **Gestión Inteligente de Citas:**
  - Verificación automática por correo electrónico
  - Integración con Google Calendar
  - Recordatorios automáticos
  - Gestión de conflictos de horarios

- **Interfaz Conversacional Avanzada:**
  - Procesamiento de lenguaje natural mediante LangChain y LangGraph
  - Respuestas contextuales y empáticas
  - Soporte multimodelo (GPT-4, DeepSeek)
  - Interfaz web intuitiva con Streamlit

- **Sistema de Seguridad Robusto:**
  - Validación de correos electrónicos
  - Protección contra inyecciones de prompts
  - Manejo seguro de datos sensibles
  - Sistema de logs y auditoría
  - Gestión automática de permisos y archivos

## 🛠️ Stack Tecnológico

### Backend
- Python 3.8+
- LangChain 0.3.18
- LangGraph 0.2.70
- Google Calendar API

### Frontend
- Streamlit 1.42.0

### Modelos de IA
- OpenAI GPT-4
- DeepSeek

### Integraciones
- Google Calendar
- Sistema de correo electrónico
- Almacenamiento seguro de credenciales

## 📋 Requisitos del Sistema

- Python 3.8 o superior
- Cuenta de Google Cloud Platform con Calendar API habilitada
- API Key de OpenAI o DeepSeek
- Mínimo 4GB de RAM
- Conexión a internet estable
- Docker y Docker Compose (para despliegue containerizado)

## 🚀 Guía de Instalación

### Despliegue con Docker (Recomendado) 🐳

La forma más sencilla y segura de ejecutar la aplicación es usando Docker:

1. **Preparación inicial:**
```bash
# Clonar el repositorio
git clone https://github.com/Mongar28/bot_lawyer_assistant.git
cd bot_lawyer_assistant

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

2. **Gestión con Rake:**
```bash
# Verificar y corregir permisos
rake app:fix_permissions

# Construir y iniciar la aplicación
rake app:reset

# Verificar estado de permisos
rake monitor:permissions

# Ver logs de la aplicación
rake app:logs
```

#### Comandos Rake Disponibles

- **Gestión de Aplicación:**
  - `rake app:build` - Construir imagen Docker
  - `rake app:start` - Iniciar aplicación
  - `rake app:stop` - Detener aplicación
  - `rake app:logs` - Ver logs
  - `rake app:clean` - Limpiar caché
  - `rake app:status` - Ver estado
  - `rake app:shell` - Acceder al shell
  - `rake app:reset` - Reinicio completo (incluyendo volúmenes)
  - `rake app:fix_permissions` - Corregir permisos

- **Monitoreo:**
  - `rake monitor:resources` - Ver uso de CPU/memoria
  - `rake monitor:errors` - Ver logs de errores
  - `rake monitor:permissions` - Verificar permisos de archivos

### Instalación Manual (Alternativa)

Si prefieres una instalación manual:

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 🏗️ Arquitectura del Proyecto

```
bot_lawyer_assistant/
├── app.py                    # Aplicación principal
├── config/                   # Configuraciones
│   └── prompts.yaml         # Plantillas de prompts
│   └── verification_codes.yaml  # Códigos de verificación
├── langgraph_components/    # Componentes del grafo
│   ├── graph.py            # Lógica del grafo
│   ├── graph_tools.py      # Herramientas del grafo
│   ├── llm.py             # Configuración de modelos
│   └── states.py          # Estados del sistema
├── credentials/            # Credenciales (gitignored)
│   ├── credentials.json   # Credenciales de Google
│   └── token.pickle      # Token de autenticación
├── docker-compose.yml     # Configuración de Docker Compose
├── Dockerfile            # Configuración del contenedor
├── Rakefile             # Tareas de automatización
└── requirements.txt     # Dependencias
```

## 🔒 Seguridad y Privacidad

- Validación robusta de entradas
- Encriptación de datos sensibles
- Manejo seguro de tokens y credenciales
- Límites de rate y protección contra abusos
- Logs de auditoría y monitoreo
- Sistema automático de gestión de permisos
- Volúmenes Docker dedicados para datos sensibles
- Contenedor con usuario no privilegiado

## 🔧 Solución de Problemas

### Problemas Comunes

1. **Errores de Permisos:**
   ```bash
   # Ejecutar corrección automática de permisos
   rake app:fix_permissions
   ```

2. **Problemas de Autenticación:**
   - Verificar que credentials.json está en el directorio correcto
   - Ejecutar `rake app:reset` para reiniciar completamente

3. **Errores de Docker:**
   ```bash
   # Reiniciar completamente los contenedores
   rake app:reset
   ```

4. **Verificar Estado del Sistema:**
   ```bash
   rake monitor:permissions  # Ver permisos
   rake app:status          # Estado de contenedores
   rake monitor:errors      # Ver errores
   ```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.