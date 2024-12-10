-- Вводить по одной в psql (в указанном порядке)

CREATE TABLE user_data (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hpsw VARCHAR(255) NOT NULL,
    is_admin INTEGER DEFAULT 0,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    description TEXT,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    location TEXT,
    event_type VARCHAR(50) NOT NULL,
    participant_limit INTEGER,
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE event_files (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    file_name VARCHAR(255) NOT NULL,
    file_data TEXT, -- Для хранения base64 изображений и других файлов
    file_type VARCHAR(50) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);