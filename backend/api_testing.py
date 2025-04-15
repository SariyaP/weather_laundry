import unittest
import requests
import json
from datetime import datetime, timedelta

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8080/laundry-api/v1"  # Adjust if your Flask app runs on a different port

# --- Helper Function ---
def assert_json_response(test_case, response, status_code=200):
    test_case.assertEqual(response.status_code, status_code)
    test_case.assertEqual(response.headers.get('Content-Type'), 'application/json')
    try:
        return response.json()
    except json.JSONDecodeError:
        test_case.fail("Response is not valid JSON")
        return None

# --- API Test Suite ---
class ApiEndpointsTest(unittest.TestCase):

    # Helper function to insert test data (for integration tests)
    def _insert_kidbright_data(self, temp, light, humidity):
        data = {"temp": temp, "light": light, "humidity": humidity}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/kidbright", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def _insert_api_weather_data(self, temp, wind_kph, humidity, condition):
        data = {"temp": temp, "wind_kph": wind_kph, "humidity": humidity, "condition": condition}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/api_data", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    # --- Kidbright Data Endpoints ---
    def test_get_latest_kidbright_data(self):
        response = requests.get(f"{BASE_URL}/kidbright/latest")
        assert_json_response(self, response)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("time", data)
        self.assertIn("temp", data)
        self.assertIn("light", data)
        self.assertIn("humidity", data)

    def test_get_kidbright_data(self):
        response = requests.get(f"{BASE_URL}/kidbright")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertLessEqual(len(data), 50)
            self.assertIn("id", data[0])
            self.assertIn("time", data[0])
            self.assertIn("temp", data[0])
            self.assertIn("light", data[0])
            self.assertIn("humidity", data[0])

    def test_get_kidbright_by_id_success(self):
        # Assuming there's at least one entry, you might need to insert one for a reliable test
        latest_response = requests.get(f"{BASE_URL}/kidbright/latest")
        if latest_response.status_code == 200:
            latest_data = latest_response.json()
            data_id = latest_data["id"]
            response = requests.get(f"{BASE_URL}/kidbright/{data_id}")
            assert_json_response(self, response)
            data = response.json()
            self.assertEqual(data["id"], data_id)
        else:
            self.skipTest("No Kidbright data available to test get by ID")

    def test_get_kidbright_by_id_not_found(self):
        response = requests.get(f"{BASE_URL}/kidbright/999999") # Assuming this ID doesn't exist
        self.assertEqual(response.status_code, 404)

    def test_get_kidbright_by_timerange(self):
        now = datetime.now()
        start_time = (now - timedelta(hours=1)).isoformat()
        end_time = now.isoformat()
        response = requests.get(f"{BASE_URL}/kidbright/range?start={start_time}&end={end_time}")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("time", data[0])
            # Further assertions on the time range can be added

    def test_insert_kidbright_data(self):
        data = {"temp": 28.5, "light": 70.2, "humidity": 62.1}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/kidbright", json=data, headers=headers)
        assert_json_response(self, response)
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["message"], "Data inserted")

    # --- API Data Endpoints ---
    def test_get_api_data_latest(self):
        response = requests.get(f"{BASE_URL}/api_data/latest")
        assert_json_response(self, response)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("time", data)
        self.assertIn("temp", data)
        self.assertIn("wind_kph", data)
        self.assertIn("humidity", data)
        self.assertIn("condition", data)

    def test_get_api_data_by_id_success(self):
        latest_response = requests.get(f"{BASE_URL}/api_data/latest")
        if latest_response.status_code == 200:
            latest_data = latest_response.json()
            data_id = latest_data["id"]
            response = requests.get(f"{BASE_URL}/api_data/{data_id}")
            assert_json_response(self, response)
            data = response.json()
            self.assertEqual(data["id"], data_id)
        else:
            self.skipTest("No API data available to test get by ID")

    def test_get_api_data_by_id_not_found(self):
        response = requests.get(f"{BASE_URL}/api_data/999999") # Assuming this ID doesn't exist
        self.assertEqual(response.status_code, 404)

    def test_get_api_data_by_timerange(self):
        now = datetime.now()
        start_time = (now - timedelta(hours=1)).isoformat()
        end_time = now.isoformat()
        response = requests.get(f"{BASE_URL}/api_data/range?start={start_time}&end={end_time}")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("time", data[0])

    def test_insert_api_data(self):
        data = {"temp": 32.1, "wind_kph": 5.6, "humidity": 75.3, "condition": "Cloudy"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/api_data", json=data, headers=headers)
        assert_json_response(self, response)
        response_data = response.json()
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(response_data["message"], "API data inserted")

    # --- Aggregation Endpoints ---
    def test_get_kidbright_avg(self):
        response = requests.get(f"{BASE_URL}/kidbright/avg")
        assert_json_response(self, response)
        data = response.json()
        self.assertIn("avg_temp", data)
        self.assertIn("avg_light", data)
        self.assertIn("avg_humidity", data)

    def test_get_kidbright_min_max(self):
        response = requests.get(f"{BASE_URL}/kidbright/minmax")
        assert_json_response(self, response)
        data = response.json()
        self.assertIn("min_temp", data)
        self.assertIn("max_temp", data)
        self.assertIn("min_light", data)
        self.assertIn("max_light", data)
        self.assertIn("min_humidity", data)
        self.assertIn("max_humidity", data)

    def test_get_kidbright_hourly_average(self):
        response = requests.get(f"{BASE_URL}/kidbright/hourlyaverage")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("hour", data[0])
            self.assertIn("avg_temp", data[0])
            self.assertIn("avg_light", data[0])
            self.assertIn("avg_humidity", data[0])

    def test_get_api_data_avg(self):
        response = requests.get(f"{BASE_URL}/api_data/avg")
        assert_json_response(self, response)
        data = response.json()
        self.assertIn("avg_temp", data)
        self.assertIn("avg_wind", data)
        self.assertIn("avg_humidity", data)

    def test_get_api_data_recent_days(self):
        response = requests.get(f"{BASE_URL}/api_data/recent_days")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("day", data[0])
            self.assertIn("avg_temp", data[0])
            self.assertIn("avg_wind", data[0])
            self.assertIn("avg_humidity", data[0])

    # --- Forecast Endpoints ---
    def test_forecast_temperature(self):
        response = requests.get(f"{BASE_URL}/forecast/temperature")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("date", data[0])
            self.assertIn("predicted_temp", data[0])

    def test_forecast_humidity(self):
        response = requests.get(f"{BASE_URL}/forecast/humidity")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("date", data[0])
            self.assertIn("predicted_humidity", data[0])

    def test_forecast_light(self):
        response = requests.get(f"{BASE_URL}/forecast/light")
        assert_json_response(self, response)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("date", data[0])
            self.assertIn("predicted_light", data[0])

# --- Integration Test Suite ---
class IntegrationTest(unittest.TestCase):

    def test_kidbright_data_insertion_and_retrieval(self):
        # 1. Insert Kidbright data via the API
        test_data = {"temp": 27.0, "light": 65.5, "humidity": 70.0}
        headers = {"Content-Type": "application/json"}
        insert_response = requests.post(f"{BASE_URL}/kidbright", json=test_data, headers=headers)
        assert_json_response(self, insert_response, 200)
        insert_result = insert_response.json()
        self.assertEqual(insert_result["status"], "success")

        # 2. Retrieve the latest data and verify the inserted values
        latest_response = requests.get(f"{BASE_URL}/kidbright/latest")
        assert_json_response(self, latest_response)
        latest_data = latest_response.json()
        self.assertEqual(float(latest_data["temp"]), test_data["temp"])
        self.assertEqual(float(latest_data["light"]), test_data["light"])
        self.assertEqual(float(latest_data["humidity"]), test_data["humidity"])

    def test_api_data_insertion_and_timerange_retrieval(self):
        # 1. Insert API weather data
        test_data = {"temp": 33.5, "wind_kph": 4.2, "humidity": 68.0, "condition": "Partly Cloudy"}
        headers = {"Content-Type": "application/json"}
        insert_response = requests.post(f"{BASE_URL}/api_data", json=test_data, headers=headers)
        assert_json_response(self, insert_response, 200)
        insert_result = insert_response.json()
        self.assertEqual(insert_result["status"], "success")

        # 2. Retrieve data within a recent timerange and check for the inserted data
        now = datetime.now()
        start_time = (now - timedelta(minutes=5)).isoformat()
        end_time = now.isoformat()
        range_response = requests.get(f"{BASE_URL}/api_data/range?start={start_time}&end={end_time}")
        assert_json_response(self, range_response)
        range_data = range_response.json()
        found = False
        for item in range_data:
            if float(item.get("temp", -99)) == test_data["temp"] and \
               float(item.get("wind_kph", -99)) == test_data["wind_kph"] and \
               float(item.get("humidity", -99)) == test_data["humidity"] and \
               item.get("condition") == test_data["condition"]:
                found = True
                break
        self.assertTrue(found, "Inserted API data not found within the time range")

    # Add more integration tests to cover interactions between different parts of your application
    # For example, if there's a process that uses Kidbright data to trigger an action via another API.

if __name__ == '__main__':
    unittest.main()