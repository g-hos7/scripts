# Tim Barnes
# v0.0.3
# 2022-07-08
#
# Find restaurants within a given geographic area and choose one at random.
# The user enters their address and desired search radius.
# The script uses the yelp api to find restaurants within the specified radius
# around the user's address.

from requests import request
from os import environ
from random import randrange
from dotenv import load_dotenv
from urllib.parse import quote

API_HOST = "https://api.yelp.com"
SEARCH_PATH = "/v3/businesses/search"
DEFAULT_TERM = "food"
KILOMETER_CONVERSION_FACTOR = 0.62137119

location_prompt = "Enter your street address: "
radius_prompt = "Enter the number of miles to search in: "


def get_location(prompt):

    return input(prompt)


# Get radius in miles, convert to meters, and return a rounded number
def get_radius(prompt):
    radius_in_miles = int(input(prompt))
    radius_in_meters = (radius_in_miles / KILOMETER_CONVERSION_FACTOR) * 1000

    return round(radius_in_meters)


def get_api_key():
    load_dotenv()

    return environ.get("yelp_api_key")


def get_random_number(list):

    return randrange(0, len(list))


def make_request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, radius):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'radius': radius
    }

    return make_request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


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
    location = get_location(location_prompt)
    radius = get_radius(radius_prompt)
    api_key = get_api_key()
    business_list = search(api_key, DEFAULT_TERM, location, radius)
    names_list = parse_results(business_list)
    place_to_eat = random_picker(names_list)

    print(f"\nEat lunch at {place_to_eat} today!\n")


main()