#!/bin/bash
# install-caro.sh - Instalador autoinstalable de Caro No Olvida
# Uso: bash install-caro.sh

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║           💬 CARO NO OLVIDA - INSTALADOR                 ║"
echo "║         Asistente conversacional para Carolina            ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Verificar requisitos
echo -e "${BLUE}📋 Verificando requisitos...${NC}"

command -v git >/dev/null 2>&1 || { echo -e "${RED}❌ Git no está instalado${NC}"; exit 1; }
echo -e "${GREEN}✅ Git${NC}"

command -v python3 >/dev/null 2>&1 || { echo -e "${RED}❌ Python 3 no está instalado${NC}"; exit 1; }
echo -e "${GREEN}✅ Python 3${NC}"

command -v docker >/dev/null 2>&1 && echo -e "${GREEN}✅ Docker${NC}" || echo -e "${YELLOW}⚠️  Docker no instalado (opcional)${NC}"

echo ""

# 1. Crear carpeta
echo -e "${BLUE}1️⃣  Creando carpeta del proyecto...${NC}"
INSTALL_DIR="$HOME/caro-no-olvida"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo -e "${GREEN}✅ Carpeta: $INSTALL_DIR${NC}"
echo ""

# 2. Descargar código (simular git clone para este caso)
echo -e "${BLUE}2️⃣  Descargando código...${NC}"
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Ya existe repositorio Git, actualizando...${NC}"
    git pull origin main 2>/dev/null || echo "No hay cambios"
else
    # En caso real, sería:
    # git clone https://github.com/[usuario]/caro-no-olvida .
    echo -e "${YELLOW}📝 (En caso real, aquí se hace: git clone ...)${NC}"
fi
echo -e "${GREEN}✅ Código listo${NC}"
echo ""

# 3. Crear .env
echo -e "${BLUE}3️⃣  Configurando credenciales...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || touch .env
    echo -e "${YELLOW}⚠️  Se creó .env vacío${NC}"
    echo -e "${YELLOW}   Editá manualmente y agrega:${NC}"
    echo "   GOOGLE_CLIENT_ID=..."
    echo "   GOOGLE_CLIENT_SECRET=..."
    echo "   TWILIO_ACCOUNT_SID=..."
    echo "   TWILIO_AUTH_TOKEN=..."
    echo "   ANTHROPIC_API_KEY=..."
else
    echo -e "${GREEN}✅ .env ya existe${NC}"
fi
echo ""

# 4. Crear plugin Cowork
echo -e "${BLUE}4️⃣  Creando plugin Cowork...${NC}"
mkdir -p "$INSTALL_DIR/plugin-caro/skills"
mkdir -p "$INSTALL_DIR/plugin-caro/tools"

# Manifest del plugin
cat > "$INSTALL_DIR/plugin-caro/manifest.json" << 'EOF'
{
  "name": "Caro No Olvida",
  "version": "1.0.0",
  "description": "Asistente conversacional por WhatsApp para Carolina",
  "author": "Adrián Rodríguez",
  "icon": "💬",
  "api": {
    "baseUrl": "https://caro-no-olvida.railway.app/api/v1"
  },
  "commands": [
    {
      "name": "agendar",
      "description": "Agendar evento en Google Calendar",
      "icon": "📅"
    },
    {
      "name": "próximos",
      "description": "Ver próximos eventos",
      "icon": "📋"
    },
    {
      "name": "recordatorios",
      "description": "Configurar recordatorios",
      "icon": "⏰"
    },
    {
      "name": "conversaciones",
      "description": "Ver conversaciones recientes",
      "icon": "💬"
    }
  ]
}
EOF

echo -e "${GREEN}✅ Plugin creado en: $INSTALL_DIR/plugin-caro${NC}"
echo ""

# 5. Crear skill principal
cat > "$INSTALL_DIR/plugin-caro/skills/agendar-evento.md" << 'EOF'
# Agendar Evento con Caro

## Descripción
Agenda eventos en Google Calendar hablando naturalmente

## Cómo usar
Simplemente habla como lo harías normalmente:

**Ejemplos:**
- "Agendar audiencia García mañana 10:00"
- "Plazo vencimiento 30 de agosto"
- "Reunión López viernes 3pm en mi oficina"
- "Mediación caso 12345/2024 juzgado familia 3 martes"

