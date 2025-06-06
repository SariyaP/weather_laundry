import sys
from datetime import timedelta
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import pymysql
from dbutils.pooled_db import PooledDB
from flask import abort
from flask import jsonify
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from statsmodels.tsa.arima.model import ARIMA
from stub.swagger_server.models.api_data import ApiData
from config import *
from dry_estimator import calc_drying_hours
from pmdarima import auto_arima

sys.path.append(OPENAPI_STUB_DIR)
from swagger_server import models

pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    maxconnections=1,
    blocking=True
)


def get_latest_kidbright_data():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT id, time, temp, light, humidity
                FROM kidbright_project
                ORDER BY time DESC
                LIMIT 1
            """)
            result = cs.fetchone()
    finally:
        conn.close()

    if result:
        return models.KidbrightData(*result)
    else:
        abort(404)


def get_kidbright_data():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT id, time, temp, light, humidity 
                FROM kidbright_project 
                ORDER BY time DESC 
                LIMIT 50
            """)
            result = [models.KidbrightData(*row) for row in cs.fetchall()]
    finally:
        conn.close()
    
    return result


def get_kidbright_by_id(data_id):
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT id, time, temp, light, humidity 
                FROM kidbright_project 
                WHERE id = %s
            """, [data_id])
            row = cs.fetchone()
    finally:
        conn.close()

    if row:
        return models.KidbrightData(*row)
    else:
        abort(404)


def get_kidbright_by_timerange(start, end):
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT id, time, temp, light, humidity 
                FROM kidbright_project 
                WHERE time BETWEEN %s AND %s 
                ORDER BY time ASC
            """, [start, end])
            result = [models.KidbrightData(*row) for row in cs.fetchall()]
    finally:
        conn.close()

    return result


def insert_kidbright_data(temp, light, humidity):
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                INSERT INTO kidbright_project (time, temp, light, humidity)
                VALUES (NOW(), %s, %s, %s)
            """, [temp, light, humidity])
            conn.commit()
    finally:
        conn.close()
    
    return {"status": "success", "message": "Data inserted"}


def get_api_data_latest():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT id, time, temp, wind_kph, humidity, w_condition
                FROM api_data 
                ORDER BY time DESC 
                LIMIT 1
            """)
            row = cs.fetchone()
    finally:
        conn.close()

    if row:
        id, time, temp, wind_kph, humidity, w_condition = row

        try:
            drying_time = calc_drying_hours(temp, humidity, wind_kph, width=2)
            drying_status = classify_drying_status(drying_time, w_condition)

            return jsonify({
                "id": id,
                "time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "temp": temp,
                "wind_kph": wind_kph,
                "humidity": humidity,
                "w_condition": w_condition,
                "estimated_drying_time_hours": round(drying_time, 2),
                "drying_status": drying_status
            })

        except Exception as e:
            abort(400, f"Error calculating drying condition: {str(e)}")

    else:
        abort(404, "No API data found.")


def get_api_data_by_id(data_id):
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT id, time, temp, wind_kph, humidity, condition 
                FROM api_data 
                WHERE id = %s
            """, [data_id])
            row = cs.fetchone()
    finally:
        conn.close()

    if row:
        return models.ApiData(*row)
    else:
        abort(404)


def get_api_data_by_timerange(start, end):
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT id, time, temp, wind_kph, humidity, condition 
                FROM api_data 
                WHERE time BETWEEN %s AND %s 
                ORDER BY time ASC
            """, [start, end])
            result = [models.ApiData(*row) for row in cs.fetchall()]
    finally:
        conn.close()

    return result


