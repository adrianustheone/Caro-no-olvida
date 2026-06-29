# 🚀 Deploy Carolina Reminder en Railway (Gratis)

Railway te ofrece **$5 USD/mes gratis** para experimentar. Carolina Reminder corre perfectamente dentro de ese presupuesto.

---

## ⚡ Quickstart Railway (10 minutos)

### Paso 1: Crear cuenta en Railway
1. Ve a https://railway.app
2. Sign up con GitHub (recomendado)
3. Conecta tu cuenta

### Paso 2: Clonar repo en GitHub
```bash
# Si aún no tenés en GitHub:
git clone https://github.com/tuusuario/carolina-reminder
cd carolina-reminder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tuusuario/carolina-reminder
git push -u origin main
```

### Paso 3: Crear proyecto en Railway

1. **Ve a Railway Dashboard** → New Project
2. Selecciona **"Deploy from GitHub"**
3. Conecta tu repo `carolina-reminder`
4. Railway automáticamente:
   - ✅ Lee el `Dockerfile`
   - ✅ Levanta PostgreSQL
   - ✅ Levanta Redis
   - ✅ Configura variables

### Paso 4: Agregar variables de entorno

En Railway Dashboard → Project → Variables:

```
# Google OAuth
GOOGLE_CLIENT_ID = tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET = tu-secret
GOOGLE_REDIRECT_URI = https://carolina-reminder-xxxx.railway.app/api/v1/auth/google/callback

# Twilio
TWILIO_ACCOUNT_SID = ACxxxxxxxx
TWILIO_AUTH_TOKEN = tu-token
TWILIO_WHATSAPP_FROM = whatsapp:+14155552671

# Database (se genera automáticamente)
DATABASE_URL = (Railway la crea)

# Redis (se genera automáticamente)
CELERY_BROKER_URL = (Railway la crea)
CELERY_RESULT_BACKEND = (Railway la crea)

# App
DEBUG = false
SECRET_KEY = cambiar-esto-a-algo-largo-y-random
ALGORITHM = HS256
```

### Paso 5: Deploy

Railway automáticamente deployará cuando haga `git push`.

Tu URL será: `https://carolina-reminder-[random].railway.app`

---

## ✅ Verificar que funciona

```bash
# 1. Health check
curl https://carolina-reminder-xxxx.railway.app/

# 2. Ver configuración
curl https://carolina-reminder-xxxx.railway.app/api/v1/user/config

# 3. Ver recordatorios actuales
curl https://carolina-reminder-xxxx.railway.app/api/v1/settings/reminders
```

---

## 🎯 Obtener las credenciales necesarias

### 1. Google OAuth (2 min)

1. Ve a https://console.cloud.google.com
2. **Create Project** → "Carolina Reminder"
3. **Enable APIs** → busca "Google Calendar API" → Enable
4. **Credentials** → Create Credentials:
   - Type: OAuth 2.0 Client ID
   - Application: Web Application
   - Authorized JavaScript origins:
     ```
     https://carolina-reminder-xxxx.railway.app
     http://localhost:8000
     ```
   - Authorized redirect URIs:
     ```
     https://carolina-reminder-xxxx.railway.app/api/v1/auth/google/callback
     http://localhost:8000/api/v1/auth/google/callback
     ```
5. Download JSON → Copia `client_id` y `client_secret`

### 2. Twilio WhatsApp (2 min)

1. Ve a https://www.twilio.com/console
2. Sign up (gratis)
3. **Messaging** → **Try it out** → **WhatsApp**
4. Obtendrás:
   - `ACCOUNT_SID`
   - `AUTH_TOKEN`
   - Sandbox number: `+14155552671`
5. Carolina debe enviarle "join codigo" para activar el sandbox

---

## 📋 Configurar Carolina

Una vez deployado:

### 1. Conectar Google Calendar
```
https://carolina-reminder-xxxx.railway.app/
Click: "Conectar Google Calendar"
```

