import pandas as pd
import os

#  Check if files exist
#  Sprawdź, czy pliki istnieją
inverter_file = "outputs/inverter_with_scaled_power.csv"
solcast_history_file = "data/solcast_history.csv"
solcast_forecast_file = "data/solcast_forecast.csv"

def check_dates(file_path, time_column, description):
    """
    Check and print date range and record count for a CSV file.
    Sprawdź i wyświetl zakres dat oraz liczbę rekordów w pliku CSV.
    """
    if not os.path.isfile(file_path):
        print(f"❌ File {file_path} does not exist!")
        return

    try:
        df = pd.read_csv(file_path)
        df[time_column] = pd.to_datetime(df[time_column])
        print(f"\n {description} ({file_path}):")
        print(f" Date range: {df[time_column].min()} → {df[time_column].max()}")
        print(f" Number of records: {len(df)}")
    except Exception as e:
        print(f" Error reading {file_path}: {e}")

print("\n===========================")
print(" CHECKING DATE RANGES")
print("===========================\n")

check_dates(inverter_file, "timestamp", "Inverter Data")
check_dates(solcast_history_file, "period_end", "Solcast HISTORY")
check_dates(solcast_forecast_file, "period_end", "Solcast FORECAST")

print("\n===========================")
