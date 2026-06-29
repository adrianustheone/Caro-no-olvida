# 🚀 CARO NO OLVIDA - INSTALACIÓN AUTOMÁTICA

**Una línea y listo. 2 minutos.**

---

## 🎯 Lo que vas a lograr

```
Terminal → bash install-master.sh
    ↓
Automáticamente:
  ✅ Descarga Caro No Olvida
  ✅ Crea plugin Cowork
  ✅ Configura credenciales
  ✅ Prepara para Railway
    ↓
En tu teléfono:
  ✅ Abre Cowork
  ✅ Add Plugin → caro-no-olvida
    ↓
¡Listo! A agendar eventos hablando
```

---

## 📱 PASO A PASO

### **PASO 1: Descargar instalador (30 segundos)**

Abre tu terminal (Mac: Terminal, Windows: PowerShell, Linux: Terminal):

```bash
# Opción A: Desde GitHub (cuando esté disponible)
bash <(curl -s https://raw.githubusercontent.com/[usuario]/caro-no-olvida/main/install-master.sh)

# Opción B: Local (si ya descargaste)
cd ~/caro-no-olvida
bash install-master.sh
```

**Eso es todo.** El script hace:
- ✅ Crea carpeta `~/caro-no-olvida`
- ✅ Descarga código
- ✅ Crea plugin Cowork
- ✅ Genera archivo .env

---

### **PASO 2: Agregar credenciales (1 minuto)**

El script te dice:
```
⚙️ Se creó .env
   Editá: nano ~/caro-no-olvida/.env
```

Abre y completa:
```bash
nano ~/caro-no-olvida/.env
```

Necesitás 5 valores (ver abajo cómo obtenerlos):

```
GOOGLE_CLIENT_ID=abc123...
GOOGLE_CLIENT_SECRET=xyz789...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=tu-token...
ANTHROPIC_API_KEY=sk-ant-...
```

**¿Dónde conseguir cada uno?**

#### 1. Google OAuth
```
1. Ve a: https://console.cloud.google.com
2. Crea proyecto: "Caro No Olvida"
3. Habilita: Google Calendar API
4. Credenciales → OAuth → Aplicación web
5. Copia: CLIENT_ID y CLIENT_SECRET
6. Pega en .env
```

#### 2. Twilio WhatsApp
```
1. Ve a: https://www.twilio.com/console
2. Sign up si no tenés cuenta
3. Copia: ACCOUNT SID y AUTH TOKEN
4. Pega en .env
5. Para sandbox: TWILIO_WHATSAPP_FROM = whatsapp:+14155552671
```

#### 3. Claude API
```
1. Ve a: https://console.anthropic.com
2. Dashboard → API Keys
3. Create new key
4. Copia: sk-ant-xxxxx
5. Pega en .env
```

**Guardá el archivo** (Ctrl+O, Enter, Ctrl+X en nano)

---

### **PASO 3: Deploy automático (5 minutos)**

El script te dice:
```
🚀 Deploy a Railway:
   cd ~/caro-no-olvida
   bash setup-railway.sh
```

Ejecutá:
```bash
cd ~/caro-no-olvida
bash setup-railway.sh
```

El script:
- ✅ Verifica GitHub
- ✅ Sube código a GitHub
- ✅ Te da instrucciones Railway
- ✅ Abre https://railway.app

**En Railway Dashboard:**
1. New Project → Import from GitHub
2. Selecciona: `caro-no-olvida`
3. Click **Variables** → Agrega los 9 valores (mirá el output del script)
4. Click **Deploy** (botón rojo)
5. Espera 3-5 minutos

Cuando veas: **🟢 SUCCESS** → ¡Listo!

Tu URL será: `https://caro-no-olvida-XXXX.railway.app`

---

### **PASO 4: Instalar en Cowork (1 minuto)**

El instalador creó el archivo:
```
~/caro-no-olvida/caro-no-olvida-v1.0.0.zip
```

En tu teléfono (Cowork app):
1. Settings ⚙️
2. Add Plugin
3. Select file
4. Busca: `caro-no-olvida-v1.0.0.zip`
5. Install
6. ¡Aparece en tus plugins!

---

### **PASO 5: Conectar Google & WhatsApp (2 minutos)**

