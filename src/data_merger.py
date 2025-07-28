import os
import pandas as pd
import numpy as np

class DataMerger:
    def __init__(self, inverter_file, solcast_file):
        self.inverter_file = inverter_file
        self.solcast_file = solcast_file

        # Base project directory, one level above this file's folder
        # Bazowy katalog projektu, o poziom wyżej niż folder tego pliku
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.outputs_dir = os.path.join(base_dir, "outputs")

        # Ensure output directory exists
        # Upewnij się, że katalog wyjściowy istnieje
        os.makedirs(self.outputs_dir, exist_ok=True)

        # Full paths to output files
        # Pełne ścieżki do plików wyjściowych
        self.final_matched_file = os.path.join(self.outputs_dir, "final_matched.csv")
        self.training_data_file = os.path.join(self.outputs_dir, "training_data.csv")

    def match_and_prepare_data(self):
        # Load data from CSV files
        # Wczytaj dane z plików CSV
        inverter_data = pd.read_csv(self.inverter_file)
        solcast_data = pd.read_csv(self.solcast_file)

        # Convert timestamps to datetime and localize/convert timezones
        # Konwersja czasów i zmiana stref czasowych
        inverter_data['timestamp'] = pd.to_datetime(inverter_data['timestamp'])
        inverter_data['timestamp'] = inverter_data['timestamp'].dt.tz_localize('Europe/Warsaw').dt.tz_convert('UTC')
        solcast_data['period_end'] = pd.to_datetime(solcast_data['period_end'], utc=True)

        # Data ranges
        # Zakresy dat
        min_solcast = solcast_data['period_end'].min()
        max_solcast = solcast_data['period_end'].max()

        print("\n=== CHECKING DATE RANGES ===")
        print(f"Inverter: {inverter_data['timestamp'].min()} → {inverter_data['timestamp'].max()}")
        print(f"Solcast : {min_solcast} → {max_solcast}")

        # Limit inverter data to Solcast date range
        # Ogranicz dane falownika do zakresu dat Solcast
        inverter_data = inverter_data[
            (inverter_data['timestamp'] >= min_solcast) &
            (inverter_data['timestamp'] <= max_solcast)
        ]

        print(f" Inverter data after limiting: {len(inverter_data)} records")

        # Sort data by timestamp
        # Sortuj dane po czasie
        inverter_data = inverter_data.sort_values('timestamp')
        solcast_data = solcast_data.sort_values('period_end')

        # Merge using nearest match within 3 minutes tolerance
        # Scal dane na podstawie najbliższego czasu z tolerancją 3 minut
        merged_data = pd.merge_asof(
            inverter_data,
            solcast_data[['period_end', 'ghi', 'air_temp']],
            left_on='timestamp',
            right_on='period_end',
            direction='nearest',
            tolerance=pd.Timedelta('3min')
        )

        missing_ghi = merged_data['ghi'].isna().sum()
        print(f" Number of unmatched rows (ghi NaN): {missing_ghi}")

        # Set timestamp as index
        # Ustaw timestamp jako indeks
        merged_data = merged_data.reset_index(drop=True).set_index('timestamp')

        # Calculate energy sums in 15-minute intervals
        # Oblicz sumy energii w 15-minutowych przedziałach
        energy_15min = (
            merged_data['energy_kWh']
            .resample('15min')
            .sum()
            .round(4)
            .to_frame(name='energy_15min_kWh')
        )

        # Clip energy values to non-negative and zero out if above 2.0 kWh (filter outliers)
        # Ogranicz wartości energii do nieujemnych i wyzeruj, jeśli powyżej 2 kWh (usuń outliery)
        energy_15min['energy_15min_kWh'] = energy_15min['energy_15min_kWh'].clip(lower=0.0)
        energy_15min.loc[energy_15min['energy_15min_kWh'] > 2.0, 'energy_15min_kWh'] = 0.0

        # Join energy data back to merged dataframe
        # Dołącz dane o energii do połączonych danych
        merged_data = merged_data.join([energy_15min]).reset_index()

        # Create time-based features
        # Utwórz cechy czasowe
        merged_data['hour_decimal'] = merged_data['timestamp'].dt.hour + merged_data['timestamp'].dt.minute / 60
        merged_data['day_of_year'] = merged_data['timestamp'].dt.dayofyear
        merged_data['sin_hour'] = np.sin(2 * np.pi * merged_data['hour_decimal'] / 24)
        merged_data['cos_hour'] = np.cos(2 * np.pi * merged_data['hour_decimal'] / 24)

        # Save full matched data
        # Zapisz pełne dane po dopasowaniu
        merged_data.to_csv(self.final_matched_file, index=False)

        # Create training dataset - only rows with ghi and energy available
        # Stwórz zbiór treningowy - tylko tam, gdzie dostępne są GHI i energia
        training_data = merged_data[
            (merged_data['ghi'].notna()) &
            (merged_data['energy_15min_kWh'].notna())
        ][[
            'timestamp', 'ghi', 'air_temp', 'sin_hour', 'cos_hour', 'day_of_year', 'energy_15min_kWh'
        ]]

        training_data.to_csv(self.training_data_file, index=False)

        print(f" Training data saved: {len(training_data)} records")

        return training_data
