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
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMA

from config import *
from dry_estimator import calc_drying_hours

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


def get_connection():
    return pool.connection()


def get_latest_kidbright_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, time, temp, light, humidity
            FROM kidbright_project
            ORDER BY time DESC
            LIMIT 1
        """)
        result = cs.fetchone()
    if result:
        return models.KidbrightData(*result)
    else:
        abort(404)


def get_kidbright_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, time, temp, light, humidity 
            FROM kidbright_project 
            ORDER BY time DESC 
            LIMIT 50
        """)
        return [models.KidbrightData(*row) for row in cs.fetchall()]


def get_kidbright_by_id(data_id):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, time, temp, light, humidity 
            FROM kidbright_project 
            WHERE id = %s
        """, [data_id])
        row = cs.fetchone()
        if row:
            return models.KidbrightData(*row)
        else:
            abort(404)


def get_kidbright_by_timerange(start, end):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, time, temp, light, humidity 
            FROM kidbright_project 
            WHERE time BETWEEN %s AND %s 
            ORDER BY time ASC
        """, [start, end])
        return [models.KidbrightData(*row) for row in cs.fetchall()]


def insert_kidbright_data(temp, light, humidity):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            INSERT INTO kidbright_project (time, temp, light, humidity)
            VALUES (NOW(), %s, %s, %s)
        """, [temp, light, humidity])
        conn.commit()
        return {"status": "success", "message": "Data inserted"}


def get_api_data_latest():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, time, temp, wind_kph, humidity, condition 
            FROM api_data 
            ORDER BY time DESC 
            LIMIT 1
        """)
        row = cs.fetchone()
        if row:
            return models.ApiData(*row)
        else:
            abort(404)


def get_api_data_by_id(data_id):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, time, temp, wind_kph, humidity, condition 
            FROM api_data 
            WHERE id = %s
        """, [data_id])
        row = cs.fetchone()
        if row:
            return models.ApiData(*row)
        else:
            abort(404)


def get_api_data_by_timerange(start, end):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, time, temp, wind_kph, humidity, condition 
            FROM api_data 
            WHERE time BETWEEN %s AND %s 
            ORDER BY time ASC
        """, [start, end])
        return [models.ApiData(*row) for row in cs.fetchall()]


def insert_api_data(temp, wind_kph, humidity, condition):
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            INSERT INTO api_data (time, temp, wind_kph, humidity, condition)
            VALUES (NOW(), %s, %s, %s, %s)
        """, [temp, wind_kph, humidity, condition])
        conn.commit()
        return {"status": "success", "message": "API data inserted"}


def get_kidbright_avg():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT 
                ROUND(AVG(temp), 2), 
                ROUND(AVG(light), 2), 
                ROUND(AVG(humidity), 2)
            FROM kidbright_project
        """)
        row = cs.fetchone()
        return {
            "avg_temp": row[0],
            "avg_light": row[1],
            "avg_humidity": row[2]
        }


def get_kidbright_min_max():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT 
                MIN(temp), MAX(temp), 
                MIN(light), MAX(light), 
                MIN(humidity), MAX(humidity)
            FROM kidbright_project
        """)
        row = cs.fetchone()
        return {
            "min_temp": row[0],
            "max_temp": row[1],
            "min_light": row[2],
            "max_light": row[3],
            "min_humidity": row[4],
            "max_humidity": row[5]
        }


def get_kidbright_hourly_average():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT 
                HOUR(time) AS hour,
                ROUND(AVG(temp), 2),
                ROUND(AVG(light), 2),
                ROUND(AVG(humidity), 2)
            FROM kidbright_project
            GROUP BY HOUR(time)
            ORDER BY hour
        """)
        return [
            {
                "hour": row[0],
                "avg_temp": row[1],
                "avg_light": row[2],
                "avg_humidity": row[3]
            }
            for row in cs.fetchall()
        ]


def get_api_data_avg():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT 
                ROUND(AVG(temp), 2), 
                ROUND(AVG(wind_kph), 2), 
                ROUND(AVG(humidity), 2)
            FROM api_data
        """)
        row = cs.fetchone()
        return {
            "avg_temp": row[0],
            "avg_wind": row[1],
            "avg_humidity": row[2]
        }


def get_api_condition_count():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT condition, COUNT(*) 
            FROM api_data
            GROUP BY condition
            ORDER BY COUNT(*) DESC
        """)
        return [
            {"condition": row[0], "count": row[1]}
            for row in cs.fetchall()
        ]


def get_api_data_recent_days(days=7):
    with pool.connection() as conn, conn.cursor() as cs:
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
        return [
            {
                "day": str(row[0]),
                "avg_temp": row[1],
                "avg_wind": row[2],
                "avg_humidity": row[3]
            }
            for row in cs.fetchall()
        ]


def forecast_data(column_name):
    password = DB_PASSWD
    encoded_password = quote_plus(password)
    engine = create_engine(
        f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}')
    query = f"SELECT time, {column_name} FROM kidbright_project ORDER BY time ASC"
    df = pd.read_sql(query, engine)

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


def predict_w_condition_next_14_days():
    encoded_password = quote_plus(DB_PASSWD)
    engine = create_engine(
        f'mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}')
    query = "SELECT temp, wind_kph, humidity, w_condition FROM api_data"
    df = pd.read_sql(query, engine)
    df.dropna(inplace=True)
    le = LabelEncoder()
    df['w_condition_encoded'] = le.fit_transform(df['w_condition'])
    features = ['temp', 'wind_kph', 'humidity']
    X = df[features]
    y = df['w_condition_encoded']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y,
                                                        test_size=0.2,
                                                        random_state=42)
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
    forecast_query = "SELECT time, temp, wind_kph, humidity FROM api_data ORDER BY time ASC"
    forecast_df = pd.read_sql(forecast_query, engine)
    forecast_df['time'] = pd.to_datetime(forecast_df['time'])
    forecast_df.set_index('time', inplace=True)
    daily_avg = forecast_df.resample('D').mean().dropna()
    forecast_days = 14
    temp_forecast = forecast_column(daily_avg, 'temp', steps=forecast_days)
    wind_forecast = forecast_column(daily_avg, 'wind_kph', steps=forecast_days)
    humidity_forecast = forecast_column(daily_avg, 'humidity',
                                        steps=forecast_days)
    last_date = daily_avg.index[-1]
    future_dates = [last_date + timedelta(days=i) for i in
                    range(1, forecast_days + 1)]

    future_data = pd.DataFrame({
        'date': future_dates,
        'temp': temp_forecast,
        'wind_kph': wind_forecast,
        'humidity': humidity_forecast
    })

    future_scaled = scaler.transform(
        future_data[['temp', 'wind_kph', 'humidity']])

    condition_preds = knn.predict(future_scaled)
    decoded_preds = le.inverse_transform(condition_preds)

    results = []
    for i in range(forecast_days):
        results.append({
            "date": future_data['date'][i].strftime('%Y-%m-%d'),
            "temp": round(future_data['temp'][i], 2),
            "wind_kph": round(future_data['wind_kph'][i], 2),
            "humidity": round(future_data['humidity'][i], 2),
            "predicted_condition": decoded_preds[i]
        })

    return jsonify(results)

