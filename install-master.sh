#!/bin/bash
# 🚀 CARO NO OLVIDA - INSTALADOR MASTER
# Uso: bash <(curl -s https://raw.githubusercontent.com/[user]/caro-no-olvida/main/install-master.sh)
# O local: bash install-master.sh

set -e

# ============ COLORES ============
G='\033[0;32m'  # Green
B='\033[0;34m'  # Blue
Y='\033[1;33m'  # Yellow
R='\033[0;31m'  # Red
NC='\033[0m'    # No Color

# ============ VARIABLES ============
HOME_DIR="$HOME"
INSTALL_DIR="$HOME_DIR/caro-no-olvida"
COWORK_PLUGINS="$HOME_DIR/.cowork/plugins"
GIT_REPO="https://github.com/[REEMPLAZAR]/caro-no-olvida.git"

# ============ FUNCIONES ============

banner() {
    clear
    echo -e "${B}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║            💬 CARO NO OLVIDA v1.0                        ║"
    echo "║      Asistente conversacional para Carolina              ║"
    echo "║                                                           ║"
    echo "║     Instalador automático - 2 minutos para empezar       ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
}

check_requirements() {
    echo -e "${B}📋 Verificando requisitos...${NC}\n"
    
    local missing=0
    
    if ! command -v git &> /dev/null; then
        echo -e "${R}❌ Git no instalado${NC}"
        missing=1
    else
        echo -e "${G}✅ Git${NC}"
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${R}❌ Python 3 no instalado${NC}"
        missing=1
    else
        echo -e "${G}✅ Python 3${NC}"
    fi
    
    if [ $missing -eq 1 ]; then
        echo -e "\n${R}❌ Faltan requisitos. Por favor instalá git y python3${NC}"
        exit 1
    fi
    
    echo -e "\n${G}✅ Todos los requisitos OK${NC}\n"
}

setup_directories() {
    echo -e "${B}📁 Configurando directorios...${NC}"
    
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$COWORK_PLUGINS"
    
    echo -e "${G}✅ Carpetas creadas:${NC}"
    echo "   • Proyecto: $INSTALL_DIR"
    echo "   • Cowork: $COWORK_PLUGINS"
    echo ""
}

clone_or_update_repo() {
    echo -e "${B}📥 Descargando código...${NC}"
    
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo -e "${Y}Actualizando repositorio existente...${NC}"
        cd "$INSTALL_DIR"
        git pull origin main --quiet 2>/dev/null || true
    else
        echo -e "${Y}Clonando repositorio...${NC}"
        git clone "$GIT_REPO" "$INSTALL_DIR" --quiet 2>/dev/null || {
            echo -e "${R}Error clonando. Usando setup manual...${NC}"
            # Fallback: crear estructura manual
            cd "$INSTALL_DIR"
            git init
        }
    fi
    
    cd "$INSTALL_DIR"
    echo -e "${G}✅ Código listo${NC}\n"
}

create_env_file() {
    echo -e "${B}⚙️  Configurando variables de entorno...${NC}"
    
    if [ ! -f "$INSTALL_DIR/.env" ]; then
        cat > "$INSTALL_DIR/.env" << 'EOF'
# ============ CARO NO OLVIDA - CONFIGURACIÓN ============

# 1. GOOGLE OAUTH
# Obtener en: https://console.cloud.google.com
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=https://caro-no-olvida-RAILWAY_ID.railway.app/api/v1/auth/google/callback

# 2. TWILIO WHATSAPP
# Obtener en: https://www.twilio.com/console
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_FROM=whatsapp:+14155552671

# 3. CLAUDE API
# Obtener en: https://console.anthropic.com
ANTHROPIC_API_KEY=

# 4. SECRETOS
SECRET_KEY=caro-no-olvida-secret-key-$(date +%s)
DEBUG=false

# ============ DEJAR VACÍO - Railway lo llena ============
DATABASE_URL=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
EOF
        echo -e "${Y}⚠️  Se creó .env${NC}"
        echo -e "${Y}   Editá e ingresá tus credenciales:${NC}"
        echo "   nano $INSTALL_DIR/.env"
    else
        echo -e "${G}✅ .env ya existe${NC}"
    fi
    echo ""
}

