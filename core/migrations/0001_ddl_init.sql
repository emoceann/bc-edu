CREATE TABLE IF NOT EXISTS "utmlabeldict" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "source" VARCHAR(256) NOT NULL,
    "medium" VARCHAR(256) NOT NULL,
    "campaign" VARCHAR(256) NOT NULL,
    "content" INT NOT NULL
);

CREATE TABLE IF NOT EXISTS "user" (
    "id" integer primary key,
    "hash" VARCHAR(255) NOT NULL,
    "username" VARCHAR(1024),
    "full_name" VARCHAR(1024),
    "language_code" VARCHAR(8),
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);