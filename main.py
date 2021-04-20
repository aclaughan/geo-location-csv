import pandas as pd
import requests
import logging
from urllib.parse import urlencode
from secrets import GOOGLE_API_KEY

logging.basicConfig(level=logging.INFO, filename="geo.log")


def main():
    """
    given a list of human search strings, will create a CSV of google
    geolocation results
    :return:
    """
    
    addresses = \
        [
            "Nicolway, Bryanston, Sandton, South Africa",
            "Samsung, 2929 William Nicol Dr, Bryanston, South Africa",
            "Renault, bryanston, south africa"
        ]

    places = {}
    site_no = 0

    for address in addresses:
        data = extract_lat_long(address)
        places[site_no] = data
        site_no += 1
        logging.info(data)

    df = pd.DataFrame(places)
    df = df.T
    df.to_csv("places.csv")


def extract_lat_long(address):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {"address": address, "key": GOOGLE_API_KEY}

    # convert the 'English' string to HTML
    url_params = urlencode(params)

    url = f"{endpoint}?{url_params}"

    logging.info(url)

    response = requests.get(url)
    if response.status_code in range(200, 299):
        location = response.json()['results'][0]
        coords = {
            "lat": f"{location['geometry']['location']['lat']}",
            "lng": f"{location['geometry']['location']['lng']}",
            "address": f"{location['formatted_address']}",
            "plus_code": f"{location['plus_code']['global_code']}"
        }
        return coords

    else:
        return "not found"


if __name__ == '__main__':
    main()

# logging.debug(stuff)
