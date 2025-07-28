# solcast_history_fetcher.py
# Script to fetch historical data from Solcast API (user must provide API key)

import requests
import pandas as pd
from datetime import datetime
import os

# Your location data (latitude, longitude)
latitude = 51.334660
longitude = 16.860879

# Load API key from environment variable
API_KEY = os.getenv("SOLCAST_API_KEY")

if not API_KEY:
    raise ValueError("No SOLCAST_API_KEY found in environment variables. Please set your API key.")

# Endpoint for last 7 days data (168 hours)
url = (
    f"https://api.solcast.com.au/data/live/radiation_and_weather"
    f"?latitude={latitude}&longitude={longitude}"
    f"&hours=168"  # 7 days  24 hours
    f"&output_parameters=ghi,dni,air_temp"
    f"&period=PT15M"
    f"&format=json"
)

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    estimated = data.get("estimated_actuals", [])
    
    if estimated:
        df = pd.DataFrame(estimated)
        df['period_end'] = pd.to_datetime(df['period_end'])
        df = df.sort_values('period_end')
        
        filename = f"solcast_history_{datetime.now().date()}.csv"
        df.to_csv(filename, index=False)
        print(f"? Data saved to file: {filename}")
        print(df.head())
    else:
        print("?? No data found in response.")
else:
    print(f"? Error: {response.status_code}")
    print(response.text)