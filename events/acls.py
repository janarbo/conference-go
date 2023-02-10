import json
import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

def get_photo(city, state):

    headers = {"Authorization":PEXELS_API_KEY}
    location = f"{city} {state}"
    URL = f"https://api.pexels.com/v1/search?query={location}&per_page=1&page=1"
    response = requests.get(URL, headers=headers)
    r = json.loads(response.content)
    pic = {"picture_url": r["photos"][0]["src"]["original"]}

    return pic



    # Create a dictionary for the headers to use in the request
    # Create the URL for the request with the city and state
    # Make the request
    # Parse the JSON response
    # Return a dictionary that contains a `picture_url` key and
    #   one of the URLs for one of the pictures in the response


def get_weather_data( city, state):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},US&limit=1&appid={OPEN_WEATHER_API_KEY}"
    response = requests.get(url)
    r = json.loads(response.content)
    lat = r[0]["lat"]
    lon = r[0]["lon"]


    # Create the URL for the geocoding API with the city and state
    # Make the request
    # Parse the JSON response
    # Get the latitude and longitude from the response
    url_w = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}"
    response_w = requests.get(url_w)
    r_w = json.loads(response_w.content)
    weather = {"main_temp":r_w["main"]["temp"], "weather_description":r_w["weather"][0]["description"],}
    return weather
    # Create the URL for the current weather API with the latitude
    #   and longitude
    # Make the request
    # Parse the JSON response
    # Get the main temperature and the weather's description and put
    #   them in a dictionary
    # Return the dictionary
