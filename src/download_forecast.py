from dotenv import load_dotenv
load_dotenv()

import requests
import pandas as pd
from datetime import datetime
import os

def download_solcast_forecast():
    """
    Downloads forecast data from Solcast (online) and saves it to the 'data/' folder
    in the main project directory.
    Pobiera dane prognozy z Solcast (online) i zapisuje do folderu 'data/' w katalogu głównym projektu.
    """

    API_KEY = os.getenv("SOLCAST_API_KEY")
    if not API_KEY:
        raise ValueError(" Missing API key. Set the SOLCAST_API_KEY environment variable or create a .env file")

    latitude = 51.334660
    longitude = 16.860879

    url = (
        f"https://api.solcast.com.au/data/forecast/radiation_and_weather?"
        f"latitude={latitude}&longitude={longitude}"
        f"&output_parameters=ghi,air_temp"
        f"&format=json&period=PT15M"
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Forecast data downloaded successfully.")  # Prognoza pobrana poprawnie.
        data = response.json()
        forecast = data.get("forecasts", [])

        if forecast:
            df = pd.DataFrame(forecast)
            df['period_end'] = pd.to_datetime(df['period_end'])
            df = df.sort_values("period_end")

            # Set main project directory (parent of src folder)
            # Ustal katalog główny projektu (nadrzędny względem folderu src)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            data_dir = os.path.join(parent_dir, "data")
            os.makedirs(data_dir, exist_ok=True)

            main_file = os.path.join(data_dir, "solcast_forecast.csv")

            # Backup path with timestamp (date + hour + minute + second)
            # Pełna ścieżka kopii zapasowej z timestampem (data + godzina + minuty + sekundy)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_file = os.path.join(data_dir, f"solcast_forecast_backup_{timestamp}.csv")

            df.to_csv(main_file, index=False)
            df.to_csv(backup_file, index=False)

            print(f"Data saved to: {main_file}")
            print(f"Backup saved to: {backup_file}")

            return df
        else:
            print("No forecast data found in response.")  # Brak danych prognozy w odpowiedzi.
            return None
    else:
        print(f"Download error: {response.status_code}")  # Błąd pobierania
        print(response.text)
        return None

def download_solcast_forecast_demo():
    """
    Demo version - loads data from a local demo file in the main 'data/' directory.
    Wersja demo - wczytuje dane z lokalnego pliku demo w katalogu 'data/' w katalogu głównym.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data")

    demo_file = os.path.join(data_dir, "solcast_forecast_2025-07-25_demo.csv")
    if not os.path.exists(demo_file):
        raise FileNotFoundError(f"Demo file does not exist: {demo_file}")
    print(" [DEMO] Loading data from local demo file...")
    df = pd.read_csv(demo_file)
    print(f"Loaded {len(df)} records from demo file.")
    return df

if __name__ == "__main__":
    USE_DEMO = os.getenv("USE_DEMO", "0") == "1"  # Default 0 = online, 1 = demo

    if USE_DEMO:
        download_solcast_forecast_demo()
    else:
        download_solcast_forecast()
