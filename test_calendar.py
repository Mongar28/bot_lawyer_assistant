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

# Si modificas estos scopes, elimina el archivo token.pickle
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify'
]

# Almacenamiento temporal de códigos de verificación
verification_codes = {}

def get_calendar_service():
    """Obtiene el servicio de Google Calendar."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def get_gmail_service():
    """Obtiene el servicio de Gmail usando las mismas credenciales."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def generate_verification_code():
    """Genera un código de verificación de 6 dígitos."""
    return ''.join(random.choices(string.digits, k=6))

def test_send_verification_code():
    """Prueba el envío de código de verificación."""
    try:
        # Datos de prueba
        client_email = "cristian.montoyag1@udea.edu.co"  # Cambia esto por tu correo
        action = "agendar"
        details = """
        Fecha: 12/02/2025
        Hora: 10:00 AM
        Cliente: Cliente Prueba
        Motivo: Prueba de verificación
        """
        
        service = get_gmail_service()
        code = generate_verification_code()
        
        # Guardar código
        verification_codes[client_email] = {
            'code': code,
            'expires': datetime.now() + timedelta(minutes=10),
            'action': action,
            'details': details
        }
        
        # Crear mensaje
        message = MIMEText(f"""
        Hola,
        
        Has solicitado {action} una cita con el abogado Saul.
        
        Detalles de la operación:
        {details}
        
        Tu código de verificación es: {code}
        
        Este código expirará en 10 minutos.
        
        Si no solicitaste esta acción, por favor ignora este correo.
        
        Saludos,
        Temis - Asistente Virtual
        """)
        
        message['to'] = client_email
        message['subject'] = f'Código de verificación - {action} cita'
        
        # Codificar el mensaje
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        # Enviar correo
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        
        print(f"Código de verificación enviado. Message ID: {sent_message['id']}")
        return code  # Retornamos el código para probarlo después
    except Exception as e:
        print(f"Error al enviar código de verificación: {str(e)}")
        return None

def test_verify_code(email: str, code: str):
    """Prueba la verificación del código."""
    try:
        if email not in verification_codes:
            print("No hay código de verificación pendiente para este correo.")
            return False
            
        verification = verification_codes[email]
        
        if datetime.now() > verification['expires']:
            del verification_codes[email]
            print("El código ha expirado.")
            return False
            
        if code != verification['code']:
            print("Código incorrecto.")
            return False
            
        # Código válido
        print("Código verificado correctamente.")
        del verification_codes[email]
        return True
    except Exception as e:
        print(f"Error al verificar código: {str(e)}")
        return False

def test_create_event():
    """Prueba la creación de un evento"""
    try:
        service = get_calendar_service()
        
        # Datos de prueba
        client_name = "Cliente Prueba"
        client_email = "cliente@ejemplo.com"
        reason = "Consulta legal"
        
        # Crear evento de prueba
        start_time = datetime.now()
        end_time = start_time.replace(hour=start_time.hour + 1)
        
        event = {
            'summary': f'Cita con {client_name}',
            'description': f'Motivo: {reason}',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Bogota',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Bogota',
            },
            'attendees': [
                {'email': client_email}
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', 
                                      body=event, 
                                      sendUpdates='all').execute()
        print(f"Evento creado exitosamente: {event.get('htmlLink')}")
        return event['id']
    except Exception as e:
        print(f"Error al crear evento: {str(e)}")
        return None

def test_modify_event(event_id: str):
    """Prueba la modificación de un evento"""
    try:
        service = get_calendar_service()
        
        # Obtener evento existente
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        
        # Modificar hora (1 hora más tarde)
        start_time = datetime.fromisoformat(event['start']['dateTime'])
        new_start = start_time.replace(hour=start_time.hour + 1)
        new_end = new_start.replace(hour=new_start.hour + 1)
        
        event['start']['dateTime'] = new_start.isoformat()
        event['end']['dateTime'] = new_end.isoformat()
        
        # Actualizar evento
        updated_event = service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event,
            sendUpdates='all'
        ).execute()
        
        print(f"Evento modificado exitosamente: {updated_event.get('htmlLink')}")
    except Exception as e:
        print(f"Error al modificar evento: {str(e)}")

def test_search_events():
    """Prueba la búsqueda de eventos"""
    try:
        service = get_calendar_service()
        
        # Buscar eventos
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        if not events:
            print('No se encontraron eventos próximos.')
        else:
            print('Eventos próximos:')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                attendees = event.get('attendees', [])
                attendee_emails = [att['email'] for att in attendees]
                print(f"- {event['summary']}")
                print(f"  Fecha: {start}")
                print(f"  Descripción: {event.get('description', 'Sin descripción')}")
                print(f"  Asistentes: {', '.join(attendee_emails)}")
                print(f"  ID: {event['id']}\n")
    except Exception as e:
        print(f"Error al buscar eventos: {str(e)}")

if __name__ == "__main__":
    print("Probando sistema de verificación...")
    
    # 1. Probar envío de código
    print("\n1. Enviando código de verificación...")
    code = test_send_verification_code()
    
    if code:
        # 2. Probar verificación con código correcto
        print("\n2. Probando verificación con código correcto...")
        test_verify_code("cristian.montoyag1@udea.edu.co", code)
        
        # 3. Probar verificación con código incorrecto
        print("\n3. Probando verificación con código incorrecto...")
        test_verify_code("cristian.montoyag1@udea.edu.co", "000000")
    
    # 4. Crear evento si la verificación fue exitosa
    print("\n4. Probando creación de evento...")
    test_create_event()