def insert_api_data(temp, wind_kph, humidity, condition):
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                INSERT INTO api_data (time, temp, wind_kph, humidity, condition)
                VALUES (NOW(), %s, %s, %s, %s)
            """, [temp, wind_kph, humidity, condition])
            conn.commit()
    finally:
        conn.close()

    return {"status": "success", "message": "API data inserted"}


def get_kidbright_avg():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT 
                    ROUND(AVG(temp), 2), 
                    ROUND(AVG(light), 2), 
                    ROUND(AVG(humidity), 2)
                FROM kidbright_project
            """)
            row = cs.fetchone()
    finally:
        conn.close()

    return {
        "avg_temp": row[0],
        "avg_light": row[1],
        "avg_humidity": row[2]
    }


def get_kidbright_min_max():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT 
                    MIN(temp), MAX(temp), 
                    MIN(light), MAX(light), 
                    MIN(humidity), MAX(humidity)
                FROM kidbright_project
            """)
            row = cs.fetchone()
    finally:
        conn.close()

    return {
        "min_temp": row[0],
        "max_temp": row[1],
        "min_light": row[2],
        "max_light": row[3],
        "min_humidity": row[4],
        "max_humidity": row[5]
    }


def get_kidbright_hourly_average():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT 
                    HOUR(time) AS hour,
                    ROUND(AVG(temp), 2) AS avg_temp,
                    ROUND(AVG(light), 2) AS avg_light,
                    ROUND(AVG(humidity), 2) AS avg_humidity
                FROM kidbright_project
                WHERE time > NOW() - INTERVAL 24 HOUR
                GROUP BY HOUR(time)
                ORDER BY hour DESC
            """)
            rows = cs.fetchall()
    finally:
        conn.close()

    if rows:
        return [
            {
                "hour": f"{int(row[0]):02d}:00:00",
                "avg_temp": row[1],
                "avg_light": row[2],
                "avg_humidity": row[3]
            }
            for row in rows
        ]
    else:
        abort(404)


def get_api_data_avg():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT 
                    ROUND(AVG(temp), 2), 
                    ROUND(AVG(wind_kph), 2), 
                    ROUND(AVG(humidity), 2)
                FROM api_data
            """)
            row = cs.fetchone()
    finally:
        conn.close()

    return {
        "avg_temp": row[0],
        "avg_wind": row[1],
        "avg_humidity": row[2]
    }


def get_api_condition_count():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT condition, COUNT(*) 
                FROM api_data
                GROUP BY condition
                ORDER BY COUNT(*) DESC
            """)
            result = [{"condition": row[0], "count": row[1]} for row in cs.fetchall()]
    finally:
        conn.close()

    return result


