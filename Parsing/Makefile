# ===================================================================
# Makefile - Projet Parsing (Deliveroo + Quotes Scraper)
# ===================================================================

PYTHON = .venv/bin/python3
PIP = .venv/bin/pip

# --- 1. SETUP DE L'ENVIRONNEMENT ---

.venv/bin/activate: requirements.txt
	@echo "--- Création de l'environnement virtuel... ---"
	python3 -m venv .venv
	. .venv/bin/activate && \$(PIP) install --upgrade pip
	. .venv/bin/activate && \$(PIP) install -r requirements.txt
	touch .venv/bin/activate
	@echo "--- Environnement prêt. ---"

setup: .venv/bin/activate
	@echo "--- ✓ Dépendances installées. ---"

# --- 2. PARSING & SCRAPING ---

# Parsing des emails Deliveroo
all_deliveroo_orders.json: scripts/extract_all_mails.py Mails/*.html .venv/bin/activate
	@echo "--- [1/2] Parsing des emails Deliveroo... ---"
	\$(PYTHON) scripts/extract_all_mails.py
	@echo "--- [1/2] ✓ Fichier 'all_deliveroo_orders.json' créé. ---"

# Scraping des quotes (Bonus)
all_quotes.json: scripts/bonus.py .venv/bin/activate
	@echo "--- [2/2] Scraping des quotes (bonus)... ---"
	\$(PYTHON) scripts/bonus.py
	@echo "--- [2/2] ✓ Fichier 'all_quotes.json' créé. ---"

# --- 3. COMMANDES PRINCIPALES ---

# Cible par défaut : Parsing des emails Deliveroo
run: setup all_deliveroo_orders.json
	@echo "--- ✓ Parsing Deliveroo terminé. ---"

# Cible bonus : Scraping des quotes
bonus: setup all_quotes.json
	@echo "--- ✓ Scraping bonus terminé. ---"

# Cible "all" : Tout parser (Deliveroo + Bonus)
all: setup all_deliveroo_orders.json all_quotes.json
	@echo "--- ✓✓ TOUT EST PRÊT. Tous les fichiers JSON générés. ---"

# Nettoyer les fichiers générés
clean:
	@echo "--- Nettoyage des fichiers générés... ---"
	rm -f all_deliveroo_orders.json all_quotes.json
	rm -rf __pycache__
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	@echo "--- ✓ Nettoyage terminé. ---"

# Nettoyer tout (y compris .venv)
clean-all: clean
	@echo "--- Suppression de l'environnement virtuel... ---"
	rm -rf .venv
	@echo "--- ✓ Nettoyage complet terminé. ---"

# Afficher l'aide
help:
	@echo "==================================================================="
	@echo "  Makefile - Projet Parsing"
	@echo "==================================================================="
	@echo ""
	@echo "Cibles disponibles :"
	@echo "  make setup      : Créer l'environnement virtuel et installer les dépendances"
	@echo "  make run        : Parser les emails Deliveroo (défaut)"
	@echo "  make bonus      : Scraper les quotes (exercice bonus)"
	@echo "  make all        : Tout exécuter (emails + bonus)"
	@echo "  make clean      : Supprimer les fichiers JSON générés"
	@echo "  make clean-all  : Supprimer .venv et les fichiers générés"
	@echo "  make help       : Afficher cette aide"
	@echo ""

# Target "phony" pour que 'make' ne confonde pas avec des noms de fichiers
.PHONY: setup run bonus all clean clean-all help