import requests
import pandas as pd
from datetime import datetime
import os


def download_solcast_forecast():
    """Pobiera forecast z Solcast i zapisuje do folderu data/."""
    API_KEY = "W7QQ2rWO7cBM8GPiWpwpwyFwAUAoPUNX"
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
        print(" Prognoza pobrana poprawnie.")
        data = response.json()
        forecast = data.get("forecasts", [])

        if forecast:
            df = pd.DataFrame(forecast)
            df['period_end'] = pd.to_datetime(df['period_end'])
            df = df.sort_values("period_end")

            os.makedirs("data", exist_ok=True)
            main_file = "data/solcast_forecast.csv"
            backup_file = f"data/solcast_forecast_{datetime.now().date()}.csv"

            df.to_csv(main_file, index=False)
            df.to_csv(backup_file, index=False)

            print(f" Dane zapisane do: {main_file}")
            print(f" Kopia archiwalna: {backup_file}")

            return df

        else:
            print(" Brak danych prognozy w odpowiedzi.")
            return None

    else:
        print(f" Błąd pobierania: {response.status_code}")
        print(response.text)
        return None


if __name__ == "__main__":
    download_solcast_forecast()