En Cowork, abre **Caro No Olvida**:

1. **Conectar Google Calendar**
   - Click "Conectar Google"
   - Autoriza con tu Google
   - ✅ Done

2. **Configurar WhatsApp**
   - Ingresa tu número
   - (Ejemplo: +541234567890)
   - ✅ Done

3. **Activar Twilio Sandbox** (Carolina recibe SMS)
   - Envía desde WhatsApp a: **+14155552671**
   - Mensaje: `join caro-no-olvida`
   - Twilio confirma
   - ✅ Done

---

### **PASO 6: ¡A hablar! (Ya está)**

Abre Cowork y habla con Caro:

```
"Agendar audiencia García mañana 10:00"

Caro responde:
✅ Evento agendado!
🏛️ Audiencia García
📅 2026-06-28 a las 10:00
Recordatorios: noche anterior + 2h

📱 También aparece en Google Calendar
```

---

## ✅ CHECKLIST FINAL

- [ ] Ejecuté `bash install-master.sh`
- [ ] Completé `.env` con 5 credenciales
- [ ] Ejecuté `bash setup-railway.sh`
- [ ] Agregué 9 variables en Railway
- [ ] Railway dice: SUCCESS ✅
- [ ] Instalé plugin en Cowork
- [ ] Conecté Google Calendar
- [ ] Configuré WhatsApp
- [ ] Activé Twilio Sandbox
- [ ] ¡Probé: "Agendar audiencia mañana 10:00"!

---

## 🆘 SI ALGO FALLA

### "Error: Git/Python no encontrado"
```
Linux: sudo apt install git python3
Mac: brew install git python3
Windows: Descargá desde python.org y git-scm.com
```

### "Error en Railway"
```
1. Ver logs: Dashboard → Logs
2. Buscar ERROR
3. Falta variable: Agregá en Dashboard
```

### "Plugin no aparece en Cowork"
```
1. Reinicia Cowork
2. Archivo debe estar en carpeta de plugins
3. Nombre: caro-no-olvida-v1.0.0.zip
```

### "Google Calendar no conecta"
```
1. Verifica GOOGLE_CLIENT_ID en .env
2. Verifica GOOGLE_REDIRECT_URI en Railway
3. Ambas deben coincidir exactamente
```

### "WhatsApp no recibe mensajes"
```
1. Verificá que confirmaste "join caro-no-olvida" en Twilio
2. Verifica TWILIO_ACCOUNT_SID en Railway
3. Espera 1-2 minutos después de activar
```

---

## 📊 DESPUÉS DE INSTALAR

### Ver próximos eventos
```
"¿Qué tengo próximo?"
"Ver próximos 7 días"
```

### Cambiar recordatorios
```
"Cambiar resumen diario a 7am"
"Recordatorio noche anterior a 19:00"
"Sin recordatorio 2h antes"
```

### Historial
```
"Ver conversaciones recientes"
"Mostrar historial"
```

---

## 🎯 RESUMEN

```
1 línea en terminal:
   bash install-master.sh

Luego:
   Editar .env (1 min)
   Railway Deploy (5 min)
   Cowork instalar (1 min)
   Conectar Google + WhatsApp (2 min)

TOTAL: ~10 minutos

RESULTADO: 
   Caro No Olvida funcionando en tu teléfono ✅
```

---

## 📞 SOPORTE

**Documentación:**
- `GUIDE_USAGE.md` - Cómo usar Caro
- `QUICK_REFERENCE.md` - Tarjeta rápida
- `README.md` - Visión general

**Archivos de log:**
```bash
# Si algo falla en Railway
# Ve a: Dashboard → Logs

# Si algo falla local
tail -f ~/caro-no-olvida/error.log
```

---

## ✨ ¡YA ESTÁ!

Carolina solo ejecuta:

```bash
bash install-master.sh
```

Y en 2 minutos + 8 minutos de setup (credenciales + Railway) está lista para agendar eventos hablando por Cowork.

**Sin terminal. Sin comandos. Sin complicaciones.**

Solo: **"Agendar audiencia García mañana 10:00"** → ✅ Hecho

---

*Caro No Olvida v1.0*  
*Para Carolina, con ❤️*
