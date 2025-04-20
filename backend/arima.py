import pandas as pd
import pymysql
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from config import *
from urllib.parse import quote_plus
import matplotlib
import numpy as np
from pmdarima import auto_arima

matplotlib.use('TkAgg')


def predict_temperature():
    # Connect to MySQL
    password = DB_PASSWD
    encoded_password = quote_plus(password)
    engine = create_engine(f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}')

    query = "SELECT time, humidity FROM kidbright_project ORDER BY time ASC"
    df = pd.read_sql(query, engine)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # Use Auto ARIMA to find best order
    stepwise_model = auto_arima(df['humidity'], seasonal=False, trace=True, suppress_warnings=True)
    best_order = stepwise_model.order

    # Fit ARIMA with best order
    model = ARIMA(df['humidity'], order=best_order)
    model_fit = model.fit()

    # Forecast
    forecast_steps = 14
    forecast_result = model_fit.get_forecast(steps=forecast_steps)
    forecast = forecast_result.predicted_mean

    # Future dates
    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')

    # Print forecast
    print("Temperature Forecast for the Next 14 Days:")
    for i, (date, humidity) in enumerate(zip(future_dates, forecast), 1):
        print(f"Day {i}: {date.strftime('%Y-%m-%d')} - Forecasted Temperature: {humidity:.2f}°C")

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['humidity'], label='Historical Data')
    plt.plot(future_dates, forecast, label='Forecasted Values', color='red')
    plt.title('humidity Forecast for the Next 14 Days')
    plt.xlabel('Date')
    plt.ylabel('humidity (%)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return forecast


# Run the forecast
forecasted_values = predict_temperature()
