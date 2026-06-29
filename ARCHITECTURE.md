# 🏗️ Arquitectura de Carolina Reminder

## Diagrama de flujos

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAROLINA (Samsung A55)                          │
│                       Google Calendar + WhatsApp                        │
└──────────────────────────┬──────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────────┐   ┌──────────┐    ┌─────────────┐
    │   Google   │   │ WhatsApp │    │  Calendarios│
    │  Calendar  │   │ (Twilio) │    │             │
    └──────┬─────┘   └─────┬────┘    └──────┬──────┘
           │               │                │
           └───────────────┼────────────────┘
                    ▼
        ┌──────────────────────────┐
        │   CAROLINA REMINDER API  │
        │      (FastAPI)           │
        │   http://localhost:8000  │
        └──────┬────────┬──────┬───┘
               │        │      │
        ┌──────▼─┐  ┌───▼──┐  ┌▼─────────┐
        │Sync    │  │Events│  │WhatsApp  │
        │Calendar│  │API   │  │Webhook   │
        └──────┬─┘  └───┬──┘  └┬─────────┘
               │        │      │
               └────────┼──────┘
                        ▼
        ┌──────────────────────────┐
        │   POSTGRESQL DATABASE    │
        │                          │
        │  • Users                 │
        │  • CalendarEvents        │
        │  • Reminders             │
        │  • TaskNotes             │
        │  • MessageLogs           │
        └──────┬─────────────────┬─┘
               │                 │
        ┌──────▼──┐        ┌─────▼──────┐
        │  Celery │        │    Redis   │
        │  Tasks  │        │   Cache    │
        └──────┬──┘        └─────┬──────┘
               │                 │
        ┌──────▼─────────────────▼──┐
        │   Background Workers      │
        │                           │
        │ • sync_all_calendars     │
        │ • send_scheduled_reminders│
        │ • send_daily_summary      │
        │ • check_plazo_alerts      │
        └──────────────────────────┘
```

---

## Flujo detallado de un recordatorio

```
1. SINCRONIZACIÓN (Cada 15 min)
   ├─ Celery task: sync_all_calendars()
   ├─ Conecta con Google Calendar API
   ├─ Obtiene eventos próximos 90 días
   ├─ Detecta tipo: [AUDIENCIA] [PLAZO] [DOCUMENTO]
   └─ Guarda en PostgreSQL

2. CREACIÓN DE RECORDATORIOS (Automático)
   ├─ Para cada evento detectado:
   │  ├─ Si AUDIENCIA: recordatorios a 24h, 2h, 30min
   │  ├─ Si PLAZO: recordatorios cada día hasta vencimiento
   │  └─ Si DOCUMENTO: recordatorio 1 día antes
   └─ Se guardan en tabla reminders

3. ENVÍO DE ALERTAS (Cada 5 min)
   ├─ Celery task: send_scheduled_reminders()
   ├─ Busca recordatorios vencidos
   ├─ Formatea mensaje según tipo
   ├─ Conecta Twilio WhatsApp API
   ├─ Envía a Carolina: whatsapp:+541234567890
   └─ Registra en MessageLogs

4. Carolina RECIBE
   ├─ Notificación en Samsung A55
   │  └─ 🏛️ RECORDATORIO: MAÑANA
   │     📅 10:00 - Audiencia TOC Nº4 García
   │     Juzgado: San Martín
   └─ Puede responder comandos:
      └─ "hoy", "nota: ...", "próximos 7 días"
```

---

## Stack tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Carolina)                    │
│  ├─ Google Calendar (Lee eventos)                           │
│  ├─ WhatsApp (Recibe recordatorios)                         │
│  └─ Samsung A55 (Dispositivo)                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BACKEND LAYER (API)                      │
│  ├─ FastAPI (Framework web)                                 │
│  ├─ Python 3.11 (Runtime)                                   │
│  ├─ SQLAlchemy (ORM)                                        │
│  └─ Uvicorn (ASGI server)                                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  BACKGROUND PROCESSING                      │
│  ├─ Celery (Task queue)                                     │
│  ├─ Redis (Message broker)                                  │
│  ├─ Celery Beat (Task scheduler)                            │
│  └─ Workers (Ejecutan tasks)                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATIONS                             │
│  ├─ Google Calendar API (Sync eventos)                      │
│  ├─ Twilio WhatsApp API (Enviar mensajes)                   │
│  └─ PostgreSQL (Persistencia)                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT OPTIONS                       │
│  ├─ Local: Docker Compose                                   │
│  ├─ Railway: Container + DB automático                      │
│  └─ Render: Similar a Railway                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Modelos de datos (Relaciones)

```
┌────────────┐
│   User     │ (Carolina)
├────────────┤
│ id         │◄──────────────┐
│ name       │                │
│ whatsapp   │                │
│ google_*   │                │
│ timezone   │                │ 1:N
└────────────┘                │
                              │
    ┌──────────────────────────┴──────────────────────┐
    │                                                  │
    ▼                                                  ▼
