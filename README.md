# Temis - Asistente Legal Virtual 👩‍⚖️

Temis es un asistente virtual inteligente diseñado para gestionar citas y consultas con el Dr. Saul. Utilizando tecnología de punta en procesamiento de lenguaje natural, ofrece una interfaz conversacional profesional y segura para la programación y consulta de citas legales, brindando una experiencia personalizada y eficiente. Si bien este asistente cumple con un proposito particular, puede configurar para adapatarse a otro tipo de consultas o citas.

## � Objetivos del Proyecto

- Automatizar y optimizar la gestión de citas legales
- Proporcionar atención 24/7 a consultas básicas
- Reducir tiempos de espera y mejorar la experiencia del cliente
- Mantener un registro organizado de las consultas y citas

## �🌟 Características Principales

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

## 🛠️ Stack Tecnológico

### Backend
- Python 3.8+
- LangChain 0.3.18
- LangGraph 0.2.70
- Google Calendar API

### Frontend
- Streamlit 1.42.0

### Modelos de IA
- OpenAI GPT-4o-mini
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

## 🚀 Guía de Instalación

### 1. Preparación del Entorno

```bash
# Clonar el repositorio
git clone https://github.com/Mongar28/bot_lawyer_assistant.git
cd bot_lawyer_assistant

# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate    # Windows
```

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración del Entorno

Crear archivo `.env` con las siguientes variables:
```env
OPENAI_API_KEY=tu_api_key_openai
DEEPSEEK_API_KEY=tu_api_key_deepseek  # Opcional
GOOGLE_CALENDAR_CREDENTIALS=path/to/credentials.json
```

### 4. Configuración de Google Calendar

1. Crear proyecto en Google Cloud Console
2. Habilitar Calendar API
3. Crear credenciales OAuth
4. Descargar archivo de credenciales
5. Colocar en directorio `credentials/`

### Alternativa: Despliegue con Docker 🐳

También puedes ejecutar la aplicación usando Docker, lo que garantiza un entorno consistente y aislado:

1. **Construir y ejecutar con Docker Compose:**
```bash
# Construir la imagen
docker-compose build

# Iniciar la aplicación
docker-compose up -d
```

2. **O usar los comandos Rake para gestión:**
```bash
# Construir la imagen
rake app:build

# Iniciar la aplicación
rake app:start

# Ver logs
rake app:logs

# Detener la aplicación
rake app:stop
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

- **Monitoreo:**
  - `rake monitor:resources` - Ver uso de CPU/memoria
  - `rake monitor:errors` - Ver logs de errores

#### Configuración Docker

El proyecto incluye:
- `Dockerfile` - Configuración del contenedor basado en Ubuntu 22.04
- `docker-compose.yml` - Orquestación de servicios
- Variables de entorno y volúmenes configurados
- Healthcheck automático

## 💻 Uso y Operación

### Iniciar la Aplicación

```bash
streamlit run app.py
```

### Flujo de Uso

1. Acceder a `http://localhost:8501`
2. Ingresar correo electrónico para autenticación
3. Interactuar con el asistente para:
   - Consultar disponibilidad
   - Agendar citas
   - Realizar consultas generales
   - Gestionar citas existentes

## 🏗️ Arquitectura del Proyecto

```
bot_lawyer_assistant/
├── app.py                     # Aplicación principal
├── config/                    # Configuraciones
│   └── prompts.yaml          # Plantillas de prompts
├── langgraph_components/     # Componentes del grafo
│   ├── graph.py             # Lógica del grafo
│   ├── graph_tools.py       # Herramientas del grafo
│   ├── llm.py              # Configuración de modelos
│   └── states.py           # Estados del sistema
├── credentials/             # Credenciales (gitignored)
└── requirements.txt        # Dependencias
```

## 🔒 Seguridad y Privacidad

- Validación robusta de entradas
- Encriptación de datos sensibles
- Manejo seguro de tokens y credenciales
- Límites de rate y protección contra abusos
- Logs de auditoría y monitoreo

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Crear Pull Request

### Guías de Contribución

- Seguir PEP 8 para código Python
- Documentar nuevas funciones
- Agregar tests unitarios
- Mantener la seguridad como prioridad

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para detalles.

## 👥 Equipo

- **Cristian Montoya Garces**
  - Rol: Desarrollador Principal
  - GitHub: [@Mongar28](https://github.com/Mongar28)
  - Email: cristian.montoya.g@gmail.com

## 📞 Soporte y Contacto

- **Email de Soporte:** cristian.montoya.g@gmail.com
- **Issues:** [GitHub Issues](https://github.com/Mongar28/bot_lawyer_assistant/issues)
- **Wiki:** [Documentación Detallada](https://github.com/Mongar28/bot_lawyer_assistant/wiki)

## 🔄 Estado del Proyecto

![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-green)
![Versión](https://img.shields.io/badge/Versión-1.0.0-blue)