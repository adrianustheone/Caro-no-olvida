# 🚀 SETUP CARO NO OLVIDA - Guía paso a paso (30 min)

## Resumen
Vamos a poner a **Caro No Olvida funcionando en Railway** en 3 pasos simples:

1. Obtener 3 credenciales (Google, Twilio, Claude)
2. Ejecutar script de setup
3. Deploy automático en Railway

---

## ⏱️ PASO 1: Obtener credenciales (15 min)

### A) Google OAuth (5 min)

1. **Abre** https://console.cloud.google.com
2. **Crea proyecto:**
   - Click en el nombre del proyecto (arriba a la izquierda)
   - "Crear proyecto"
   - Nombre: "Caro No Olvida"
   - Crear

3. **Habilita Google Calendar API:**
   - Búsqueda: "Google Calendar API"
   - Click en el resultado
   - "Habilitar"

4. **Crea credenciales OAuth:**
   - Menú lateral: "Credenciales"
   - "+ Crear credencial"
   - "ID de cliente OAuth"
   - Tipo: "Aplicación web"
   - URIs autorizadas:
     ```
     http://localhost:8000/api/v1/auth/google/callback
     ```
   - Crear

5. **Descarga JSON:**
   - Click en la credencial que creaste
   - "Descargar JSON" (o copia los datos)
   - Copiar:
     - `client_id`
     - `client_secret`

**Guardá estos datos:**
```
GOOGLE_CLIENT_ID = [tu valor]
GOOGLE_CLIENT_SECRET = [tu valor]
```

### B) Twilio WhatsApp (5 min)

1. **Abre** https://www.twilio.com/console
2. **Sign up** (si no tenés cuenta)
   - Email, password, verificación

3. **Ve a WhatsApp Sandbox:**
   - Menú: "Messaging" → "Try it out" → "WhatsApp"

4. **Copia:**
   - `ACCOUNT SID`
   - `AUTH TOKEN`

5. **Para Sandbox (pruebas):**
   ```
   TWILIO_WHATSAPP_FROM = whatsapp:+14155552671
   ```

**Guardá estos datos:**
```
TWILIO_ACCOUNT_SID = [tu valor]
TWILIO_AUTH_TOKEN = [tu valor]
TWILIO_WHATSAPP_FROM = whatsapp:+14155552671
```

### C) Claude API (5 min)

1. **Abre** https://console.anthropic.com
2. **Sign up** o login
3. **Dashboard → API Keys**
4. **Crea nueva key:**
   - Click "+ Create Key"
   - Nombre: "Caro No Olvida"
   - Copiar

**Guardá este dato:**
```
ANTHROPIC_API_KEY = sk-ant-[tu valor]
```

---

## ⏱️ PASO 2: Preparar código local (5 min)

### En tu terminal:

```bash
# 1. Clonar/descargar Caro No Olvida
git clone https://github.com/[tu-usuario]/caro-no-olvida
cd caro-no-olvida

# 2. Crear archivo .env
cp .env.example .env

# 3. Editar .env con tus credenciales
# Abre .env y completa:
# GOOGLE_CLIENT_ID=...
# GOOGLE_CLIENT_SECRET=...
# TWILIO_ACCOUNT_SID=...
# TWILIO_AUTH_TOKEN=...
# ANTHROPIC_API_KEY=...
```

---

## ⏱️ PASO 3: Deploy en Railway (10 min)

### A) Preparar GitHub:

```bash
# Desde la carpeta caro-no-olvida
git add .
git commit -m "Caro No Olvida: Setup inicial"
git push origin main
```

### B) Setup en Railway:

1. **Ve a** https://railway.app
2. **Sign up** (con GitHub es más fácil)
3. **New Project** → "Import from GitHub"
4. **Selecciona** tu repo: `caro-no-olvida`
5. **Espera** a que se cree el proyecto

### C) Agregar variables en Railway:

En Railway Dashboard:

1. Click en tu proyecto
2. **Variables** (en el menú lateral)
3. **Agregar variables:**