┌──────────────────┐                         ┌──────────────────┐
│ CalendarEvent    │                         │  TaskNote        │
├──────────────────┤                         ├──────────────────┤
│ id               │                         │ id               │
│ user_id (FK)     │◄────────┐               │ user_id (FK)     │
│ google_event_id  │         │               │ content          │
│ title            │         │1:N            │ tags             │
│ start_time       │         │               │ is_completed     │
│ event_type       │         │               └──────────────────┘
│ is_completed     │         │
└────────┬─────────┘         │
         │                   │
         │ 1:N               │
         │                   │
         ▼                   │
    ┌─────────────┐          │
    │ Reminder    │          │
    ├─────────────┤          │
    │ id          │          │
    │ event_id-──┬┘          │
    │ minutes    │           │
    │ scheduled  │           │
    │ sent_at    │           │
    └─────────────┘          │
                             │
                    ┌────────┘
                    │
                    ▼
            ┌──────────────────┐
            │ MessageLog       │
            ├──────────────────┤
            │ id               │
            │ content          │
            │ sent_at          │
            │ twilio_sid       │
            └──────────────────┘
```

---

## Timeline típico de un día para Carolina

```
┌─────────────────────────────────────────────────────────────┐
│                     DÍA TIPO DE CAROLINA                    │
└─────────────────────────────────────────────────────────────┘

06:30 AM
  └─ Despierta, cansada. Fibromialgia activa. Niebla mental.

07:00 AM
  └─ ✨ WhatsApp trae RESUMEN DIARIO:
     │  📋 Hoy JUEVES:
     │  🏛️ AUDIENCIAS:
     │     10:00 - Audiencia mediación García
     │  ⏰ PLAZOS:
     │     Vencimiento apelación López (hoy)
     │  📋 DOCUMENTACIÓN:
     │     Traer: sentencia anterior, prueba cohabitación
     └─ ✅ Carolina ahora sabe QUÉ HACER (sin leer calendar)

09:00 AM
  └─ Celery → Sync automático de Google Calendar (cada 15 min)

09:30 AM
  └─ ⏰ Alerta: "EN 30 MIN - Audiencia García 10:00"
     ├─ Location: Juzgado Familia Nº3, San Isidro
     ├─ Cliente: García, María
     └─ Case: 45678/2024

10:00 AM
  └─ Audiencia

14:00 PM
  └─ 💼 Recordatorio: "Reunión cliente López - 14:00"
     ├─ Traer: DNI, escritos
     └─ Carolina responde: "✅ Completado"

16:00 PM
  └─ 🔴 ALERTA URGENTE:
     ⏰ VENCE HOY - Recurso apelación López
     ├─ Plazo: ABSOLUTO (no hay prórroga)
     ├─ Presentar ante: TOC Federal Nº2
     └─ Carolina envía: "nota: recurso entregado a las 16:30"

18:00 PM
  └─ Niebla mental nuevamente
     └─ Nota rápida: "recordar que cliente dijo que se muda 30/7"

19:30 PM
  └─ Dashboard web (desde laptop):
     ├─ Ver eventos completados ✅
     ├─ Ver notas guardadas
     └─ Exportar caso García a PDF para archivo

21:00 PM
  └─ Celery task: check_plazo_alerts()
     └─ Avisa de plazos próximos (7 días, 3 días, 1 día)
```

---

## Ventajas de esta arquitectura para Carolina

✅ **Sin fricción**: Solo conecta Google Calendar 1 vez  
✅ **Automático**: Todo corre en background (Celery)  
✅ **Resiliente**: Si falla, reintentas (Celery retry)  
✅ **Escalable**: Funciona igual con 1 evento o 100  
✅ **Privado**: Todo en tu servidor (Railway/local)  
✅ **Forense**: Genera logs completos (auditoría)  
✅ **Extensible**: Fácil agregar OUCHURUS, análisis IA, etc.  

---

## Próximas integraciones posibles

```
┌──────────────────────────────────────────────────────────┐
│         CAROLINA REMINDER v1.0+ INTEGRATIONS            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────┐        ┌──────────────────┐       │
│  │   OUCHURUS      │        │  Google Workspace│       │
│  │  (Análisis IA)  │        │   (Mail/Drive)   │       │
│  └────────┬────────┘        └────────┬─────────┘       │
│           │                         │                  │
│  ┌────────▼──────────────────────────▼───────┐        │
│  │        CAROLINA REMINDER (Core)            │        │
│  └────────┬──────────────────────────┬────────┘        │
│           │                          │                 │
│  ┌────────▼─────┐            ┌──────▼─────────┐      │
│  │  JUBA/SAIJ   │            │  Zapier/IFTTT  │      │
│  │ (Jurisprudencia)         │ (Automation)    │      │
│  └──────────────┘            └─────────────────┘      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

**Hecho con 💪 para Carolina**

*Documentación v1.0 - Junio 2026*
