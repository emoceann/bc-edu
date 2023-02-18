CREATE TABLE IF NOT EXISTS "webinarroom" (
    "id" VARCHAR(1024) NOT NULL  PRIMARY KEY,
    "title" VARCHAR(2048) NOT NULL,
    "is_autowebinar" INT NOT NULL,
    "closest_date" TIMESTAMP
)