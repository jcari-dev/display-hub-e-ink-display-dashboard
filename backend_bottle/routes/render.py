from bottle import Bottle, request, response
from routes.render_utils.main_render import display_text_at_position

render_routes = Bottle()


@render_routes.route('/<:re:.*>', method='OPTIONS')
def handle_options():
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With"
    response.status = 200
    return {}


@render_routes.route('/', method='POST')
def render_display():

    data = request.json
    print(data)
    modules_to_render = data["modules"]

    display_text_at_position(modules_to_render)

    return {"hi": True}
