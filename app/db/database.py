from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.settings.db import service_database_settings

DATABASE_URL = service_database_settings.postgresql_url
engine = create_engine(DATABASE_URL, echo=True,)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