def get_api_data_recent_days(days=7):
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT DATE(time) AS day,
                       ROUND(AVG(temp), 2),
                       ROUND(AVG(wind_kph), 2),
                       ROUND(AVG(humidity), 2)
                FROM api_data
                WHERE time >= NOW() - INTERVAL %s DAY
                GROUP BY day
                ORDER BY day ASC
            """, [days])
            result = [
                {
                    "day": str(row[0]),
                    "avg_temp": row[1],
                    "avg_wind": row[2],
                    "avg_humidity": row[3]
                }
                for row in cs.fetchall()
            ]
    finally:
        conn.close()

    return result

def get_api_hourly_avg():
    conn = pool.connection()
    try:
        with conn.cursor() as cs:
            cs.execute("""
                SELECT 
                    HOUR(time) AS hour,
                    ROUND(AVG(temp), 2) AS avg_temp,
                    ROUND(AVG(wind_kph), 2) AS avg_wind,
                    ROUND(AVG(humidity), 2) AS avg_humidity
                FROM api_data
                WHERE time > NOW() - INTERVAL 24 HOUR
                GROUP BY hour
                ORDER BY hour DESC
            """)
            result = [
                {
                    "hour": f"{int(row[0]):02d}:00:00",
                    "avg_temp": row[1],
                    "avg_wind": row[2],
                    "avg_humidity": row[3]
                }
                for row in cs.fetchall()
            ]
    finally:
        conn.close()

    return result



def forecast_data(column_name):
    query = f"SELECT time, {column_name} FROM kidbright_project ORDER BY time ASC"
    conn = pool.connection()
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()

    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    if column_name == 'temp':
        df = df[(df['temp'] > 10) & (df['temp'] < 45)]

    model = ARIMA(df[column_name], order=(5, 1, 0))
    model_fit = model.fit()

    forecast_steps = 14
    forecast = model_fit.forecast(steps=forecast_steps)
    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1),
                                 periods=forecast_steps, freq='D')

    result = []
    for date, value in zip(future_dates, forecast):
        result.append({
            "date": date.strftime('%Y-%m-%d'),
            f"predicted_{column_name}": round(value, 2)
        })

    return result



def forecast_temperature():
    result = forecast_data('temp')
    return jsonify(result)


def forecast_humidity():
    result = forecast_data('humidity')
    return jsonify(result)


def forecast_light():
    result = forecast_data('light')
    return jsonify(result)


def estimate_drying_time(temp, humid, wind_kph, width=2):
    try:
        drying_hours = calc_drying_hours(temp, humid, wind_kph, width)
        return jsonify({
            "estimated_drying_time_hours": drying_hours,
            "input": {
                "temp": temp,
                "humidity": humid,
                "wind_kph": wind_kph,
                "width": width
            }
        })
    except Exception as e:
        abort(400, f"Error estimating drying time: {str(e)}")


def forecast_column(df, column_name, steps=14):
    model = ARIMA(df[column_name], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast


def classify_drying_status(drying_time, weather_condition):
    weather_condition = weather_condition.lower()
    cloudy_keywords = ['cloud', 'mist', 'overcast', 'fog']
    
    is_cloudy_or_mist = any(word in weather_condition for word in cloudy_keywords)

    if drying_time <= 2:
        if is_cloudy_or_mist:
            if weather_condition == "partly cloudy":
                return "Good"
            return "Moderate"
        else:
            return "Good"
    else:
        return "Bad"
    

def predict_w_condition_next_14_days():
    conn = pool.connection()
    try:
        df = pd.read_sql("SELECT temp, wind_kph, humidity, w_condition FROM api_data", conn)
        df.dropna(inplace=True)

        le = LabelEncoder()
        df['w_condition_encoded'] = le.fit_transform(df['w_condition'])

        features = ['temp', 'wind_kph', 'humidity']
        X = df[features]
        y = df['w_condition_encoded']

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42)

        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train, y_train)

        y_pred = knn.predict(X_test)
        print("Accuracy:", round(accuracy_score(y_test, y_pred), 2))
        print(classification_report(
            y_test, y_pred,
            labels=np.unique(y),
            target_names=le.classes_,
            zero_division=0
        ))

        forecast_df = pd.read_sql(
            "SELECT time, temp, wind_kph, humidity FROM api_data ORDER BY time ASC", conn)
    finally:
        conn.close()

    forecast_df['time'] = pd.to_datetime(forecast_df['time'])
    forecast_df.set_index('time', inplace=True)

    daily_avg = forecast_df.resample('D').mean().dropna()

    forecast_days = 14
    temp_forecast = forecast_column(daily_avg, 'temp', steps=forecast_days)
    wind_forecast = forecast_column(daily_avg, 'wind_kph', steps=forecast_days)
    humidity_forecast = forecast_column(daily_avg, 'humidity', steps=forecast_days)

    last_date = daily_avg.index[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]

    future_data = pd.DataFrame({
        'date': future_dates,
        'temp': temp_forecast,
        'wind_kph': wind_forecast,
        'humidity': humidity_forecast
    })

    future_scaled = scaler.transform(future_data[['temp', 'wind_kph', 'humidity']])
    condition_preds = knn.predict(future_scaled)
    decoded_preds = le.inverse_transform(condition_preds)

    results = []
    for i in range(forecast_days):
        temp = future_data['temp'][i]
        wind_kph = future_data['wind_kph'][i]
        humidity = future_data['humidity'][i]
        weather_cond = decoded_preds[i]
        drying_time = calc_drying_hours(temp, humidity, wind_kph, width=2)
        drying_status = classify_drying_status(drying_time, weather_cond)

        results.append({
            "date": future_data['date'][i].strftime('%Y-%m-%d'),
            "temp": round(temp, 2),
            "wind_kph": round(wind_kph, 2),
            "humidity": round(humidity, 2),
            "predicted_condition": weather_cond,
            "estimated_drying_time_hours": round(drying_time, 2),
            "drying_status": drying_status
        })

    return jsonify(results)

def forecast_column_exclusive(series, steps=12):
    stepwise_model = auto_arima(
    series,
    seasonal=False,
    trace=False,
    suppress_warnings=True,
    max_p=3,
    max_q=3,
    max_d=1,
    stepwise=True
    )
    best_order = stepwise_model.order

    model = ARIMA(series, order=best_order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast


def get_api_hourly_avg_and_forecast():
    conn = pool.connection()
    try:
        df = pd.read_sql("SELECT time, temp, wind_kph, humidity FROM api_data ORDER BY time ASC", conn)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        df_hourly = df.resample('H').mean().interpolate()

        df_past_12 = df_hourly.last('12H')

        future_index = pd.date_range(start=df_hourly.index[-1] + pd.Timedelta(hours=1), periods=12, freq='H')

        forecast_temp = forecast_column_exclusive(df_hourly['temp'], steps=12)
        forecast_wind = forecast_column_exclusive(df_hourly['wind_kph'], steps=12)
        forecast_humidity = forecast_column_exclusive(df_hourly['humidity'], steps=12)

        df_forecast_12 = pd.DataFrame({
            'temp': forecast_temp,
            'wind_kph': forecast_wind,
            'humidity': forecast_humidity
        }, index=future_index)

        # Add source column to both
        df_past_12['source'] = 'actual'
        df_forecast_12['source'] = 'forecast'

        df_past_12 = df_past_12.round(2)
        df_forecast_12 = df_forecast_12.round(2)

        # Combine
        combined_df = pd.concat([df_past_12, df_forecast_12])

        # Reset index to format datetime in result
        combined_df = combined_df.reset_index().rename(columns={'index': 'datetime'})
        combined_df['datetime'] = combined_df['datetime'].dt.strftime('%H:%M')

        result = combined_df.to_dict(orient='records')
        return result

    finally:
        conn.close()


def get_kidbright_hourly_avg_and_forecast():
    conn = pool.connection()
    try:
        df = pd.read_sql("SELECT time, temp, humidity, light FROM kidbright_project ORDER BY time ASC", conn)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        df_hourly = df.resample('H').mean().interpolate()

        df_past_12 = df_hourly.last('12H')

        future_index = pd.date_range(start=df_hourly.index[-1] + pd.Timedelta(hours=1), periods=12, freq='H')

        forecast_temp = forecast_column_exclusive(df_hourly['temp'], steps=12)
        forecast_humidity = forecast_column_exclusive(df_hourly['humidity'], steps=12)
        forecast_light = forecast_column_exclusive(df_hourly['light'], steps=12)

        df_forecast_12 = pd.DataFrame({
            'temp': forecast_temp,
            'humidity': forecast_humidity,
            'light': forecast_light
        }, index=future_index)

        df_past_12['source'] = 'actual'
        df_forecast_12['source'] = 'forecast'

        df_past_12 = df_past_12.round(2)
        df_forecast_12 = df_forecast_12.round(2)

        combined_df = pd.concat([df_past_12, df_forecast_12])

        combined_df = combined_df.reset_index().rename(columns={'index': 'datetime'})
        combined_df['datetime'] = combined_df['datetime'].dt.strftime('%H:%M')

        result = combined_df.to_dict(orient='records')
        return result

    finally:
        conn.close()
