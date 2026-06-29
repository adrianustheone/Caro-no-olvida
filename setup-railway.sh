#!/bin/bash
# setup-railway.sh - Deploy automático de Caro No Olvida en Railway

set -e

echo "🚀 CARO NO OLVIDA - Setup Railway"
echo "=================================="
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar que git está conectado a GitHub
echo -e "${BLUE}1. Verificando GitHub...${NC}"
if ! git remote -v | grep -q github.com; then
    echo -e "${YELLOW}⚠️  No hay conexión a GitHub.${NC}"
    echo "Para setup automático necesitás:"
    echo "  git remote add origin https://github.com/TU_USUARIO/caro-no-olvida"
    echo "  git push -u origin main"
    exit 1
fi
echo -e "${GREEN}✅ GitHub configurado${NC}"
echo ""

# 2. Verificar archivos críticos
echo -e "${BLUE}2. Verificando archivos...${NC}"
for file in "main.py" "requirements.txt" "Procfile" "railway.json" ".env.example"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}  ✅ $file${NC}"
    else
        echo -e "${YELLOW}  ❌ $file falta${NC}"
        exit 1
    fi
done
echo ""

# 3. Crear .env
echo -e "${BLUE}3. Preparando .env...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Creado .env desde .env.example${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANTE: Editá .env con tus credenciales:${NC}"
    echo "   - GOOGLE_CLIENT_ID"
    echo "   - GOOGLE_CLIENT_SECRET"
    echo "   - TWILIO_ACCOUNT_SID"
    echo "   - TWILIO_AUTH_TOKEN"
    echo "   - ANTHROPIC_API_KEY"
else
    echo -e "${GREEN}✅ .env ya existe${NC}"
fi
echo ""

# 4. Push a GitHub
echo -e "${BLUE}4. Subiendo a GitHub...${NC}"
git add .
git commit -m "Caro No Olvida: Ready for Railway deployment" 2>/dev/null || echo "  (Sin cambios nuevos)"
git push origin main 2>/dev/null || echo "  (Ya está actualizado)"
echo -e "${GREEN}✅ Código en GitHub${NC}"
echo ""

# 5. Instrucciones Railway
echo -e "${BLUE}5. Instrucciones para Railway${NC}"
echo ""
echo "👉 Ahora necesitás:"
echo ""
echo "   1. Ve a https://railway.app"
echo "   2. New Project → Import from GitHub"
echo "   3. Selecciona este repo: caro-no-olvida"
echo ""
echo "   4. En Railway Dashboard → Variables → Agrega:"
echo "      GOOGLE_CLIENT_ID=..."
echo "      GOOGLE_CLIENT_SECRET=..."
echo "      TWILIO_ACCOUNT_SID=..."
echo "      TWILIO_AUTH_TOKEN=..."
echo "      ANTHROPIC_API_KEY=..."
echo "      TWILIO_WHATSAPP_FROM=whatsapp:+14155552671"
echo "      DEBUG=false"
echo ""
echo "   5. Click en Deploy"
echo ""
echo "   6. Espera ~3-5 minutos"
echo ""
echo "   7. Tu URL será:"
echo "      https://caro-no-olvida-[random].railway.app"
echo ""

echo -e "${GREEN}=================================="
echo "✨ Setup completado!"
echo "==================================${NC}"
echo ""
echo "Próximos pasos:"
echo "  1. Obtén credenciales (Google, Twilio, Claude)"
echo "  2. Agregá las variables en Railway"
echo "  3. Hace Deploy"
echo "  4. Carolina conecta Google Calendar"
echo "  5. ¡A hablar con Caro! 💬"
echo ""
