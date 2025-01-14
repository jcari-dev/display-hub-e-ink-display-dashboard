from bottle import Bottle, request, response

weather_routes = Bottle()


@weather_routes.route('/test', method='GET')
def save_settings():

    return {
        "message": "works"
    }
