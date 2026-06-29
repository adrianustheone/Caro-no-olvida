from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Base, User, CalendarEvent, Reminder, EventType
from services_google import GoogleCalendarService
from services_whatsapp import WhatsAppService

# Inicializa Celery
celery_app = Celery(
    'carolina_reminder',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Configura Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Argentina/Buenos_Aires',
)

# Base de datos
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Servicios
google_service = GoogleCalendarService(settings)
whatsapp_service = WhatsAppService(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN,
    settings.TWILIO_WHATSAPP_FROM
)


@celery_app.task(name='sync_all_calendars')
def sync_all_calendars():
    """
    Sincroniza Google Calendar cada 15 minutos
    Cuando sincroniza, automáticamente crea recordatorios
    """
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.is_active == True).all()
        
        for user in users:
            try:
                # Reconecta credenciales
                service = google_service.get_calendar_service(user.google_token)
                
                # Sincroniza eventos
                google_service.sync_events(user.id, service, db)
                
                # Automáticamente crea recordatorios para nuevos eventos
                create_reminders_for_user(user, db)
                
                print(f"✅ Sincronizados eventos para {user.name}")
            
            except Exception as e:
                print(f"❌ Error sincronizando {user.name}: {e}")
        
        return {"status": "success", "users_synced": len(users)}
    
    finally:
        db.close()


def create_reminders_for_user(user: User, db: sessionmaker):
    """
    Crea recordatorios automáticamente para eventos sin recordatorios
    - Recordatorio noche anterior (default 20:00 = 8pm)
    - Recordatorio 2 horas antes del evento
    """
    # Obtén eventos sin recordatorios
    events_without_reminders = db.query(CalendarEvent).filter(
        and_(
            CalendarEvent.user_id == user.id,
            CalendarEvent.is_completed == False,
            CalendarEvent.start_time >= datetime.utcnow()
        )
    ).all()
    
    for event in events_without_reminders:
        # Chequea si ya tiene recordatorios
        existing = db.query(Reminder).filter(
            Reminder.event_id == event.id
        ).first()
        
        if existing:
            continue  # Ya tiene recordatorios
        
        # RECORDATORIO 1: Noche anterior a las 20:00 (configurable)
        day_before = event.start_time - timedelta(days=1)
        reminder_night = Reminder(
            event_id=event.id,
            user_id=user.id,
            minutes_before=1440,  # 24 horas
            scheduled_for=day_before.replace(
                hour=user.reminder_night_before_hour, 
                minute=0, 
                second=0
            ),
            reminder_type='whatsapp'
        )
        db.add(reminder_night)
        
        # RECORDATORIO 2: 2 horas antes (si está habilitado)
        if user.reminder_2h_before:
            reminder_2h = Reminder(
                event_id=event.id,
                user_id=user.id,
                minutes_before=120,  # 2 horas
                scheduled_for=event.start_time - timedelta(hours=2),
                reminder_type='whatsapp'
            )
            db.add(reminder_2h)
    
    db.commit()


@celery_app.task(name='send_scheduled_reminders')
def send_scheduled_reminders():
    """
    Envía recordatorios que están vencidos
    Se ejecuta cada 5 minutos
    
    Recordatorios:
    - Noche anterior (hora configurable)
    - 2 horas antes
    """
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        
        # Busca recordatorios que deben enviarse AHORA
        pending_reminders = db.query(Reminder).filter(
            and_(
                Reminder.scheduled_for <= now,
                Reminder.sent_at.is_(None)
            )
        ).all()
        
        for reminder in pending_reminders:
            try:
                user = db.query(User).filter(User.id == reminder.user_id).first()
                event = db.query(CalendarEvent).filter(
                    CalendarEvent.id == reminder.event_id
                ).first()
                
                if not user or not event:
                    reminder.sent_at = datetime.utcnow()
                    reminder.sent_successfully = False
                    db.commit()
                    continue
                
                # Formatea mensaje según si es noche anterior o 2h antes
                if reminder.minutes_before == 1440:  # Noche anterior
                    message = f"🌙 RECORDATORIO NOCHE ANTERIOR\n\n"
                    message += f"📅 MAÑANA a las {event.start_time.strftime('%H:%M')}\n"
                    message += f"📌 {event.title}\n"
                    
                    if event.event_type == EventType.AUDIENCIA:
                        message += f"🏛️ {event.juzgado or 'Juzgado'}\n"
                        if event.location:
                            message += f"📍 {event.location}\n"
                    elif event.event_type == EventType.PLAZO:
                        message += f"⚠️ PLAZO CRÍTICO\n"
                    elif event.event_type == EventType.DOCUMENTO:
                        message += f"📋 Necesitás presentar/traer documentación\n"
                    
                    if event.description:
                        message += f"\nℹ️ {event.description[:150]}\n"
                    
                    message += f"\n💡 Preparate para mañana"
                
                elif reminder.minutes_before == 120:  # 2 horas antes
                    message = f"⏰ EN 2 HORAS - RECORDATORIO\n\n"
                    message += f"📌 {event.title}\n"
                    message += f"🕐 {event.start_time.strftime('%H:%M')}\n"
                    
                    if event.event_type == EventType.AUDIENCIA:
                        message += f"🏛️ {event.juzgado or 'Juzgado'}\n"
                        if event.location:
                            message += f"📍 {event.location}\n"
                    elif event.event_type == EventType.PLAZO:
                        message += f"⚠️ PLAZO CRÍTICO - No olvides\n"
                    elif event.event_type == EventType.DOCUMENTO:
                        message += f"📋 Trae: {event.description or 'documentación'}\n"
                    
                    message += f"\n⚡ ¡MOVE!"
                
                else:
                    message = whatsapp_service.format_reminder_message(event, reminder.minutes_before)
                
                # Envía por WhatsApp
                to_whatsapp = f"whatsapp:{user.whatsapp_number}"
                success = whatsapp_service.send_message(to_whatsapp, message)
                
                # Actualiza registro
                reminder.sent_at = datetime.utcnow()
                reminder.sent_successfully = success
                
                db.commit()
                
                print(f"✅ Recordatorio enviado a {user.name}: {event.title}")
            
            except Exception as e:
                print(f"❌ Error enviando recordatorio: {e}")
                db.rollback()
        
        return {"status": "success", "reminders_sent": len(pending_reminders)}
    
    finally:
        db.close()