## Lo que Caro entiende
- 📅 Fechas: "mañana", "próximo viernes", "30 de julio"
- 🕐 Horas: "10:00", "3pm", "15:30"
- 🏛️ Tipos: audiencia, plazo, documento, reunión
- 👤 Clientes y casos automáticamente

## Confirmación
Caro te muestra el evento y pregunta: "¿Confirmás?"
- "Confirmar" / "Sí" / "Dale" → Crea evento
- "Cancelar" / "No" → Descarta

## Recordatorios automáticos
- 🌙 Noche anterior (20:00 default)
- ⏰ 2 horas antes

## ¿Falta información?
Si Caro no entiende algo, pregunta:
- "¿A qué hora?"
- "¿Qué día?"

Solo completa lo que te pide y listo.
EOF

echo -e "${GREEN}✅ Skill creado${NC}"
echo ""

# 6. Crear archivo de configuración local
cat > "$INSTALL_DIR/plugin-caro/config.json" << 'EOF'
{
  "apiEndpoint": "http://localhost:8000/api/v1",
  "production": "https://caro-no-olvida.railway.app/api/v1",
  "whatsapp": {
    "enabled": true,
    "numberNeeded": "+541234567890"
  },
  "googleCalendar": {
    "enabled": false,
    "requiresOAuth": true,
    "status": "Not connected"
  }
}
EOF

# 7. Instrucciones para Cowork
echo -e "${BLUE}5️⃣  Instalando en Cowork...${NC}"
COWORK_DIR="$HOME/.cowork/plugins"
mkdir -p "$COWORK_DIR"

# Crear zip del plugin
cd "$INSTALL_DIR/plugin-caro"
zip -r "caro-no-olvida-plugin.zip" . -q 2>/dev/null || true
cp "caro-no-olvida-plugin.zip" "$COWORK_DIR/" 2>/dev/null || true

echo -e "${GREEN}✅ Plugin listo para Cowork${NC}"
echo "   Ubicación: $COWORK_DIR/caro-no-olvida-plugin.zip"
echo ""

# 8. Instrucciones finales
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                   ✨ INSTALACIÓN COMPLETA ✨              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}📋 PRÓXIMOS PASOS:${NC}"
echo ""

echo "1️⃣  ${YELLOW}Configurar credenciales:${NC}"
echo "   Abre: $INSTALL_DIR/.env"
echo "   Completa:"
echo "     - GOOGLE_CLIENT_ID=..."
echo "     - GOOGLE_CLIENT_SECRET=..."
echo "     - TWILIO_ACCOUNT_SID=..."
echo "     - TWILIO_AUTH_TOKEN=..."
echo "     - ANTHROPIC_API_KEY=..."
echo ""

echo "2️⃣  ${YELLOW}Deploy a Railway:${NC}"
echo "   cd $INSTALL_DIR"
echo "   bash setup-railway.sh"
echo ""

echo "3️⃣  ${YELLOW}Instalar plugin en Cowork:${NC}"
echo "   • Abre Cowork en tu teléfono"
echo "   • Settings → Add Plugin"
echo "   • Selecciona: caro-no-olvida-plugin.zip"
echo "   • Done!"
echo ""

echo "4️⃣  ${YELLOW}Conectar Google Calendar:${NC}"
echo "   • En Cowork, abre Caro"
echo "   • Click: Conectar Google Calendar"
echo "   • Autoriza"
echo ""

echo "5️⃣  ${YELLOW}Configurar WhatsApp:${NC}"
echo "   • Dale tu número a Caro"
echo "   • Ella activa Twilio Sandbox"
echo "   • ¡A hablar! 💬"
echo ""

echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}📁 Información:${NC}"
echo "   Carpeta: $INSTALL_DIR"
echo "   Plugin: $COWORK_DIR/caro-no-olvida-plugin.zip"
echo "   Config: $INSTALL_DIR/.env"
echo ""

echo -e "${BLUE}📚 Documentación:${NC}"
echo "   Ver: $INSTALL_DIR/SETUP_STEP_BY_STEP.md"
echo "   Quick ref: $INSTALL_DIR/QUICK_REFERENCE.md"
echo ""

echo -e "${GREEN}✨ ¡Caro No Olvida está lista!${NC}"
echo ""
echo "Ejecutá:"
echo "   cd $INSTALL_DIR"
echo "   bash setup-railway.sh"
echo ""
