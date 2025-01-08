from database.module_settings.email import EmailSettings
from database.module_settings.news import NewsSettings
from database.module_settings.stocks import StocksSettings
from database.module_settings.traffic import TrafficSettings
from database.module_settings.weather import WeatherSettings
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def get_settings(request: Request, module: str):
    try:
        print(f"The module: {module} has been selected.")
        weather_settings = await WeatherSettings.get_or_none(
            id=1
        )

        return {

            "scale": weather_settings.scale,
            "zipcode": weather_settings.zipcode,
            "timezone": weather_settings.timezone
        }

    except Exception as e:
        raise Exception(e)
