from cryptography.fernet import Fernet
from db import Base
from sqlalchemy import Column, Integer, String

cipher = Fernet(Fernet.generate_key())


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


class StockSettings(Base):
    __tablename__ = "stock_settings"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(25), nullable=False)


class TrafficSettings(Base):
    __tablename__ = "traffic_settings"

    id = Column(Integer, primary_key=True, index=True)
    zipcode = Column(String(5), nullable=False)
    status = Column(String(10), nullable=False, default="inactive")
    _api_key = Column("api_key", String, nullable=False, default="-")

    @property
    def api_key(self):
        """Decrypt and return the API key."""
        return cipher.decrypt(self._api_key.encode()).decode()

    @api_key.setter
    def api_key(self, value):
        """Encrypt and store the API key."""
        self._api_key = cipher.encrypt(value.encode()).decode()
