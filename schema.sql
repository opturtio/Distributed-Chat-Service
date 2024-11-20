CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    sender TEXT,
    created_at TIMESTAMP,
    msg TEXT
);

CREATE TABLE IF NOT EXISTS peers (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    username TEXT,
    ip TEXT,
    priority INTEGER
);
