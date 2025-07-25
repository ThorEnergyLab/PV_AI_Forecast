import pandas as pd
import numpy as np
import joblib
from tensorflow import keras


class Predictor:
    def __init__(self, model_path, scaler_path):
        print(" Wczytuję model i skaler...")
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        print(" Model i skaler wczytane.")

    def prepare_forecast_data(self, df):
        print(" Przygotowuję dane forecastu...")

        df['period_end'] = pd.to_datetime(df['period_end'], utc=True)
        df['hour_decimal'] = df['period_end'].dt.hour + df['period_end'].dt.minute / 60
        df['sin_hour'] = np.sin(2 * np.pi * df['hour_decimal'] / 24)
        df['cos_hour'] = np.cos(2 * np.pi * df['hour_decimal'] / 24)

        features = ['ghi', 'air_temp', 'sin_hour', 'cos_hour']

        missing_cols = [col for col in features if col not in df.columns]
        if missing_cols:
            raise ValueError(f" Missing columns in forecast data: {missing_cols}")

        print(" Dane forecastu przygotowane.")

        return df, features

    def predict(self, forecast_df):
        df, features = self.prepare_forecast_data(forecast_df)

        X_pred = df[features].values
        X_scaled = self.scaler.transform(X_pred)

        print(" Uruchamiam predykcję...")
        y_pred = self.model.predict(X_scaled).flatten()
        # zabezpieczenie przed wartosciami ujemnymi
        y_pred = np.clip(y_pred, 0, None)

        #  Zabezpieczenie: jeśli GHI == 0 → energia też 0
        y_pred[df['ghi'] == 0] = 0

        df['energia_15min_pred [kWh]'] = y_pred
        print(" Predykcja zakończona.")
        return df

    def save_prediction(self, df):
        print(" Zapisuję prognozę do outputs/prognoza_z_predykcja.csv...")
        df.to_csv("outputs/prognoza_z_predykcja.csv", index=False)
        print(" Zapisano.")

    def agreguj_dziennie(self, df):
        print(" Agreguję prognozę dzienną...")

        df['period_end'] = pd.to_datetime(df['period_end'], utc=True)
        df['data'] = df['period_end'].dt.date

        df_sum = (
            df.groupby('data')['energia_15min_pred [kWh]']
            .sum()
            .reset_index()
            .rename(columns={'energia_15min_pred [kWh]': 'energia_suma_dzien [kWh]'})
        )

        df_sum.to_csv("outputs/prognoza_suma_dzienna.csv", index=False)

        print(" Agregacja dzienna zapisana jako outputs/prognoza_suma_dzienna.csv.")
        return df_sum 
