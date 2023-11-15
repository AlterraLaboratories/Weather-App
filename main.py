import os
import requests
from datetime import date

# Define your API key and the base URL
API_KEY = ""
BASE_URL = "http://api.weatherapi.com/v1/current.json"
ASTRONOMY_BASE_URL = "http://api.weatherapi.com/v1/astronomy.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_weather(city_name, advanced=False, astronomy=False):
    try:
        # Get the current date
        current_date = date.today().strftime("%Y-%m-%d")
        
        # Construct the API request URL with the API key, city name, and current date for astronomy data
        astronomy_url = f"{ASTRONOMY_BASE_URL}?key={API_KEY}&q={city_name}&dt={current_date}"
        
        # Send an HTTP GET request to the astronomy API if astronomy option is selected
        if astronomy:
            response = requests.get(astronomy_url)
            
            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                # Parse the JSON response for astronomy data
                astronomy_data = response.json()
                
                # Extract and display astronomy information
                location = astronomy_data['location']['name']
                sunrise = astronomy_data['astronomy']['astro']['sunrise']
                sunset = astronomy_data['astronomy']['astro']['sunset']
                moonrise = astronomy_data['astronomy']['astro']['moonrise']
                moonset = astronomy_data['astronomy']['astro']['moonset']
                moon_phase = astronomy_data['astronomy']['astro']['moon_phase']
                moon_illumination = astronomy_data['astronomy']['astro']['moon_illumination']

                print(f"Astronomy in {location} (Date: {current_date}):")
                print(f"Sunrise: {sunrise}")
                print(f"Sunset: {sunset}")
                print(f"Moonrise: {moonrise}")
                print(f"Moonset: {moonset}")
                print(f"Moon Phase: {moon_phase}")
                print(f"Moon Illumination: {moon_illumination}%")

                input("\nPress Enter to return to the selection menu...")
                clear_screen()
            else:
                print("Error: Unable to fetch astronomy data.")
        else:
            # Construct the API request URL with the API key and city name for weather data
            weather_url = f"{BASE_URL}?key={API_KEY}&q={city_name}&aqi=no"
            
            # Send an HTTP GET request to the weather API
            response = requests.get(weather_url)
            
            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                # Parse the JSON response for weather data
                weather_data = response.json()
                
                # Extract and display relevant weather information
                location = weather_data['location']['name']
                temperature = weather_data['current']['temp_c']
                condition = weather_data['current']['condition']['text']
                last_updated = weather_data['current']['last_updated']
                
                print(f"Weather in {location} (Date: {current_date}):")
                print(f"Temperature: {temperature}°C")
                print(f"Condition: {condition}")
                print(f"Last Updated: {last_updated}")
                
                if advanced:
                    # Extract advanced weather information
                    wind_speed = weather_data['current']['wind_kph']
                    wind_direction = weather_data['current']['wind_dir']
                    wind_degree = weather_data['current']['wind_degree']
                    humidity = weather_data['current']['humidity']
                    cloud = weather_data['current']['cloud']
                    feels_like_c = weather_data['current']['feelslike_c']
                    uv = weather_data['current']['uv']
                    
                    print(f"Wind Speed: {wind_speed} km/h")
                    print(f"Wind Direction: {wind_direction}")
                    print(f"Wind Degree: {wind_degree} °")
                    print(f"Humidity: {humidity} %")
                    print(f"Clouds: {cloud} %")
                    print(f"Feels Like Temperature: {feels_like_c}°C")
                    print(f"UV Index: {uv}")
                    
                input("\nPress Enter to return to the selection menu...")
                clear_screen()
            else:
                print("Error: Unable to fetch weather data.")
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    print("Welcome to the Alterra Laboratories Weather App!")
    print("")
    print("Select an option:")
    print("1. Show Weather")
    print("2. Show Advanced Weather")
    print("3. Show Astronomy")
    print("4. Set Custom API Key")
    print("5. Exit")

    selection = input("Selection: ")
    if selection == "1":
        clear_screen()
        city_name = input("Enter a city name: ")
        clear_screen()
        get_weather(city_name)
    elif selection == "2":
        clear_screen()
        city_name = input("Enter a city name: ")
        clear_screen()
        get_weather(city_name, advanced=True)
    elif selection == "3":
        clear_screen()
        city_name = input("Enter a city name: ")
        clear_screen()
        get_weather(city_name, astronomy=True)
    elif selection == "4":
        clear_screen()
        API_KEY = input("Enter your API Key: ")
        clear_screen()
    elif selection == "5":
        exit()
    else:
        print("Invalid selection")
