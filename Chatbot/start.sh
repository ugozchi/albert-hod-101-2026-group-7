#!/usr/bin/env bash
set -e

VENV_DIR=".venv"
REQ_FILE="requirements.txt"
DB_SCRIPT="create_db.py"

echo "========================================="
echo "🚀 STARTUP SCRIPT"
echo "========================================="

# Détecter l'OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    OS_TYPE="windows"
    PYTHON_CMD="python"
    VENV_ACTIVATE="$VENV_DIR/Scripts/activate"
    echo "💻 OS détecté: Windows"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    PYTHON_CMD="python3"
    VENV_ACTIVATE="$VENV_DIR/bin/activate"
    echo "🍎 OS détecté: macOS"
else
    OS_TYPE="linux"
    PYTHON_CMD="python3"
    VENV_ACTIVATE="$VENV_DIR/bin/activate"
    echo "🐧 OS détecté: Linux"
fi

echo ""

# 1) Vérifier/Créer le venv
if [[ ! -d "$VENV_DIR" ]]; then
    echo "📦 Création du venv dans $VENV_DIR..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo "✅ venv créé"
else
    echo "✅ venv existe déjà: $VENV_DIR"
fi

echo ""

# 2) Activer le venv
echo "🔌 Activation du venv..."
source "$VENV_ACTIVATE"
echo "✅ venv activé"

echo ""

# 3) Mettre à jour pip
echo "⬆️  Mise à jour de pip..."
python -m pip install --upgrade pip --quiet
echo "✅ pip à jour"

echo ""

# 4) Vérifier et installer les dépendances
if [[ -f "$REQ_FILE" ]]; then
    echo "📥 Vérification des dépendances..."
    
    # Vérifier si des packages sont déjà installés
    if pip freeze | grep -q .; then
        echo "ℹ️  Packages déjà installés, vérification des mises à jour..."
    else
        echo "📦 Aucun package trouvé, installation complète..."
    fi
    
    pip install -r "$REQ_FILE" --quiet
    echo "✅ Dépendances installées/vérifiées"
else
    echo "⚠️  ATTENTION: $REQ_FILE introuvable"
    exit 1
fi

echo ""

# 5) Créer la base de données vectorielle
if [[ -f "$DB_SCRIPT" ]]; then
    echo "🗄️  Lancement de la création de la base de données..."
    python "$DB_SCRIPT"
    echo "✅ Base de données créée"
else
    echo "❌ ERREUR: $DB_SCRIPT introuvable"
    exit 1
fi

echo ""
echo "✅ SETUP TERMINÉ AVEC SUCCÈS!"
echo ""
echo "Pour lancer l'app: Lancer LM Studio, Mettre le server en Running, ensuite lancer : streamlit run app.py"