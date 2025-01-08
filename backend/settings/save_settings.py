from database.module_settings.email import EmailSettings
from database.module_settings.news import NewsSettings
from database.module_settings.stocks import StocksSettings
from database.module_settings.traffic import TrafficSettings
from database.module_settings.weather import WeatherSettings
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/")
async def save_settings(request: Request):
    try:
        body = await request.body()
        json_body = await request.json()
        module = json_body["type"]
        settings = json_body["settings"]

        if module == "weather":

            scale_map = {
                "fahrenheit": "f",
                "celcious": "c",
                "kelvin": "k"
            }

            zipcode = settings.get("zipcode", "")
            scale = settings.get("scale", "")
            timezone = settings.get("timezone", "")

            await WeatherSettings.update_or_create(
                id=1, defaults={
                    "zipcode": zipcode,
                    "scale": scale_map[scale],
                    "timezone": timezone
                }
            )

        print(settings)
    except Exception as e:
        raise Exception(e)
