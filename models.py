from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    whatsapp_number = Column(String(20), unique=True)  # Ej: +541234567890
    google_token = Column(Text)  # Token OAuth de Google
    google_refresh_token = Column(Text)
    google_calendar_id = Column(String(255))  # ID del calendar
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Preferencias de recordatorios CONFIGURABLES
    daily_summary_hour = Column(Integer, default=8)  # 8am default - CONFIGURABLE
    timezone = Column(String(50), default="America/Argentina/Buenos_Aires")
    
    # Recordatorio noche anterior (default 20:00 = 8pm)
    reminder_night_before_hour = Column(Integer, default=20)
    # Recordatorio 2 horas antes (default True)
    reminder_2h_before = Column(Boolean, default=True)


class EventType(str, enum.Enum):
    AUDIENCIA = "audiencia"  # Mediación, juzgado
    PLAZO = "plazo"  # Vencimiento de recurso
    DOCUMENTO = "documento"  # Entregar/traer prueba
    REUNION = "reunion"  # Reunión con cliente
    OTRO = "otro"


class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    google_event_id = Column(String(255), unique=True)  # ID único de Google
    title = Column(String(255))
    description = Column(Text, nullable=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(255), nullable=True)
    event_type = Column(Enum(EventType), default=EventType.OTRO)
    
    # Datos de familia
    client_name = Column(String(100), nullable=True)  # Ej: "García, María"
    case_number = Column(String(50), nullable=True)  # Ej: "23456/2024"
    juzgado = Column(String(255), nullable=True)  # Ej: "Juzgado Familia Nº 3"
    
    # Control
    is_reminded_24h = Column(Boolean, default=False)
    is_reminded_2h = Column(Boolean, default=False)
    is_reminded_30min = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    
    synced_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)  # FK a CalendarEvent
    user_id = Column(Integer)
    
    # Tipo de recordatorio
    minutes_before = Column(Integer)  # 1440 (24h), 120 (2h), 30 (30min)
    reminder_type = Column(String(50))  # 'whatsapp', 'app', etc
    
    scheduled_for = Column(DateTime)
    sent_at = Column(DateTime, nullable=True)
    sent_successfully = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class MessageLog(Base):
    __tablename__ = "message_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    whatsapp_number = Column(String(20))
    message_content = Column(Text)
    message_type = Column(String(50))  # 'reminder', 'summary', 'alert'
    
    sent_at = Column(DateTime, default=datetime.utcnow)
    twilio_sid = Column(String(255), nullable=True)
    sent_successfully = Column(Boolean, default=True)


class TaskNote(Base):
    __tablename__ = "task_notes"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    event_id = Column(Integer, nullable=True)  # Opcional: relacionada a evento
    
    content = Column(Text)
    tags = Column(String(255), nullable=True)  # Ej: "traer_documento,urgente"
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class WhatsAppConversation(Base):
    __tablename__ = "whatsapp_conversations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    whatsapp_number = Column(String(20))
    
    # Mensaje de Carolina
    user_message = Column(Text)
    
    # Interpretación de Claude
    parsed_data = Column(Text)  # JSON: acción, tipo evento, fecha, etc.
    
    # Respuesta de Caro
    bot_response = Column(Text)
    
    # Seguimiento
    status = Column(String(50))  # 'pending_confirmation', 'confirmed', 'cancelled'
    
    # Si se creó evento, guardamos el ID
    created_event_id = Column(Integer, nullable=True)
    google_event_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
