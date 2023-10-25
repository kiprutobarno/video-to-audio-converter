CREATE USER IF NOT EXISTS 'auth_user' @'localhost' IDENTIFIED BY "auth123";

CREATE DATABASE IF NOT EXISTS auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user' @'localhost';

USE auth;

CREATE TABLE IF NOT EXISTS users(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO
    users(username, password)
VALUES
    ('admin', 'admin123');