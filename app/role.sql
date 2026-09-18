-- the following commands are to create a user and to grant him acces only to this database

-- drop the role if exists 
drop role if exists todo_conn;
-- create the role :
create role todo_conn with login password 'connexion_pass';

-- revoke all acess to the role :
do $$
declare
  r record;
begin
  for r in 
    SELECT datname FROM pg_database where not datistemplate
    loop
      execute format('revoke all privileges on database %I from todo_conn;', r.datname);
    end loop;
    rollback;
  end $$;
