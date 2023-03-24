-- "user" definition

-- Drop table

-- DROP TABLE "user";

CREATE TABLE IF NOT EXISTS "user" (
	id bigserial NOT NULL,
	hash varchar(255) NOT NULL,
	username varchar(1024) NULL,
	full_name varchar(1024) NULL,
	created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
	language_code varchar(8) NULL,
	is_admin bool NOT NULL DEFAULT false,
	email varchar(255) NULL UNIQUE,
	phone_number varchar(16) NULL,
	webinar_time timestamptz NULL,
	test_finished bool NOT NULL DEFAULT false,
	knowledgebase_red bool NOT NULL DEFAULT false,
	newbie bool NOT NULL DEFAULT false,
	experienced bool NOT NULL DEFAULT false,
	coins int4 NOT NULL DEFAULT 0,
	"rank" varchar(10) NOT NULL DEFAULT 'Падаван'::character varying,
	CONSTRAINT user_pkey PRIMARY KEY (id)
);


-- utmlabeldict definition

-- Drop table

-- DROP TABLE utmlabeldict;

CREATE TABLE IF NOT EXISTS utmlabeldict (
	id uuid NOT NULL,
	"source" varchar(256) NOT NULL,
	medium varchar(256) NOT NULL,
	campaign varchar(256) NOT NULL,
	"content" int4 NOT NULL,
	CONSTRAINT utmlabeldict_pkey PRIMARY KEY (id)
);


-- webinarroom definition

-- Drop table

-- DROP TABLE webinarroom;

CREATE TABLE IF NOT EXISTS webinarroom (
	id varchar(1024) NOT NULL,
	title varchar(2048) NOT NULL,
	is_autowebinar bool NOT NULL,
	closest_date timestamptz NULL,
	report_id varchar(2048) NULL,
	original_report jsonb NULL,
	"close" bool NOT NULL DEFAULT false,
	CONSTRAINT webinarroom_pkey PRIMARY KEY (id)
);


-- nowpayment definition

-- Drop table

-- DROP TABLE nowpayment;

CREATE TABLE IF NOT EXISTS nowpayment (
	payment_id bigserial NOT NULL,
	payment_status varchar(10) NOT NULL,
	price_amount numeric(16, 2) NOT NULL,
	price_currency varchar(3) NOT NULL,
	pay_amount numeric(16, 10) NOT NULL,
	pay_currency varchar(6) NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	user_id int8 NOT NULL,
	CONSTRAINT nowpayment_pkey PRIMARY KEY (payment_id),
	CONSTRAINT nowpayment_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);


-- utmlabelm2muser definition

-- Drop table

-- DROP TABLE utmlabelm2muser;

CREATE TABLE IF NOT EXISTS utmlabelm2muser (
	id uuid NOT NULL,
	created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
	user_id int8 NOT NULL,
	utm_label_id uuid NOT NULL,
	CONSTRAINT utmlabelm2muser_pkey PRIMARY KEY (id),
	CONSTRAINT utmlabelm2muser_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
	CONSTRAINT utmlabelm2muser_utm_label_id_fkey FOREIGN KEY (utm_label_id) REFERENCES utmlabeldict(id) ON DELETE CASCADE
);
