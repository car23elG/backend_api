from pydantic import BaseModel
from typing import Optional
import datetime
class ArticleCreate(BaseModel):
    titre: str
    contenu: str
    auteur: str
    categorie: Optional[str] = None
    tags: Optional[str] = None
class ArticleRead(ArticleCreate):
    id: int
    date: datetime.datetime
    class Config:
        orm_mode = True

