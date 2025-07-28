import pandas as pd
import sys

def check_data_ranges(inverter_file, solcast_file):
    """
    Check if date ranges in inverter and Solcast data overlap.
    Sprawdź, czy zakresy dat w danych z falownika i Solcast się pokrywają.
    """
    try:
        df_inverter = pd.read_csv(inverter_file)
        df_solcast = pd.read_csv(solcast_file)

        # Convert timestamps to datetime
        # Konwersja kolumn czasowych na datetime
        df_inverter['timestamp'] = pd.to_datetime(df_inverter['timestamp'])
        df_solcast['period_end'] = pd.to_datetime(df_solcast['period_end'])

        min_inv, max_inv = df_inverter['timestamp'].min(), df_inverter['timestamp'].max()
        min_sol, max_sol = df_solcast['period_end'].min(), df_solcast['period_end'].max()

        print("\n===========================")
        print(" CHECKING DATA RANGES")
        print("===========================\n")
        print(f"Inverter: {min_inv} → {max_inv}")
        print(f"Solcast : {min_sol} → {max_sol}")

        # Check if ranges overlap
        # Sprawdź, czy zakresy się pokrywają
        if max_inv < min_sol or min_inv > max_sol:
            print("\n No overlapping data ranges found!")
            sys.exit(1)
        else:
            print("\n Data ranges are OK. You can proceed.\n")

    except Exception as e:
        print(f"\n Error while checking data ranges: {e}")
        sys.exit(1)

def check_missing_values(file_path):
    """
    Check for missing values in the CSV file.
    Sprawdź braki danych w pliku CSV.
    """
    df = pd.read_csv(file_path)
    nan_counts = df.isna().sum()

    print("\n Checking for missing data:")
    print(nan_counts[nan_counts > 0])

    if nan_counts.sum() > 0:
        print(" Data contains missing values!\n")
    else:
        print(" No missing values in data.\n")
