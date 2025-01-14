import os

from bottle import Bottle, request, response
from db import init_db
from routes import (render_routes, setting_routes, traffic_routes,
                    weather_routes)

app = Bottle()

init_db()

# os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'


@app.hook("after_request")
def enable_cors():
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With"


app.mount('/weather', weather_routes)
app.mount('/settings', setting_routes)
app.mount('/render', render_routes)
app.mount('/traffic', traffic_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8001)
