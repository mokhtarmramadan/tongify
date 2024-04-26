CREATE DATABASE IF NOT EXISTS tongify_db;
CREATE USER IF NOT EXISTS 'tongify_dev'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON tongify_db.* TO 'tongify_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'tongify_dev'@'localhost';
