create table if not exists "nowpayment"(
    "payment_id" bigint not null primary key,
    "payment_status" char(10),
    "price_amount" decimal(16, 2),
    "price_currency" char(3),
    "pay_amount" decimal(16, 10),
    "pay_currency" char(6),
    "user_id" bigint not null references "user" ("id") on delete cascade,
    "created_at" timestamp not null,
    "updated_at" timestamp not null
);