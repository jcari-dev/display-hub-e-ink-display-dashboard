from bottle import Bottle, HTTPResponse, request, response
from utils.utils import (consume_file_traffic_api_file,
                         generate_traffic_api_file)

traffic_routes = Bottle()


@traffic_routes.route('/<:re:.*>', method='OPTIONS')
def handle_options():
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With"
    response.status = 200
    return {}


@traffic_routes.route('/generate', method='GET')
def generate_api_file_endpoint():
    try:
        generate_traffic_api_file()
        return HTTPResponse(
            status=200,
            body={
                "message": "API file generated successfully"
            }
        )
    except Exception as e:
        print(e)
        return HTTPResponse(
            status=500,
            body={
                "error": "Something went wrong while generating the API file",
                "actual_error": str(e)
            }
        )


@traffic_routes.route('/consume', method='GET')
def consume_api_file_endpoint():
    try:
        consume_file_traffic_api_file()
        return HTTPResponse(
            status=200,
            body={
                "message": "API file consumed and updated successfully"
            }
        )
    except Exception as e:
        print(e)
        return HTTPResponse(
            status=500,
            body={
                "error": "Something went wrong while consuming the API file",
                "actual_error": str(e)
            }
        )
