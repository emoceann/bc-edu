CREATE TABLE IF NOT EXISTS utmlabeldict (
    id char(36) not null  primary key,
    source varchar(256) not null,
    medium varchar(256) not null,
    campaign varchar(256) not null,
    content int not null not null 
);

CREATE TABLE IF NOT EXISTS "user" (
    id integer primary key,
    hash VARCHAR(255) NOT NULL,
    username VARCHAR(1024),
    full_name VARCHAR(1024),
    language_code VARCHAR(8),
    created_at TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);

alter table "user" add column is_admin INT NOT NULL  DEFAULT 0;

CREATE TABLE IF NOT EXISTS webinarroom (
    id VARCHAR(1024) NOT NULL  PRIMARY KEY,
    title VARCHAR(2048) NOT NULL,
    is_autowebinar INT NOT NULL,
    closest_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS utmlabelm2muser (
    id CHAR(36) NOT NULL  PRIMARY KEY,
    created_at TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    user_id BIGINT NOT NULL REFERENCES "user" (id) ON DELETE CASCADE,
    utm_label_id CHAR(36) NOT NULL REFERENCES utmlabeldict (id) ON DELETE CASCADE
);

alter table "user" add column email CHAR(255);
alter table "user" add column phone_number CHAR(16);


create table if not exists nowpayment(
    payment_id bigint not null primary key,
    payment_status char(10),
    price_amount decimal(16, 2),
    price_currency char(3),
    pay_amount decimal(16, 10),
    pay_currency char(6),
    user_id bigint not null references "user" (id) on delete cascade,
    created_at timestamp not null,
    updated_at timestamp not null
);


alter table "user" add column coins integer default 0;
alter table "user" add column rank char(10) default 'Падаван';

alter table "user" add column webinar_time TIMESTAMP;

alter table webinarroom add column original_report JSON;
alter table webinarroom add column close INT DEFAULT 0;


alter table "user" add column newbie int default 0;
alter table "user" add column experienced int default 0;
alter table "user" add column test_finished int default 0;
alter table "user" add column knowledgebase_red int default 0;

alter table webinarroom add column report_id char(2048);