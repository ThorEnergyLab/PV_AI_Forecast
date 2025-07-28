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

### ✅ Step 2: Run the full pipeline (clean → merge → train → predict)

```bash
cd src
python main.py
### ✅ Step 3: Run only prediction (without training)

```bash
cd src
python predict.py


1.env Configuration
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

This Jupyter notebook serves as an interactive environment for data exploration, preprocessing, model training, and prediction testing. It contains step-by-step code snippets, visualizations, and explanations used during the development phase of the project.

**Purpose:**

- Explore and clean historical data from MQTT and Solcast sources.
- Prototype and train the neural network model.
- Visualize intermediate results and forecasts.
- Experiment with different data processing and model configurations.

**Note:**  
This notebook is intended for development and experimentation. The production-ready code is organized in Python scripts (`main.py`, `predict.py`, etc.). You may use this notebook for further development or learning, but it is not required for running the production workflow.
