# Temis - Asistente Legal Virtual 👩‍⚖️

Temis es un asistente virtual inteligente diseñado para gestionar citas y consultas con el Dr. Saul, ofreciendo una interfaz conversacional profesional y segura para la programación y consulta de citas legales.

## 🌟 Características Principales

- Gestión inteligente de citas con verificación por correo electrónico
- Interfaz conversacional natural y empática usando Streamlit
- Sistema de validación y seguridad robusto
- Integración con calendario para gestión de citas
- Soporte para múltiples modelos de lenguaje (GPT-4, DeepSeek)

## 🛠️ Tecnologías Utilizadas

- Python 3.8+
- Streamlit para la interfaz web
- LangChain y LangGraph para el procesamiento de lenguaje natural
- Modelos de lenguaje soportados:
  - OpenAI
  - DeepSeek
- Google Calendar API para la gestión de citas

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de Google Cloud Platform con Calendar API habilitada
- API Key de OpenAI o DeepSeek (según el modelo a utilizar)
- Configuración de variables de entorno

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Mongar28/bot_lawyer_assistant.git
cd bot_lawyer_assistant
```

2. Crear y activar entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear un archivo `.env` con las siguientes variables:
```
OPENAI_API_KEY=tu_api_key_openai
DEEPSEEK_API_KEY=tu_api_key_deepseek  # Opcional, si usas DeepSeek
GOOGLE_CALENDAR_CREDENTIALS=path/to/credentials.json
```

## 💻 Uso

1. Iniciar la aplicación:
```bash
streamlit run app.py
```

2. Acceder a través del navegador:
- La aplicación estará disponible en `http://localhost:8501`
- Ingresar el correo electrónico para comenzar
- Seguir las instrucciones del asistente para gestionar citas

## 🏗️ Estructura del Proyecto

```
bot_lawyer_assistant/
├── app.py                    # Aplicación principal Streamlit
├── config/
│   └── prompts.yaml         # Configuración de prompts del asistente
├── langgraph_components/    # Componentes del grafo de conversación
│   ├── graph.py            # Definición del grafo de conversación
│   ├── llm.py             # Configuración de modelos de lenguaje
│   └── states.py          # Definición de estados
├── credentials/            # Directorio para credenciales (gitignored)
└── requirements.txt       # Dependencias del proyecto
```

## 🔒 Características de Seguridad

- Validación robusta de correos electrónicos
- Verificación en dos pasos para acceso
- Sanitización de entradas de usuario
- Protección contra inyecciones de prompts
- Manejo seguro de información sensible
- Límites de intentos en verificaciones

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- Cristian Montoya Garces - *Trabajo Inicial* - [https://github.com/Mongar28](https://github.com/Mongar28)

## 📞 Soporte

Para soporte y consultas, por favor contacta a cristian.montoya.g@gmail.com 