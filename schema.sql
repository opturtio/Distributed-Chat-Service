CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    msg TEXT
);

CREATE TABLE IF NOT EXISTS peers (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    name TEXT,
    ip TEXT
);