```
GOOGLE_CLIENT_ID = [tu valor]
GOOGLE_CLIENT_SECRET = [tu valor]
GOOGLE_REDIRECT_URI = https://[tu-railway-url].railway.app/api/v1/auth/google/callback
TWILIO_ACCOUNT_SID = [tu valor]
TWILIO_AUTH_TOKEN = [tu valor]
TWILIO_WHATSAPP_FROM = whatsapp:+14155552671
ANTHROPIC_API_KEY = [tu valor]
DEBUG = false
SECRET_KEY = caro-no-olvida-secret-key-12345
```

**Nota:** La URL de Railway aparecerá como: `https://caro-no-olvida-XXXX.railway.app`

### D) Deploy:

1. **Deploy** button (Railway hace todo automático)
2. **Espera** 3-5 minutos
3. **Cuando veas "SUCCESS"**, tu app está viva

---

## 🎉 ¡Listo! Ahora qué?

### 1. Conectar Google Calendar

```
https://tu-railway-url.railway.app/
Click: "Conectar Google Calendar"
Autoriza
```

### 2. Configurar WhatsApp

```bash
curl -X POST "https://tu-railway-url.railway.app/api/v1/setup/whatsapp" \
  -H "Content-Type: application/json" \
  -d '{"whatsapp_number": "+541234567890"}'
```

Reemplazar `+541234567890` con el número de Carolina.

### 3. Activar Twilio Sandbox

Carolina necesita enviar a Twilio:

```
Enviar a: +14155552671
Mensaje: "join caro-no-olvida"
```

Twilio responde confirmando.

### 4. ¡Carolina empieza a usar Caro!

```
Carolina envía: "Agendar audiencia García mañana 10:00"
Caro responde: "✅ Evento agendado!..."
Carolina ve en Google Calendar: Evento creado ✅
Recordatorios automáticos: Noche anterior + 2h ⏰
```

---

## 📱 Ejemplos para Carolina

```
"Audiencia García mañana 10:00"
"Plazo vencimiento 30 de agosto"
"Reunión López viernes 3pm"
"Mediación caso 12345/2024 juzgado familia 3 martes"
```

---

## ✅ Checklist final

- [ ] Google OAuth credenciales ✓
- [ ] Twilio account SID + token ✓
- [ ] Claude API key ✓
- [ ] .env completado ✓
- [ ] GitHub push ✓
- [ ] Railway deploy ✓
- [ ] Google Calendar conectado ✓
- [ ] WhatsApp configurado ✓
- [ ] Twilio sandbox activado ✓
- [ ] Carolina probó primer mensaje ✓

---

## 🆘 Si algo falla

### "Error: Google no conecta"
→ Verifica que `GOOGLE_REDIRECT_URI` en Railway coincida exactamente con tu URL

### "WhatsApp no envía mensajes"
→ Verifica que Carolina hizo el "join" en Twilio Sandbox

### "Claude API error"
→ Verifica que `ANTHROPIC_API_KEY` sea válida (comienza con `sk-ant-`)

### "Base de datos error"
→ Railway la crea automáticamente, espera 2 minutos más

### Ver logs en Railway:
```
Dashboard → Tu proyecto → Logs (tab)
```

---

## 📞 Soporte

Si algo no funciona:
1. Chequea los logs en Railway
2. Verifica que todas las variables están
3. Asegúrate que GitHub está actualizado
4. Reinicia el deploy

---

## 🎯 Resultado final

```
Carolina:
  ✅ Habla con Caro por WhatsApp
  ✅ Ve eventos en Google Calendar
  ✅ Recibe recordatorios automáticos
  ✅ Sin concentración requerida
  ✅ Sin código ni tecnicismo

Adrián:
  ✅ App corriendo en Railway (gratis)
  ✅ Claude entiende español
  ✅ Google Calendar sincronizado
  ✅ Base de datos automática
  ✅ Escalable y mantenible
```

---

## 🚀 Ya estás listo

Ejecutá:
```bash
bash setup-railway.sh
```

Y sigue las instrucciones que aparecen.

¡Caro No Olvida está listo para ayudar a Carolina! 💪

---

*Guía v1.0 - Junio 2026*
*Para Carolina, con amor 💜*
