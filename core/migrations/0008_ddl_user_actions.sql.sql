create table if not exists "useractions"(
    "user_id" bigint not null references "user" ("id") on delete cascade,
    "rank" char(10),
    "coins" integer
);
