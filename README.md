# BlogBackend – API Backend pour Blog

## Description

Ce projet est une API backend pour gérer un blog simple avec des articles.  
Chaque article contient : `titre`, `contenu`, `auteur`, `date`, `categorie` et `tags`.  
L'API est développée avec Python **FastAPI**, utilise **SQLite** comme base de données et est documentée automatiquement via **Swagger UI**.  
Elle permet de créer, lire, modifier, supprimer et rechercher des articles.

---

## Technologies utilisées

- Python 3.8+
- FastAPI – framework web pour créer l'API
- SQLite – base de données légère
- SQLAlchemy – ORM pour gérer les interactions avec la base
- Pydantic – validation des données
- Uvicorn – serveur ASGI pour lancer l'application

---

## Prérequis

- Ubuntu (ou tout système Linux)
- Python 3 et pip installés
- curl installé (`sudo apt install curl`)

---

## Installation et exécution

### 1. Cloner le dépôt

```bash
git clone https://github.com//BlogBackend.git
cd BlogBackend
```

### 2. Créer et activer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

> Tu verras `(venv)` apparaître au début de ta ligne de commande.

### 3. Installer les dépendances

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 4. ⚠️ Corriger le bug de la route search

Dans `main.py`, la route `/api/articles/search` doit être placée **avant** la route `/api/articles/{id}`, sinon FastAPI interprète `search` comme un `id` entier et retourne une erreur 422.

Déplace ce bloc **avant** `GET /api/articles/{id}` :

```python
@app.get("/api/articles/search", response_model=List[ArticleRead])
def search_articles(query: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(
        (Article.titre.contains(query)) | (Article.contenu.contains(query))
    ).all()
    return articles
```

### 5. Lancer le serveur

```bash
uvicorn main:app --reload --port 8000
```

Tu devrais voir :

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

- API disponible sur : http://127.0.0.1:8000
- Documentation Swagger : http://127.0.0.1:8000/docs
- Redoc (alternative) : http://127.0.0.1:8000/redoc

---

## Structure du projet

```
BlogBackend/
├── main.py        # fichier principal avec tous les endpoints
├── models.py      # définition de la table Article
├── database.py    # connexion à SQLite
├── schemas.py     # validation des données entrantes et sortantes
├── blog.db        # base de données SQLite (générée automatiquement)
├── .gitignore     # fichiers à ignorer dans Git
└── README.md      # ce fichier
```

---

## Endpoints disponibles

| Méthode  | Endpoint                        | Description                        |
|----------|---------------------------------|------------------------------------|
| POST     | /api/articles                   | Créer un article                   |
| GET      | /api/articles                   | Lister tous les articles           |
| GET      | /api/articles/{id}              | Lire un article unique             |
| PUT      | /api/articles/{id}              | Modifier un article                |
| DELETE   | /api/articles/{id}              | Supprimer un article               |
| GET      | /api/articles/search?query=     | Rechercher un article par texte    |

---

## Exemples d'utilisation avec curl

> Installe curl si nécessaire : `sudo apt install curl`

### Créer un article

```bash
curl -X POST "http://127.0.0.1:8000/api/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Mon premier article",
    "contenu": "Contenu de larticle",
    "auteur": "Duval Ts",
    "categorie": "Tech",
    "tags": "Python,Backend"
  }'
```

### Lister tous les articles

```bash
curl -X GET "http://127.0.0.1:8000/api/articles"
```

### Lire un article précis (ex: id=1)

```bash
curl -X GET "http://127.0.0.1:8000/api/articles/1"
```

### Modifier un article (ex: id=1)

```bash
curl -X PUT "http://127.0.0.1:8000/api/articles/1" \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Article modifié",
    "contenu": "Contenu modifié",
    "auteur": "Duval Ts",
    "categorie": "Tech",
    "tags": "Python,Backend"
  }'
```

### Supprimer un article (ex: id=1)

```bash
curl -X DELETE "http://127.0.0.1:8000/api/articles/1"
```

### Rechercher un article par mot-clé

```bash
curl -X GET "http://127.0.0.1:8000/api/articles/search?query=Python"
```

---

## Tester avec Swagger UI

Swagger UI est intégré automatiquement par FastAPI. Une fois le serveur lancé, ouvre ton navigateur et accède à :

```
http://127.0.0.1:8000/docs
```

> Alternative Redoc : http://127.0.0.1:8000/redoc

### Comment utiliser Swagger :

1. **Ouvre** http://127.0.0.1:8000/docs dans ton navigateur
2. **Clique sur un endpoint** (ex: `POST /api/articles`)
3. **Clique sur "Try it out"**
4. **Remplis le champ JSON** avec tes données, par exemple :

```json
{
  "titre": "Mon article",
  "contenu": "Contenu de larticle",
  "auteur": "Duval Ts",
  "categorie": "Tech",
  "tags": "Python"
}
```

5. **Clique sur "Execute"** → la réponse s'affiche directement

> ⚠️ Le serveur doit tourner (`uvicorn main:app --reload --port 8000`) avant d'ouvrir Swagger.

---

## Déploiement (optionnel)

L'API peut être déployée sur Railway, Render ou Heroku.  
Swagger sera accessible directement après déploiement pour tester les endpoints.

---

## Auteur

Donfack Donkeng Carel Sandra
