import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
from statsmodels.tsa.arima.model import ARIMA
from config import *
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import numpy as np
from datetime import timedelta

def forecast_column(df, column_name, steps=14):
    model = ARIMA(df[column_name], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast

def predict_w_condition_next_14_days():
    # 1. Connect to MySQL
    password = "pichapop.ro@ku.th"
    encoded_password = quote_plus(password)
    engine = create_engine(f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}')

    # 2. Get training data
    query = "SELECT temp, wind_kph, humidity, w_condition FROM api_data"
    df = pd.read_sql(query, engine)
    df.dropna(inplace=True)

    # 3. Encode condition labels
    le = LabelEncoder()
    df['w_condition_encoded'] = le.fit_transform(df['w_condition'])

    # 4. Normalize features
    features = ['temp', 'wind_kph', 'humidity']
    X = df[features]
    y = df['w_condition_encoded']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Train KNN
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    # 6. Evaluate model
    y_pred = knn.predict(X_test)
    print("Accuracy:", round(accuracy_score(y_test, y_pred), 2))
    print(classification_report(
        y_test, y_pred,
        labels=np.unique(y),
        target_names=le.classes_,
        zero_division=0
    ))

    # 7. Forecast next 14 days for temp, wind_kph, humidity
    forecast_query = "SELECT time, temp, wind_kph, humidity FROM api_data ORDER BY time ASC"
    forecast_df = pd.read_sql(forecast_query, engine)
    forecast_df['time'] = pd.to_datetime(forecast_df['time'])
    forecast_df.set_index('time', inplace=True)

    # Daily average
    daily_avg = forecast_df.resample('D').mean().dropna()

    # Forecast each variable
    forecast_days = 14
    temp_forecast = forecast_column(daily_avg, 'temp', steps=forecast_days)
    wind_forecast = forecast_column(daily_avg, 'wind_kph', steps=forecast_days)
    humidity_forecast = forecast_column(daily_avg, 'humidity', steps=forecast_days)

    # 8. Prepare future dates and features
    last_date = daily_avg.index[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]

    future_data = pd.DataFrame({
        'date': future_dates,
        'temp': temp_forecast,
        'wind_kph': wind_forecast,
        'humidity': humidity_forecast
    })

    # 9. Normalize forecasted features
    future_scaled = scaler.transform(future_data[['temp', 'wind_kph', 'humidity']])

    # 10. Predict condition
    condition_preds = knn.predict(future_scaled)
    decoded_preds = le.inverse_transform(condition_preds)

    # 11. Print results
    print("\n🧠 Weather Condition Predictions for the Next 14 Days:")
    for i in range(forecast_days):
        print(f"Day {i+1} - {future_data['date'][i].strftime('%Y-%m-%d')}: "
              f"Temp: {future_data['temp'][i]:.2f}°C, "
              f"Wind: {future_data['wind_kph'][i]:.2f} kph, "
              f"Humidity: {future_data['humidity'][i]:.2f}%, "
              f"Predicted Condition: {decoded_preds[i]}")

    return decoded_preds


# Run it
if __name__ == "__main__":
    predict_w_condition_next_14_days()
