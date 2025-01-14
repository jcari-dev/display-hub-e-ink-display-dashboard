import requests


def convert_to_lat_long(zipcode="32836"):
    """
    Convert a ZIP code to latitude and longitude using a local file.
    """
    try:
        with open("./data_submodules/US.txt", "r") as file_map:
            for line in file_map:
                columns = line.strip().split("\t")
                zipcode_column = columns[1]

                if zipcode == zipcode_column:
                    lat_column = columns[9]
                    long_column = columns[10]
                    return {
                        "lat": float(lat_column),
                        "long": float(long_column)
                    }
        return {"error": f"ZIP code {zipcode} not found in the file."}

    except FileNotFoundError:
        return {"error": "Data file not found."}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


def gather_weather_data(scale, timezone, zipcode="32836"):
    """
    Gather weather data for a given ZIP code.
    """
    try:

        latlong = convert_to_lat_long(zipcode)
        if "error" in latlong:
            return latlong

        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latlong["lat"],
                "longitude": latlong["long"],
                "current_weather": True,
                "temperature_unit": scale,
                "timezone": "auto"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return {"data": data}

    except requests.exceptions.RequestException as e:
        print(e)

        return {"error": f"Request error: {e}"}
    except ValueError as e:
        print(e)

        return {"error": f"JSON decode error: {e}"}
    except Exception as e:
        print(e)
        return {"error": f"Unexpected error: {e}"}
