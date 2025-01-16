import csv
import time

import requests
from db import get_db
from db.models import TrafficSettings

# TomTom API configuration
BASE_URL_INCIDENTS = "https://api.tomtom.com/traffic/services/5/incidentDetails"

# Icon category dictionary for human-readable descriptions
icon_category_dict = {
    0: "Accident",
    1: "Fog",
    2: "Dangerous Conditions",
    3: "Rain",
    4: "Ice",
    5: "Jam",
    6: "Lane Closed",
    7: "Road Closed",
    8: "Heavy Traffic",
    9: "Road Works",
    10: "Narrow Lanes",
    11: "Tow Trucks",
    14: "Other"
}

street_abbreviations = {
    "Street": "St",
    "Avenue": "Ave",
    "Boulevard": "Blvd",
    "Road": "Rd",
    "Drive": "Dr",
    "Court": "Ct",
    "Lane": "Ln",
    "Terrace": "Ter",
    "Place": "Pl",
    "Square": "Sq",
    "Circle": "Cir",
    "Highway": "Hwy",
    "Parkway": "Pkwy",
    "Trail": "Trl",
    "Way": "Wy",
    "Expressway": "Expy",
    "Freeway": "Fwy",
    "Crescent": "Cres",
    "Alley": "Aly",
    "Fort": "Ft",
    "Mount": "Mt",
    "Station": "Sta"
}


def abbreviate_address(address):
    # Replace street types with abbreviations
    for full, abbrev in street_abbreviations.items():
        address = address.replace(full, abbrev)
    # Add a newline after each comma
    address = address.replace(", ", ",\n", 1)
    return address

# Load ZIP-to-lat/lon data from the provided file


def get_lat_lon_from_zip(zip_code, file_path="./data_submodules/US.txt"):
    with open(file_path, mode="r") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            if row[1] == zip_code:  # Compare ZIP code
                return float(row[9]), float(row[10])  # Return lat, lon
    raise ValueError(f"ZIP code {zip_code} not found in dataset")

# Reverse Geocoding Function for human-readable addresses


def reverse_geocode(lat, lon, api_key):
    url = f"https://api.tomtom.com/search/2/reverseGeocode/{lat},{lon}.json"
    params = {"key": api_key, "language": "en-GB"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        address = data.get("addresses", [{}])[0].get(
            "address", {}).get("freeformAddress", "Unknown Location")
        return address
    else:
        return f"Error: {response.status_code}"

# Function to fetch active/recent incidents for a ZIP code


# Function to fetch active/recent incidents
def fetch_incidents():
    try:
        print("Starting incident fetch process...")

        # Get the TrafficSettings record with id=1
        print("Fetching TrafficSettings from the database...")
        db = next(get_db())
        traffic_settings = db.get(TrafficSettings, 1)
        if not traffic_settings:
            raise ValueError("Traffic settings with id=1 not found.")

        # Extract API key and ZIP code
        print("Extracting API key and ZIP code...")
        api_key = traffic_settings.api_key  # Decryption happens in the property
        zip_code = traffic_settings.zipcode
        print(f"API Key and ZIP Code successfully retrieved: {zip_code}")

        incident_list = []

        # Step 1: Convert ZIP code to lat/lon using the file
        print(f"Converting ZIP code {zip_code} to latitude and longitude...")
        lat, lon = get_lat_lon_from_zip(zip_code)
        print(f"Latitude and Longitude for {zip_code}: ({lat}, {lon})")

        # Step 2: Define bounding box (small area around ZIP code)
        delta = 0.01  # Adjust for desired radius (in degrees)
        bbox = f"{lon-delta},{lat-delta},{lon+delta},{lat+delta}"
        print(f"Bounding box for the API query: {bbox}")

        # Step 3: Query TomTom for traffic incidents
        print("Querying TomTom API for traffic incidents...")
        params = {
            "bbox": bbox,
            "fields": "{incidents{type,geometry{type,coordinates},properties{iconCategory}}}",
            "language": "en-GB",
            "categoryFilter": "0,1,2,3,4,5,6,7,8,9,10,11,14",
            "timeValidityFilter": "present",
            "key": api_key
        }
        response = requests.get(BASE_URL_INCIDENTS, params=params)

        if response.status_code == 200:
            print("API query successful. Processing incidents...")
            data = response.json()
            incidents = data.get("incidents", [])
            print(f"Number of incidents found: {len(incidents)}")
            incidents = incidents[:1]

            # Step 4: Process and display each incident
            for i, incident in enumerate(incidents):
                icon_category = incident['properties'].get(
                    'iconCategory', 'N/A')
                category_description = icon_category_dict.get(
                    icon_category, "Unknown")
                coordinates = incident['geometry']['coordinates']

                total_lat = sum(coord[1]
                                for coord in coordinates) / len(coordinates)
                total_lon = sum(coord[0]
                                for coord in coordinates) / len(coordinates)
                print(
                    f"Incident {i}: Calculated average coordinates: ({total_lat}, {total_lon})")

                street_name = reverse_geocode(total_lat, total_lon, api_key)
                print(f"Incident {i}: Reverse geocoded address: {street_name}")

                street_name = abbreviate_address(street_name)
                print(f"Incident {i}: Abbreviated address: {street_name}")

                incident_list.append((street_name, category_description))
                time.sleep(0.5)  # Adjust delay based on API limits
                print(f"Incident {i}: Added to the incident list.")

        else:
            print(
                f"Error fetching incidents: {response.status_code} - {response.text}")

        print("Incident fetch process completed.")
        return incident_list

    except ValueError as e:
        print(f"Error during incident fetching: {e}")

    finally:
        print("Closing the database connection.")
        db.close()
