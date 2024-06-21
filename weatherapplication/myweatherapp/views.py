import requests
import datetime
import math  # Import the math module for rounding up
from django.shortcuts import render
from django.http import HttpResponse

# Define your API key and endpoint
appid = '07973adbcff5ae2377c93300d86417bb'
URL = 'https://api.openweathermap.org/data/2.5/weather'

def index(request):
    city = request.GET.get('city', 'London')  # Default to London if no city is provided
    PARAMS = {'q': city, 'appid': appid, 'units': 'metric'}

    try:
        # Make the API request
        response = requests.get(URL, params=PARAMS)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the JSON response
        res = response.json()

        # Check for expected keys in the response
        if 'name' in res and 'main' in res and 'weather' in res:
            # Round up the temperature
            temperature = math.ceil(res['main']['temp'])

            weather = {
                'city': res['name'],
                'temperature': temperature,  # Use the rounded temperature
                'description': res['weather'][0]['description'],
                'icon': res['weather'][0]['icon']
            }
            
        else:
            # If keys are missing, raise a KeyError with a descriptive message
            missing_keys = [key for key in ['name', 'main', 'weather'] if key not in res]
            raise KeyError(f"Missing keys in the response: {', '.join(missing_keys)}")

        day = datetime.date.today()
        context = {'weather': weather, 'day': day}

    except requests.exceptions.HTTPError as http_err:
        context = {'error': f'HTTP error occurred: {http_err}'}
    except KeyError as key_err:
        context = {'error': f'Key error: {key_err}'}
    except Exception as err:
        context = {'error': f'Other error occurred: {err}'}

    return render(request, 'myweatherapp/index.html', context)
