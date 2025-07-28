from predictor import Predictor
from visualizer import Visualizer
import pandas as pd
from datetime import datetime
import sys
import os

from dotenv import load_dotenv
load_dotenv()  # załaduj zmienne środowiskowe / load environment variables

# Set paths relative to location of predict.py
# Ustaw ścieżki względem lokalizacji pliku predict.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 'data' and 'models' directories are in parent folder relative to src
# Katalogi 'data' i 'models' znajdują się w katalogu nadrzędnym względem src
data_dir = os.path.join(parent_dir, "data")
models_dir = os.path.join(parent_dir, "models")

sys.path.append(data_dir)  # dodaj katalog z danymi do ścieżki importu / add data directory to import path

# Import forecast download function
# Import funkcji pobierania prognozy
from download_forecast import download_solcast_forecast

def main():
    print(" Start predykcji...")  # Start prediction...

    use_demo = os.getenv("USE_DEMO", "0")  # tryb DEMO lub ONLINE / demo or online mode

    if use_demo == "1":
        print(" Tryb DEMO - wczytuję dane z lokalnego pliku demo...")  # Demo mode - loading local demo file
        forecast_file = os.path.join(data_dir, "solcast_forecast_2025-07-25_demo.csv")
        forecast = pd.read_csv(forecast_file)
    else:
        print(" Tryb ONLINE - pobieram i wczytuję najnowszy forecast...")  # Online mode - download and load latest forecast
        download_solcast_forecast()
        forecast_file = os.path.join(data_dir, "solcast_forecast.csv")
        forecast = pd.read_csv(forecast_file)

    # Prepare folder to save results in parent directory relative to src
    # Przygotuj katalog do zapisu wyników w katalogu nadrzędnym względem src
    predictions_dir = os.path.join(parent_dir, "predictions")
    os.makedirs(predictions_dir, exist_ok=True)

    # Load model and scaler paths
    # Wczytaj ścieżki do modelu i skalera
    model_path = os.path.join(models_dir, "model_trained.keras")
    scaler_path = os.path.join(models_dir, "production_scaler.pkl")
    predictor = Predictor(model_path, scaler_path)  # utwórz obiekt Predictor / create Predictor object

    # Perform prediction
    # Wykonaj predykcję
    prediction = predictor.predict(forecast)

    # Timestamp for output files
    # Znacznik czasu dla plików wynikowych
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Suffix for filenames, depends on demo or live mode
    # Sufiks plików wynikowych zależny od trybu DEMO lub LIVE
    suffix = "_demo" if use_demo == "1" else ""

    # Save prediction to CSV
    # Zapisz predykcję do pliku CSV
    csv_pred = os.path.join(predictions_dir, f"forecast{suffix}_{timestamp}.csv")
    prediction.to_csv(csv_pred, index=False)
    print(f" Saved forecast to {csv_pred}")

    # Aggregate daily sums and save to CSV
    # Agreguj sumy dzienne i zapisz do pliku CSV
    df_sum = predictor.aggregate_daily(prediction)
    csv_sum = os.path.join(predictions_dir, f"daily_sum{suffix}_{timestamp}.csv")
    df_sum.to_csv(csv_sum, index=False)
    print(f" Saved daily sum to {csv_sum}")

    # Generate plot and save as PDF
    # Wygeneruj wykres i zapisz jako PDF
    viz = Visualizer()
    pdf_plot = os.path.join(predictions_dir, f"plot{suffix}_{timestamp}.pdf")
    viz.save_best_day(prediction, pdf_plot)
    print(f" Plot saved as {pdf_plot}")

    print(" Prediction completed successfully.")  # Predykcja zakończona pomyślnie.

if __name__ == "__main__":
    main()
