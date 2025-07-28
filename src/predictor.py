import pandas as pd
import numpy as np
import joblib
from tensorflow import keras
import os

# Set path to outputs directory relative to this file location
# Ustaw ścieżkę do katalogu outputs względem lokalizacji tego pliku
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
outputs_dir = os.path.join(parent_dir, "outputs")
os.makedirs(outputs_dir, exist_ok=True)

class Predictor:
    def __init__(self, model_path, scaler_path):
        print(" Loading model and scaler...")  # Wczytuję model i skaler...
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        print(" Model and scaler loaded.")  # Model i skaler wczytane.

    def prepare_forecast_data(self, df):
        print(" Preparing forecast data...")  # Przygotowuję dane forecastu...

        # Convert period_end to datetime with UTC timezone
        # Konwersja period_end do datetime z UTC
        df['period_end'] = pd.to_datetime(df['period_end'], utc=True)

        # Calculate decimal hour from timestamp
        # Oblicz godziny dziesiętne z timestampu
        df['hour_decimal'] = df['period_end'].dt.hour + df['period_end'].dt.minute / 60

        # Add sine and cosine of hour to capture daily cyclicity
        # Dodaj sinus i cosinus godziny dla modelowania cykliczności dobowej
        df['sin_hour'] = np.sin(2 * np.pi * df['hour_decimal'] / 24)
        df['cos_hour'] = np.cos(2 * np.pi * df['hour_decimal'] / 24)

        features = ['ghi', 'air_temp', 'sin_hour', 'cos_hour']  # cechy wejściowe / input features

        # Check for missing columns in forecast data
        # Sprawdź brakujące kolumny w danych prognozy
        missing_cols = [col for col in features if col not in df.columns]
        if missing_cols:
            raise ValueError(f" Missing columns in forecast data: {missing_cols}")

        print(" Forecast data prepared.")  # Dane forecastu przygotowane.

        return df, features

    def predict(self, forecast_df):
        df, features = self.prepare_forecast_data(forecast_df)

        # Extract feature matrix and scale it
        # Pobierz macierz cech i skaluj ją
        X_pred = df[features].values
        X_scaled = self.scaler.transform(X_pred)

        print(" Running prediction...")  # Uruchamiam predykcję...
        y_pred = self.model.predict(X_scaled).flatten()

        # Clip negative predictions to zero
        # Zabezpieczenie przed wartościami ujemnymi
        y_pred = np.clip(y_pred, 0, None)

        # If GHI == 0 (no sun), predicted energy is also zero
        # Jeśli GHI == 0 → energia też 0
        y_pred[df['ghi'] == 0] = 0

        # Add prediction results as new column
        # Dodaj predykcję jako nową kolumnę
        df['energy_15min_pred_kWh'] = y_pred

        print(" Prediction finished.")  # Predykcja zakończona.
        return df

    def save_prediction(self, df):
        print(" Saving forecast to outputs/forecast_with_prediction.csv...")  # Zapisuję prognozę do pliku...
        df.to_csv(os.path.join(outputs_dir, "forecast_with_prediction.csv"), index=False)
        print(" Saved.")  # Zapisano.

    def aggregate_daily(self, df):
        print(" Aggregating daily forecast...")  # Agreguję prognozę dzienną...

        # Convert period_end to datetime with UTC timezone
        # Konwersja period_end do datetime z UTC
        df['period_end'] = pd.to_datetime(df['period_end'], utc=True)

        # Extract date part only for aggregation
        # Wyodrębnij datę bez czasu do agregacji
        df['date'] = df['period_end'].dt.date

        # Group by date and sum predicted energy
        # Grupuj po dacie i sumuj energię predykcyjną
        df_sum = (
            df.groupby('date')['energy_15min_pred_kWh']
            .sum()
            .reset_index()
            .rename(columns={'energy_15min_pred_kWh': 'daily_energy_sum_kWh'})
        )

        # Save daily sum to CSV
        # Zapisz sumę dzienną do pliku CSV
        df_sum.to_csv(os.path.join(outputs_dir, "forecast_daily_sum.csv"), index=False)

        print(" Daily aggregation saved as outputs/forecast_daily_sum.csv.")  # Agregacja zapisana
        return df_sum

