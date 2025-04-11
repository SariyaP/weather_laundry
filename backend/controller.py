import sys
from flask import abort
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

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

