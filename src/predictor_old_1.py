import pandas as pd
import numpy as np
from tensorflow import keras
import joblib


class Predictor:
    def __init__(self, model_path, scaler_path):
        print("📥 Wczytuję model i skaler...")
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        print("✅ Model i skaler wczytane.")

    def predict(self, forecast):
        print("🔧 Przygotowuję dane forecastu...")

        forecast = forecast.copy()
        forecast['period_end'] = pd.to_datetime(forecast['period_end'])

        # Feature engineering
        forecast['hour'] = forecast['period_end'].dt.hour + forecast['period_end'].dt.minute / 60
        forecast['sin_hour'] = np.sin(2 * np.pi * forecast['hour'] / 24)
        forecast['cos_hour'] = np.cos(2 * np.pi * forecast['hour'] / 24)

        X_pred = forecast[['ghi', 'air_temp', 'sin_hour', 'cos_hour']].values

        print("✅ Dane forecastu przygotowane.")

        print("🤖 Uruchamiam predykcję...")
        y_pred = self.model.predict(self.scaler.transform(X_pred)).flatten()
        y_pred = np.maximum(y_pred, 0)  # Zero jeśli ujemne

        forecast['energia_15min_pred [kWh]'] = np.round(y_pred, 4)

        print("✅ Predykcja zakończona.")
        return forecast

    def save_prediction(self, prediction):
        print("💾 Zapisuję prognozę do outputs/prognoza_z_predykcja.csv...")
        prediction.to_csv("outputs/prognoza_z_predykcja.csv", index=False)
        print("✅ Zapisano.")

    def agreguj_dziennie(self, prediction):
        print("📊 Agreguję prognozę dzienną...")
        prediction['data'] = prediction['period_end'].dt.date
        suma_dzienna = (
            prediction.groupby('data')['energia_15min_pred [kWh]']
            .sum()
            .reset_index()
            .rename(columns={'energia_15min_pred [kWh]': 'energia_dzienna_pred [kWh]'})
        )
        suma_dzienna.to_csv("outputs/prognoza_suma_dzienna.csv", index=False)
        print("✅ Agregacja dzienna zapisana jako outputs/prognoza_suma_dzienna.csv.")
