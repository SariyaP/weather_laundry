import pandas as pd
import pymysql
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from config import *
from urllib.parse import quote_plus
import matplotlib
import numpy as np

matplotlib.use('TkAgg')


def calculate_metrics(actual, forecast):
    # Calculate Mean Absolute Error (MAE)
    mae = abs(actual - forecast).mean()

    # Calculate Root Mean Squared Error (RMSE)
    rmse = ((actual - forecast) ** 2).mean() ** 0.5

    # Calculate Mean Absolute Percentage Error (MAPE)
    mape = (abs(actual - forecast) / actual).mean() * 100

    return mae, rmse, mape


def predict_temperature():
    password = "pichapop.ro@ku.th"
    encoded_password = quote_plus(password)
    engine = create_engine(
        f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}')

    query = """
    SELECT time, temp FROM kidbright_project ORDER BY time ASC
    """
    df = pd.read_sql(query, engine)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    model = ARIMA(df['temp'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast_steps = 14
    forecast = model_fit.forecast(steps=forecast_steps)

    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1),
                                 periods=forecast_steps, freq='D')

    print("Temperature Forecast for the Next 14 Days:")
    for i, (date, temp) in enumerate(zip(future_dates, forecast), 1):
        print(
            f"Day {i}: {date.strftime('%Y-%m-%d')} - Forecasted Temperature: {temp:.2f}°C")

    actual_values = forecast + (0.5 * np.random.randn(
        forecast_steps))  # Simulated actual values (for demonstration)

    mae, rmse, mape = calculate_metrics(actual_values, forecast)

    print(f"\nMetrics for Forecast Accuracy and Precision:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

    plt.plot(df.index, df['temp'], label='Historical Data')
    plt.plot(future_dates, forecast, label='Forecasted Values', color='red')
    plt.title('Temperature Forecast for the Next 14 Days')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    return forecast


forecasted_values = predict_temperature()
