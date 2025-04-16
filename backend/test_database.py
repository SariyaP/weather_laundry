import unittest
import pymysql
from dbutils.pooled_db import PooledDB
import config


class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.pool = PooledDB(
            creator=pymysql,
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWD,
            database=config.DB_NAME,
            charset='utf8mb4',
            autocommit=True
        )

    def test_connection_success(self):
        conn = self.pool.connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_query_execution(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)
        conn.close()

    def test_invalid_credentials(self):
        with self.assertRaises(pymysql.err.OperationalError):
            bad_pool = PooledDB(
                creator=pymysql,
                host=config.DB_HOST,
                user="wrong_user",
                password="wrong_password",
                database=config.DB_NAME
            )
            conn = bad_pool.connection()
            conn.close()


if __name__ == '__main__':
    unittest.main()
