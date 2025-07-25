import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras import layers, models, Input, callbacks
import joblib
import matplotlib.pyplot as plt


class ModelTrainer:
    def __init__(self, df):
        self.df = df
        self.model = None
        self.scaler = StandardScaler()

    def przygotuj_cechy_i_etykiety(self):
        X = self.df[["ghi", "air_temp", "sin_hour", "cos_hour"]].values
        y = self.df["energia_15min [kWh]"].values
        return X, y

    def skaluj_dane(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, y_train, y_test

    def zbuduj_model(self):
        self.model = models.Sequential([
            Input(shape=(4,)),
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    def trenuj(self, X_train, y_train, X_test, y_test):
        early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        self.historia = self.model.fit(
            X_train, y_train,
            epochs=100,
            batch_size=32,
            validation_data=(X_test, y_test),
            callbacks=[early_stop]
        )

    def ocen_model(self, X_test, y_test):
        y_test_pred = self.model.predict(X_test).flatten()

        mae = mean_absolute_error(y_test, y_test_pred)
        mse = mean_squared_error(y_test, y_test_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_test_pred)

        print(f"MAE: {mae:.3f} kWh")
        print(f"RMSE: {rmse:.3f} kWh")
        print(f"R²: {r2:.3f}")

    def zapisz_model_i_scaler(self):
        self.model.save('models/model_trained.keras')
        joblib.dump(self.scaler, "models/scaler_produkcji.pkl")
        print("Model i scaler zapisane.")

    def wykres_uczenia(self):
        plt.figure(figsize=(8, 5))
        plt.plot(self.historia.history['loss'], label='Strata treningowa')
        plt.plot(self.historia.history['val_loss'], label='Strata walidacyjna')
        plt.xlabel('Epoka')
        plt.ylabel('MSE')
        plt.title('Postęp uczenia się modelu')
        plt.legend()
        plt.grid(True)
        plt.show()

    def run(self):
        X, y = self.przygotuj_cechy_i_etykiety()
        X_train, X_test, y_train, y_test = self.skaluj_dane(X, y)
        self.zbuduj_model()
        self.trenuj(X_train, y_train, X_test, y_test)
        self.ocen_model(X_test, y_test)
        self.wykres_uczenia()
        self.zapisz_model_i_scaler()
