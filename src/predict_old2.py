from predictor import Predictor
from visualizer import Visualizer
import pandas as pd


def main():
    print("🚀 Start predykcji...")

    # 🔧 Ładujemy model i skaler
    predictor = Predictor("models/model_trained.keras", "models/scaler_produkcji.pkl")

    # 📥 Wczytaj forecast
    forecast = pd.read_csv("data/solcast_forecast.csv")
    prediction = predictor.predict(forecast)

    # 💾 Zapis wyników
    predictor.save_prediction(prediction)
    predictor.agreguj_dziennie(prediction)

    # 📊 Wykres dla dnia z pełnymi danymi
    viz = Visualizer()
    viz.plot_best_day(prediction)

    print("✅ Predykcja zakończona pomyślnie.")


if __name__ == "__main__":
    main()
