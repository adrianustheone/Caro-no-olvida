#!/bin/bash
# 🚀 CARO NO OLVIDA - SCRIPT MASTER PARA ADRIÁN
# Ejecutar en tu máquina: bash deploy-final.sh
# O copiar y pegar cada sección

set -e

# Colores
G='\033[0;32m'
B='\033[0;34m'
Y='\033[1;33m'
R='\033[0;31m'
NC='\033[0m'

clear
echo -e "${B}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║        🚀 CARO NO OLVIDA - DEPLOY FINAL                 ║"
echo "║                                                           ║"
echo "║        Adrián: Ejecutá esto en tu máquina               ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# PASO 1: Verificar que está en la carpeta correcta
echo -e "${B}1️⃣  Verificando ubicación...${NC}"
if [ ! -f "main.py" ]; then
    echo -e "${R}❌ ERROR: No estoy en la carpeta caro-no-olvida${NC}"
    echo "Ejecutá primero:"
    echo "  cd ~/caro-no-olvida"
    echo "Luego:"
    echo "  bash deploy-final.sh"
    exit 1
fi
echo -e "${G}✅ Estoy en ~/caro-no-olvida${NC}\n"

# PASO 2: Verificar Git
echo -e "${B}2️⃣  Verificando Git...${NC}"
if ! git status &> /dev/null; then
    echo -e "${R}❌ Git no inicializado${NC}"
    exit 1
fi
echo -e "${G}✅ Git OK${NC}"
echo "   Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "   Remote: $(git remote -v | head -1)"
echo ""

# PASO 3: Ver commits pendientes
echo -e "${B}3️⃣  Status de cambios...${NC}"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${G}✅ Todo limpio, listo para push${NC}\n"
else
    echo -e "${Y}⚠️  Hay cambios sin commitear${NC}"
    echo "Archivos modificados:"
    git status --short
    echo ""
    echo "¿Quieres commitearlos? (s/n)"
    read -r commit_choice
    if [ "$commit_choice" = "s" ]; then
        git add .
        git commit -m "📝 Cambios antes del push final"
        echo -e "${G}✅ Committeado${NC}\n"
    fi
fi

# PASO 4: Ver logs
echo -e "${B}4️⃣  Commits a pushear...${NC}"
echo -e "${Y}Últimos 3 commits:${NC}"
git log --oneline -3
echo ""

# PASO 5: Confirmación
echo -e "${Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${B}🎯 A PUNTO DE HACER PUSH${NC}"
echo ""
echo "Repositorio: $(git remote get-url origin)"
echo "Branch: main"
echo "Archivos: $(git ls-files | wc -l)"
echo ""
echo -e "${Y}Necesitarás tu GitHub token${NC}"
echo "¿Continuamos? (s/n)"
read -r continue_choice

if [ "$continue_choice" != "s" ]; then
    echo "Cancelado"
    exit 0
fi

echo ""

# PASO 6: HACER PUSH
echo -e "${B}5️⃣  Haciendo push a GitHub...${NC}"
echo -e "${Y}Ingresá tus credenciales cuando pida:${NC}"
echo "  Username: adrianustheone"
echo "  Password: [pega tu token, no verás lo que escribís]"
echo ""

if git push -u origin main; then
    echo ""
    echo -e "${G}✅ ¡PUSH EXITOSO!${NC}\n"
else
    echo ""
    echo -e "${R}❌ Error en el push${NC}"
    echo "Probables causas:"
    echo "  • Token incorrecto"
    echo "  • Sin conexión a internet"
    echo "  • Repositorio no existe en GitHub"
    exit 1
fi

# PASO 7: Verificar
echo -e "${B}6️⃣  Verificando GitHub...${NC}"
echo "Ve a: https://github.com/adrianustheone/Caro-no-olvida"
echo ""
echo -e "${G}✅ Debe ver todos los archivos:${NC}"
echo "   • main.py"
echo "   • install-master.sh"
echo "   • INSTALAR_COWORK.md"
echo "   • Y 30+ archivos más"
echo ""

# PASO 8: Comando para Carolina
echo -e "${B}7️⃣  Comando para Carolina${NC}"
echo ""
echo -e "${Y}Compartí este comando con Carolina:${NC}"
echo ""
echo -e "${G}bash <(curl -s https://raw.githubusercontent.com/adrianustheone/Caro-no-olvida/main/install-master.sh)${NC}"
echo ""

# RESUMEN FINAL
echo -e "${B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${G}✨ ¡TODO LISTO!${NC}"
echo ""
echo "Caro No Olvida está en GitHub ✅"
echo "Carolina puede instalar desde terminal ✅"
echo "En 10 minutos tiene todo funcionando ✅"
echo ""
echo -e "${B}Próximos pasos:${NC}"
echo "  1. Verifica en GitHub que todo está"
echo "  2. Compartí URL con Carolina"
echo "  3. Carolina ejecuta: bash <(curl -s ...install-master.sh)"
echo "  4. ¡Caro No Olvida funcionando en Cowork!"
echo ""
echo -e "${B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${G}🎉 ¡Hecho con ❤️ para Carolina!${NC}"
echo ""
