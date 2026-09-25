# ⚡ Energy Consumption Prediction & Web Dashboard

An end-to-end Machine Learning web application and time-series analysis pipeline designed to forecast regional energy consumption (measured in Megawatts - MW). This project utilizes advanced gradient boosting algorithms and features an interactive web user interface deployed via Streamlit.

---

## 🎯 Problem Statement & Core Question
* **The Question:** *How can historical hourly energy consumption patterns and temporal indicators be leveraged to accurately predict future energy demands, enabling better resource allocation and grid management?*
* **Objective:** Build a robust regression model capable of forecasting energy load requirements based on time features (hour, day, month, seasonal markers) and historical lag data, and package it into an accessible, real-time web application.

---

## 🛠️ Step-by-Step Methodology & What Was Done

### **Step 1: Data Preprocessing & Time-Series Formatting**
* Loaded historical energy consumption datasets and converted datetime columns into proper datetime objects.
* Sorted records chronologically to maintain the temporal integrity critical for time-series forecasting.

### **Step 2: Feature Engineering**
To feed machine learning models temporal context, multiple predictive features were extracted from raw timestamps:
* **Temporal Indicators:** Extracted `Hour`, `DayOfWeek`, `DayOfYear`, `Month`, and `Year`.
* **Binary Flags:** Created an `IsWeekend` feature to differentiate weekday vs. weekend consumption behaviors.
* **Lag Features:** Built critical historical lookback features (`Lag_1` for consumption 1 hour prior and `Lag_24` for consumption 24 hours prior) to capture short-term autoregressive trends.

### **Step 3: Model Training & Evaluation**
* Performed a chronological train-test split to prevent data leakage.
* Trained and compared multiple regression models, including **Random Forest Regressor** and **XGBoost Regressor**.
* Evaluated performance using standard metrics: **Mean Absolute Error (MAE)**, **Root Mean Squared Error (RMSE)**, and **$R^2$ Score**, finding that XGBoost yielded optimal prediction accuracy.
* Serialized the final trained model into a binary file (`energy_model.pkl`) using `joblib`.

### **Step 4: Interactive Web Application Development (`app.py`)**
* Developed a responsive web interface using **Streamlit**.
* Designed custom input widgets allowing users to select target dates, hours of the day, and input recent historical lag values (MW).
* Automatically formats these inputs into the exact feature schema expected by the machine learning model to generate instant predictions.

---

## 📂 Project Structure

```text
├── energy_model.pkl       # Serialized XGBoost regression model (trained via Colab)
├── app.py                 # Streamlit web application script & user interface
├── requirements.txt       # Project python dependencies
└── README.md              # Project documentation and workflow description
