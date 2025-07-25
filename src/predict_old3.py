from predictor import Predictor
from visualizer import Visualizer
from download_forecast import download_solcast_forecast
import pandas as pd


def main():
    print("🚀 Start predykcji...")

    # 🌤 Pobieranie najnowszego forecastu
    print("📡 Pobieram forecast z Solcast...")
    forecast_df = download_solcast_forecast()
    if forecast_df is None:
        print("❌ Nie można wykonać predykcji — brak forecastu.")
        return

    # 🔧 Ładujemy model i skaler
    predictor = Predictor("models/model_trained.keras", "models/scaler_produkcji.pkl")

    # 🤖 Predykcja
    prediction = predictor.predict(forecast_df)

    # 💾 Zapis wyników
    predictor.save_prediction(prediction)
    predictor.agreguj_dziennie(prediction)

    # 📊 Wykres dla dnia z pełnymi danymi
    viz = Visualizer()
    viz.plot_best_day(prediction)  # 🔥 automatycznie wybiera dzień z pełnymi danymi

    print("✅ Predykcja zakończona pomyślnie.")


if __name__ == "__main__":
    main()
