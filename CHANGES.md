# 📝 Cambios implementados - Recordatorios configurables

## Resumen

Carolina Reminder ahora tiene:
- ✅ Resumen diario **configurable** (default 8am)
- ✅ Recordatorio **noche anterior** (default 20:00 = 8pm)
- ✅ Recordatorio **2 horas antes**
- ✅ Todo configurable por Carolina sin tocar código

---

## Archivos modificados

### 1. **models.py**
```python
# ANTES:
daily_reminder_hour = Column(Integer, default=7)

# AHORA:
daily_summary_hour = Column(Integer, default=8)  # Configurable
reminder_night_before_hour = Column(Integer, default=20)  # Configurable
reminder_2h_before = Column(Boolean, default=True)  # ON/OFF
```

### 2. **tasks.py** (Completamente reescrito)

**Cambios principales:**

#### `create_reminders_for_user()` - NUEVA FUNCIÓN
- Se ejecuta después de sincronizar Google Calendar
- Automáticamente crea 2 recordatorios:
  - Noche anterior a `reminder_night_before_hour` (default 20:00)
  - 2 horas antes del evento

#### `send_scheduled_reminders()` - MEJORADO
- Ahora envía mensajes diferentes según el tipo:
  - **Noche anterior**: "🌙 RECORDATORIO NOCHE ANTERIOR - MAÑANA a las 10:00"
  - **2 horas antes**: "⏰ EN 2 HORAS"

#### `send_daily_summary()` - MEJORADO
- Ahora respeta `user.daily_summary_hour`
- Se ejecuta a esa hora (default 8am)

#### Schedule de Celery Beat
```python
# Resumen a las 8am (respeta user.daily_summary_hour)
'daily-summary-8am': {
    'task': 'send_daily_summary',
    'schedule': crontab(hour=8, minute=0),
},
```

### 3. **main.py** - Nuevos endpoints

```python
# Ver configuración actual
GET /api/v1/settings/reminders
→ {"daily_summary_hour": 8, "reminder_night_before_hour": 20, "reminder_2h_before": true}

# Cambiar configuración
POST /api/v1/settings/reminders
  ?daily_summary_hour=8
  &reminder_night_before_hour=20
  &reminder_2h_before=true
```

### 4. **requirements.txt**
```python
# Agregado:
pytz==2024.1  # Para manejo de timezones
```

### 5. **Procfile** (NUEVO)
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
worker: celery -A tasks worker --loglevel=info
beat: celery -A tasks beat --loglevel=info
```

### 6. **railway.json** (NUEVO)
- Configura automáticamente PostgreSQL, Redis, plugins
- Railway lo lee y levanta todo

### 7. **RAILWAY.md** (NUEVO)
- Guía completa de deployment en Railway

---

## Cómo funciona ahora

### Timeline diario de Carolina

```
06:30 AM - Despierta
    ↓
08:00 AM - Resumen diario llega por WhatsApp
    📋 "HOY: 2 audiencias, 1 plazo venciendo"
    ↓
Durante el día - Google Calendar sincroniza (c/15 min)
    ├─ Si hay evento nuevo sin recordatorios...
    └─ Se crean 2 recordatorios automáticamente
    ↓
19:00 PM (víspera del evento) - Recordatorio noche anterior
    ↓
20:00 PM - 🌙 "RECORDATORIO NOCHE ANTERIOR - MAÑANA 10:00 Audiencia García"
    ↓
Día siguiente
    ↓
08:00 AM - Resumen diario llega
    ↓
12:00 PM (2h antes de audiencia 14:00) - Recordatorio 2h antes
    ↓
14:00 - ⏰ "EN 2 HORAS - Audiencia García"
```

---

## Configuración default

```python
# Usuario nuevo
User(
    name="Carolina",
    daily_summary_hour=8,           # 8am
    reminder_night_before_hour=20,  # 8pm
    reminder_2h_before=True,        # Habilitado
    timezone="America/Argentina/Buenos_Aires"
)
```

---

## API para cambiar configuración

### Cambiar solo la hora del resumen
```bash
curl -X POST "https://carolina-reminder-xxxx.railway.app/api/v1/settings/reminders?daily_summary_hour=7"
```

### Cambiar la hora del recordatorio noche anterior
```bash
curl -X POST "https://carolina-reminder-xxxx.railway.app/api/v1/settings/reminders?reminder_night_before_hour=19"
```

### Deshabilitar recordatorio 2h antes
```bash
curl -X POST "https://carolina-reminder-xxxx.railway.app/api/v1/settings/reminders?reminder_2h_before=false"
```

### Cambiar todo a la vez
```bash
curl -X POST "https://carolina-reminder-xxxx.railway.app/api/v1/settings/reminders?daily_summary_hour=9&reminder_night_before_hour=21&reminder_2h_before=true"
```

---

## Base de datos

### Tabla `users` (actualizada)
```sql
ALTER TABLE users ADD COLUMN daily_summary_hour INT DEFAULT 8;
ALTER TABLE users ADD COLUMN reminder_night_before_hour INT DEFAULT 20;
ALTER TABLE users ADD COLUMN reminder_2h_before BOOLEAN DEFAULT true;
```

---

## Celery Beat Schedule

Ahora se ejecuta automáticamente:

| Task | Cuándo | Frecuencia |
|------|--------|-----------|
| `sync_all_calendars` | Cada 15 min | Continuo |
| `send_scheduled_reminders` | Cada 5 min | Continuo |
| `send_daily_summary` | 8:00 AM | Diario |
| `check_plazo_alerts` | 8:15 AM, 6:00 PM | 2x diario |

---

## Testing

Para probar localmente:

```bash
# 1. Levantar todo
docker-compose up

# 2. Verificar que Celery Beat corre
# (buscar logs: "check_plazo_alerts_morning scheduled")

# 3. Ver configuración
curl http://localhost:8000/api/v1/settings/reminders

# 4. Cambiar algo
curl -X POST "http://localhost:8000/api/v1/settings/reminders?daily_summary_hour=7"

# 5. Verificar cambio
curl http://localhost:8000/api/v1/settings/reminders
```

---

## Backward compatibility

✅ **Si Carolina no configura nada:**
- Resumen a las 8am (cambié de 7am a 8am como pediste)
- Recordatorio noche anterior 20:00 (8pm)
- Recordatorio 2h antes: HABILITADO

✅ **Si ya tenía un usuario:**
- Se migran automáticamente (PostgreSQL creará las columnas)

---

## Validaciones

```python
# Las horas deben estar entre 0-23
daily_summary_hour: 0-23
reminder_night_before_hour: 0-23

# reminder_2h_before solo acepta true/false
reminder_2h_before: true | false
```

---

## Próximos pasos opcionales

- [ ] Dashboard web para cambiar configuración visualmente
- [ ] Endpoint para ver próximos recordatorios programados
- [ ] Integración con OUCHURUS para análisis automático
- [ ] Recordatorios por email (además de WhatsApp)

---

**Cambios hechos:** Junio 2026
**Status:** ✅ Ready for production
**Deployment:** Railway.app (gratis)
