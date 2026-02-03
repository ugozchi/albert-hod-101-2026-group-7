# 🎭 Othello RAG Chatbot

Un chatbot conversationnel intelligent basé sur la pièce *Othello* de Shakespeare, utilisant la technique **RAG** (Retrieval-Augmented Generation) pour fournir des réponses précises et contextuelles.

## 📋 Table des matières

- [Description](#-description)
- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [Stack technique](#-stack-technique)

---

## 📖 Description

Ce projet combine une **base de données vectorielle** (ChromaDB) avec un **modèle de langage local** (LM Studio) pour créer un assistant capable de répondre à des questions sur la pièce *Othello* en s'appuyant sur le texte original.


## ✨ Fonctionnalités

- 💬 **Interface de chat interactive**
- 🔍 **Recherche sémantique** dans le texte d'Othello
- 🔄 **Reformulation automatique** des questions pour améliorer la recherche
- 📚 **Sources citées** pour chaque réponse
- 🤖 **Support multi-modèles** via LM Studio

---

## 🔧 Prérequis

### Logiciels requis

- **Python 3.8+** (compatible Python 3.13)
- **Git Bash** (Windows) ou terminal Unix (macOS/Linux)
- **LM Studio** ([Télécharger ici](https://lmstudio.ai/))

### Modèles LLM recommandés

Téléchargez et chargez dans LM Studio l'un de ces modèles :
- Mistral 3B/7B
- Llama 2/3
- Phi-3
- Tout modèle compatible OpenAI API

---

## 📦 Installation

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd othello-rag
```

### 2. Rendre le script exécutable

```bash
chmod +x start.sh
```

### 3. Lancer le script de démarrage

```bash
./start.sh
```

**Ce script automatique va :**
1. ✅ Créer un environnement virtuel Python (`.venv`)
2. ✅ Installer toutes les dépendances (`requirements.txt`)
3. ✅ Générer la base de données vectorielle (`create_db.py`)

---

## 🚀 Utilisation

### Démarrer l'application

1. **Lancer LM Studio**
   - Ouvrir l'application
   - Aller dans **Developer → Start Server**
   - Vérifier que le serveur tourne sur `http://localhost:1234`

2. **Lancer le chatbot**

```bash
streamlit run app.py
```

3. **Utiliser l'interface**
   - Rendez-vous sur `http://localhost:8501`
   - Vérifiez le statut dans la sidebar (✅ modèle chargé, ✅ base vectorielle prête)
   - Allez dans l'onglet **💬 Chat**
   - Posez vos questions !

---

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│  Question   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Query Rewriting (optional) │ ← Génère des variantes
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   ChromaDB Search           │ ← Recherche sémantique
│   (sentence-transformers)   │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   Context Augmentation      │ ← Top 5 chunks pertinents
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   LM Studio (Local LLM)     │ ← Génération de réponse
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│   Answer + Sources          │
└─────────────────────────────┘
```

---

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| **Frontend** | Streamlit |
| **Vector DB** | ChromaDB |
| **Embeddings** | sentence-transformers (`all-MiniLM-L6-v2`) |
| **LLM** | LM Studio (API OpenAI-compatible) |
| **Chunking** | Découpage par scène |
| **HTTP Client** | httpx |

---

## 📁 Structure du projet

```
othello-rag/
├── app.py                  # Application Streamlit principale
├── create_db.py           # Script de création de la base vectorielle
├── chroma_manager.py      # Gestion ChromaDB
├── start.sh               # Script de démarrage automatisé
├── requirements.txt       # Dépendances Python
├── .venv/                 # Environnement virtuel (généré)
└── chroma_db/             # Base de données vectorielle (générée)
```

---

## 🐛 Dépannage

### Problème : "Aucun modèle chargé"

**Solution :**
1. Ouvrir LM Studio
2. Charger un modèle dans l'onglet **Chat**
3. Activer le serveur : **Developer → Start Server**
4. Rafraîchir l'application Streamlit

### Problème : "Base vectorielle manquante"

**Solution :**
```bash
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
python create_db.py
```

### Problème : Erreurs de permission sur `start.sh`

**Solution :**
```bash
chmod +x start.sh
```

---

## 📄 Licence

Ce projet est à usage éducatif.

---

## 🙏 Remerciements

- Shakespeare pour *Othello* 🎭
- La communauté open-source pour les outils utilisés