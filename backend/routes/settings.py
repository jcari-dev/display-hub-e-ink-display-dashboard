from bottle import Bottle, request, response
from db import get_db
from db.models import (NewsSettings, StockSettings, TrafficSettings,
                       WeatherSettings)

setting_routes = Bottle()


@setting_routes.route('/<:re:.*>', method='OPTIONS')
def handle_options():
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With"
    response.status = 200
    return {}


@setting_routes.route('/save', method=['POST'])
def save_settings():
    data = request.json
    module = data["module"]
    settings_fetched = data["settings"]
    saved_settings = {}

    db = next(get_db())

    try:
        if module == "weather":
            settings = db.get(WeatherSettings, 1)
            if settings:
                settings.scale = settings_fetched["scale"]
                settings.zipcode = settings_fetched["zipcode"]
                settings.timezone = settings_fetched["timezone"]
            else:
                settings = WeatherSettings(
                    id=1,
                    scale=settings_fetched["scale"],
                    zipcode=settings_fetched["zipcode"],
                    timezone=settings_fetched["timezone"]
                )
                db.add(settings)

            db.commit()
            db.refresh(settings)

            saved_settings = {
                "id": settings.id,
                "scale": settings.scale,
                "zipcode": settings.zipcode,
                "timezone": settings.timezone
            }

        elif module == "news":
            settings = db.get(NewsSettings, 1)
            if settings:
                settings.outlet = settings_fetched["outlet"]
                settings.rss_feed = settings_fetched["rss_feed"]
                settings.language = settings_fetched["language"]
            else:
                settings = NewsSettings(
                    id=1,
                    outlet=settings_fetched["outlet"],
                    rss_feed=settings_fetched["rss_feed"],
                    language=settings_fetched["language"]
                )
                db.add(settings)

            db.commit()
            db.refresh(settings)

            saved_settings = {
                "id": settings.id,
                "outlet": settings.outlet,
                "rss_feed": settings.rss_feed,
                "language": settings.language
            }
        elif module == "stocks":
            settings = db.get(StockSettings, 1)
            if settings:
                settings.ticker = settings_fetched["ticker"]
            else:
                settings = StockSettings(
                    id=1,
                    ticker=settings_fetched["ticker"],
                )
                db.add(settings)

            db.commit()
            db.refresh(settings)

            saved_settings = {
                "id": settings.id,
                "ticker": settings.ticker,
            }
        elif module == "traffic":
            settings = db.get(TrafficSettings, 1)
            if settings:
                settings.zipcode = settings_fetched["zipcode"]
            else:
                settings = TrafficSettings(
                    id=1,
                    zipcode=settings_fetched["zipcode"],
                )
                db.add(settings)

            db.commit()
            db.refresh(settings)

            saved_settings = {
                "id": settings.id,
                "zipcode": settings.zipcode,
            }

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return saved_settings


@setting_routes.route('/get', method=['GET'])
def get_settings():
    db = next(get_db())
    # TODO ENSURE YOU'RE ONLY PULLING THE SETTINGS FROM THE MODULE YOU ASKED.

    module = request.query.module

    if not module:
        db.close()
        response.status = 400
        return {"error": "Module parameter is required"}
    if module == "weather":
        settings = db.get(WeatherSettings, 1)

        db.close()

        if not settings:
            response.status = 404
            return {"error": "Weather settings not found"}
        return {
            "id": settings.id,
            "scale": settings.scale,
            "zipcode": settings.zipcode,
            "timezone": settings.timezone
        }

    elif module == "news":
        settings = db.get(NewsSettings, 1)

        db.close()

        if not settings:
            response.status = 404
            return {"error": "News settings not found"}
        return {
            "id": settings.id,
            "language": settings.language,
            "outlet": settings.outlet,
            "rss_feed": settings.rss_feed,

        }
    elif module == "stocks":
        settings = db.get(StockSettings, 1)

        db.close()

        if not settings:
            response.status = 404
            return {"error": "Stock settings not found"}
        return {
            "id": settings.id,
            "ticker": settings.ticker,

        }
    elif module == "traffic":
        settings = db.get(TrafficSettings, 1)

        db.close()

        if not settings:
            response.status = 404
            return {"error": "Traffic settings not found"}
        return {
            "id": settings.id,
            "zipcode": settings.zipcode,

        }
