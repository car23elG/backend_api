from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# créer les tables si elles n’existent pas
Base.metadata.create_all(bind=engine)