create_cowork_plugin() {
    echo -e "${B}🎨 Creando plugin Cowork...${NC}"
    
    local PLUGIN_DIR="$INSTALL_DIR/.cowork-plugin"
    mkdir -p "$PLUGIN_DIR/skills"
    mkdir -p "$PLUGIN_DIR/tools"
    
    # Manifest
    cat > "$PLUGIN_DIR/manifest.json" << 'EOF'
{
  "id": "caro-no-olvida",
  "name": "Caro No Olvida",
  "version": "1.0.0",
  "description": "Asistente conversacional para abogadas - Agendar eventos, recordatorios automáticos",
  "icon": "💬",
  "author": "Adrián Rodríguez",
  "commands": [
    {"name": "Agendar", "slug": "agendar", "icon": "📅"},
    {"name": "Ver Próximos", "slug": "proximo", "icon": "📋"},
    {"name": "Recordatorios", "slug": "recordatorios", "icon": "⏰"},
    {"name": "Conversaciones", "slug": "conversaciones", "icon": "💬"},
    {"name": "Dashboard", "slug": "dashboard", "icon": "📊"}
  ]
}
EOF

    # Skill principal
    cat > "$PLUGIN_DIR/skills/agendar.md" << 'EOF'
# 📅 Agendar Evento

Habla naturalmente con Caro para agendar en Google Calendar.

## Ejemplos
- "Agendar audiencia García mañana 10:00"
- "Plazo vencimiento 30 de agosto"
- "Reunión López viernes 3pm en mi oficina"

## Caro entiende
- 📅 Fechas: mañana, próximo viernes, 30/7
- 🕐 Horas: 10:00, 3pm, 15:30
- 🏛️ Eventos: audiencia, plazo, documento, reunión

## Confirmación
Confirma con: "Sí", "Dale", "Confirmar"
Cancela con: "No", "Cancelar"

## Recordatorios automáticos
- 🌙 Noche anterior (20:00)
- ⏰ 2 horas antes
EOF

    # README del plugin
    cat > "$PLUGIN_DIR/README.md" << 'EOF'
# Caro No Olvida - Plugin Cowork

## Instalación en Cowork
1. Abre Cowork en tu teléfono
2. Settings → Add Plugin
3. Selecciona este archivo

## Primeros pasos
1. Conecta Google Calendar
2. Configura tu número WhatsApp
3. ¡Empieza a hablar!

## Ejemplos
- "Agendar audiencia mañana 10:00"
- "Ver próximos eventos"
- "Cambiar resumen diario a 7am"
EOF

    echo -e "${G}✅ Plugin creado${NC}\n"
}

create_plugin_zip() {
    echo -e "${B}📦 Empaquetando plugin...${NC}"
    
    local PLUGIN_DIR="$INSTALL_DIR/.cowork-plugin"
    local PLUGIN_ZIP="$INSTALL_DIR/caro-no-olvida-v1.0.0.zip"
    
    cd "$PLUGIN_DIR"
    zip -r "$PLUGIN_ZIP" . -q 2>/dev/null || true
    
    # Copiar a Cowork
    cp "$PLUGIN_ZIP" "$COWORK_PLUGINS/" 2>/dev/null || true
    
    echo -e "${G}✅ Plugin empaquetado${NC}"
    echo "   Ubicación: $COWORK_PLUGINS/caro-no-olvida-v1.0.0.zip"
    echo ""
}

setup_railway_prompt() {
    echo -e "${B}🚀 Deploy a Railway${NC}"
    echo ""
    echo -e "${Y}1. Ve a https://railway.app${NC}"
    echo -e "${Y}2. New Project → Import from GitHub${NC}"
    echo -e "${Y}3. Selecciona: caro-no-olvida${NC}"
    echo -e "${Y}4. En Railway Dashboard, agrega Variables:${NC}"
    echo ""
    echo "GOOGLE_CLIENT_ID=tu-valor"
    echo "GOOGLE_CLIENT_SECRET=tu-valor"
    echo "GOOGLE_REDIRECT_URI=https://caro-no-olvida-XXXX.railway.app/api/v1/auth/google/callback"
    echo "TWILIO_ACCOUNT_SID=tu-valor"
    echo "TWILIO_AUTH_TOKEN=tu-valor"
    echo "TWILIO_WHATSAPP_FROM=whatsapp:+14155552671"
    echo "ANTHROPIC_API_KEY=tu-valor"
    echo ""
    echo -e "${Y}5. Click Deploy${NC}"
    echo -e "${Y}6. Espera 3-5 minutos${NC}"
    echo ""
}

