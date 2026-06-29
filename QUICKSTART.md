# ⚡ QUICKSTART - 5 minutos para tener funcionando Carolina Reminder

## Opción A: Railway (Lo más fácil) 🚀

### 1. Regístrate en Railway
👉 https://railway.app

### 2. Crea estas 3 credenciales (5 min cada una)

**A) Google Calendar** (2 min)
- Ve a: https://console.cloud.google.com
- Crea proyecto "Carolina"
- Enable: "Google Calendar API"
- OAuth Credentials (web app)
- Copia `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`

**B) Twilio** (2 min)
- Ve a: https://www.twilio.com/console
- Obtén `ACCOUNT_SID` y `AUTH_TOKEN`
- Usa el WhatsApp Sandbox: `+14155552671`

**C) PostgreSQL**
- Railway la crea automáticamente ✅

### 3. Deploy en Railway
```bash
# En Railway dashboard:
# → New → Import GitHub Repo
# → Select carolina-reminder repo
# → Agregar variables de entorno (ver arriba)
# → Deploy!

# Tu URL será:
https://carolina-reminder-XXXX.railway.app
```

### 4. Configurar Carolina (2 min)

1. Abre: `https://tu-app.railway.app`
2. Click: "Conectar Google Calendar"
3. Autoriza
4. API call: `POST /api/v1/setup/whatsapp`
   ```json
   {"whatsapp_number": "+541234567890"}
   ```
5. ¡Listo! ¡Recibe confirmación por WhatsApp!

---

## Opción B: Local con Docker (Si quieres experimentar) 🐳

```bash
# 1. Clonar
git clone https://github.com/adrianrodriguez/carolina-reminder
cd carolina-reminder

# 2. Crear .env (copiar de .env.example y completar)
cp .env.example .env
# Editar y agregar tus credenciales de Google y Twilio

# 3. Ejecutar todo
docker-compose up

# Accede a: http://localhost:8000
```

---

## Opción C: Local sin Docker (Si tienes todo instalado)

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate  # o: venv\Scripts\activate
pip install -r requirements.txt

# 2. Variables
cp .env.example .env
# Editar con credenciales

# 3. Terminal 1: Backend
uvicorn main:app --reload

# 4. Terminal 2: Celery Worker
celery -A tasks worker --loglevel=info

# 5. Terminal 3: Celery Beat
celery -A tasks beat --loglevel=info

# Accede a: http://localhost:8000
```

---

## Test rápido

Una vez corriendo, probá estos comandos:

```bash
# Ver eventos de hoy
curl http://localhost:8000/api/v1/events/today

# Ver configuración de Carolina
curl http://localhost:8000/api/v1/user/config

# Crear nota rápida
curl -X POST http://localhost:8000/api/v1/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "Acordarme que el cliente se muda el 30/7"}'
```

---

## WhatsApp Sandbox (Importante para pruebas)

Si usas Twilio Sandbox (números de prueba):

1. **Carolina debe enviar a:** `+14155552671`
2. **Mensaje de activación:** "join [code]" (Twilio te lo da)
3. Después recibe todos los mensajes de la app

---

## Estructura de eventos en Google Calendar

Para que el sistema interprete bien, cuando crees eventos en Google Calendar, incluí en el título:

```
[AUDIENCIA] Mediación caso García - 10:00
[PLAZO] Vencimiento recurso apelación - 30/07/2026
[DOCUMENTO] Presentar escrito de demanda
[REUNION] Reunión cliente López - 14:30
```

El sistema automáticamente:
- Detecta el tipo
- Envía recordatorios con prioridad correcta
- Alerta si hay plazos venciendo

---

## ¿Listo?

Una vez corriendo, Carolina recibe:

```
🏛️ RECORDATORIO: MAÑANA
📅 10:00
📌 Audiencia TOC Nº4 - Caso García
Juzgado: San Martín
📍 Av. Belgrano 1234
```

---

## Soporte rápido

| Problema | Solución |
|----------|----------|
| No recibo WhatsApp | ¿Estás en el Sandbox? Envía "join" primero |
| Google no conecta | Verifica REDIRECT_URI en .env vs Google Console |
| "Base de datos no conecta" | Verifica DATABASE_URL en .env |
| Celery no funciona | Verifica que Redis esté corriendo |

---

**¡Ahora ya podés empezar a codear! 🚀**

Próximo paso: Personalizar mensajes, agregar más tipos de eventos, integración con OUCHURUS.

---

*Para detalles completos, ver README.md*
