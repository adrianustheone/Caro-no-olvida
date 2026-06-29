from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.api_python_client import build
from datetime import datetime, timedelta
from typing import Optional, List
import json

from models import CalendarEvent, EventType, User


class GoogleCalendarService:
    """Servicio para sincronizar eventos de Google Calendar de Carolina"""
    
    def __init__(self, config):
        self.config = config
        self.scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    
    def create_flow(self):
        """Crea el flujo OAuth de Google"""
        return Flow.from_client_config(
            {
                "installed": {
                    "client_id": self.config.GOOGLE_CLIENT_ID,
                    "client_secret": self.config.GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.config.GOOGLE_REDIRECT_URI]
                }
            },
            scopes=self.scopes
        )
    
    def get_calendar_service(self, credentials_json: str):
        """Obtiene el servicio de Google Calendar con credenciales"""
        credentials = Credentials.from_authorized_user_info(json.loads(credentials_json))
        return build('calendar', 'v3', credentials=credentials)
    
    def parse_event_type(self, title: str, description: str = "") -> EventType:
        """Detecta automáticamente el tipo de evento por palabras clave"""
        text = (title + " " + (description or "")).lower()
        
        if any(word in text for word in ["audiencia", "mediación", "juzgado", "tribunal"]):
            return EventType.AUDIENCIA
        elif any(word in text for word in ["plazo", "vencimiento", "recurso", "apelación"]):
            return EventType.PLAZO
        elif any(word in text for word in ["documento", "prueba", "sentencia", "traer", "entregar"]):
            return EventType.DOCUMENTO
        elif any(word in text for word in ["reunión", "cliente", "consulta"]):
            return EventType.REUNION
        
        return EventType.OTRO
    
    def extract_family_law_info(self, title: str, description: str = "") -> dict:
        """Extrae información específica de derecho de familia"""
        text = (title + "\n" + (description or "")).strip()
        
        info = {
            "client_name": None,
            "case_number": None,
            "juzgado": None
        }
        
        # Busca números de caso (ej: 23456/2024)
        import re
        case_match = re.search(r'(\d+/\d{4})', text)
        if case_match:
            info["case_number"] = case_match.group(1)
        
        # Busca juzgados (muy simplificado)
        if "juzgado" in text.lower():
            juzgado_match = re.search(r'Juzgado\s+([^,\n]+)', text, re.IGNORECASE)
            if juzgado_match:
                info["juzgado"] = juzgado_match.group(1).strip()
        
        return info
    
    def create_event(self, service, event_data: dict) -> str:
        """
        Crea un evento en Google Calendar desde datos naturales
        
        Args:
            service: Google Calendar service
            event_data: {
                "title": "Título",
                "date": "2026-06-28",
                "time": "10:00",
                "juzgado": "...",
                "location": "...",
                "description": "...",
                "type": "AUDIENCIA|PLAZO|..."
            }
        
        Returns:
            google_event_id si éxito, None si error
        """
        try:
            from datetime import timedelta
            
            # Combina fecha + hora
            start_time_str = f"{event_data.get('date')}T{event_data.get('time')}:00"
            dt = datetime.fromisoformat(start_time_str)
            end_dt = dt + timedelta(hours=1)
            end_time_str = end_dt.isoformat()
            
            # Construye descripción
            description_parts = []
            if event_data.get('description'):
                description_parts.append(event_data.get('description'))
            
            if event_data.get('juzgado'):
                description_parts.append(f"Juzgado: {event_data.get('juzgado')}")
            
            if event_data.get('case_number'):
                description_parts.append(f"Caso: {event_data.get('case_number')}")
            
            if event_data.get('client_name'):
                description_parts.append(f"Cliente: {event_data.get('client_name')}")
            
            # Agrega tipo de evento en descripción
            if event_data.get('type'):
                description_parts.insert(0, f"[{event_data.get('type')}]")
            
            description = "\n".join(description_parts)
            
            # Crea el evento en Google Calendar
            event_body = {
                'summary': event_data.get('title'),
                'description': description,
                'start': {
                    'dateTime': start_time_str,
                    'timeZone': 'America/Argentina/Buenos_Aires'
                },
                'end': {
                    'dateTime': end_time_str,
                    'timeZone': 'America/Argentina/Buenos_Aires'
                }
            }
            
            if event_data.get('location'):
                event_body['location'] = event_data.get('location')
            
            created_event = service.events().insert(
                calendarId='primary',
                body=event_body
            ).execute()
            
            event_id = created_event.get('id')
            print(f"✅ Evento creado en Google Calendar: {event_data.get('title')} ({event_id})")
            return event_id
        
        except Exception as e:
            print(f"❌ Error creando evento en Google Calendar: {e}")
            return None
    
    async def sync_events(self, user_id: int, service, db_session) -> List[CalendarEvent]:
        """
        Sincroniza eventos de Google Calendar para Carolina
        Retorna lista de nuevos/actualizados eventos
        """
        try:
            # Obtén eventos de los próximos 90 días
            now = datetime.utcnow().isoformat() + 'Z'
            end_date = (datetime.utcnow() + timedelta(days=90)).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                timeMax=end_date,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            synced_events = []
            
            for event in events:
                google_event_id = event.get('id')
                
                # Chequea si ya existe
                existing = db_session.query(CalendarEvent).filter_by(
                    google_event_id=google_event_id
                ).first()
                
                start_time = datetime.fromisoformat(
                    event['start'].get('dateTime', event['start'].get('date')).replace('Z', '+00:00')
                )
                end_time = datetime.fromisoformat(
                    event['end'].get('dateTime', event['end'].get('date')).replace('Z', '+00:00')
                )
                
                title = event.get('summary', 'Sin título')
                description = event.get('description', '')
                location = event.get('location', '')
                
                event_type = self.parse_event_type(title, description)
                family_info = self.extract_family_law_info(title, description)
                
                if existing:
                    # Actualiza evento existente
                    existing.title = title
                    existing.description = description
                    existing.start_time = start_time
                    existing.end_time = end_time
                    existing.location = location
                    existing.event_type = event_type
                    existing.client_name = family_info.get('client_name')
                    existing.case_number = family_info.get('case_number')
                    existing.juzgado = family_info.get('juzgado')
                    existing.synced_at = datetime.utcnow()
                else:
                    # Crea nuevo evento
                    new_event = CalendarEvent(
                        user_id=user_id,
                        google_event_id=google_event_id,
                        title=title,
                        description=description,
                        start_time=start_time,
                        end_time=end_time,
                        location=location,
                        event_type=event_type,
                        client_name=family_info.get('client_name'),
                        case_number=family_info.get('case_number'),
                        juzgado=family_info.get('juzgado')
                    )
                    db_session.add(new_event)
                
                synced_events.append(event)
            
            db_session.commit()
            return synced_events
        
        except Exception as e:
            print(f"Error sincronizando eventos: {e}")
            raise
