from bottle import Bottle, HTTPResponse, request, response
from routes.render_utils.main_render import (display_clear,
                                             display_text_at_position)

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
    try:
        data = request.json
        modules_to_render = data["modules"]
        display_text_at_position(modules_to_render)
        return HTTPResponse(
            status=200,
            body={
                "message": "Display rendered successfully"
            }
        )
    except Exception as e:
        print(e)
        return HTTPResponse(
            status=500,
            body={
                "error": "Something went wrong",
                "actual_error": str(e)
            }
        )


@render_routes.route('/clear', method='GET')
def clear_display():
    try:
        display_clear()
        return HTTPResponse(
            status=200,
            body={
                "message": "Display cleared successfully"
            }
        )
    except Exception as e:
        return HTTPResponse(
            status=500,
            body={
                "error": "Something went wrong",
                "actual_error": str(e)
            }
        )
