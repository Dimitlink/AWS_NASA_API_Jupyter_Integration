CREATE TABLE asteroids (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    estimated_diameter_min_km FLOAT NOT NULL,
    estimated_diameter_max_km FLOAT NOT NULL,
    is_potentially_hazardous BOOLEAN NOT NULL,
    first_observation_date DATE,
    first_orbiting_body TEXT,
    first_approach_date DATE,
    first_approach_kmh FLOAT,
    first_approach_miss_distance FLOAT,
    last_observation_date DATE,
    last_orbiting_body TEXT,
    last_approach_date DATE,
    last_approach_kmh FLOAT,
    last_approach_miss_distance FLOAT,
    num_approaches INT NOT NULL
);
