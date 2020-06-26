CREATE SCHEMA `nextbee_media_job` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin ;

CREATE TABLE job
(job_id int NOT NULL PRIMARY KEY,
 job_desc char,
 hrs_required float NOT NULL,
 assignee char,
 status bool);

CREATE TABLE employee
(employee_id int NOT NULL PRIMARY KEY,
 available_hrs float NOT NULL,
 job_id int,
 status bool);
