# Tim Barnes
# v0.0.2
# 2022-07-08
#
# Find restaurants within a given geographic area and choose one at random.
# The user enters their address and desired search radius.
# The script uses the yelp api to find restaurants within the specified radius
# around the user's address.

import random
import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote

API_HOST = "https://api.yelp.com"
SEARCH_PATH = "/v3/businesses/search"
DEFAULT_TERM = "food"

location_prompt = "Enter your address: "
radius_prompt = "Enter your desired search radius in whole miles: "


def get_input(prompt):
    return input(prompt)


def get_api_key():
    load_dotenv()
    return os.environ.get("yelp_api_key")


def convert_miles_to_meters(miles):
    conversion_factor = 0.62137119
    kilometers = int(miles) / conversion_factor
    meters = kilometers * 1000
    return round(meters)


def get_random_number(list):
    return random.randrange(0, len(list))


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, radius):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'radius': radius
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def parse_results(results):
    businesses = results["businesses"]
    list = []
    for business in businesses:
        list.append(business["name"])
    return list


def random_picker(list):
    number = get_random_number(list)
    return list[number]


def main():
    location = get_input(location_prompt)
    radius = convert_miles_to_meters(get_input(radius_prompt))
    api_key = get_api_key()
    result = search(api_key, DEFAULT_TERM, location, radius)
    options = parse_results(result)
    place_to_eat = random_picker(options)

    print(f"\nEat lunch at {place_to_eat} today!\n")


main()