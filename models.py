from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()
class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    contenu = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    categorie = Column(String, nullable=True)
    tags = Column(String, nullable=True)
