import json
import random
import time
from datetime import datetime
import psycopg2

DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'saisindhu2005'
DB_HOST = 'finalproject.cjmiqqig0kbt.us-east-1.rds.amazonaws.com'
DB_PORT = '5432'


try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("Connection to the database established successfully.")
except psycopg2.Error as err:
    print(f"Error: {err}")
    exit(1)

def create_tables():
    create_traffic_flow_table = """
    CREATE TABLE IF NOT EXISTS traffic_flow (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ NOT NULL,
        location_id INT NOT NULL,
        vehicle_count INT NOT NULL,
        average_speed NUMERIC(5,2) NOT NULL,
        traffic_density NUMERIC(5,2) NOT NULL
    );
    """
    create_air_quality_table = """
    CREATE TABLE IF NOT EXISTS air_quality (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ NOT NULL,
        location_id INT NOT NULL,
        PM2_5 NUMERIC(5,2) NOT NULL,
        PM10 NUMERIC(5,2) NOT NULL,
        NO2 NUMERIC(5,2) NOT NULL,
        SO2 NUMERIC(5,2) NOT NULL,
        CO NUMERIC(5,2) NOT NULL,
        O3 NUMERIC(5,2) NOT NULL,
        AQI INT NOT NULL
    );
    """
    create_energy_consumption_table = """
    CREATE TABLE IF NOT EXISTS energy_consumption (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ NOT NULL,
        location_id INT NOT NULL,
        household_energy_usage NUMERIC(5,2) NOT NULL,
        commercial_energy_usage NUMERIC(5,2) NOT NULL,
        industrial_energy_usage NUMERIC(5,2) NOT NULL,
        solar_energy_generated NUMERIC(5,2) NOT NULL,
        wind_energy_generated NUMERIC(5,2) NOT NULL
    );
    """
    create_waste_management_table = """
    CREATE TABLE IF NOT EXISTS waste_management (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ NOT NULL,
        location_id INT NOT NULL,
        waste_collected NUMERIC(5,2) NOT NULL,
        recycled_waste NUMERIC(5,2) NOT NULL,
        organic_waste NUMERIC(5,2) NOT NULL,
        hazardous_waste NUMERIC(5,2) NOT NULL
    );
    """
    cur.execute(create_traffic_flow_table)
    cur.execute(create_air_quality_table)
    cur.execute(create_energy_consumption_table)
    cur.execute(create_waste_management_table)
    conn.commit()

def generate_traffic_flow_data():
    record = (
        datetime.now(),
        random.randint(1, 10),
        random.randint(0, 100),
        round(random.uniform(20, 80), 2),
        round(random.uniform(0.1, 1.0), 2)
    )
    return record

def generate_air_quality_data():
    record = (
        datetime.now(),
        random.randint(1, 10),
        round(random.uniform(0, 150), 2),
        round(random.uniform(0, 200), 2),
        round(random.uniform(0, 100), 2),
        round(random.uniform(0, 50), 2),
        round(random.uniform(0, 10), 2),
        round(random.uniform(0, 200), 2),
        random.randint(0, 500)
    )
    return record

def generate_energy_consumption_data():
    record = (
        datetime.now(),
        random.randint(1, 10),
        round(random.uniform(0, 5), 2),
        round(random.uniform(0, 20), 2),
        round(random.uniform(0, 50), 2),
        round(random.uniform(0, 10), 2),
        round(random.uniform(0, 15), 2)
    )
    return record

def generate_waste_management_data():
    record = (
        datetime.now(),
        random.randint(1, 10),
        round(random.uniform(0, 100), 2),
        round(random.uniform(0, 50), 2),
        round(random.uniform(0, 30), 2),
        round(random.uniform(0, 10), 2)
    )
    return record

def send_data_to_rds(data, table_name, columns):
    sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
    cur.execute(sql, data)
    conn.commit()

def simulate_real_time_data():
    while True:
        data_type = random.choice(["traffic_flow", "air_quality", "energy_consumption", "waste_management"])
        if data_type == "traffic_flow":
            data = generate_traffic_flow_data()
            send_data_to_rds(data, 'traffic_flow', ['timestamp', 'location_id', 'vehicle_count', 'average_speed', 'traffic_density'])
        elif data_type == "air_quality":
            data = generate_air_quality_data()
            send_data_to_rds(data, 'air_quality', ['timestamp', 'location_id', 'PM2_5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'AQI'])
        elif data_type == "energy_consumption":
            data = generate_energy_consumption_data()
            send_data_to_rds(data, 'energy_consumption', ['timestamp', 'location_id', 'household_energy_usage', 'commercial_energy_usage', 'industrial_energy_usage', 'solar_energy_generated', 'wind_energy_generated'])
        else:
            data = generate_waste_management_data()
            send_data_to_rds(data, 'waste_management', ['timestamp', 'location_id', 'waste_collected', 'recycled_waste', 'organic_waste', 'hazardous_waste'])
        
        print(json.dumps(data, default=str))  
        time.sleep(random.uniform(0.5, 2))  

if __name__ == "__main__":
    try:
        create_tables()
        simulate_real_time_data()
    except KeyboardInterrupt:
        cur.close()
        conn.close()
