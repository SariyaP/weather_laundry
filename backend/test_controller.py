import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from controller import *
from swagger_server import models
import werkzeug


class TestController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('controller.pool')
    def test_get_latest_kidbright_data_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (
            1, '2025-04-15 18:00:00', 25.5, 600.0, 70.0)
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_latest_kidbright_data()
        self.assertIsInstance(result, models.KidbrightData)
        self.assertEqual(result.id, 1)
        self.assertEqual(str(result.time), '2025-04-15 18:00:00')
        self.assertEqual(result.temp, 25.5)
        self.assertEqual(result.light, 600.0)
        self.assertEqual(result.humidity, 70.0)

    @patch('controller.pool')
    def test_get_latest_kidbright_data_not_found(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        with self.assertRaises(werkzeug.exceptions.NotFound):
            get_latest_kidbright_data()

    @patch('controller.pool')
    def test_get_kidbright_data_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            (1, '2025-04-15 18:00:00', 25.5, 600.0, 70.0),
            (2, '2025-04-15 17:00:00', 26.0, 650.0, 72.0)
        ]
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_data()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], models.KidbrightData)
        self.assertEqual(result[0].id, 1)

    @patch('controller.pool')
    def test_get_kidbright_by_timerange_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            (1, '2025-04-15 10:00:00', 24.0, 550.0, 65.0),
            (2, '2025-04-15 11:00:00', 24.5, 580.0, 68.0)
        ]
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_by_timerange('2025-04-15 09:00:00',
                                            '2025-04-15 12:00:00')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], models.KidbrightData)

    @patch('controller.pool')
    def test_get_api_data_latest_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (
            1, '2025-04-15 18:00:00', 32.0, 15.5, 80.0, 'Clear')
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_api_data_latest()
        self.assertIsInstance(result, models.ApiData)
        self.assertEqual(result.id, 1)

    @patch('controller.pool')
    def test_get_api_data_latest_not_found(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        with self.assertRaises(werkzeug.exceptions.NotFound):
            get_api_data_latest()

    @patch('controller.pool')
    def test_get_api_data_by_id_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (
            1, '2025-04-15 18:00:00', 32.0, 15.5, 80.0, 'Clear')
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_api_data_by_id(1)
        self.assertIsInstance(result, models.ApiData)
        self.assertEqual(result.id, 1)

    @patch('controller.pool')
    def test_get_api_data_by_id_not_found(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = None
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        with self.assertRaises(werkzeug.exceptions.NotFound):
            get_api_data_by_id(99)

    @patch('controller.pool')
    def test_get_api_data_by_timerange_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            (1, '2025-04-15 10:00:00', 30.0, 10.0, 75.0, 'Cloudy'),
            (2, '2025-04-15 11:00:00', 31.0, 12.0, 78.0, 'Partly Cloudy')
        ]
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_api_data_by_timerange('2025-04-15 09:00:00',
                                           '2025-04-15 12:00:00')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], models.ApiData)

    @patch('controller.pool')
    def test_insert_api_data_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = insert_api_data(33.0, 18.0, 82.0, 'Rain')
        self.assertEqual(result,
                         {"status": "success", "message": "API data inserted"})
        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO api_data (time, temp, wind_kph, humidity, condition)
            VALUES (NOW(), %s, %s, %s, %s)
        """, [33.0, 18.0, 82.0, 'Rain'])
        mock_conn.commit.assert_called_once()

    @patch('controller.pool')
    def test_get_kidbright_avg_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (26.5, 620.0, 71.0)
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_avg()
        self.assertEqual(result, {
            "avg_temp": 26.5,
            "avg_light": 620.0,
            "avg_humidity": 71.0
        })

    @patch('controller.pool')
    def test_get_kidbright_avg_no_data(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (None, None, None)
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_avg()
        self.assertEqual(result, {
            "avg_temp": None,
            "avg_light": None,
            "avg_humidity": None
        })

    @patch('controller.pool')
    def test_get_kidbright_min_max_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (
            20.0, 30.0, 500.0, 700.0, 60.0, 80.0)
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_min_max()
        self.assertEqual(result, {
            "min_temp": 20.0,
            "max_temp": 30.0,
            "min_light": 500.0,
            "max_light": 700.0,
            "min_humidity": 60.0,
            "max_humidity": 80.0
        })

    @patch('controller.pool')
    def test_get_kidbright_min_max_no_data(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (None,) * 6
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_min_max()
        self.assertEqual(result, {
            "min_temp": None,
            "max_temp": None,
            "min_light": None,
            "max_light": None,
            "min_humidity": None,
            "max_humidity": None
        })

    @patch('controller.pool')
    def test_get_kidbright_hourly_average_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = [
            (10, 25.0, 600.0, 70.0),
            (11, 26.0, 650.0, 72.0)
        ]
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_hourly_average()
        self.assertEqual(result, [
            {"hour": 10, "avg_temp": 25.0, "avg_light": 600.0,
             "avg_humidity": 70.0},
            {"hour": 11, "avg_temp": 26.0, "avg_light": 650.0,
             "avg_humidity": 72.0}
        ])

    @patch('controller.pool')
    def test_get_kidbright_hourly_average_no_data(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchall.return_value = []
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_kidbright_hourly_average()
        self.assertEqual(result, [])

    @patch('controller.pool')
    def test_get_api_data_avg_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (31.5, 16.0, 79.0)
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_api_data_avg()
        self.assertEqual(result, {
            "avg_temp": 31.5,
            "avg_wind": 16.0,
            "avg_humidity": 79.0
        })

    @patch('controller.pool')
    def test_get_api_data_avg_no_data(self, mock_pool):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (None, None, None)
        mock_pool.connection.return_value.__enter__.return_value = mock_conn

        result = get_api_data_avg()
