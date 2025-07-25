import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import matplotlib.pyplot as plt


class ModelTrainer:
    def __init__(self, df):
        self.df = df
        self.scaler = StandardScaler()
        self.model = None

    def prepare_data(self):
        X = self.df[['ghi', 'air_temp', 'sin_hour', 'cos_hour']]
        y = self.df['energia_15min [kWh]']
        return X, y

    def build_model(self, input_dim):
        model = Sequential([
            Dense(64, activation='relu', input_dim=input_dim),
            Dense(32, activation='relu'),
            Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self):
        print("🧠 Przygotowuję dane do treningu...")

        X, y = self.prepare_data()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print("🧠 Buduję model...")
        self.model = self.build_model(input_dim=X_train_scaled.shape[1])

        print("🚀 Start treningu...")
        early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

        history = self.model.fit(
            X_train_scaled, y_train,
            validation_data=(X_test_scaled, y_test),
            epochs=200,
            batch_size=16,
            callbacks=[early_stop],
            verbose=1
        )

        print("💾 Zapisuję model i scaler...")
        self.model.save("models/model_trained.keras")
        joblib.dump(self.scaler, "models/scaler_produkcji.pkl")
        print("✅ Model zapisany.")

        self.plot_training_history(history)
        self.evaluate_model(X_test_scaled, y_test)

    def plot_training_history(self, history):
        plt.figure(figsize=(8, 5))
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Training History')
        plt.xlabel('Epoch')
        plt.ylabel('Loss (MSE)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def evaluate_model(self, X_test, y_test):
        print("\n📊 Wyniki na danych testowych:")

        y_pred = self.model.predict(X_test).flatten()

        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        print(f"🔸 R² Score       : {r2:.4f}")
        print(f"🔸 MAE (kWh)      : {mae:.4f}")
        print(f"🔸 RMSE (kWh)     : {rmse:.4f}")
