import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import pickle

# Part - 2

# Replace with your Tomorrow.io API Key
TOMORROW_API_KEY = ""
TOMORROW_URL = "https://api.tomorrow.io/v4/timelines"

# Location coordinates for Village: The Soul of India, Hicksville, NY
latitude = 40.768435
longitude = -73.525125

# current weather data and hourly forecast
def get_tomorrow_weather(lat, lon):
    params = {
        "location": f"{lat},{lon}",
        "fields": [
            "temperature",
            "precipitationIntensity",
            "precipitationProbability",
            "precipitationType",
            "weatherCode"
        ],
        "timesteps": "1h",  # Hourly forecast
        "units": "imperial", # for fahrenheit
        "apikey": TOMORROW_API_KEY,
    }
    response = requests.get(TOMORROW_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Tomorrow.io API Error: {response.status_code}, {response.text}")
        return None

# calling the api by giving lat and long of the place
weather_data = get_tomorrow_weather(latitude, longitude)

if weather_data and "data" in weather_data:
    intervals = weather_data["data"]["timelines"][0]["intervals"]
    
    if intervals:
        current_forecast = intervals[0]  # Current hour's data
        
        time = current_forecast["startTime"]
        time_obj = datetime.fromisoformat(time[:-1]) 
        # Convert UTC time to Hicksville local time
        time_local = time_obj.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York"))
        time_hr = time_local.strftime("%H") # Format the time in 24-hour format
        # current time in fahrenheit
        temp = current_forecast["values"]["temperature"] 
        # precipitation probability of upcoming 1 hour
        precip_prob = current_forecast["values"]["precipitationProbability"] 
        # precipitation amount of  current time
        precip_intensity = current_forecast["values"]["precipitationIntensity"] 

        print(f"Weather Forecast at {time_hr}:")
        print(f"  Temperature: {temp}°F")
        print(f"  Precipitation Probability: {precip_prob:.2f} %")
        print(f"  Precipitation Intensity: {precip_intensity} mm/h")
    else:
        print("No hourly data available.")
else:
    print("Failed to fetch Tomorrow.io data.")

# setting the precipitation value
# if precipitation is happening is happening that time
if(precip_intensity > 0): 
    # then precipitation value is 100
    precipitation = 100 
else:  # else precipitation value is the probability of precipitation in upcoming 1 hour
    precipitation = precip_prob

# Part - 3

# ml model file name
filename = 'price_prediction_model.sav'
 
# load the ml model
loaded_model = pickle.load(open(filename, 'rb'))

# weather data collected through api for prediction 
prediction_data = pd.DataFrame({
    'temperature': [temp],
    'precipitation': [precipitation],
    'time_of_day': [time_hr]
})

# Predict the percentage by passing the data in loaded ml model
predicted_percentage = loaded_model.predict(prediction_data)

# Print the Result
print(f'Predicted Percentage: {predicted_percentage[0]:.2f} %')
print(f'Price should be increased {round(predicted_percentage[0])} %')