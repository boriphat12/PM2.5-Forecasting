
```
# 🌫️ PM2.5 Air Quality Forecasting: Bangkok

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)
![Optuna](https://img.shields.io/badge/Tuning-Optuna-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-green)

A Machine Learning project to **forecast PM2.5 concentrations 1 hour in advance** for Bangkok, Thailand. The model is designed to simulate a real-world warning system scenario, strictly avoiding data leakage by using only historical data (Lag features) and temporal information.

## 📌 Project Overview

Air pollution (PM2.5) is a critical health issue in Bangkok. This project aims to build a robust forecasting model that can predict future air quality levels without relying on concurrent weather data (which is unknown in a real-time forecasting context).

**Key Performance:**
- **R² Score:** 0.9600 (Excellent Fit)
- **RMSE:** 16.29 µg/m³
- **MAE:** ~10.51 µg/m³

## 📂 Repository Structure

```bash
├── main.py                 # Script to fetch data from OpenWeatherMap & Open-Meteo APIs
├── pm25_prediction.ipynb   # Main notebook: Cleaning, Feature Engineering, Modeling (XGBoost)
├── .env                    # API Keys (Create this file yourself)
└── README.md               # Project documentation

```

## 🛠️ Methodology

### 1. Data Collection (`main.py`)

Fetches historical data from **Jan 2023 to Present**:

* **Pollutants:** PM2.5, PM10, NO, NO2, O3, CO, SO2, NH3 (Source: *OpenWeatherMap*)
* **Weather:** Temp, Humidity, Rain, Wind (Source: *Open-Meteo*)

### 2. Data Cleaning

* **Sensor Errors:** Zeros in `PM2.5`, `PM10` are treated as errors and imputed.
* **Valid Zeros:** Zeros in `Ozone` and `NO` are retained (natural chemical reaction at night).

### 3. Feature Engineering (Anti-Leakage) 🚀

Strictly using **PAST** data to predict the **FUTURE**:

* **❌ Excluded:** Current-timestamp variables (e.g., Current PM10, Temp) to prevent looking ahead.
* **✅ Included:**
* **Lags:** PM2.5 at `t-1` (1 hr ago), `t-2`, and `t-24`.
* **Time:** Hour of Day, Day of Week.
* **Rolling Stats:** 3-hour mean (shifted by 1 hour).



### 4. Model Optimization

* **Model:** XGBoost Regressor
* **Tuning:** Hyperparameters optimized using **Optuna** (50 trials).
* **Split:** Train (2023-2024) | Test (2025-Present).

## 📊 Results

Evaluated on unseen data from 2025:

| Metric | Score | Interpretation |
| --- | --- | --- |
| **R²** | **0.9600** | The model explains 96% of the variance. |
| **RMSE** | **16.29** | Root Mean Squared Error. |

**Key Driver:** The model relies heavily on **Recent History (Lag-1)** and **Time of Day**, confirming valid forecasting logic.

## 🚀 How to Run

1. **Clone the repository**
```bash
git clone [https://github.com/yourusername/pm25-forecasting.git](https://github.com/yourusername/pm25-forecasting.git)

```


2. **Install required libraries**
```bash
pip install pandas numpy xgboost scikit-learn optuna matplotlib seaborn python-dotenv requests openmeteo-requests retry-requests

```


3. **Setup API Key**
Create a file named `.env` in the same folder and add your key:
```env
API_TOKEN=your_openweathermap_api_key

```


4. **Run the Project**
* First, run `main.py` to fetch the latest data.
* Then, open `pm25_prediction.ipynb` to train and evaluate the model.



---

```

```
