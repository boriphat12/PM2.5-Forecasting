# PM2.5 Air Quality Forecasting: Bangkok

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)
![Optuna](https://img.shields.io/badge/Tuning-Optuna-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-green)

A Machine Learning project to **forecast PM2.5 concentrations 1 hour in advance** for Bangkok, Thailand. The model is designed to simulate a real-world warning system scenario, strictly avoiding data leakage by using only historical data (Lag features) and temporal information.

## Project Overview

Air pollution (PM2.5) is a critical health issue in Bangkok. This project aims to build a robust forecasting model that can predict future air quality levels without relying on concurrent weather data (which is unknown in a real-time forecasting context).

**Key Performance:**
- **R² Score:** 0.9600
- **RMSE:** 16.29 µg/m³
- **MAE:** ~10.51 µg/m³

## Repository Structure

```bash
├── main.py                 # Script to fetch data from OpenWeatherMap & Open-Meteo APIs
├── pm25_prediction.ipynb   # Main notebook: Cleaning, Feature Engineering, Modeling (XGBoost)
├── .env                    # API Keys (Create this file yourself)
└── README.md               # Project documentation
```
## Methodology
### 1. Data Collection (`main.py`)

Fetches historical data from **Jan 2023 to Present**:

* **Pollutants:** PM2.5, PM10, NO, NO2, O3, CO, SO2, NH3 (Source: *OpenWeatherMap*)
* **Weather:** Temp, Humidity, Rain, Wind (Source: *Open-Meteo*)

### 2. Data Cleaning

* **Sensor Errors:** Zeros in `PM2.5`, `PM10` are treated as errors and imputed using Linear Interpolation.
* **Valid Zeros:** Zeros in `Ozone` and `NO` are retained, as they reflect real nocturnal photochemical reactions (Titration effect).

### 3. Feature Engineering (Anti-Leakage Strategy) 🚀

Strictly using **PAST** data to predict the **FUTURE** to prevent data leakage:

* **Excluded:** Current-timestamp variables (e.g., Current PM10, Temp) were removed to avoid look-ahead bias.
* **Included:**
* **Lags:** PM2.5 at `t-1` (1 hr ago), `t-2`, and `t-24` (Yesterday).
* **Time:** Hour of Day, Day of Week, Month.
* **Rolling Stats:** 3-hour and 24-hour rolling means (shifted by 1 hour).



### 4. Model Optimization

* **Algorithm:** XGBoost Regressor
* **Tuning:** Hyperparameters were optimized using **Optuna** (50 trials).
* **Split:** Strictly time-based splitting (Train: 2023-2024, Test: 2025-Present).

## Results

The model was evaluated on unseen data from 2025.

| Metric | Score | Interpretation |
| --- | --- | --- |
| **R²** | **0.9600** | The model explains 96% of the variance in PM2.5 levels. |
| **RMSE** | **16.29** | Root Mean Squared Error. |
| **MAE** | **10.51** | Average prediction error is +/- 10.51 µg/m³. |

**Key Drivers:**
The analysis confirms that **Recent History (Lag-1)** and **Time of Day** are the most critical predictors, validating the forecasting logic.

## How to Run

1. **Clone the repository**
```bash
git clone [https://github.com/boriphat12/PM2.5-Forecasting.git](https://github.com/boriphat12/PM2.5-Forecasting.git)

```


2. **Install required libraries**
```bash
pip install pandas numpy xgboost scikit-learn optuna matplotlib seaborn python-dotenv requests openmeteo-requests retry-requests

```


3. **Setup API Key**
Create a file named `.env` in the project root and add your API key:
```env
API_TOKEN=your_openweathermap_api_key

```


4. **Run the Project**
* **Step 1:** Run `main.py` to fetch the latest data (updates `pm25_bkk.csv`).
* **Step 2:** Open `pm25_prediction.ipynb` to train the model and view results.



---
