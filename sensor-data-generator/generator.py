import psycopg2
import time
import random
import os

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "sensor_data")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id SERIAL PRIMARY KEY,
                temperature FLOAT,
                humidity FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()

def insert_reading(conn, temp, humidity):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO readings (temperature, humidity) VALUES (%s, %s)", (temp, humidity))
    conn.commit()

def main():
    print("Connecting to database...")
    while True:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            create_table(conn)
            print("Connected to database. Starting data generation...")
            break
        except psycopg2.OperationalError as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    while True:
        temp = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)
        insert_reading(conn, temp, humidity)
        print(f"Inserted new reading: Temp={temp}°C, Humidity={humidity}%")
        time.sleep(10)

if __name__ == '__main__':
    main()