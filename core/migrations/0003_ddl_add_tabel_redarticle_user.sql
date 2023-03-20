create table if not exists "redarticleuser"(
    user int8 NOT NULL,
    article_title varchar(64),
    constraint redarticleuser_user_fkey foreign key (user) references "user"(id) on delete cascade
);