### 2. Configurar WhatsApp
```bash
curl -X POST https://carolina-reminder-xxxx.railway.app/api/v1/setup/whatsapp \
  -H "Content-Type: application/json" \
  -d '{"whatsapp_number": "+541234567890"}'
```

### 3. (Opcional) Cambiar horarios
```bash
# Resumen a las 8am, recordatorio noche anterior 20:00, 2h antes
curl -X POST "https://carolina-reminder-xxxx.railway.app/api/v1/settings/reminders?daily_summary_hour=8&reminder_night_before_hour=20&reminder_2h_before=true"
```

---

## 💰 Costos (Gratis con Railway)

Railway incluye **$5 USD/mes GRATIS**:

- PostgreSQL: ~$1/mes (pequeña BD)
- Redis: ~$0.5/mes (cache)
- API (Web + Celery Workers): ~$2/mes
- **Total: ~$3.5/mes** ← Gratis!

Después, paga por uso (pero muy barato).

---

## 🔄 Celery Workers en Railway

Railway ejecuta los Procfile automáticamente:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT  ← API
worker: celery -A tasks worker --loglevel=info      ← Background tasks
beat: celery -A tasks beat --loglevel=info          ← Scheduler
```

**Verificar que corre:**

1. Railway Dashboard → Deployments → Logs
2. Debe ver:
   ```
   ✅ sync_all_calendars started
   ✅ send_daily_summary scheduled
   ✅ send_scheduled_reminders started
   ```

---

## 🔧 Troubleshooting Railway

### "Error: DATABASE_URL no está configurada"
→ Railway debe crear PostgreSQL automáticamente. En variables, debería estar.

### "Celery no corre"
→ Verifica que Redis esté activo en Railway Dashboard

### "Google no conecta"
→ Asegurate que GOOGLE_REDIRECT_URI en Railway coincida exactamente con:
```
https://carolina-reminder-[random].railway.app/api/v1/auth/google/callback
```

### "WhatsApp no envía mensajes"
→ Verifica en Twilio Console que el sandbox esté activo

---

## 📊 Monitorear

Railway Dashboard te muestra:
- **Logs**: Qué está pasando en tiempo real
- **Metrics**: CPU, memoria, requests
- **Deployments**: Historial de cambios

---

## 🔄 Redeploy (después de cambios)

```bash
# Hacer cambios en código
git add .
git commit -m "Update: feature nueva"
git push origin main

# Railway automáticamente redeploya
# (puedes verlo en Dashboard → Deployments)
```

---

## ✨ Ventajas Railway vs. Render/Heroku

| Aspecto | Railway | Render | Heroku |
|--------|---------|--------|--------|
| **$5 gratis/mes** | ✅ | ✅ | ❌ (fue removido) |
| **Setup automático** | ✅ | ✅ | ❌ |
| **PostgreSQL gratis** | ✅ | ✅ | ❌ |
| **Celery/Redis** | ✅ | ✅ | Caro |
| **Speed** | ⚡ | ⚡ | Lento |

Railway es la mejor opción para este proyecto.

---

## 🎓 Paso a paso visual

```
GitHub Repo
    ↓
Railway → Lee Dockerfile
    ↓
Crea PostgreSQL + Redis
    ↓
Levanta 3 services:
├─ uvicorn (API)
├─ celery worker (sync, recordatorios)
└─ celery beat (scheduler)
    ↓
Google Calendar → Sincroniza eventos
    ↓
WhatsApp ← Twilio envía recordatorios
    ↓
Carolina recibe en Samsung A55 ✅
```

---

## 🚀 Ya está!

```
✅ App corriendo en Railway (gratis)
✅ PostgreSQL + Redis levantados
✅ Celery sincronizando calendarios
✅ Recordatorios por WhatsApp
✅ Carolina recibe alertas
```

**Próximo paso:** Que Carolina conecte su Google Calendar y comience a recibir recordatorios.

---

*Última actualización: Junio 2026*

Para soporte: Ver README.md
