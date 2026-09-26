-- this file is written for the psql client app for postgres sql do not use it for other clients

\c postgres 

drop database if exists to_do;
create database to_do;

\c to_do

-- grant privileges to the role we created with  the script role.sql
-- for the existing tables :
grant select, insert, update, delete
on all tables in schema public
to todo_conn;

grant usage, select 
on all sequences in schema public
to todo_conn;

-- for the future tables :
alter default privileges in schema public
grant select, insert, update, delete  on tables 
to todo_conn;

alter default privileges in schema public
grant usage, select on sequences
to todo_conn;

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