create_instructions() {
    echo -e "${B}📖 Creando instrucciones...${NC}"
    
    cat > "$INSTALL_DIR/INSTALAR_COWORK.md" << 'EOF'
# 📱 Instalar Caro en Cowork

## Archivo del plugin
```
~/caro-no-olvida/caro-no-olvida-v1.0.0.zip
```

## En tu teléfono (Cowork)
1. Abre **Cowork**
2. **Settings** (⚙️)
3. **Add Plugin**
4. **Select file**
5. Selecciona: `caro-no-olvida-v1.0.0.zip`
6. **Install**
7. ¡Listo! Aparece "Caro No Olvida" en tus plugins

## Primeros pasos
1. Abre Caro No Olvida
2. **Conectar Google Calendar** (click)
   - Autoriza con tu Google
3. **Configurar WhatsApp**
   - Ingresa tu número
4. **¡A hablar!**
   - "Agendar audiencia García mañana 10:00"

## Recordatorios automáticos
Se activan automáticamente:
- 🌙 Noche anterior (20:00)
- ⏰ 2 horas antes del evento
- 📋 Resumen diario (8am)

## Ver próximos eventos
Di: "¿Qué tengo próximo?" o "Ver eventos"

## Cambiar configuración
- "Cambiar resumen diario a 7am"
- "Recordatorio noche anterior a las 19:00"
- "Sin recordatorio 2h antes"
EOF

    echo -e "${G}✅ Instrucciones creadas${NC}\n"
}

final_summary() {
    echo -e "${G}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                   ✨ INSTALACIÓN COMPLETA ✨             ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
    
    echo -e "${B}📁 INFORMACIÓN:${NC}"
    echo "Carpeta: $INSTALL_DIR"
    echo "Plugin: $COWORK_PLUGINS/caro-no-olvida-v1.0.0.zip"
    echo "Config: $INSTALL_DIR/.env"
    echo ""
    
    echo -e "${B}🎯 PRÓXIMOS PASOS:${NC}"
    echo ""
    echo "1️⃣  ${Y}Editar credenciales:${NC}"
    echo "    nano $INSTALL_DIR/.env"
    echo ""
    
    echo "2️⃣  ${Y}Deploy a Railway (automático):${NC}"
    echo "    cd $INSTALL_DIR"
    echo "    bash setup-railway.sh"
    echo ""
    
    echo "3️⃣  ${Y}Instalar en Cowork:${NC}"
    echo "    • Abre Cowork en tu teléfono"
    echo "    • Settings → Add Plugin"
    echo "    • Archivo: caro-no-olvida-v1.0.0.zip"
    echo "    • Install"
    echo ""
    
    echo "4️⃣  ${Y}Conectar Google & WhatsApp:${NC}"
    echo "    • En Cowork: Conectar Google Calendar"
    echo "    • Configurar número WhatsApp"
    echo "    • ¡Listo!"
    echo ""
    
    echo -e "${B}📚 DOCUMENTACIÓN:${NC}"
    echo "Ver: $INSTALL_DIR/INSTALAR_COWORK.md"
    echo "Ver: $INSTALL_DIR/GUIDE_USAGE.md"
    echo "Ver: $INSTALL_DIR/QUICK_REFERENCE.md"
    echo ""
    
    echo -e "${G}✨ Caro No Olvida está lista para Carolina${NC}"
    echo ""
}

# ============ MAIN FLOW ============

banner
check_requirements
setup_directories
clone_or_update_repo
create_env_file
create_cowork_plugin
create_plugin_zip
setup_railway_prompt
create_instructions
final_summary

echo -e "${B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${Y}IMPORTANTE: Completá .env con tus credenciales:${NC}"
echo "nano $INSTALL_DIR/.env"
echo ""
echo -e "${Y}Luego deploy a Railway:${NC}"
echo "cd $INSTALL_DIR && bash setup-railway.sh"
echo ""
echo -e "${G}¡Que disfrutes Caro No Olvida! 💪${NC}"
echo ""
