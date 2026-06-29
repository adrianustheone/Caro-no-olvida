# 💬 Caro No Olvida

**Asistente conversacional por WhatsApp para abogadas que luchan contra la fibromialgia**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 ¿Qué es Caro No Olvida?

Carolina es abogada. Tiene fibromialgia. Algunos días la niebla mental le gana.

**Caro No Olvida** es su asistente que:
- ✅ **Entiende lenguaje natural**: "Agendar audiencia García mañana 10:00"
- ✅ **Crea en Google Calendar**: Carolina ve visual
- ✅ **Envía recordatorios**: Noche anterior + 2 horas antes
- ✅ **No requiere concentración**: Todo por WhatsApp
- ✅ **Es gratis**: Corre en Railway sin costo

---

## 💬 Flujo conversacional

```
Carolina:     "Agendar audiencia García mañana 10:00"
                            ↓
Caro (Claude): Interpreta mensaje
                            ↓
Google Calendar: Crea evento
                            ↓
Carolina:     "✅ Confirmado! 
              Recordatorios: noche anterior + 2h"
                            ↓
Google Calendar: Evento visible
                            ↓
WhatsApp:     Recordatorios automáticos ⏰
```

---

## 🚀 Empezar en 30 minutos

### 👉 [GUÍA PASO A PASO](./SETUP_STEP_BY_STEP.md)

O si preferís comando único:

```bash
bash setup-railway.sh
```

---

## 📋 ¿Cómo usa Carolina Caro?

### Ejemplos:

```
"Agendar audiencia García mañana 10:00"
"Plazo vencimiento 15 de agosto"
"Reunión López viernes 3pm en mi oficina"
"Mediación caso 12345/2024 juzgado familia 3 martes"
"Cambiar resumen diario a las 7am"
"Ver próximos eventos"
```

### Caro responde:

```
✅ Evento agendado!

🏛️ Audiencia García
📅 2026-06-28 a las 10:00
📍 Juzgado: [Donde sea]
📱 También aparece en Google Calendar

Recordatorios:
🌙 Noche anterior: 20:00
⏰ 2 horas antes: 08:00
```

---

## 🛠️ Stack técnico

```
FastAPI             → API
Claude API          → Entiende lenguaje natural
Google Calendar API → Sincronización visual
Twilio WhatsApp     → Mensajes
PostgreSQL          → Base de datos
Redis + Celery      → Tasks automáticas
Railway             → Deployment (gratis)
```

---

## 📊 Capacidades

| Capacidad | Detalles |
|-----------|----------|
| 🧠 **NLP** | Claude entiende español, fechas, horas |
| 📅 **Calendarios** | Sincroniza con Google Calendar visual |
| 💬 **Chat** | Conversaciones naturales por WhatsApp |
| 🔔 **Recordatorios** | Noche anterior + 2 horas antes |
| ⚖️ **Derecho de familia** | Detecta audiencias, plazos, documentos |
| 📝 **Historial** | Guarda conversaciones de Carolina |
| ⚙️ **Configurable** | Cambia horarios sin código |

---

## 📱 Recordatorios automáticos

```
NOCHE ANTERIOR (20:00 default)
🌙 "RECORDATORIO NOCHE ANTERIOR
   MAÑANA 10:00 - Audiencia García
   Juzgado: San Martín
   Preparate para mañana"

2 HORAS ANTES
⏰ "EN 2 HORAS
   Audiencia García 14:00
   🏛️ Juzgado: San Martín
   ¡MOVE!"

RESUMEN DIARIO (8:00 AM default)
📋 "HOY VIERNES:
   🏛️ 10:00 - Audiencia García
   ⏰ 15:00 - PLAZO venciendo"
```

---

## 📚 Documentación

- **[SETUP_STEP_BY_STEP.md](./SETUP_STEP_BY_STEP.md)** ← **COMIENZA AQUÍ** 👈
- [GUIDE_USAGE.md](./GUIDE_USAGE.md) - Cómo usar Caro
- [CARO_NO_OLVIDA.md](./CARO_NO_OLVIDA.md) - Cambios técnicos
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Diagramas
- [RAILWAY.md](./RAILWAY.md) - Deploy en Railway
- [ROADMAP.md](./ROADMAP.md) - Features futuras

---

## 💻 Para desarrolladores

### Requisitos
- Python 3.9+
- PostgreSQL (local)
- Redis (local)
- Credenciales: Google OAuth, Twilio, Claude API

### Instalar local

```bash
git clone https://github.com/[usuario]/caro-no-olvida
cd caro-no-olvida
cp .env.example .env
# Editar .env con credenciales

# Opción A: Docker
docker-compose up

# Opción B: Manual
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Tests

```bash
# Sincronizar calendarios
curl http://localhost:8000/api/v1/events/today

# Ver configuración
curl http://localhost:8000/api/v1/user/config

# Simular WhatsApp
curl -X POST http://localhost:8000/api/v1/whatsapp/webhook \
  -d "From=whatsapp:+541234567890" \
  -d "Body=Agendar audiencia García mañana 10:00"
```

---

## 🔧 Configuración

### Recordatorios

```bash
# Cambiar resumen diario a 7am
curl -X POST "https://caro.railway.app/api/v1/settings/reminders?daily_summary_hour=7"

# Cambiar noche anterior a 19:00
curl -X POST "https://caro.railway.app/api/v1/settings/reminders?reminder_night_before_hour=19"

# Deshabilitar recordatorio 2h antes
curl -X POST "https://caro.railway.app/api/v1/settings/reminders?reminder_2h_before=false"
```

---

## 💰 Costos

| Servicio | Costo/mes |
|----------|-----------|
| Railway (DB + API) | $3.50 |
| Claude API | $2-5 |
| Twilio WhatsApp | $1 |
| Google Calendar | Gratis |
| **TOTAL** | **~$6-10** |
| **Railway gratis** | -$5 ✅ |
| **Neto** | **~$1-5** o **gratis** |

---

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el repo
2. Crea rama: `git checkout -b feature/nueva-feature`
3. Commit: `git commit -m "Add: descripción"`
4. Push: `git push origin feature/nueva-feature`
5. Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](./LICENSE)

---

## 💜 Agradecimientos

Hecho para Carolina, una abogada valiente que no se deja vencer por la fibromialgia.

Y para todos los que luchan contra enfermedades invisibles pero reales.

**Caro No Olvida** es un recordatorio de que la tecnología debe servir para hacer la vida más fácil.

---

## 🚀 ¿Listo?

**👉 [Guía paso a paso - 30 minutos](./SETUP_STEP_BY_STEP.md)**

O ejecutá:
```bash
bash setup-railway.sh
```

---

## 📞 Soporte

- Documentación: Ver carpeta `*.md`
- Issues: GitHub Issues
- Ayuda: Contactá a Adrián (@rodriguezdiaz)

---

**Caro No Olvida v2.0**  
*Asistente conversacional para abogadas*  
Junio 2026 | Made with ❤️ by Adrián
