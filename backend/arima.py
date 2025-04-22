import pandas as pd
import pymysql
from dbutils.pooled_db import PooledDB
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from config import *
from urllib.parse import quote_plus
import matplotlib
import numpy as np
from pmdarima import auto_arima

matplotlib.use('TkAgg')

# Setup pooled DB connection
password = quote_plus(DB_PASSWD)
pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    charset='utf8mb4',
    autocommit=True,
    blocking=True,
    maxconnections=5
)

def predict_humidity():
    # Connect using pool
    conn = pool.connection()
    
    try:
        query = "SELECT time, humidity FROM api_data ORDER BY time ASC"
        df = pd.read_sql(query, conn)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        # Resample to hourly data
        df = df.resample('H').mean().interpolate()

        # Auto ARIMA to find best (p,d,q)
        stepwise_model = auto_arima(df['humidity'], seasonal=False, trace=True, suppress_warnings=True)
        best_order = stepwise_model.order

        # Fit ARIMA
        model = ARIMA(df['humidity'], order=best_order)
        model_fit = model.fit()

        # Forecast next 12 hours
        forecast_steps = 12
        forecast_result = model_fit.get_forecast(steps=forecast_steps)
        forecast = forecast_result.predicted_mean

        # Generate future hourly timestamps
        future_times = pd.date_range(start=df.index[-1] + pd.Timedelta(hours=1), periods=forecast_steps, freq='H')

        # Print forecast
        print("Humidity Forecast for the Next 12 Hours:")
        for i, (timestamp, humidity) in enumerate(zip(future_times, forecast), 1):
            print(f"Hour {i}: {timestamp.strftime('%Y-%m-%d %H:%M')} - Forecasted Humidity: {humidity:.2f}%")

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['humidity'], label='Historical Humidity')
        plt.plot(future_times, forecast, label='Forecasted Humidity', color='red')
        plt.title('Humidity Forecast for the Next 12 Hours')
        plt.xlabel('Datetime')
        plt.ylabel('Humidity (%)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return forecast

    finally:
        conn.close()

# Run the forecast
forecasted_values = predict_humidity()
