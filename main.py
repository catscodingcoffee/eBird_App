import json
import os
from pathlib import Path

from ebird.api.requests import *
from ebird.api.requests.validation import clean_lat, clean_lng

from geopy.geocoders import Nominatim, GoogleV3

from dotenv import load_dotenv

_region_lookup = json.loads(Path("references/region_lookup.json").read_text())


def get_api_key()->tuple[str,str]:
    '''
    Retrieves API keys
    :return: tuple of API keys
    '''
    load_dotenv()
    api_key = os.getenv("EBIRD_API_KEY")
    google_api_key = os.getenv("MAPS_API_KEY")
    return api_key,google_api_key

def get_coordinates(address:str)->dict:
    '''
    Gets coordinates from user entered address
    :param address: str address to get coordinates of
    :return: dictionary of latitude and longitude
    '''
    try:
        google_api_key = get_api_key()[1]
        geolocator = GoogleV3(google_api_key,domain="maps.googleapis.com",user_agent='ebird_app')
        location = geolocator.geocode(address)
        info = {}
        info["lat"] = location.latitude
        info["lng"] = location.longitude
        return info
    except AttributeError:
        return "Address not found"

def get_area_info(coordinates: tuple[float,float])->dict:
    google_api_key = get_api_key()[1]
    geolocator = GoogleV3(google_api_key, domain="maps.googleapis.com", user_agent='ebird_app')
    location= geolocator.reverse(coordinates)
    address = location.raw
    info = {}
    for component in address["address_components"]:
        types = component["types"]
        if "locality" in types:
            info["city"] = component["long_name"]
        elif "administrative_area_level_2" in types:
            info["county"] = component["long_name"]
        elif "administrative_area_level_1" in types:
            info["state"] = component["short_name"]
        elif "country" in types:
            info["country"] = component["short_name"]

    return info

def create_ebird_region(info: dict) -> str:
    code = f"{info['country']}-{info['state']}"
    if code not in _region_lookup["subnational1"]:
        raise ValueError(f"'{code}' is not a recognized eBird subnational1 region code")
    return code


def get_user_location()->str:
    try:
        user_location = input("Enter your address or city,state combination: ")
        return user_location
    except TypeError:
        return "Invalid entry"



def main():
    ebird_key = get_api_key()[0]
    user_location = '13134 SW Tamera Ln Tigard OR'#get_user_location()
    info_dict = get_coordinates(user_location)
    lat = info_dict["lat"]
    lng = info_dict["lng"]

    area = get_area_info((lat,lng))
    '''for s in area:
        print(s)'''


    '''
    google_api_key = get_api_key()[1]
    geolocator = GoogleV3(google_api_key, domain="maps.googleapis.com", user_agent='ebird_app')
    location = geolocator.reverse((info_dict["lat"],info_dict["lng"]))
    print(location)
    '''
    print(f"The coordinates of {user_location} is latitude {info_dict["lat"]} and longitude {info_dict["lng"]}")


if __name__ == '__main__':
    main()