from predictor import Predictor
from visualizer import Visualizer
import pandas as pd
from datetime import datetime
from pobierz_forecast import download_forecast  # dodany import pobierania forecastu
import os


def main():
    print("🚀 Start predykcji...")

    # 📥 Pobierz najnowszy forecast i zapisz do data/
    download_forecast()

    # 📂 Przygotuj folder do zapisu
    os.makedirs("predykcja", exist_ok=True)

    # 🔧 Wczytaj model i skaler
    predictor = Predictor("models/model_trained.keras", "models/scaler_produkcji.pkl")

    # 📄 Wczytaj forecast
    forecast = pd.read_csv("data/solcast_forecast.csv")
    prediction = predictor.predict(forecast)

    # 🕒 Znacznik czasu do nazw plików
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # 💾 Zapis CSV z predykcją
    csv_pred = f"predykcja/prognoza_{timestamp}.csv"
    prediction.to_csv(csv_pred, index=False)
    print(f"✅ Zapisano prognozę do {csv_pred}")

    # 💾 Agregacja dzienna
    df_sum = predictor.agreguj_dziennie(prediction)
    csv_sum = f"predykcja/suma_dzienna_{timestamp}.csv"
    df_sum.to_csv(csv_sum, index=False)
    print(f"✅ Zapisano sumę dzienną do {csv_sum}")

    # 📊 Wykres
    viz = Visualizer()
    pdf_plot = f"predykcja/wykres_{timestamp}.pdf"
    viz.save_best_day(prediction, pdf_plot)
    print(f"✅ Wykres zapisany jako {pdf_plot}")

    print("🎉 Predykcja zakończona pomyślnie.")


if __name__ == "__main__":
    main()
