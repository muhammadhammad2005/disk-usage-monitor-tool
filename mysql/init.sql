CREATE DATABASE IF NOT EXISTS alnafi;

CREATE USER IF NOT EXISTS 'mysql_user'@'%' IDENTIFIED BY 'test123';
GRANT ALL PRIVILEGES ON alnafi.* TO 'mysql_user'@'%';
FLUSH PRIVILEGES;

USE alnafi;

CREATE TABLE IF NOT EXISTS my_df_data (
    filesystem VARCHAR(255),
    size VARCHAR(50),
    used VARCHAR(50),
    avail VARCHAR(50),
    usage_with_per INT,
    mounted_on VARCHAR(255),
    datetime VARCHAR(50),
    ip_address VARCHAR(50),
    hostname VARCHAR(100)
);
