# PV AI Forecasting
This project predicts photovoltaic (PV) energy production based on weather forecasts from Solcast and real-time data from the inverter (via MQTT). The AI model predicts energy production in 15-minute intervals and calculates daily totals.

Important:
The scripts and models provided operate on a neural network trained with data from the author’s specific PV installation.
To achieve accurate predictions tailored to your own installation, you must train your own model using:

Real inverter data collected via MQTT from your specific inverter device

Historical weather data for your location downloaded from Solcast API

Without training on your own data, predictions may not accurately reflect your installation’s performance.

---

## 📦 Project Structure

PV_AI_Forecast/
├── data/                 ← Input data (e.g., mqtt_data.csv, solcast_history.csv, solcast_forecast.csv)
├── outputs/              ← Processed data and results (pivoted CSVs, aggregated reports, plots)
├── models/               ← Saved AI models (e.g., model_trained.keras, scaler_produkcji.pkl)
├── src/                  ← Main Python scripts:
│   ├── data_cleaner.py         ← Data cleaning and preprocessing from MQTT raw data
│   ├── data_merger.py          ← Merging inverter and weather forecast data
│   ├── model_trainer.py        ← Training the neural network model
│   ├── predictor.py            ← Predicting energy production using trained model
│   ├── visualizer.py           ← Plotting and saving results as PDF
│   ├── main.py                 ← Full pipeline: training + prediction (demo and online modes)
│   ├── predict.py              ← Prediction only (uses pre-trained model)
│   ├── mqtt_data_collector.py  ← Example script to collect MQTT data from inverter (*requires adaptation*)
│   └── solcast_history_downloader.py ← Example script to download historical weather data from Solcast (*requires adaptation*)
├── pipeline.ipynb         ← Jupyter notebook for interactive exploration and testing
├── README.md              ← Project description and instructions (this file)
├── requirements.txt       ← Python dependencies
├── .gitignore             ← Git ignore rules
└── .env.example.txt       ← Example environment variables file (API keys, mode flags)
  

---

## Features

- ✅ Cleaning and filtering data from MQTT (inverter or LAN Controller).  
- ✅ Merging inverter data with Solcast data (historical for training or forecast for prediction).  
- ✅ AI model training (regression using a Multi-Layer Perceptron).  
- ✅ Energy production prediction based on weather forecast.  
- ✅ Aggregating results to 15-minute intervals and daily totals.  
- ✅ Visualization of predictions and historical data.  

> ⚠️ Note:  
> Some scripts (e.g., `mqtt_data_collector.py`, `solcast_history_downloader.py`) require technical configuration and adaptation to your hardware and API.

---

## Operation Modes

- **Full Pipeline (Demo Mode)**  
  Run the complete process — data cleaning, model training, and prediction — using static demo data from a sample inverter dataset.  
  Controlled by setting `DEMO=1` in the `.env` file.

- **Online Prediction Mode**  
  Perform predictions using live weather data fetched from Solcast API and the pre-trained model (trained on the sample inverter data).  
  Controlled by setting `DEMO=0` in the `.env` file.

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


### ✅ Step 2: Run the full pipeline (clean → merge → train → predict)

```bash
cd src
python main.py

### ✅ Step 3: Run only prediction (without training)

```bash
cd src
python predict.py

## ⚙️ `.env` Configuration

This project uses a `.env` file to store environment variables that control how the program runs.

### 📋 How to prepare your `.env` file

1. Copy the `.env.example` file to `.env` in the root folder:

```bash
cp .env.example .env

Or create a new .env file and paste the contents from .env.example.

2. Fill in your Solcast API key:
SOLCAST_API_KEY=your_api_key_here 🔑
3. Set the mode with USE_DEMO:

1 — Demo mode (loads data from local CSV file) 🛠️

0 — Production mode (fetches data online) ☁️

⚠️ Important notes
.env is ignored by Git thanks to .gitignore, so your secrets stay safe 🔒

Never share your API key publicly! 🚫🔑

## Interactive Notebook (`pipeline.ipynb`)

This Jupyter notebook provides an interactive environment for:

Exploring and cleaning historical MQTT and Solcast data.

Prototyping and training the neural network model.

Visualizing intermediate results and predictions.

Experimenting with data processing and model configurations.

Note:
This notebook is for development and learning purposes. The production workflow is implemented in Python scripts (main.py, predict.py, etc.). Use the notebook to extend or explore the project, but it is not required for regular use.

**Note:**  
This notebook is intended for development and experimentation. The production-ready code is organized in Python scripts (`main.py`, `predict.py`, etc.). You may use this notebook for further development or learning, but it is not required for running the production workflow.

### Example Scripts
MQTT Data Collector Script (mqtt_data_collector.py)

A simple example Python script that connects to an MQTT broker, subscribes to specific topic patterns, and appends incoming messages to a CSV file with timestamps.

Note:
Connection details (BROKER, PORT, USERNAME, PASSWORD, TOPIC) must be configured in the script before running.
This script serves as a basic example for collecting data from your inverter or other MQTT-enabled devices for further processing.


## Example Historical Data Downloader

This script fetches historical solar radiation data from the Solcast API. It requires your API key to be set as the environment variable SOLCAST_API_KEY.

Important:
This script is currently untested outside the Jupyter notebook environment and should be considered a starting point for your own implementation.