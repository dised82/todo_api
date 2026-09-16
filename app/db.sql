-- this file is written for the psql client app for postgres sql do not use it for other clients

\c postgres 

drop database if exists to_do;
create database to_do;

\c to_do

create table users(
  id serial primary key,
  name varchar(255),
  uname varchar(25) unique,
  password_hash text not null,
  created_at timestamp default now()
);

create table list(
  id serial primary key,
  name varchar(255),
  user_id integer,
  foreign key (user_id) references users(id)
  on delete cascade
);

create table element(
  id serial primary key,
  list_id integer,
  name varchar(255),
  content text,
  state boolean,
  foreign key (list_id) references list(id)
  on delete cascade
);
