BEGIN;

CREATE SEQUENCE seq1
START 1 INCREMENT BY 1 NO MAXVALUE CACHE 1;

CREATE SEQUENCE seq2
START 1 INCREMENT BY 1 NO MAXVALUE CACHE 1;

CREATE SEQUENCE seq5
START 1 INCREMENT BY 1 NO MAXVALUE CACHE 1;

CREATE SEQUENCE seq3
START 1 INCREMENT BY 1 NO MAXVALUE CACHE 1;

CREATE SEQUENCE seq4
START 1 INCREMENT BY 1 NO MAXVALUE CACHE 1;


CREATE TABLE users (
id integer PRIMARY KEY DEFAULT nextval('seq2'),
name varchar(50)
);

CREATE TABLE category(
id integer PRIMARY KEY DEFAULT nextval('seq3'),
name varchar(40),
cat_id integer references category(id)
);

CREATE TABLE item_detail(
id integer PRIMARY KEY DEFAULT nextval('seq4'),
name varchar(255),
date_s date,
user_id int references users(id),
cat_id int references category(id)
);

CREATE TABLE raf_item(
id integer PRIMARY KEY DEFAULT nextval('seq1'),
item_id integer,
url varchar,
content varchar,
creation date
);

CREATE TABLE item(
id integer PRIMARY KEY DEFAULT nextval('seq5'),
itemdet_id integer references item_detail(id),
raf_item integer references raf_item(id)
);
END;
