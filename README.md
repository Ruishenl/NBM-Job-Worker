# NBM-Job-Worker

To run a simulation job, following thing is needed: 
1. Setup redis-server on the local machine 
2. Setup a db with the sql file in the `db_patches` dir 
3. Run the server and client file in the `main` dir 
4. Run the command `rq worker` to start up a tmp default redis queue worker
5. Manipulation the db is required to make the logic works. One should first
create several rows for employee and make sure the status is True

This repo is more for a high-level demonstration of the structure only; there are issues sill not being fixed yet.

ENV VAR: 
MYSQL_DB_PWD