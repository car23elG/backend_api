from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Article, Base
from schemas import ArticleCreate, ArticleRead
from typing import List

app = FastAPI(title="Blog API")

# dépendance pour récupérer la session de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# POST /api/articles
# Créer un article
# -----------------------
@app.post("/api/articles", response_model=ArticleRead, status_code=201)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

# -----------------------
# GET /api/articles
# Lister tous les articles
# -----------------------
@app.get("/api/articles", response_model=List[ArticleRead])
def read_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return articles

# -----------------------
# GET /api/articles/{id}
# Lire un article unique
# -----------------------
@app.get("/api/articles/{id}", response_model=ArticleRead)
def read_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article

# -----------------------
# PUT /api/articles/{id}
# Modifier un article
# -----------------------
@app.put("/api/articles/{id}", response_model=ArticleRead)
def update_article(id: int, updated: ArticleCreate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    for key, value in updated.dict().items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article

# -----------------------
# DELETE /api/articles/{id}
# Supprimer un article
# -----------------------
@app.delete("/api/articles/{id}")
def delete_article(id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    db.delete(article)
    db.commit()
    return {"detail": "Article supprimé avec succès"}

# -----------------------
# GET /api/articles/search?query=texte
# Rechercher un article par texte
# -----------------------
@app.get("/api/articles/search", response_model=List[ArticleRead])
def search_articles(query: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(
        (Article.titre.contains(query)) | (Article.contenu.contains(query))
    ).all()
    return articles
