import os
import pandas as pd
from data_cleaner import MQTTDataCleaner
from data_merger import DataMerger
from model_trainer import ModelTrainer
from predictor import Predictor
from visualizer import Visualizer
from datetime import datetime
from dotenv import load_dotenv
from download_forecast import download_solcast_forecast, download_solcast_forecast_demo  # <-- import

load_dotenv()  # załaduj zmienne środowiskowe, w tym USE_DEMO / load environment variables, including USE_DEMO

# Set base directory of the project (parent to src folder)
# Ustal katalog główny projektu (nadrzędny względem folderu src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths for input and output files
# Ścieżki do plików wejściowych i wyjściowych
mqtt_path = os.path.join(BASE_DIR, "data", "mqtt_data.csv")
solcast_path = os.path.join(BASE_DIR, "data", "solcast_history.csv")
inverter_output_path = os.path.join(BASE_DIR, "outputs", "inverter_data_plus_power.csv")
model_path = os.path.join(BASE_DIR, "models", "model_trained.keras")
scaler_path = os.path.join(BASE_DIR, "models", "production_scaler.pkl")

print("\n===========================")
print(" SPRAWDZAMY ZAKRESY DAT")  # Checking date ranges
print("===========================\n")

# Load MQTT data without header, assign column names, convert timestamps to datetime
# Wczytaj dane MQTT bez nagłówka, nadaj nazwy kolumn, konwertuj timestamp na datetime
mqtt = pd.read_csv(mqtt_path, header=None, names=['timestamp', 'topic', 'value'])
mqtt['timestamp'] = pd.to_datetime(mqtt['timestamp'])
print(f"MQTT: from {mqtt['timestamp'].min()} to {mqtt['timestamp'].max()}")

# Load Solcast historical data and convert period_end to datetime
# Wczytaj dane historyczne Solcast i konwertuj kolumnę period_end na datetime
solcast = pd.read_csv(solcast_path)
solcast['period_end'] = pd.to_datetime(solcast['period_end'])
print(f"Solcast: from {solcast['period_end'].min()} to {solcast['period_end'].max()}\n")

print("===========================\n")


def main():
    print(" Starting process...")  # Start procesu...

    # 1. Cleaning MQTT data: load, clean, pivot, rename, and resample
    # 1. Czyszczenie danych MQTT: wczytanie, oczyszczenie, przekształcenie i próbkowanie
    cleaner = MQTTDataCleaner(mqtt_path)
    cleaner.load_and_clean()       # Load and clean raw MQTT data / Wczytaj i oczyść surowe dane MQTT
    cleaner.pivot_and_rename()     # Pivot table and rename columns / Przekształć dane i zmień nazwy kolumn
    cleaner.resample_data()        # Resample data to regular intervals / Próbkuj dane do regularnych interwałów

    # 2. Merge inverter output data with Solcast forecast data
    # 2. Połączenie danych wyjściowych z falownika z prognozą Solcast
    merger = DataMerger(inverter_output_path, solcast_path)
    training_data = merger.match_and_prepare_data()  # Match and prepare training data / Dopasuj i przygotuj dane treningowe

    # 3. Train the machine learning model using the prepared training data
    # 3. Trenowanie modelu ML na przygotowanych danych treningowych
    trainer = ModelTrainer(training_data)
    trainer.train()  # Run the training / Uruchom trenowanie modelu

    # --- Download Solcast forecast, either demo or online based on USE_DEMO environment variable ---
    # --- Pobieranie prognozy Solcast - demo lub online w zależności od zmiennej środowiskowej USE_DEMO ---
    use_demo = os.getenv("USE_DEMO", "0")
    if use_demo == "1":
        print(" DEMO mode - loading local demo data...")  # Tryb demo - ładowanie lokalnych danych demo
        forecast = download_solcast_forecast_demo()
    else:
        print(" ONLINE mode - downloading latest forecast...")  # Tryb online - pobieranie najnowszej prognozy
        download_solcast_forecast()
        forecast_path = os.path.join(BASE_DIR, "data", "solcast_forecast.csv")
        forecast = pd.read_csv(forecast_path)

    # 4. Use the trained model to predict energy production based on forecast data
    # 4. Użycie wytrenowanego modelu do predykcji produkcji energii na podstawie prognozy
    predictor = Predictor(model_path, scaler_path)
    prediction = predictor.predict(forecast)  # Perform prediction / Wykonaj predykcję

    # Prepare directory to save prediction results, create if missing
    # Przygotuj katalog do zapisu wyników predykcji, utwórz jeśli nie istnieje
    predictions_dir = os.path.join(BASE_DIR, "predictions")
    os.makedirs(predictions_dir, exist_ok=True)

    suffix = "_demo" if use_demo == "1" else ""  # Suffix for demo or live run
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")  # Timestamp for filenames

    # Save prediction results as CSV file
    # Zapisz wyniki predykcji do pliku CSV
    csv_pred = os.path.join(predictions_dir, f"forecast{suffix}_{timestamp}.csv")
    prediction.to_csv(csv_pred, index=False)
    print(f" Saved forecast to {csv_pred}")

    # Aggregate prediction to daily sums and save
    # Agreguj wyniki do sum dziennych i zapisz
    df_sum = predictor.aggregate_daily(prediction)
    csv_sum = os.path.join(predictions_dir, f"daily_sum{suffix}_{timestamp}.csv")
    df_sum.to_csv(csv_sum, index=False)
    print(f" Saved daily sum to {csv_sum}")

    # Generate plot for the best prediction day and save as PDF
    # Wygeneruj wykres dla najlepszego dnia prognozy i zapisz jako PDF
    viz = Visualizer()
    pdf_plot = os.path.join(predictions_dir, f"plot{suffix}_{timestamp}.pdf")
    viz.save_best_day(prediction, pdf_plot)
    print(f" Plot saved as {pdf_plot}")

    print(" Process completed successfully.")  # Proces zakończony pomyślnie.


if __name__ == "__main__":
    main()
