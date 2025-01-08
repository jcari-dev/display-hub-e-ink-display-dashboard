from database.module_settings.weather import WeatherSettings
from fastapi import APIRouter, Request
from module_data_gen.thirdparty_apis.weather import gather_weather_data

router = APIRouter()


@router.get("/")
async def weather_root():
    print(gather_weather_data)
    return {"message": "Base Weather URL."}


@router.get("/test")
async def weather_test_root():
    data = gather_weather_data()
    print(data)
    if "data" in data:
        print("Weather API Test: Weather data fetched successfully!")
        return {"message": "Weather data fetched successfully!", "data": data["data"]}
    elif "error" in data:
        print("Weather API Test: Failed to fetch weather data")
        return {"message": "Failed to fetch weather data", "error": data["error"]}
    else:
        print("Weather API Test: Unexpected error")
        return {"message": "Unexpected error", "error": "Unknown issue occurred"}
