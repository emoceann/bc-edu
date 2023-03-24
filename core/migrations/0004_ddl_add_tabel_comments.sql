CREATE TABLE IF NOT EXISTS "commentsnotion" (
    "page_id" uuid NOT NULL PRIMARY KEY,
    "comment_id" uuid NOT NULL,
    "message" varchar(2048) NOT NULL,
    "user_email_id" VARCHAR(255) NOT NULL REFERENCES "user" ("email") ON DELETE CASCADE
 );
