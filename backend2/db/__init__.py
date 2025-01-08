from config import SessionLocal, engine
from sqlalchemy.ext.declarative import declarative_base

# Base class for models
Base = declarative_base()

# Dependency for getting DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database and create tables


def init_db():
    from db.models import WeatherSettings
    Base.metadata.create_all(bind=engine)
