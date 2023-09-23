import os
import requests

# Define your API key and the base URL
API_KEY = "8938813919c045c5ad7150828232309"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_weather(city_name):
    try:
        # Construct the API request URL with the API key and city name
        url = f"{BASE_URL}?key={API_KEY}&q={city_name}&aqi=no"

        # Send an HTTP GET request to the API
        response = requests.get(url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and display relevant weather information
            location = data['location']['name']
            temperature = data['current']['temp_c']
            condition = data['current']['condition']['text']

            clear_screen()  # Clear the screen before displaying weather
            print(f"Weather in {location}:")
            print(f"Temperature: {temperature}°C")
            print(f"Condition: {condition}")
            
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
    print("2. Exit")

    selection = input("Selection: ")
    if selection == "1":
        clear_screen() # Clear the screen before displaying options
        city_name = input("Enter a city name: ")
        clear_screen()
        get_weather(city_name) # Call the get_weather function
    elif selection == "2":
        exit()
    else:
        print("Invalid selection")
