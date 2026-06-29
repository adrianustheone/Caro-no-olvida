from twilio.rest import Client
from datetime import datetime
from typing import List

from models import MessageLog, CalendarEvent, EventType


class WhatsAppService:
    """Servicio para enviar recordatorios por WhatsApp a Carolina"""
    
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number  # whatsapp:+14155552671
    
    def send_message(self, to_whatsapp: str, message: str) -> bool:
        """
        Envía un mensaje por WhatsApp
        to_whatsapp: Ej: "whatsapp:+541234567890"
        """
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_whatsapp
            )
            return True
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
            return False
    
    def format_reminder_message(self, event: CalendarEvent, minutes_before: int) -> str:
        """Formatea un recordatorio según tipo de evento"""
        
        emoji_map = {
            EventType.AUDIENCIA: "🏛️",
            EventType.PLAZO: "⏰",
            EventType.DOCUMENTO: "📋",
            EventType.REUNION: "💼",
            EventType.OTRO: "📅"
        }
        
        emoji = emoji_map.get(event.event_type, "📅")
        
        # Calcula tiempo restante
        time_left = ""
        if minutes_before == 1440:  # 24 horas
            time_left = "MAÑANA"
        elif minutes_before == 120:  # 2 horas
            time_left = "EN 2 HORAS"
        elif minutes_before == 30:  # 30 minutos
            time_left = "EN 30 MIN"
        
        # Mensaje base
        message = f"{emoji} RECORDATORIO: {time_left}\n"
        message += f"📅 {event.start_time.strftime('%H:%M')}\n"
        message += f"📌 {event.title}\n"
        
        # Información contextual según tipo
        if event.event_type == EventType.AUDIENCIA:
            message += f"\n🏛️ Juzgado: {event.juzgado or 'Ver calendario'}\n"
            if event.location:
                message += f"📍 Ubicación: {event.location}\n"
        
        elif event.event_type == EventType.PLAZO:
            message += f"\n⚠️ PLAZO CRÍTICO - No olvides\n"
        
        elif event.event_type == EventType.DOCUMENTO:
            message += f"\n📋 Necesitás presentar/traer documentación\n"
        
        if event.description:
            message += f"\nℹ️ {event.description[:150]}\n"
        
        message += f"\n---"
        
        return message
    
    def format_daily_summary(self, events: List[CalendarEvent]) -> str:
        """Genera resumen diario de eventos para Carolina"""
        
        if not events:
            return "✅ Hoy no tenés eventos programados.\n¡Aprovecha para descansar!"
        
        message = "📋 RESUMEN DEL DÍA\n"
        message += f"🗓️ {events[0].start_time.strftime('%A, %d de %B')}\n\n"
        
        # Agrupa por tipo
        by_type = {}
        for event in events:
            et = event.event_type
            if et not in by_type:
                by_type[et] = []
            by_type[et].append(event)
        
        # Audiencias primero
        if EventType.AUDIENCIA in by_type:
            message += "🏛️ AUDIENCIAS:\n"
            for event in by_type[EventType.AUDIENCIA]:
                message += f"  • {event.start_time.strftime('%H:%M')} - {event.title}\n"
        
        # Plazos (urgente)
        if EventType.PLAZO in by_type:
            message += "\n⏰ PLAZOS (URGENTE):\n"
            for event in by_type[EventType.PLAZO]:
                message += f"  • {event.title}\n"
        
        # Documentos
        if EventType.DOCUMENTO in by_type:
            message += "\n📋 DOCUMENTACIÓN:\n"
            for event in by_type[EventType.DOCUMENTO]:
                message += f"  • {event.start_time.strftime('%H:%M')} - {event.title}\n"
        
        # Reuniones
        if EventType.REUNION in by_type:
            message += "\n💼 REUNIONES:\n"
            for event in by_type[EventType.REUNION]:
                message += f"  • {event.start_time.strftime('%H:%M')} - {event.title}\n"
        
        message += "\n💡 Respondé con 'detalle X' para más info"
        
        return message
    
    def format_plazo_alert(self, event: CalendarEvent, days_remaining: int) -> str:
        """Alerta especial para plazos procesales"""
        
        if days_remaining == 0:
            urgency = "🚨 HOY VENCE"
        elif days_remaining == 1:
            urgency = "⚠️ MAÑANA VENCE"
        elif days_remaining <= 3:
            urgency = "🔴 VENCE EN " + str(days_remaining) + " DÍAS"
        else:
            urgency = f"🟡 Vence en {days_remaining} días"
        
        message = f"{urgency}\n"
        message += f"⚖️ {event.title}\n"
        if event.case_number:
            message += f"📑 Caso: {event.case_number}\n"
        if event.description:
            message += f"ℹ️ {event.description[:100]}\n"
        message += f"\n⏱️ Días restantes: {days_remaining}\n"
        
        return message
    
    async def log_message(self, user_id: int, to_whatsapp: str, content: str, 
                         message_type: str, db_session, twilio_sid: str = None):
        """Registra en BD que se envió un mensaje"""
        log = MessageLog(
            user_id=user_id,
            whatsapp_number=to_whatsapp,
            message_content=content,
            message_type=message_type,
            twilio_sid=twilio_sid,
            sent_successfully=True
        )
        db_session.add(log)
        db_session.commit()
