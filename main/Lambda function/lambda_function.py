import requests
import psycopg2
import os
from datetime import datetime, timedelta

# API configuration
API_KEY = os.environ["API_KEY"]
START_DATE = datetime(2025, 1, 1)
DAYS_PER_REQUEST = 7
TOTAL_WEEKS = 2

# Database credentials obtained from environment variables
DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "port": os.environ["DB_PORT"]
}

# Initialize a session for HTTP requests
session = requests.Session()

def extract():
    """Extracts asteroid IDs from NASA's NEO API"""
    all_neo_ids = []

    for i in range(TOTAL_WEEKS):
        start_date = START_DATE + timedelta(days=i * DAYS_PER_REQUEST)
        end_date = start_date + timedelta(days=DAYS_PER_REQUEST - 1)

        API_URL = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date.strftime('%Y-%m-%d')}&end_date={end_date.strftime('%Y-%m-%d')}&api_key={API_KEY}"

        try:
            response = session.get(API_URL)
            response.raise_for_status()
            data = response.json()
            for date in data["near_earth_objects"]:
                for asteroid in data["near_earth_objects"][date]:
                    all_neo_ids.append(asteroid["id"])
        except requests.RequestException as e:
            print(f"Error related to the API request: {e}")
            continue

    return all_neo_ids

def lookup_asteroid(neo_id):
    """Retrieves additional data for a specific asteroid based on its ID"""
    API_URL = f"https://api.nasa.gov/neo/rest/v1/neo/{neo_id}?api_key={API_KEY}"
    
    try:
        response = session.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error related to the API request for NEO ID {neo_id}: {e}")
        return None

def transform(neo_data_list):
    """Formats and transforms the raw asteroid data into a structured format"""
    transformed = []

    for neo in neo_data_list:
        if not neo:
            continue  

        orbital_data = neo.get("orbital_data", {})
        first_approach = neo["close_approach_data"][0] if neo["close_approach_data"] else None
        last_approach = neo["close_approach_data"][-1] if len(neo["close_approach_data"]) > 1 else first_approach

        transformed.append({
            "id": int(neo["id"]),
            "name": neo.get("name", "N/A"),
            "estimated_diameter_min_km": neo["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
            "estimated_diameter_max_km": neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
            "is_potentially_hazardous": neo.get("is_potentially_hazardous_asteroid", False),
            "first_observation_date": orbital_data.get("first_observation_date", None),
            "first_orbiting_body": first_approach["orbiting_body"] if first_approach else None,
            "first_approach_date": first_approach["close_approach_date"] if first_approach else None,
            "first_approach_kmh": float(first_approach["relative_velocity"]["kilometers_per_hour"]) if first_approach else None,
            "first_approach_miss_distance": float(first_approach["miss_distance"]["kilometers"]) if first_approach else None,
            "last_observation_date": orbital_data.get("last_observation_date", None),
            "last_orbiting_body": last_approach["orbiting_body"] if last_approach else None,
            "last_approach_date": last_approach["close_approach_date"] if last_approach else None,
            "last_approach_kmh": float(last_approach["relative_velocity"]["kilometers_per_hour"]) if last_approach else None,
            "last_approach_miss_distance": float(last_approach["miss_distance"]["kilometers"]) if last_approach else None,
            "num_approaches": len(neo["close_approach_data"])
        })

    return transformed

def load(data):
    """Loads the transformed data into the PostgreSQL database"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    sql = """
        INSERT INTO asteroids (id, name, estimated_diameter_min_km, estimated_diameter_max_km, is_potentially_hazardous,
                              first_observation_date, first_orbiting_body, first_approach_date, first_approach_kmh,
                              first_approach_miss_distance, last_observation_date, last_orbiting_body, last_approach_date,
                              last_approach_kmh, last_approach_miss_distance, num_approaches)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            estimated_diameter_min_km = EXCLUDED.estimated_diameter_min_km,
            estimated_diameter_max_km = EXCLUDED.estimated_diameter_max_km,
            is_potentially_hazardous = EXCLUDED.is_potentially_hazardous,
            first_observation_date = EXCLUDED.first_observation_date,
            first_orbiting_body = EXCLUDED.first_orbiting_body,
            first_approach_date = EXCLUDED.first_approach_date,
            first_approach_kmh = EXCLUDED.first_approach_kmh,
            first_approach_miss_distance = EXCLUDED.first_approach_miss_distance,
            last_observation_date = EXCLUDED.last_observation_date,
            last_orbiting_body = EXCLUDED.last_orbiting_body,
            last_approach_date = EXCLUDED.last_approach_date,
            last_approach_kmh = EXCLUDED.last_approach_kmh,
            last_approach_miss_distance = EXCLUDED.last_approach_miss_distance,
            num_approaches = EXCLUDED.num_approaches;
    """

    cur.executemany(sql, [
        (
            asteroid["id"], asteroid["name"], asteroid["estimated_diameter_min_km"],
            asteroid["estimated_diameter_max_km"], asteroid["is_potentially_hazardous"],
            asteroid["first_observation_date"], asteroid["first_orbiting_body"], asteroid["first_approach_date"],
            asteroid["first_approach_kmh"], asteroid["first_approach_miss_distance"],
            asteroid["last_observation_date"], asteroid["last_orbiting_body"], asteroid["last_approach_date"],
            asteroid["last_approach_kmh"], asteroid["last_approach_miss_distance"],
            asteroid["num_approaches"]
        ) for asteroid in data
    ])

    conn.commit()
    cur.close()
    conn.close()

def lambda_handler(event, context):
    """Lambda's main function"""
    try:
        asteroid_ids = extract()
        asteroid_details = [lookup_asteroid(neo_id) for neo_id in asteroid_ids]
        transformed_data = transform(asteroid_details)
        load(transformed_data)
        return {"statusCode": 200, "body": "ETL executed successfully"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
