from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    # Get city from form input or default to 'Indore'
    city = request.POST.get('city', 'Indore')

    # API keys (Ensure these are set correctly)
    API_KEY = "53d4e4fcde475537dca3013f37c23cd3"  # Your OpenWeatherMap API key
    SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"  # Replace with actual search engine ID

    # OpenWeatherMap API URL
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    PARAMS = {'units': 'metric'}

    # Google Image Search API URL
    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    search_type = 'image'
    
    google_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge"

    # Try fetching weather data
    try:
        weather_response = requests.get(weather_url, params=PARAMS)
        weather_data = weather_response.json()

        # Ensure the API response contains expected keys
        if "weather" not in weather_data or "main" not in weather_data:
            raise KeyError("Invalid response from weather API")

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

    except (requests.RequestException, KeyError) as e:
        messages.error(request, 'Could not fetch weather data. Using default values.')
        description = 'clear sky'
        icon = '01d'
        temp = 25
        day = datetime.date.today()

    # Try fetching an image for the city
    image_url = None
    try:
        google_response = requests.get(google_url)
        google_data = google_response.json()

        # Ensure API response contains images
        search_items = google_data.get("items")
        if search_items and len(search_items) > 1:
            image_url = search_items[1]['link']
        else:
            image_url = None

    except (requests.RequestException, KeyError) as e:
        messages.error(request, 'Could not fetch image for the city.')

    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'exception_occurred': False,
        'image_url': image_url or "https://via.placeholder.com/1920x1080?text=No+Image+Available"
    })
