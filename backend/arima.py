import pandas as pd
import pymysql
from dbutils.pooled_db import PooledDB
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from config import *
from urllib.parse import quote_plus
import matplotlib
import numpy as np
from pmdarima import auto_arima

matplotlib.use('TkAgg')

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

def predict_and_combine_humidity():
    conn = pool.connection()

    try:
        query = "SELECT time, humidity FROM api_data ORDER BY time ASC"
        df = pd.read_sql(query, conn)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        df_hourly = df.resample('H').mean().interpolate()
        stepwise_model = auto_arima(df_hourly['humidity'], seasonal=False, trace=False, suppress_warnings=True)
        best_order = stepwise_model.order

        model = ARIMA(df_hourly['humidity'], order=best_order)
        model_fit = model.fit()

        forecast_steps = 12
        forecast_result = model_fit.get_forecast(steps=forecast_steps)
        forecast = forecast_result.predicted_mean
        future_times = pd.date_range(start=df_hourly.index[-1] + pd.Timedelta(hours=1), periods=forecast_steps, freq='H')

        df_future = pd.DataFrame({'humidity': forecast.values}, index=future_times)
        df_past_12 = df_hourly.last('12H')

        combined_df = pd.concat([df_past_12, df_future])
        combined_df['source'] = ['actual'] * len(df_past_12) + ['forecast'] * len(df_future)

        plt.figure(figsize=(12, 6))
        plt.plot(df_past_12.index, df_past_12['humidity'], label='Past 12 Hours (Actual)', marker='o')
        plt.plot(df_future.index, df_future['humidity'], label='Next 12 Hours (Forecast)', color='red', linestyle='--', marker='x')
        plt.title('Humidity: Past 12 Hours + Next 12 Hours Forecast')
        plt.xlabel('Datetime')
        plt.ylabel('Humidity (%)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return combined_df

    finally:
        conn.close()

combined_humidity_df = predict_and_combine_humidity()
print(combined_humidity_df)
