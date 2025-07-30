# ☀️ PV_AI_Forecast

**Photovoltaic Energy Production Forecast Using Neural Networks and Real-World Data**

This repository contains a complete pipeline for predicting solar energy production using:
- Real data from a Modbus-based inverter installation,
- Solar irradiance forecasts from the Solcast API,
- A neural network regression model built with TensorFlow/Keras.

---

## 📄 Thesis (PDF)

This project was developed as part of my postgraduate thesis in Data Science (DSW Wrocław, 2025):

**"Prediction of Photovoltaic Energy Using a Neural Network"**

📥 [Click here to read the full PDF](./docs/Pacybulenko_PV_Energy_Thesis_2025.pdf)

---

## 🧠 Model Overview

- Input features:
  - Global Horizontal Irradiance (GHI)
  - Air Temperature
  - Encoded time (`sin_hour`, `cos_hour`)
- Target:
  - Energy generated over the next 15-minute window
- Metrics:
  - MAE = 0.056 kWh
  - RMSE = 0.082 kWh
  - R² = 0.896

---

## ⚙️ Technologies Used

- Python 3.12
- pandas, numpy, scikit-learn
- TensorFlow / Keras
- SOLCAST API (GHI forecast)
- MQTT + Modbus RTU (data acquisition)
- Jupyter Notebook

---

## 📦 Directory Structure

PV_AI_Forecast/
├── data/ # Training data & Solcast forecasts
├── src/ # Scripts for preprocessing, training, prediction
├── docs/ # Final thesis PDF and documentation
└── README.md

---

## 🔮 Future Development

- Add DHI and more weather features (cloud cover, humidity)
- Replace MLP with LSTM for time-series continuity
- Deploy as lightweight prediction API or dashboard
- Per-installation model tuning for deployment in OZE projects

---

## 👤 Author

Paweł Pacybulenko  
[LinkedIn (optional)](https://www.linkedin.com/in/your-name/)  
[Thor Energy Lab](https://github.com/ThorEnergyLab)

---


## 📦 Project Structure
```
PV_AI_Forecast/
├── data/                       ← Input data (e.g., mqtt_data.csv, solcast_history.csv, solcast_forecast.csv)
├── outputs/                    ← Processed data and results (pivoted CSVs, aggregated reports, plots)
├── models/                     ← Saved AI models (e.g., model_trained.keras, scaler_produkcji.pkl)
├── src/                        ← Main Python scripts:
│   ├── data_cleaner.py             ← Data cleaning and preprocessing from MQTT raw data
│   ├── data_merger.py              ← Merging inverter and weather forecast data
│   ├── model_trainer.py            ← Training the neural network model
│   ├── predictor.py                ← Predicting energy production using trained model
│   ├── visualizer.py               ← Plotting and saving results as PDF
│   ├── main.py                    ← Full pipeline: training + prediction (demo and online modes)
│   ├── predict.py                 ← Prediction only (uses pre-trained model)
│   ├── mqtt_data_collector.py    ← Example script to collect MQTT data from inverter (requires adaptation)
│   └── solcast_history_downloader.py ← Example script to download historical weather data from Solcast (requires adaptation)
├── pipeline.ipynb              ← Jupyter notebook for interactive exploration and testing
├── README.md                   ← Project description and instructions (this file)
├── requirements.txt            ← Python dependencies
├── .gitignore                 ← Git ignore rules
└── .env.example.txt            ← Example environment variables file (API keys, mode flags)

  

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

## ⚠️ Important Notice

Integration of this program with a real photovoltaic installation requires solid technical knowledge including:

- MQTT protocol configuration and message handling  
- LAN controller setup and communication  
- Understanding inverter register maps and data acquisition  
- Fundamentals of photovoltaic system operation  
- Awareness of how varying weather conditions affect system behavior  

This project provides tools and example scripts, but successful deployment and training of the prediction model depend on correctly obtaining and preparing installation-specific data.  

Users without experience in these areas should be prepared for a learning curve or seek expert assistance.

### Future Possibilities

Once integrated with a specific installation, this system can potentially be extended to control devices based on forecasted and real-time energy production. This capability can help optimize:

- Scheduling of production processes  
- Operation of household appliances  
- Energy management and load balancing  

Such features will enable smarter use of renewable energy tailored to actual and predicted system output.
