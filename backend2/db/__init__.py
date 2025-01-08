from config import SessionLocal, engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from db.models import WeatherSettings
    Base.metadata.create_all(bind=engine)
