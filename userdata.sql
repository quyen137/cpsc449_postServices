-- $ sqlite3 userdata.db < userdata.sql
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS userdata;
CREATE TABLE userdata (
    id INTEGER primary key,
    article VARCHAR,
    username VARCHAR,     
    community VARCHAR,  
    UNIQUE(username)
);
INSERT INTO userdata(article, username, community) VALUES('The body lay naked and facedown, a deathly gray, spatters of blood staining the snow around it.','alex', 'cpsc449');
INSERT INTO userdata(article, username, community) VALUES('a deathly gray, spatters of blood staining the snow around it.','ray','cpsc421');
INSERT INTO userdata(article, username, community) VALUES('The body lay naked and staining the snow around it.','john','cpsc421');
INSERT INTO userdata(article, username, community) VALUES('The body lay naked and , spatters of blood staining the snow around it.','kevin','cpsc449');
INSERT INTO userdata(article, username, community) VALUES('The body lay naked and facedown, a deathly gray, spatters of blood staining the snow around it.','peter','cpsc432');
INSERT INTO userdata(article, username, community) VALUES('The body lay naked and facedown,blood staining the snow around it.','ben','cpsc432');
COMMIT;
