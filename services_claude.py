import json
from datetime import datetime, timedelta
from typing import Optional
from anthropic import Anthropic

# Cliente Anthropic
client = Anthropic()


class CaroNoOlvidaAI:
    """
    AI assistant para Carolina que entiende lenguaje natural
    y crea eventos en Google Calendar automáticamente
    """
    
    def __init__(self, api_key: str = None):
        self.model = "claude-opus-4-6"
        self.conversation_history = []
    
    def parse_event_from_message(self, message: str) -> dict:
        """
        Convierte un mensaje natural de Carolina en datos de evento
        
        Ej: "Agendar audiencia García mañana a las 10:00"
        → {
            "title": "Audiencia García",
            "date": "2026-06-28",
            "time": "10:00",
            "type": "AUDIENCIA",
            "description": "..."
        }
        """
        
        # Prompt para Claude
        prompt = f"""Eres Caro, asistente de Carolina, abogada especialista en derecho de familia.

Carolina acaba de escribir por WhatsApp:
"{message}"

Tu tarea: EXTRAE la información del evento que quiere agendar y retorna SOLO un JSON válido (sin explicaciones ni markdown).

Si Carolina quiere agendar algo, retorna:
{{
    "action": "create_event",
    "title": "Título del evento",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "type": "AUDIENCIA|PLAZO|DOCUMENTO|REUNION|OTRO",
    "client_name": "Nombre del cliente (si aplica)",
    "case_number": "Número de caso (si aplica)",
    "juzgado": "Juzgado/sala (si aplica)",
    "location": "Lugar (si aplica)",
    "description": "Descripción o notas",
    "confidence": 0.0-1.0
}}

Si NO logras extraer información clara (fecha/hora ambigua, información faltante):
{{
    "action": "ask_clarification",
    "question": "¿Qué pregunta necesito hacerle a Carolina?",
    "extracted": {{
        "title": "Lo que entendí",
        "date": null,
        "time": null
    }}
}}

Si es un comando genérico (no es agendar):
{{
    "action": "other",
    "response": "Respuesta de Carolina"
}}

REGLAS:
- Las fechas deben ser YYYY-MM-DD
- Las horas deben ser HH:MM (24h)
- Si dice "mañana", calcula la fecha (hoy es {datetime.utcnow().strftime('%Y-%m-%d')})
- Si dice "próxima semana lunes", calcula correctamente
- Para audiencias/mediaciones: type="AUDIENCIA"
- Para plazos vencimiento: type="PLAZO"
- Para documentación: type="DOCUMENTO"
- Si es reunión con cliente: type="REUNION"

Responde SOLO JSON, sin ningún otro texto."""

        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extrae el JSON de la respuesta
            response_text = response.content[0].text.strip()
            
            # Si tiene markdown backticks, los elimina
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            return result
        
        except json.JSONDecodeError as e:
            return {
                "action": "error",
                "message": f"Error parsing response: {str(e)}",
                "raw_response": response_text if 'response_text' in locals() else None
            }
        except Exception as e:
            return {
                "action": "error",
                "message": str(e)
            }
    
    def generate_confirmation_message(self, event_data: dict) -> str:
        """
        Genera un mensaje amable de confirmación para Carolina
        """
        if event_data.get("action") == "error":
            return f"❌ Disculpa, hubo un error procesando tu mensaje: {event_data.get('message')}"
        
        if event_data.get("action") == "ask_clarification":
            return f"🤔 {event_data.get('question')}\n\nLo que entendí hasta ahora:\n{json.dumps(event_data.get('extracted'), indent=2, ensure_ascii=False)}"
        
        if event_data.get("action") == "other":
            return event_data.get("response", "Entendido")
        
        if event_data.get("action") == "create_event":
            emoji_map = {
                "AUDIENCIA": "🏛️",
                "PLAZO": "⏰",
                "DOCUMENTO": "📋",
                "REUNION": "💼",
                "OTRO": "📅"
            }
            
            emoji = emoji_map.get(event_data.get("type", "OTRO"), "📅")
            
            message = f"✅ Evento agendado!\n\n"
            message += f"{emoji} {event_data.get('title')}\n"
            message += f"📅 {event_data.get('date')} a las {event_data.get('time')}\n"
            
            if event_data.get("juzgado"):
                message += f"🏛️ {event_data.get('juzgado')}\n"
            
            if event_data.get("location"):
                message += f"📍 {event_data.get('location')}\n"
            
            if event_data.get("case_number"):
                message += f"📑 Caso: {event_data.get('case_number')}\n"
            
            message += f"\n📱 También aparece en Google Calendar"
            message += f"\n💬 Respondé 'confirmar' si está bien o 'cancelar' si cambiaste de idea"
            
            return message
        
        return "✅ Listo"
    
    def understand_yes_no(self, message: str) -> str:
        """
        Entiende si Carolina dijo sí, no, cancelar, etc.
        Retorna: 'yes', 'no', 'unknown'
        """
        msg_lower = message.lower().strip()
        
        yes_words = ["sí", "si", "confirmar", "ok", "dale", "bueno", "perfecto", "listo", "yes", "yep"]
        no_words = ["no", "cancelar", "cancel", "nope", "nah", "mejor no"]
        
        for word in yes_words:
            if word in msg_lower:
                return "yes"
        
        for word in no_words:
            if word in msg_lower:
                return "no"
        
        return "unknown"
