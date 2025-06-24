# Chatbot d'Orientation Post-Bac

## 🚀 Présentation

Ce projet propose un **chatbot d'orientation** simple et interactif destiné aux élèves de terminale. Le bot :

- Pose des questions sur les centres d'intérêt de l'utilisateur
- Propose des métiers en lien avec ces centres d'intérêt via l'API ROME ou un dictionnaire local
- Affiche des fiches détail métier (description et liens)
- Gère les dialogues multi-étapes, les réponses oui/non, et corrige les fautes d'orthographe

Le chatbot s'utilise en **ligne de commande** ou via une **interface web Flask**.

---

## 📦 Structure du projet

```text
├── config.py           # Clés CLIENT_ID / CLIENT_SECRET pour l'API ROME
├── rome_api.py         # Wrapper pour l'API ROME + dictionnaire
├── chatbot.py          # Logique de discussion (multi-étapes, orthographe)
├── webapp.py           # Application Flask pour interface web du chatbot
├── requirements.txt    # Dépendances Python du projet
└── README.md           # Document d'explication du projet (vous êtes ici)

```

## 🤖 Arbre de Conversation

Le chatbot fonctionne selon un machine à états :
```
[ask_interest]
  └─> l'utilisateur saisit un centre d'intérêt
       ├─> API ROME renvoie des métiers (ou fallback local)
       └─> suggestions affichées
            └─> transition vers [ask_job_choice]

[ask_job_choice]
  └─> l'utilisateur choisit un numéro (1-3)
       ├─> si valide : récupération du métier sélectionné
       │     └─> transition vers [show_detail]
       └─> sinon : redemande le numéro

[show_detail]
  └─> affichage de la fiche métier (description)
       ├─> si 'oui' : transition vers [ask_continue]
       ├─> si 'non' : retour à [ask_interest]
       └─> sinon : redemande 'oui' ou 'non'

[ask_continue]
  └─> l'utilisateur décide de continuer
       ├─> si 'oui' : retour à [ask_interest]
       └─> si 'non' : transition vers [end]

[end]
  └─> fin de session, invite à relancer pour recommence

```
Chaque état est stocké dans chatbot.contexts ```[context_id]['stage'] ```. La correction orthographique est appliquée avant chaque traitement pour fiabiliser l'interprétation.

## ⚙️ Installation

1. **Cloner le dépôt**  
   ```bash
   git clone https://github.com/JLWear/Chat-Bot
   cd chatbot-orientation
Créer et activer un environnement virtuel

Installer les dépendances

```
pip install -r requirements.txt 
pip install Flask requests pyspellchecker
```


Configurer les clés API

Renommer config.example.py en config.py

Compléter CLIENT_ID et CLIENT_SECRET pour l’API ROME (Pôle Emploi)
