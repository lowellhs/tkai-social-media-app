CREATE SCHEMA tkai_2019;

SET search_path TO tkai_2019;

CREATE TABLE Follow (
    usernameX VARCHAR(120) NOT NULL,
    usernameY VARCHAR(120) NOT NULL,
    PRIMARY KEY (usernameX, usernameY)
);

CREATE TABLE Pengguna (
    username VARCHAR (120) NOT NULL,
    password VARCHAR (200) NOT NULL,
    fullname VARCHAR (100) NOT NULL,
    email VARCHAR (200) NOT NULL,
    profile_pict VARCHAR (200) NULL,
    PRIMARY KEY (username)
);

CREATE TABLE Tweet (
    tweet_id SERIAL,
    username VARCHAR(200) NOT NULL,
    text VARCHAR(750) NOT NULL,
    create_time VARCHAR(100) NULL,
    update_time VARCHAR(100) NULL,
    flag_view INT NOT NULL,
    PRIMARY KEY (tweet_id)
);