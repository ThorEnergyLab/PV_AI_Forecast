from data_cleaner import MQTTDataCleaner
from data_merger import DataMerger
from model_trainer import ModelTrainer
from predictor import Predictor
from visualizer import Visualizer
import pandas as pd
import pandas as pd

# Test zakresów dat
print("\n===========================")
print("📅 SPRAWDZAMY ZAKRESY DAT")
print("===========================\n")

# Dane MQTT
mqtt = pd.read_csv("data/mqtt_data.csv", header=None, names=['timestamp', 'topic', 'value'])
mqtt['timestamp'] = pd.to_datetime(mqtt['timestamp'])
print(f"MQTT: od {mqtt['timestamp'].min()} do {mqtt['timestamp'].max()}")

# Dane Solcast
solcast = pd.read_csv("data/solcast_history.csv")
solcast['period_end'] = pd.to_datetime(solcast['period_end'])
print(f"Solcast: od {solcast['period_end'].min()} do {solcast['period_end'].max()}\n")

print("===========================\n")

def main():
    print("🚀 Start procesu...")

    # 1. Czyszczenie danych MQTT
    cleaner = MQTTDataCleaner("data/mqtt_data.csv")
    cleaner.load_and_clean()
    cleaner.pivot_and_rename()
    cleaner.resample_data()

    # 2. Łączenie z prognozą Solcast
    merger = DataMerger("outputs/dane_falownika_plus_roz_moc.csv", "data/solcast_history.csv")
    dane_treningowe = merger.dopasuj_i_przygotuj_dane()

    # 3. Trenowanie modelu
    trener = ModelTrainer(dane_treningowe)
    trener.run()

    # 4. Predykcja na danych prognozowanych
    predictor = Predictor("models/model_trained.keras", "models/scaler_produkcji.pkl")
    forecast = pd.read_csv("data/solcast_forecast.csv")
    prediction = predictor.predict(forecast)
    predictor.save_prediction(prediction)
    predictor.agreguj_dziennie(prediction)

    # 5. Wizualizacja dla wybranego dnia
    viz = Visualizer()
    viz.plot_daily(prediction, target_date="2025-06-18")

    print("✅ Proces zakończony pomyślnie.")


if __name__ == "__main__":
    main()
