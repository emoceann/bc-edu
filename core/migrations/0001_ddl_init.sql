CREATE TABLE IF NOT EXISTS utmlabeldict (
    id char(36) not null  primary key,
    source varchar(256) not null,
    medium varchar(256) not null,
    campaign varchar(256) not null,
    content int not null not null 
);

CREATE TABLE IF NOT EXISTS "user" (
    id bigint primary key,
    hash VARCHAR(255) NOT NULL,
    username VARCHAR(1024),
    full_name VARCHAR(1024),
    language_code VARCHAR(8),
    created_at TIMESTAMP with time zone NOT NULL,
    updated_at TIMESTAMP with time zone NOT NULL,
    is_admin INT NOT NULL  DEFAULT 0,
    email CHAR(255),
    phone_number CHAR(16),
    coins integer default 0,
    rank char(10) default 'Падаван',
    webinar_time TIMESTAMP,
    close INT DEFAULT 0,
    newbie int default 0,
    experienced int default 0,
    test_finished int default 0,
    knowledgebase_red int default 0
);

CREATE TABLE IF NOT EXISTS webinarroom (
    id VARCHAR(1024) NOT NULL  PRIMARY KEY,
    title VARCHAR(2048) NOT NULL,
    is_autowebinar INT NOT NULL,
    closest_date TIMESTAMP,
    original_report JSON,
    report_id char(2048)
);

CREATE TABLE IF NOT EXISTS utmlabelm2muser (
    id CHAR(36) NOT NULL  PRIMARY KEY,
    created_at TIMESTAMP with time zone NOT NULL,
    user_id BIGINT NOT NULL REFERENCES "user" (id) ON DELETE CASCADE,
    utm_label_id CHAR(36) NOT NULL REFERENCES utmlabeldict (id) ON DELETE CASCADE
);


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
