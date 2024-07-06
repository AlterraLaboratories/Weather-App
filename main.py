import os
import requests
from datetime import datetime
from geopy.geocoders import Nominatim

# Define your API keys and base URLs
WEATHER_API_KEY = "YOUR_API_KEY"
N2YO_API_KEY = "YOUR_API_KEY"
BASE_URL = "http://api.weatherapi.com/v1/current.json"
ASTRONOMY_BASE_URL = "http://api.weatherapi.com/v1/astronomy.json"
N2YO_BASE_URL = "https://api.n2yo.com/rest/v1/satellite"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_coordinates(location_input):
    try:
        geolocator = Nominatim(user_agent="alterra_satellite_tracker", timeout=10)  # Increase timeout if needed
        location = geolocator.geocode(location_input)
        if location:
            return location.latitude, location.longitude
        else:
            # Assume the input is already in the format "latitude, longitude"
            coords = location_input.split(',')
            if len(coords) == 2:
                return float(coords[0].strip()), float(coords[1].strip())
            else:
                return None, None
    except requests.exceptions.Timeout:
        print("Error: Connection to geocoding service timed out. Please try again later.")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def get_weather(city_name, advanced=False, astronomy=False):
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")

        if astronomy:
            astronomy_url = f"{ASTRONOMY_BASE_URL}?key={WEATHER_API_KEY}&q={city_name}&dt={current_date}"
            response = requests.get(astronomy_url)

            if response.status_code == 200:
                astronomy_data = response.json()

                # Check if 'astronomy' key exists in the response
                if 'astronomy' in astronomy_data:
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
                print(f"Error: Unable to fetch astronomy data. Status code: {response.status_code}")
        else:
            weather_url = f"{BASE_URL}?key={WEATHER_API_KEY}&q={city_name}&aqi=no"
            response = requests.get(weather_url)

            if response.status_code == 200:
                weather_data = response.json()

                location = weather_data['location']['name']
                temperature = weather_data['current']['temp_c']
                condition = weather_data['current']['condition']['text']
                last_updated = weather_data['current']['last_updated']

                print(f"Weather in {location} (Date: {current_date}):")
                print(f"Temperature: {temperature}°C")
                print(f"Condition: {condition}")
                print(f"Last Updated: {last_updated}")

                if advanced:
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
                print(f"Error: Unable to fetch weather data. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

def satellite_menu():
    while True:
        print("Satellite Options:")
        print("1. Get TLE")
        print("2. Get Position")
        print("3. Get Radio Passes")
        print("4. Get Visual Passes")
        print("5. Back to Main Menu")
        
        selection = input("Selection: ")
        
        if selection == "5":
            clear_screen()
            break
        else:
            norad_id = input("Enter the NORAD ID: ")
            clear_screen()

            if selection == "1":
                tle_data = get_tle(norad_id)
                formatted_data = format_tle_data(tle_data)
                print(formatted_data)
            elif selection == "2":
                location_input = input("Enter your location (city name or lat, lon): ")
                observer_lat, observer_lon = get_coordinates(location_input)
                if observer_lat is None or observer_lon is None:
                    print("Error: Unable to fetch coordinates for the location.")
                else:
                    position_data = get_position(norad_id, observer_lat, observer_lon)
                    formatted_data = format_position_data(position_data)
                    print(formatted_data)
            elif selection == "3":
                location_input = input("Enter your location (city name or lat, lon): ")
                observer_lat, observer_lon = get_coordinates(location_input)
                if observer_lat is None or observer_lon is None:
                    print("Error: Unable to fetch coordinates for the location.")
                else:
                    radio_passes_data = get_radio_passes(norad_id, observer_lat, observer_lon)
                    if radio_passes_data:
                        formatted_data = format_passes_data(radio_passes_data)
                        for data in formatted_data:
                            print(data)
                    else:
                        print("Error: Unable to fetch radio passes data.")
            elif selection == "4":
                location_input = input("Enter your location (city name or lat, lon): ")
                observer_lat, observer_lon = get_coordinates(location_input)
                if observer_lat is None or observer_lon is None:
                    print("Error: Unable to fetch coordinates for the location.")
                else:
                    visual_passes_data = get_visual_passes(norad_id, observer_lat, observer_lon)
                    if visual_passes_data:
                        formatted_data = format_passes_data(visual_passes_data)
                        for data in formatted_data:
                            print(data)
                    else:
                        print("Error: Unable to fetch visual passes data.")
            
            input("\nPress Enter to return to the selection menu...")
            clear_screen()

def get_norad_id(satellite_name):
    try:
        url = f"{N2YO_BASE_URL}/satellite/positions/{satellite_name}/0/0/0/&apiKey={N2YO_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            norad_id = data.get('info', {}).get('satid')
            if norad_id:
                return norad_id
            else:
                print(f"Error: NORAD ID not found for {satellite_name}")
                return None
        else:
            print(f"Error: Unable to fetch NORAD ID for {satellite_name}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return None


def get_tle(norad_id):
    url = f"{N2YO_BASE_URL}/tle/{norad_id}&apiKey={N2YO_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        tle_data = response.json()
        return tle_data
    else:
        return None

def format_tle_data(tle_data):
    if tle_data:
        info = tle_data.get('info', {})
        tle = tle_data.get('tle', 'N/A')
        sat_name = info.get('satname', 'N/A')
        sat_id = info.get('satid', 'N/A')
        transaction_count = info.get('transactionscount', 'N/A')
        
        return f"Satellite Name: {sat_name}\nSatellite ID: {sat_id}\nTransaction Count: {transaction_count}\nTLE:\n{tle}"
    else:
        return "No TLE data available."

def get_position(norad_id, observer_lat, observer_lon):
    url = f"{N2YO_BASE_URL}/positions/{norad_id}/{observer_lat}/{observer_lon}/0/1/&apiKey={N2YO_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        position_data = response.json()
        return position_data
    else:
        return None

def get_radio_passes(norad_id, observer_lat, observer_lon):
    url = f"{N2YO_BASE_URL}/radiopasses/{norad_id}/{observer_lat}/{observer_lon}/0/10/15/&apiKey={N2YO_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        passes_data = response.json()
        return passes_data
    else:
        return None

def get_visual_passes(norad_id, observer_lat, observer_lon):
    url = f"{N2YO_BASE_URL}/visualpasses/{norad_id}/{observer_lat}/{observer_lon}/0/10/15/&apiKey={N2YO_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        passes_data = response.json()
        return passes_data
    else:
        return None

def format_passes_data(passes_data):
    formatted_passes = []
    for pass_data in passes_data.get('passes', []):
        start_utc = pass_data.get('startUTC', 'N/A')
        max_el = pass_data.get('maxEl', 'N/A')
        end_utc = pass_data.get('endUTC', 'N/A')

        # Check if startAz is a dictionary before accessing its keys
        if isinstance(pass_data['startAz'], dict):
            start_az = pass_data['startAz'].get('azimuth', 'N/A')
            start_az_compass = pass_data['startAz'].get('compass', 'N/A')
        else:
            start_az = 'N/A'
            start_az_compass = 'N/A'

        if isinstance(pass_data['maxAz'], dict):
            max_az = pass_data['maxAz'].get('azimuth', 'N/A')
            max_az_compass = pass_data['maxAz'].get('compass', 'N/A')
        else:
            max_az = 'N/A'
            max_az_compass = 'N/A'

        if isinstance(pass_data['endAz'], dict):
            end_az = pass_data['endAz'].get('azimuth', 'N/A')
            end_az_compass = pass_data['endAz'].get('compass', 'N/A')
        else:
            end_az = 'N/A'
            end_az_compass = 'N/A'

        start_time = datetime.utcfromtimestamp(start_utc).strftime('%Y-%m-%d %H:%M:%S') if start_utc != 'N/A' else 'N/A'
        end_time = datetime.utcfromtimestamp(end_utc).strftime('%Y-%m-%d %H:%M:%S') if end_utc != 'N/A' else 'N/A'

        formatted_passes.append(
            f"Start Time (UTC): {start_time}, Max Elevation: {max_el}°, End Time (UTC): {end_time}, "
            f"Start Azimuth: {start_az}° ({start_az_compass}), Max Azimuth: {max_az}° ({max_az_compass}), "
            f"End Azimuth: {end_az}° ({end_az_compass})"
        )

    return formatted_passes

def format_position_data(position_data):
    if position_data:
        info = position_data.get('info', {})
        positions = position_data.get('positions', [])
        sat_name = info.get('satname', 'N/A')
        sat_id = info.get('satid', 'N/A')
        transaction_count = info.get('transactionscount', 'N/A')
        
        position_strings = []
        for pos in positions:
            sat_lat = pos.get('satlatitude', 'N/A')
            sat_lon = pos.get('satlongitude', 'N/A')
            sat_alt = pos.get('sataltitude', 'N/A')
            azimuth = pos.get('azimuth', 'N/A')
            elevation = pos.get('elevation', 'N/A')
            ra = pos.get('ra', 'N/A')
            dec = pos.get('dec', 'N/A')
            timestamp = pos.get('timestamp', 'N/A')
            eclipsed = pos.get('eclipsed', 'N/A')

            readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            position_strings.append(
                f"Latitude: {sat_lat}°, Longitude: {sat_lon}°, Altitude: {sat_alt} km, "
                f"Azimuth: {azimuth}°, Elevation: {elevation}°, RA: {ra}, Dec: {dec}, "
                f"Timestamp: {readable_time}, Eclipsed: {eclipsed}"
            )

        return f"Satellite Name: {sat_name}\nSatellite ID: {sat_id}\nTransaction Count: {transaction_count}\nPositions:\n" + "\n".join(position_strings)
    else:
        return "No position data available."

while True:
    clear_screen()
    print("Welcome to the Alterra Laboratories Weather and Satellite Tracker App!")
    print("")
    print("Select an option:")
    print("1. Show Weather")
    print("2. Show Advanced Weather")
    print("3. Show Astronomy")
    print("4. Satellite Options")
    print("5. Set Custom API Key")
    print("6. Exit")

    selection = input("Selection: ")
    clear_screen()
    
    if selection == "1":
        city_name = input("Enter a city name: ")
        clear_screen()
        get_weather(city_name)
    elif selection == "2":
        city_name = input("Enter a city name: ")
        clear_screen()
        get_weather(city_name, advanced=True)
    elif selection == "3":
        city_name = input("Enter a city name: ")
        clear_screen()
        get_weather(city_name, astronomy=True)
    elif selection == "4":
        satellite_menu()
    elif selection == "5":
        WEATHER_API_KEY = input("Enter your Weather API Key: ")
        N2YO_API_KEY = input("Enter your N2YO API Key: ")
        clear_screen()
    elif selection == "6":
        exit()
    else:
        print("Invalid selection")
