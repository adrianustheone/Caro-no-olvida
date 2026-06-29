#!/bin/bash
# 🚀 CARO NO OLVIDA - COMANDOS FINALES
# Copiar y pegar en terminal
# Reemplazar [TU_USUARIO_GITHUB] antes de ejecutar

set -e

echo "🚀 Preparando Caro No Olvida para GitHub..."
echo ""

# REEMPLAZAR ESTO:
GITHUB_USER="[TU_USUARIO_GITHUB]"
REPO_URL="https://github.com/$GITHUB_USER/caro-no-olvida.git"

# Verificar
if [ "$GITHUB_USER" = "[TU_USUARIO_GITHUB]" ]; then
    echo "❌ ERROR: Reemplazá [TU_USUARIO_GITHUB] con tu usuario"
    echo "Ejemplo: adrianrodriguez"
    exit 1
fi

echo "✅ Usuario: $GITHUB_USER"
echo "✅ Repo: $REPO_URL"
echo ""

# Entrar a carpeta
cd ~/caro-no-olvida

# 1. Inicializar Git si no existe
if [ ! -d ".git" ]; then
    echo "📝 Inicializando repositorio Git..."
    git init
    git config user.name "Carolina"
    git config user.email "carolina@example.com"
fi

# 2. Agregar cambios
echo "📥 Agregando archivos..."
git add .
git status

# 3. Commit
echo ""
echo "💾 Haciendo commit..."
git commit -m "🚀 Caro No Olvida v1.0 - Sistema completo

- Backend: FastAPI + Claude NLP + Google Calendar
- Frontend: Cowork plugin
- Deploy: Railway automático
- Docs: Guía paso a paso en español

Autoinstalable: bash install-master.sh" || echo "Cambios ya committeados"

# 4. Agregar remote
echo ""
echo "🔗 Conectando con GitHub..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

# 5. Push
echo "📤 Subiendo a GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ ¡HECHO!"
echo ""
echo "Tu repositorio está en: $REPO_URL"
echo ""
echo "Para Carolina, compartí este comando:"
echo ""
echo "bash <(curl -s https://raw.githubusercontent.com/$GITHUB_USER/caro-no-olvida/main/install-master.sh)"
echo ""
