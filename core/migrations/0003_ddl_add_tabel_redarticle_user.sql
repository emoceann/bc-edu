CREATE TABLE IF NOT EXISTS "redarticleuser" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "article_id" INT NOT NULL,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
 );