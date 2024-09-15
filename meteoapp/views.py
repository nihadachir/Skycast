# views.py
from django.shortcuts import render
import requests
from django.http import JsonResponse
import datetime

def home(request):
    # Extracting the city from the GET parameters
    city = request.GET.get('search', '')

    if not city:
        # Set a default city or handle the case as needed
        city = 'Rabat'

    # Make the current weather API request using the provided city
    current_api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=045255d77ed2260af068720f5d18670a"
    current_json_data = requests.get(current_api).json()

    if 'weather' not in current_json_data or 'main' not in current_json_data:
        return JsonResponse({'error': 'Failed to fetch current weather data'})

    # Extracting current weather information
    condition = current_json_data['weather'][0]['main']
    description = current_json_data['weather'][0]['description']
    temp = current_json_data['main']['temp'] - 273.15
    pressure = current_json_data['main']['pressure']
    humidity = current_json_data['main']['humidity']
    wind = current_json_data['wind']['speed']

    # Make the forecast API request using the provided city
    forecast_api = "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=045255d77ed2260af068720f5d18670a"
    forecast_json_data = requests.get(forecast_api).json()

    if 'list' not in forecast_json_data:
        return JsonResponse({'error': 'Failed to fetch forecast data'})

    # Extracting forecast data for each day of the week
    weekly_data = {}
    for forecast in forecast_json_data['list']:
        date_time = forecast['dt_txt']

        # Convert the date string to a datetime object
        date_obj = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

        # Get the day of the week
        day_of_week = date_obj.strftime('%A')

        temperature = forecast['main']['temp'] - 273.15
        weather_condition = forecast['weather'][0]['main']
        weather_description = forecast['weather'][0]['description']
        

        # Removed unnecessary list append operation
        if day_of_week not in weekly_data:
            weekly_data[day_of_week] = {
                'day_of_week': day_of_week,
                'temperature': temperature,
                'condition': weather_condition,
                'description': weather_description,
            }

    # Convert the dictionary values to a list
    weekly_data_list = list(weekly_data.values())

    # Creating a dictionary with current weather information and weekly forecast
    weather_data = {
        'city': city,
        'condition': condition,
        'description': description,
        'temp': temp,
        'pressure': pressure,
        'humidity': humidity,
        'wind': wind,
        'weekly_data': weekly_data_list,
    }

    # Render the template with weather data
    return render(request, 'home.html', {'weather_data': weather_data})



def get_weather_icon(condition):
    if condition == "Clear":
        return 'bx bxs-sun'
    elif condition == "Clouds":
        return 'bx bxs-cloud'
    elif condition == "Rain":
        return 'bx bxs-cloud-rain'
    elif condition == "Thunderstorm":
        return 'fas fa-wind'
    elif condition == "Snow":
        return 'bx bx-cloud-snow'
    else:
        return 'fas fa-question-circle'



def show_map(request):  
    countries = ["Maroc", "Algérie", "Mauritanie", "Egypt", "Libye", "Tanzanie", "Soudan", "Mali","Angola","niger","tchad","nigeria","namibia","Somalie","Mozambique"]
    weather_data_list = []  # Liste pour stocker les données météorologiques de chaque pays

    capital_coordinates = {
        "Maroc": [34.0151, -6.8341],
        "Algérie": [36.7526, 3.0576],
        "Mauritanie": [18.1422, -15.9784],
        "Egypt": [30.0444, 31.2357],
        "Libye": [32.8804, 13.1843],
        "Tanzanie": [-6.8244, 39.2636],
        "Soudan": [15.5978, 32.5328],
        "Mali": [12.6431, -8.0001],
        "Angola": [-11.2027, 17.8739],
        "niger": [13.5133, 2.1072],
        "tchad": [15.4542, 18.7322],
        "nigeria": [10.0000, 8.0000],
        "namibia": [-22.9576, 18.4904],
        "Somalie": [10, 49],
        "Mozambique": [-18,35],
    }

    for country in countries:
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={country}&appid=045255d77ed2260af068720f5d18670a"

        try:
            json_data = requests.get(api_url).json()

            if 'main' in json_data:
                temp_city = json_data['main']['temp'] - 273.15
            else:
                temp_city = None

            lar, lon = capital_coordinates[country]
            condition = json_data['weather'][0]['main']
            pressure = json_data['main']['pressure']

            weather_data = {
                'country': country,
                'temp_city': temp_city,
                'lon': lon,
                'lar': lar,
                'condition':condition,
                'pressure':pressure,
                'weather_icon': get_weather_icon(condition),  # Add this line
            }

            weather_data_list.append(weather_data)

        except requests.RequestException as e:
            # Gérer les erreurs liées à la requête
            print(f"Erreur pour le pays {country}: {str(e)}")

    return render(request, 'map.html', {'weather_data_list': weather_data_list})

def show_news(request):
    # Make an API request to get news data
    api_key = 'cb74bdadba6b426ea91852fb0dc8f9c4'
    api_url = f'https://newsapi.org/v2/everything?q=weather&apiKey={api_key}'
    response = requests.get(api_url)
    json_data = response.json()

    if 'articles' not in json_data:
        return JsonResponse({'error': 'Failed to fetch news data'})

    # Extract the news articles
    articles = json_data['articles']

    # Render the news template with the news articles
    return render(request, 'news.html', {'articles': articles})

def nasa_satellite_info(request):
    
     #sat_url = " https://api.maptiler.com/maps/satellite/?key=MbtNjXMvtXL9B2RxvLZ1"
     sat_url="https://api.maptiler.com/maps/hybrid/?key=lpALIx3rfUr8PBGmVBVu"
     
    
    # Passer l'URL de la carte au template
     context = {
        'sat_url': sat_url,
    }
     return render(request, 'satellite_info.html', context)
   

    
        
