CREATE DATABASE postgres;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8'; 
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed'; 
ALTER ROLE postgres SET timezone TO 'America/New_York';
GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;
CREATE SEQUENCE video_id_seq;
CREATE TABLE video_video(
     id integer NOT NULL DEFAULT nextval('video_id_seq'),
     uuid VARCHAR(100),
     title VARCHAR(200),
     description VARCHAR(2000),
     author VARCHAR(200),
     duration FLOAT DEFAULT 0,
     aspect_ratio FLOAT DEFAULT 1,
     source VARCHAR(1200),
     extension VARCHAR(10),
     time_published TIMESTAMP,
     time_created TIMESTAMP,
     meta VARCHAR(1500)
);

INSERT INTO video_video(title,uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('First Video', 
'axax-opop-axax', 'Some Description', 'Dmitry', 1.1, 1.1, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Second Video',
'axax-opop-gxgx', 'Some Description', 'Dmitry', 1.1, 1.1, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Third Video',
'axax-opop-btbt','Some Description', 'Dmitry', 1.2, 1.2, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title,uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Fourth Video',
'axax-opop-dxdx', 'Some Description', 'Dmitry', 1.2, 1.2, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Fifth Video',
'axax-opop-aiai', 'Some Description', 'Dmitry', 1.3, 1.3, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Sixth Video',
'axax-opop-fefe','Some Description', 'Dmitry', 1.3, 1.3, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title,uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Seventh Video',
'axax-opop-efef', 'Some Description', 'Dmitry', 1.4, 1.4, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Eighth Video',
'axax-opop-dgdg', 'Some Description', 'Dmitry', 1.4, 1.4, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Ninth Video',
'axax-opop-gdgd','Some Description', 'Dmitry', 1.5, 1.5, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title,uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Tenth Video',
'axax-opop-sstt', 'Some Description', 'Dmitry', 1.5, 1.5, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Eleventh Video',
'axax-opop-ttss', 'Some Description', 'Dmitry', 1.6, 1.6, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Twelfth Video',
'axax-opop-thth','Some Description', 'Dmitry', 1.6, 1.6, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title,uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Thirteenth Video',
'axax-opop-htht', 'Some Description', 'Dmitry', 1.7, 1.7, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Fourteenth Video',
'axax-opop-gbgb', 'Some Description', 'Dmitry', 1.7, 1.7, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Fifteenth Video',
'axax-opop-bfbf','Some Description', 'Dmitry', 1.8, 1.8, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title,uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Sixteenth Video',
'axax-opop-njnj', 'Some Description', 'Dmitry', 1.8, 1.8, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Seventeenth Video',
'axax-opop-jnjn', 'Some Description', 'Dmitry', 1.9, 1.9, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Eighteenth Video',
'axax-opop-fggf','Some Description', 'Dmitry', 1.9, 1.9, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title,uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('Ninteenth Video',
'axax-opop-gffg', 'Some Description', 'Dmitry', 2.0, 2.0, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
INSERT INTO video_video(title, uuid, description, author, aspect_ratio, duration, source, extension, time_published, time_created, meta) VALUES ('20th Video',
'axax-opop-yuyu', 'Some Description', 'Dmitry', 2.0, 2.0, 'http://someplace.com', 'mpg','2016-06-22 19:10:25-07' ,'2016-06-22 19:10:25-07', 'some meta');
