from db import Base
from sqlalchemy import Column, Integer, String


class WeatherSettings(Base):
    __tablename__ = "weather_settings"

    id = Column(Integer, primary_key=True, index=True)
    scale = Column(String(1), nullable=False)
    zipcode = Column(String(5), nullable=False)
    timezone = Column(String(30), nullable=False)


class NewsSettings(Base):
    __tablename__ = "news_settings"

    id = Column(Integer, primary_key=True, index=True)
    outlet = Column(String(50), nullable=False)
    rss_feed = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)