@celery_app.task(name='send_daily_summary')
def send_daily_summary():
    """
    Envía resumen diario a la hora configurada por Carolina
    Default: 8:00 AM, pero configurable vía User.daily_summary_hour
    """
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.is_active == True).all()
        
        for user in users:
            try:
                # Obtén eventos de HOY
                today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                today_end = today_start + timedelta(days=1)
                
                today_events = db.query(CalendarEvent).filter(
                    and_(
                        CalendarEvent.user_id == user.id,
                        CalendarEvent.start_time >= today_start,
                        CalendarEvent.start_time < today_end,
                        CalendarEvent.is_completed == False
                    )
                ).order_by(CalendarEvent.start_time).all()
                
                if today_events:
                    message = whatsapp_service.format_daily_summary(today_events)
                    
                    to_whatsapp = f"whatsapp:{user.whatsapp_number}"
                    whatsapp_service.send_message(to_whatsapp, message)
                    
                    print(f"✅ Resumen diario enviado a {user.name} a las {user.daily_summary_hour}:00")
            
            except Exception as e:
                print(f"❌ Error enviando resumen diario: {e}")
        
        return {"status": "success"}
    
    finally:
        db.close()


@celery_app.task(name='check_plazo_alerts')
def check_plazo_alerts():
    """
    Verifica plazos próximos a vencer y envía alertas especiales
    Se ejecuta 2 veces al día
    """
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        days_to_check = [7, 3, 1, 0]  # 7 días, 3 días, 1 día, hoy
        
        for days in days_to_check:
            target_date = now + timedelta(days=days)
            target_start = target_date.replace(hour=0, minute=0, second=0)
            target_end = target_date.replace(hour=23, minute=59, second=59)
            
            # Busca eventos de tipo PLAZO en esas fechas
            plazo_events = db.query(CalendarEvent).filter(
                and_(
                    CalendarEvent.event_type == EventType.PLAZO,
                    CalendarEvent.start_time >= target_start,
                    CalendarEvent.start_time <= target_end,
                    CalendarEvent.is_completed == False
                )
            ).all()
            
            for event in plazo_events:
                try:
                    user = db.query(User).filter(User.id == event.user_id).first()
                    if not user:
                        continue
                    
                    message = whatsapp_service.format_plazo_alert(event, days)
                    
                    to_whatsapp = f"whatsapp:{user.whatsapp_number}"
                    whatsapp_service.send_message(to_whatsapp, message)
                    
                    print(f"✅ Alerta de plazo enviada: {event.title} ({days} días)")
                
                except Exception as e:
                    print(f"❌ Error en alerta de plazo: {e}")
        
        return {"status": "success"}
    
    finally:
        db.close()


# ============ CELERY BEAT SCHEDULE ============
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    # Sincronizar calendarios cada 15 minutos
    'sync-calendars-every-15-min': {
        'task': 'sync_all_calendars',
        'schedule': 60.0 * 15,
    },
    
    # Verificar recordatorios cada 5 minutos
    'send-reminders-every-5-min': {
        'task': 'send_scheduled_reminders',
        'schedule': 60.0 * 5,
    },
    
    # Resumen diario a las 8:00 AM Buenos Aires
    'daily-summary-8am': {
        'task': 'send_daily_summary',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM
    },
    
    # Alertas de plazos 2 veces al día (8:15 AM y 6:00 PM)
    'check-plazo-alerts-morning': {
        'task': 'check_plazo_alerts',
        'schedule': crontab(hour=8, minute=15),
    },
    'check-plazo-alerts-evening': {
        'task': 'check_plazo_alerts',
        'schedule': crontab(hour=18, minute=0),
    },
}
