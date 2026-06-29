from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import json
from typing import Optional

from config import settings
from models import Base, User, CalendarEvent, TaskNote, EventType, WhatsAppConversation
from services_google import GoogleCalendarService
from services_whatsapp import WhatsAppService
from services_claude import CaroNoOlvidaAI

# ============ DATABASE ============
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea las tablas
Base.metadata.create_all(bind=engine)

# ============ FASTAPI APP ============
app = FastAPI(
    title="Caro No Olvida",
    version="1.0.0",
    description="Asistente conversacional por WhatsApp para Carolina"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ DEPENDENCIES ============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)) -> User:
    """Carolina es el único usuario en esta versión"""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no configurado")
    return user

# ============ SERVICIOS ============
google_service = GoogleCalendarService(settings)
whatsapp_service = WhatsAppService(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN,
    settings.TWILIO_WHATSAPP_FROM
)
caro_ai = CaroNoOlvidaAI()

# ============ RUTAS ============

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "app": "Caro No Olvida",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/auth/google")
async def init_google_auth(db: Session = Depends(get_db)):
    """Inicia OAuth con Google Calendar"""
    flow = google_service.create_flow()
    auth_uri, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    return {
        "auth_url": auth_uri,
        "message": "Hacé click para conectar Google Calendar"
    }

