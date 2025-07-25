import pandas as pd
import numpy as np
from tensorflow import keras
import joblib


class Predictor:
    def __init__(self, model_path, scaler_path):
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)

    def prepare_features(self, df_forecast):
        df = df_forecast.copy()
        df['period_end'] = pd.to_datetime(df['period_end'])
        df['hour'] = df['period_end'].dt.hour + df['period_end'].dt.minute / 60
        df['sin_hour'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['cos_hour'] = np.cos(2 * np.pi * df['hour'] / 24)

        features = df[['ghi', 'air_temp', 'sin_hour', 'cos_hour']].values
        scaled = self.scaler.transform(features)

        return df, scaled

    def predict(self, df_forecast):
        df, X_scaled = self.prepare_features(df_forecast)
        y_pred = self.model.predict(X_scaled).flatten()
        y_pred = np.maximum(y_pred, 0)
        df['energia_15min_pred [kWh]'] = np.round(y_pred, 4)

        return df

    def save_prediction(self, df, filename="outputs/prognoza_z_predykcja.csv"):
        df.to_csv(filename, index=False)

    def agreguj_dziennie(self, df):
        df['data'] = df['period_end'].dt.date
        suma_dzienna = (
            df.groupby('data')['energia_15min_pred [kWh]']
            .sum()
            .reset_index()
            .rename(columns={'energia_15min_pred [kWh]': 'energia_dzienna_pred [kWh]'})
        )
        suma_dzienna.to_csv("outputs/prognoza_suma_dzienna.csv", index=False)
        return suma_dzienna
