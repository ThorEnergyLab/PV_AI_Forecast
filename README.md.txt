# PV AI Forecasting

This project predicts photovoltaic (PV) energy production based on weather forecasts from Solcast and real-time data from the inverter (via MQTT). The AI model predicts energy production in 15-minute intervals and calculates daily totals.

---

## 📦 Project Structure

PV_AI_Forecast/
├── data/ ← Input data (mqtt_data.csv, solcast_history.csv, solcast_forecast.csv)
├── outputs/ ← Processed data and results (pivoted CSVs, reports)
├── models/ ← Saved AI models (model_trained.keras, scaler_produkcji.pkl)
├── src/ ← Python scripts (data_cleaner.py, data_merger.py, model_trainer.py, predictor.py, visualizer.py, main.py)
├── pipeline.ipynb ← Jupyter notebook for interactive work
├── README.md ← Project description (this file)
├── requirements.txt ← Required Python libraries
├── .gitignore ← Files and folders to be ignored by Git

yaml
Kopiuj
Edytuj

---

## 🚀 Features

- ✅ Cleaning and filtering data from MQTT (inverter or LAN Controller).
- ✅ Merging inverter data with Solcast data (historical for training or forecast for prediction).
- ✅ AI model training (regression using a Multi-Layer Perceptron).
- ✅ Energy production prediction based on weather forecast.
- ✅ Aggregating results to 15-minute intervals and daily totals.
- ✅ Visualization of predictions and historical data.

---

## 🔧 Requirements

- Python 3.9 or higher
- TensorFlow
- scikit-learn
- pandas
- numpy
- matplotlib
- seaborn
- joblib
- (optional) requests — if using Solcast API
- (optional) paho-mqtt — if using MQTT for data logging or device control

---

## ▶️ How to Run

### ✅ Step 1: Install required libraries

```bash
pip install -r requirements.txt
✅ Step 2: Run the full pipeline (clean → merge → train → predict)
bash
Kopiuj
Edytuj
cd src
python main.py
✅ Step 3: Run only prediction (without training)
bash
Kopiuj
Edytuj
cd src
python predict.py
🔥 Future Development
 Automatic downloading of Solcast forecast data every 6 hours.

 Continuous MQTT data logging to a database.

 Real-time control of devices via MQTT based on predictions and live data.

 Web dashboard for monitoring predictions and historical data.

 Automatic retraining of the AI model with new data.

👷 Project Status
✅ The pipeline is working in testing mode.

🔨 Migration from Jupyter notebook to production-grade Python scripts is in progress.

🚀 The GitHub version is under active development and will be updated regularly.

📜 License
Work in progress — the license will be defined after the initial development phase.