@app.get("/api/v1/auth/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """Callback de Google OAuth"""
    try:
        flow = google_service.create_flow()
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        user = db.query(User).first()
        if not user:
            user = User(
                name="Carolina",
                whatsapp_number="+541234567890",
                google_token=credentials.to_json(),
                google_refresh_token=credentials.refresh_token,
                google_calendar_id="primary"
            )
            db.add(user)
        else:
            user.google_token = credentials.to_json()
            user.google_refresh_token = credentials.refresh_token
        
        db.commit()
        
        return {
            "status": "success",
            "message": "Google Calendar conectado. Ahora podés hablar con Caro por WhatsApp para agendar eventos"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.post("/api/v1/setup/whatsapp")
async def setup_whatsapp(whatsapp_number: str, db: Session = Depends(get_db)):
    """Configura el número de WhatsApp de Carolina"""
    try:
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=400, detail="Primero conecta Google Calendar")
        
        user.whatsapp_number = whatsapp_number
        db.commit()
        
        to_whatsapp = f"whatsapp:{whatsapp_number}"
        message = """✅ ¡Hola Carolina! Soy Caro No Olvida.

Podés hablarme por WhatsApp para:
📅 Agendar eventos: "Audiencia García mañana 10:00"
📋 Crear tareas: "Recordarme traer DNI"
❓ Preguntar: "¿Qué tengo hoy?"

También recibirás:
🌙 Recordatorio noche anterior
⏰ Recordatorio 2 horas antes
📋 Resumen diario a las 8am

¡Vamos a no olvidar nada! 💪"""
        
        whatsapp_service.send_message(to_whatsapp, message)
        
        return {
            "status": "success",
            "message": "WhatsApp configurado",
            "whatsapp_number": whatsapp_number
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/whatsapp/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook de Twilio - Recibe mensajes de WhatsApp
    
    Aquí es donde Carolina habla con Caro No Olvida:
    - "Agendar audiencia García mañana 10:00"
    - "Reunión López 30 de julio 3pm"
    - "Plazo vencimiento 15/8"
    - Etc.
    """
    try:
        data = await request.form()
        from_whatsapp = data.get('From')  # whatsapp:+541234567890
        message_body = data.get('Body')
        
        # Obtén usuario
        user = db.query(User).first()
        if not user:
            return {"status": "error", "message": "User not found"}
        
        # Guarda el mensaje en historial
        conversation = WhatsAppConversation(
            user_id=user.id,
            whatsapp_number=from_whatsapp.replace("whatsapp:", ""),
            user_message=message_body,
            status="pending_confirmation"
        )
        db.add(conversation)
        db.commit()
        
        # ===== PROCESA EL MENSAJE CON CLAUDE =====
        parsed = caro_ai.parse_event_from_message(message_body)
        
        # Guarda el parse
        conversation.parsed_data = json.dumps(parsed, ensure_ascii=False)
        
        # Genera respuesta
        response_message = caro_ai.generate_confirmation_message(parsed)
        
        # ===== Si es "crear evento" =====
        if parsed.get("action") == "create_event":
            # Crea en Google Calendar
            try:
                service = google_service.get_calendar_service(user.google_token)
                google_event_id = google_service.create_event(service, parsed)
                
                if google_event_id:
                    # Guarda el ID
                    conversation.google_event_id = google_event_id
                    conversation.status = "pending_confirmation"
                    
                    # Agrega a la respuesta
                    response_message += "\n\n✨ Se creó en Google Calendar. Confirmás?"
            
            except Exception as e:
                print(f"Error creating event: {e}")
                response_message = f"❌ Error al crear en Google Calendar: {str(e)}\n\nIntentá de nuevo o contactá a Adrián"
                conversation.status = "error"
        
        db.commit()
        
        # ===== ENVÍA RESPUESTA A CAROLINA =====
        whatsapp_service.send_message(from_whatsapp, response_message)
        
        return {"status": "ok"}
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/events/today")
async def get_today_events(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Obtiene los eventos de HOY"""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    events = db.query(CalendarEvent).filter(
        (CalendarEvent.user_id == user.id) &
        (CalendarEvent.start_time >= today_start) &
        (CalendarEvent.start_time < today_end) &
        (CalendarEvent.is_completed == False)
    ).order_by(CalendarEvent.start_time).all()
    
    return {
        "date": today_start.strftime("%Y-%m-%d"),
        "count": len(events),
        "events": [
            {
                "id": event.id,
                "title": event.title,
                "time": event.start_time.strftime("%H:%M"),
                "type": event.event_type.value,
                "location": event.location,
                "juzgado": event.juzgado,
                "description": event.description
            }
            for event in events
        ]
    }

@app.get("/api/v1/events/upcoming")
async def get_upcoming_events(
    days: int = 7,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Obtiene eventos de los próximos X días"""
    now = datetime.utcnow()
    future = now + timedelta(days=days)
    
    events = db.query(CalendarEvent).filter(
        (CalendarEvent.user_id == user.id) &
        (CalendarEvent.start_time >= now) &
        (CalendarEvent.start_time <= future) &
        (CalendarEvent.is_completed == False)
    ).order_by(CalendarEvent.start_time).all()
    
    return {
        "days": days,
        "count": len(events),
        "events": [
            {
                "id": event.id,
                "date": event.start_time.strftime("%Y-%m-%d"),
                "time": event.start_time.strftime("%H:%M"),
                "title": event.title,
                "type": event.event_type.value,
                "juzgado": event.juzgado,
                "case_number": event.case_number
            }
            for event in events
        ]
    }

@app.post("/api/v1/events/{event_id}/complete")
async def mark_event_complete(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Marca un evento como completado"""
    event = db.query(CalendarEvent).filter(
        (CalendarEvent.id == event_id) &
        (CalendarEvent.user_id == user.id)
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    event.is_completed = True
    db.commit()
    
    return {"status": "success", "event": event.title}

@app.get("/api/v1/settings/reminders")
async def get_reminder_settings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Obtiene la configuración de recordatorios"""
    return {
        "daily_summary_hour": user.daily_summary_hour,
        "reminder_night_before_hour": user.reminder_night_before_hour,
        "reminder_2h_before": user.reminder_2h_before,
        "description": {
            "daily_summary_hour": "Hora para enviar resumen diario (0-23)",
            "reminder_night_before_hour": "Hora para recordatorio noche anterior (0-23)",
            "reminder_2h_before": "Habilitar recordatorio 2 horas antes (true/false)"
        }
    }

@app.post("/api/v1/settings/reminders")
async def update_reminder_settings(
    daily_summary_hour: int = None,
    reminder_night_before_hour: int = None,
    reminder_2h_before: bool = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Actualiza la configuración de recordatorios"""
    if daily_summary_hour is not None:
        if not (0 <= daily_summary_hour <= 23):
            raise HTTPException(status_code=400, detail="daily_summary_hour debe ser 0-23")
        user.daily_summary_hour = daily_summary_hour
    
    if reminder_night_before_hour is not None:
        if not (0 <= reminder_night_before_hour <= 23):
            raise HTTPException(status_code=400, detail="reminder_night_before_hour debe ser 0-23")
        user.reminder_night_before_hour = reminder_night_before_hour
    
    if reminder_2h_before is not None:
        user.reminder_2h_before = reminder_2h_before
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Configuración actualizada",
        "settings": {
            "daily_summary_hour": user.daily_summary_hour,
            "reminder_night_before_hour": user.reminder_night_before_hour,
            "reminder_2h_before": user.reminder_2h_before
        }
    }

@app.get("/api/v1/user/config")
async def get_user_config(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Obtiene la configuración actual de Carolina"""
    return {
        "name": user.name,
        "whatsapp": user.whatsapp_number,
        "daily_summary_hour": user.daily_summary_hour,
        "reminder_night_before_hour": user.reminder_night_before_hour,
        "reminder_2h_before": user.reminder_2h_before,
        "timezone": user.timezone,
        "google_connected": bool(user.google_token),
        "created_at": user.created_at.isoformat()
    }

@app.get("/api/v1/conversations/recent")
async def get_recent_conversations(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 10
):
    """Obtiene conversaciones recientes con Caro"""
    conversations = db.query(WhatsAppConversation).filter(
        WhatsAppConversation.user_id == user.id
    ).order_by(WhatsAppConversation.created_at.desc()).limit(limit).all()
    
    return {
        "count": len(conversations),
        "conversations": [
            {
                "id": conv.id,
                "user_message": conv.user_message,
                "bot_response": conv.bot_response,
                "status": conv.status,
                "created_at": conv.created_at.isoformat(),
                "google_event_id": conv.google_event_id
            }
            for conv in conversations
        ]
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
