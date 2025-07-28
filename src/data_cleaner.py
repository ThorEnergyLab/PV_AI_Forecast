import pandas as pd
import os

class MQTTDataCleaner:
    def __init__(self, mqtt_csv_file):
        self.mqtt_csv_file = mqtt_csv_file

        # Base project directory (one level above src)
        # Bazowy katalog projektu (o poziom wyżej niż src)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Paths to outputs folder in base directory
        # Ścieżki do folderu outputs w katalogu głównym
        outputs_dir = os.path.join(base_dir, "outputs")
        
        # Create outputs folder if it does not exist (safety)
        # Utwórz folder outputs, jeśli nie istnieje (zabezpieczenie)
        os.makedirs(outputs_dir, exist_ok=True)

        self.cleaned_file = os.path.join(outputs_dir, "inverter_raw_data.csv")
        self.pivoted_file = os.path.join(outputs_dir, "inverter_pivoted.csv")
        # Zmieniona nazwa pliku finalnego, by była spójna z main.py i DataMerger
        self.final_file = os.path.join(outputs_dir, "inverter_data_plus_power.csv")

    def load_and_clean(self):
        # Load raw MQTT CSV without header, assign column names
        # Wczytaj surowy plik CSV MQTT bez nagłówka, przypisz nazwy kolumn
        df = pd.read_csv(self.mqtt_csv_file, header=None, names=['timestamp', 'topic', 'value'])

        # Filter out unwanted topics
        # Filtruj niechciane tematy (topics)
        exclude_topics = [
            'if0754/fca/m9', 'if0754/fca/m10', 'if0754/fca/m11',
            'if0754/fca/connected', 'if0754/fca/m12', 'if0754/connected'
        ]
        df['topic'] = df['topic'].astype(str).str.strip()
        df_filtered = df[~df['topic'].isin(exclude_topics)]

        # Save cleaned data
        # Zapisz oczyszczone dane
        df_filtered.to_csv(self.cleaned_file, index=False)
        return df_filtered

    def pivot_and_rename(self):
        # Load cleaned data and pivot it: topics as columns
        # Wczytaj oczyszczone dane i przekształć (pivot): tematy jako kolumny
        df = pd.read_csv(self.cleaned_file)
        df_pivot = df.pivot(index='timestamp', columns='topic', values='value')
        df2 = df_pivot.reset_index()

        # Rename columns to meaningful names
        # Zmień nazwy kolumn na opisowe
        df2.columns = ['timestamp', 'Voltage_Ua', 'Voltage_Ub', 'Voltage_Uc',
                       'Current_Idc', 'Voltage_Udc', 'Instant_Power_Pdc', 'Total_Power_P_ALL', 'SF']

        # Save pivoted and renamed data
        # Zapisz przekształcone i przemianowane dane
        df2.to_csv(self.pivoted_file, index=False)
        return df2

    def resample_data(self):
        # Load pivoted data and resample to 5-minute intervals
        # Wczytaj dane po pivot i resampluj co 5 minut
        df = pd.read_csv(self.pivoted_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        # Resample using max value per 5 minutes (can be adjusted)
        # Resampluj dane wybierając maksymalną wartość co 5 minut
        df_resampled = df.resample('5min').max().reset_index()

        # Calculate energy [kWh] as difference of total power and round to 4 decimals
        # Oblicz energię [kWh] jako różnicę mocy całkowitej, zaokrągloną do 4 miejsc
        df_resampled['energy_kWh'] = df_resampled['Total_Power_P_ALL'].diff().round(4)
        df_resampled['energy_kWh'] = df_resampled['energy_kWh'].fillna(0)

        # Calculate scaled DC power depending on SF (scaling factor)
        # Oblicz skalowaną moc DC w zależności od współczynnika SF
        df_resampled["Scaled_P_DC"] = df_resampled.apply(self.scale_power, axis=1)

        # Save final cleaned and resampled data
        # Zapisz ostateczne dane po przeskalowaniu
        df_resampled.to_csv(self.final_file, index=False)
        return df_resampled

    @staticmethod
    def scale_power(row):
        # Scale instant power Pdc depending on SF value
        # Skaluj moc chwilową Pdc w zależności od wartości SF
        if row["SF"] == 65535.0:
            return row["Instant_Power_Pdc"] / 10
        elif row["SF"] == 65534.0:
            return row["Instant_Power_Pdc"] / 100
        elif row["SF"] == 65533.0:
            return row["Instant_Power_Pdc"] / 1000
        else:
            return row["Instant_Power_Pdc"]
