from langchain_core.tools import tool
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import json
import random
import string
from email.mime.text import MIMEText
import base64
from zoneinfo import ZoneInfo
import yaml
import fcntl
import tempfile
import shutil
import stat

# Almacenamiento temporal de códigos de verificación
VERIFICATION_FILE = '/app/config/verification_codes.yaml'

# Actualizar SCOPES para incluir Gmail
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify'
]

def get_calendar_service():
    """Obtiene el servicio de Google Calendar."""
    creds = None
    # El archivo token.pickle almacena los tokens de acceso y actualización del usuario
    if os.path.exists('credentials/token.pickle'):
        with open('credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Si no hay credenciales válidas disponibles, permite que el usuario inicie sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima ejecución
        with open('credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def get_gmail_service():
    """Obtiene el servicio de Gmail."""
    try:
        creds = None
        credentials_dir = '/app/credentials'
        token_path = os.path.join(credentials_dir, 'token.pickle')
        
        # Verificar y crear directorios si no existen
        os.makedirs(credentials_dir, mode=0o777, exist_ok=True)
        
        # Verificar permisos del directorio
        try:
            os.chmod(credentials_dir, 0o777)
        except Exception as e:
            print(f"Advertencia: No se pudieron establecer permisos en {credentials_dir}: {e}")
        
        if os.path.exists(token_path):
            print(f"Leyendo token desde {token_path}")
            try:
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                print(f"Error leyendo token: {str(e)}")
                creds = None
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refrescando token expirado")
                creds.refresh(Request())
            else:
                print("Generando nuevo token")
                credentials_file = os.path.join(credentials_dir, 'credentials.json')
                if not os.path.exists(credentials_file):
                    raise FileNotFoundError(f"No se encuentra el archivo {credentials_file}")
                
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Guardar el token directamente (sin usar archivo temporal)
            print("Guardando nuevo token")
            try:
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
                    token.flush()
                    os.fsync(token.fileno())
                
                # Intentar establecer permisos
                try:
                    os.chmod(token_path, 0o666)
                except Exception as e:
                    print(f"Advertencia: No se pudieron establecer permisos en {token_path}: {e}")
                
            except Exception as e:
                print(f"Error guardando token: {str(e)}")
                raise

        return build('gmail', 'v1', credentials=creds)
        
    except Exception as e:
        print(f"Error en get_gmail_service: {str(e)}")
        print(f"Estado del sistema:")
        print(f"- Directorio actual: {os.getcwd()}")
        print(f"- Usuario actual: {os.getuid()}:{os.getgid()}")
        print(f"- Permisos del directorio credentials:")
        try:
            print(f"  {os.stat(credentials_dir)}")
        except Exception as e:
            print(f"  Error obteniendo permisos: {e}")
        raise

def generate_verification_code():
    """Genera un código de verificación de 6 dígitos."""
    return ''.join(random.choices(string.digits, k=6))

def save_verification_code(email: str, code: str):
    """Guarda el código en el archivo YAML."""
    try:
        print(f"Iniciando guardado de código para {email}")
        
        config_dir = '/app/config'
        verification_file = os.path.join(config_dir, 'verification_codes.yaml')
        
        # Asegurar que el directorio existe
        os.makedirs(config_dir, mode=0o777, exist_ok=True)
        
        # Intentar establecer permisos del directorio
        try:
            os.chmod(config_dir, 0o777)
        except Exception as e:
            print(f"Advertencia: No se pudieron establecer permisos en {config_dir}: {e}")
        
        # Leer códigos existentes
        codes = {}
        if os.path.exists(verification_file):
            try:
                with open(verification_file, 'r') as f:
                    codes = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Error leyendo archivo: {e}")
                codes = {}
        
        # Preparar nuevo código
        current = datetime.now(ZoneInfo('America/Bogota'))
        codes[email] = {
            'code': str(code),
            'expires': (current + timedelta(minutes=10)).isoformat()
        }
        
        # Guardar directamente (sin usar archivo temporal)
        try:
            with open(verification_file, 'w') as f:
                yaml.dump(codes, f)
                f.flush()
                os.fsync(f.fileno())
            
            # Intentar establecer permisos
            try:
                os.chmod(verification_file, 0o666)
            except Exception as e:
                print(f"Advertencia: No se pudieron establecer permisos en {verification_file}: {e}")
                
        except Exception as e:
            print(f"Error escribiendo archivo: {str(e)}")
            raise
            
    except Exception as e:
        print(f"Error guardando código: {str(e)}")
        print(f"Estado del sistema:")
        print(f"- Directorio actual: {os.getcwd()}")
        print(f"- Usuario actual: {os.getuid()}:{os.getgid()}")
        print(f"- Contenido de /app/config: {os.listdir('/app/config')}")
        raise

@tool
def send_verification_code(email: str) -> str:
    """
    Genera, guarda y envía un código de verificación.
    Args:
        email (str): Correo del cliente
    Returns:
        str: Mensaje de confirmación
    """
    try:
        print(f"Iniciando proceso de envío de código para {email}")
        
        # Generar código
        code = generate_verification_code()
        print(f"Código generado: {code}")
        
        # Verificar permisos del directorio
        config_dir = '/app/config'
        print(f"Verificando permisos de {config_dir}")
        print(f"Permisos actuales: {oct(os.stat(config_dir).st_mode)}")
        
        # Guardar código
        try:
            save_verification_code(email, code)
            print("Código guardado exitosamente")
        except Exception as e:
            print(f"Error guardando código: {str(e)}")
            print(f"Stack trace completo:", exc_info=True)
            raise
        
        # Verificar si el archivo existe y sus permisos
        if os.path.exists(VERIFICATION_FILE):
            print(f"Archivo existe, permisos: {oct(os.stat(VERIFICATION_FILE).st_mode)}")
        else:
            print("El archivo no existe después de intentar guardarlo")
        
        # Enviar correo
        try:
            service = get_gmail_service()
            message = MIMEText(f"""
            Hola,
            
            Tu código de verificación es: {code}
            
            Este código expirará en 10 minutos.
            """)
            
            message['to'] = email
            message['subject'] = 'Código de Verificación - Asistente Legal'
            
            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            
            try:
                service.users().messages().send(userId="me", body=create_message).execute()
                print("Correo enviado exitosamente")
                return "Código de verificación enviado exitosamente."
            except Exception as e:
                print(f"Error enviando correo: {str(e)}")
                raise
                
        except Exception as e:
            print(f"Error con el servicio de Gmail: {str(e)}")
            raise
            
    except Exception as e:
        print(f"Error general en send_verification_code: {str(e)}")
        raise

@tool
def verify_code(email: str, code: str) -> bool:
    """
    Verifica si el código proporcionado es válido.
    Args:
        email (str): Correo del cliente
        code (str): Código a verificar
    Returns:
        bool: True si el código es válido
    """
    try:
        if not os.path.exists(VERIFICATION_FILE):
            print("Archivo de verificación no existe")
            return False
            
        with open(VERIFICATION_FILE, 'r') as f:
            # Adquirir bloqueo compartido
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                codes = yaml.safe_load(f) or {}
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        
        if email not in codes:
            print(f"No hay código para {email}")
            return False
            
        stored = codes[email]
        expiry = datetime.fromisoformat(stored['expires'])
        
        # Usar la misma zona horaria que usamos al guardar
        current = datetime.now(ZoneInfo('America/Bogota'))
        
        if current > expiry:
            print(f"Código expirado. Expira: {expiry}, Actual: {current}")
            # Limpiar código expirado
            del codes[email]
            with open(VERIFICATION_FILE, 'w') as f:
                # Adquirir bloqueo exclusivo
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    yaml.dump(codes, f)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return False
            
        # Asegurar que ambos sean strings
        stored_code = str(stored['code'])
        input_code = str(code)
        
        # Comparación exacta
        is_valid = stored_code == input_code
        # print(f"Comparando códigos: almacenado='{stored_code}' vs ingresado='{input_code}' -> {is_valid}")
        
        # Si es válido, limpiar el código usado
        if is_valid:
            del codes[email]
            with open(VERIFICATION_FILE, 'w') as f:
                # Adquirir bloqueo exclusivo
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    yaml.dump(codes, f)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
        return is_valid
    except Exception as e:
        print(f"Error verificando código: {e}")
        return False

@tool
def create_calendar_event(date: str, time: str, client_name: str, client_email: str, reason: str, is_verified: bool = False) -> str:
    """
    Agenda una cita si está verificada.
    Args:
        date (str): Fecha de la cita (DD/MM/YYYY)
        time (str): Hora de la cita (HH:MM)
        client_name (str): Nombre del cliente
        client_email (str): Correo del cliente
        reason (str): Motivo de la consulta
        is_verified (bool): Si el cliente está verificado
    Returns:
        str: Resultado de la operación
    """
    if not is_verified:
        return "Se requiere verificación para agendar la cita"
        
    try:
        # Validar horario
        hour = int(time.split(':')[0])
        if hour < 9 or hour >= 17:
            return "Las citas solo se pueden agendar entre las 9:00 AM y las 5:00 PM"
            
        # Crear evento
        event_datetime = datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
        
        service = get_calendar_service()
        event = {
            'summary': f'Cita con {client_name}',
            'description': f'Motivo: {reason}\nCorreo: {client_email}',
            'start': {
                'dateTime': event_datetime.isoformat(),
                'timeZone': 'America/Bogota',
            },
            'end': {
                'dateTime': (event_datetime + timedelta(hours=1)).isoformat(),
                'timeZone': 'America/Bogota',
            },
            'attendees': [
                {'email': client_email}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 24 horas antes
                    {'method': 'popup', 'minutes': 30}        # 30 minutos antes
                ]
            }
        }
        
        event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
        return f"Cita agendada exitosamente. Enlace: {event.get('htmlLink')}"
    except Exception as e:
        return f"Error al agendar la cita: {str(e)}"

@tool
def modify_calendar_event(event_id: str, client_email: str, new_date: str = None, new_time: str = None, is_verified: bool = False) -> str:
    """
    Modifica una cita existente.
    Args:
        event_id (str): ID del evento a modificar
        client_email (str): Correo del cliente
        new_date (str, optional): Nueva fecha (DD/MM/YYYY)
        new_time (str, optional): Nueva hora (HH:MM)
        is_verified (bool): Si el cliente está verificado
    Returns:
        str: Resultado de la operación
    """
    if not is_verified:
        return "Se requiere verificación para modificar la cita"
        
    try:
        service = get_calendar_service()
        
        # Obtener evento
        try:
            event = service.events().get(calendarId='primary', eventId=event_id).execute()
        except Exception:
            return "No se encontró la cita especificada"
            
        # Verificar que el correo coincida
        description = event.get('description', '')
        attendees = event.get('attendees', [])
        email_in_description = f"Correo: {client_email}" in description
        email_in_attendees = any(att.get('email') == client_email for att in attendees)
        
        if not (email_in_description or email_in_attendees):
            return "No tienes permiso para modificar esta cita"
            
        if new_date or new_time:
            # Obtener fecha y hora actuales del evento
            start = datetime.fromisoformat(event['start']['dateTime'])
            current_date = start.strftime("%d/%m/%Y")
            current_time = start.strftime("%H:%M")
            
            # Actualizar fecha y/o hora
            date_to_use = new_date if new_date else current_date
            time_to_use = new_time if new_time else current_time
            
            # Validar horario
            hour = int(time_to_use.split(':')[0])
            if hour < 9 or hour >= 17:
                return "Las citas solo se pueden agendar entre las 9:00 AM y las 5:00 PM"
                
            # Convertir a datetime
            new_datetime = datetime.strptime(f"{date_to_use} {time_to_use}", "%d/%m/%Y %H:%M")
            
            # Actualizar evento
            event['start']['dateTime'] = new_datetime.isoformat()
            event['end']['dateTime'] = (new_datetime + timedelta(hours=1)).isoformat()
            
            updated_event = service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return f"¡Cita modificada exitosamente! Nuevo horario: {date_to_use} a las {time_to_use}"
        else:
            return "No se especificaron cambios para la cita"
    except Exception as e:
        return f"Error al modificar la cita: {str(e)}"

@tool
def cancel_calendar_event(event_id: str, client_email: str, is_verified: bool = False) -> str:
    """
    Cancela una cita existente.
    Args:
        event_id (str): ID del evento a cancelar
        client_email (str): Correo del cliente
        is_verified (bool): Si el cliente está verificado
    Returns:
        str: Resultado de la operación
    """
    if not is_verified:
        return "Se requiere verificación para cancelar la cita"
        
    try:
        service = get_calendar_service()
        
        # Obtener evento
        try:
            event = service.events().get(calendarId='primary', eventId=event_id).execute()
        except Exception:
            return "No se encontró la cita especificada"
            
        # Verificar que el correo coincida
        description = event.get('description', '')
        attendees = event.get('attendees', [])
        email_in_description = f"Correo: {client_email}" in description
        email_in_attendees = any(att.get('email') == client_email for att in attendees)
        
        if not (email_in_description or email_in_attendees):
            return "No tienes permiso para cancelar esta cita"
            
        # Cancelar evento
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return "¡Cita cancelada exitosamente! 🗑️ Si necesitas reagendar, ¡estoy aquí para ayudarte! 😊"
    except Exception as e:
        return f"Error al cancelar la cita: {str(e)}"

@tool
def search_calendar_event(query: str = None, time_min: str = None) -> str:
    """
    Busca citas en Google Calendar.
    Args:
        query (str, optional): Texto a buscar en los eventos
        time_min (str, optional): Fecha mínima en formato DD/MM/YYYY
    Returns:
        str: Lista de citas encontradas
    """
    try:
        service = get_calendar_service()
        
        # Parámetros de búsqueda
        params = {
            'calendarId': 'primary',
            'maxResults': 10,
            'singleEvents': True,
            'orderBy': 'startTime'
        }
        
        if query:
            params['q'] = query
            
        if time_min:
            time_min_obj = datetime.strptime(time_min, "%d/%m/%Y")
            params['timeMin'] = time_min_obj.isoformat() + 'Z'

        events_result = service.events().list(**params).execute()
        events = events_result.get('items', [])

        if not events:
            return "No se encontraron citas."
            
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_events.append({
                'id': event['id'],
                'titulo': event['summary'],
                'inicio': start,
                'descripcion': event.get('description', 'Sin descripción')
            })
            
        return json.dumps(formatted_events, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error al buscar citas: {str(e)}"

@tool
def get_current_datetime() -> str:
    """
    Obtiene la fecha y hora actual en Bogotá, incluyendo el día de la semana.
    Returns:
        str: Fecha y hora actual en formato amigable
    """
    try:
        # Obtener fecha y hora actual en Bogotá
        bogota_tz = ZoneInfo('America/Bogota')
        current = datetime.now(bogota_tz)
        
        # Mapeo de días en español
        dias = {
            0: 'lunes',
            1: 'martes',
            2: 'miércoles',
            3: 'jueves',
            4: 'viernes',
            5: 'sábado',
            6: 'domingo'
        }
        
        # Formatear fecha y hora
        fecha = current.strftime("%d/%m/%Y")
        hora = current.strftime("%I:%M %p")
        dia = dias[current.weekday()]
        
        return f"Hoy es {dia} {fecha}, {hora}"
    except Exception as e:
        return f"Error al obtener fecha y hora: {str(e)}"

tools = [
    create_calendar_event,
    modify_calendar_event,
    cancel_calendar_event,
    search_calendar_event,
    get_current_datetime,
    send_verification_code,
    verify_code
]
