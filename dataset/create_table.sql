create table type(
    type varchar(10),
    against varchar(10),
    scale float(7, 6),
    primary key (type, against)
);

create table pokemon(
    pokemon_id int,
    pokemon_name varchar(20),
    type1 varchar(10),
    type2 varchar(10),
    rarity varchar(10),
    max_cp int,
    primary key (pokemon_id)
);

create table skill(
    pokemon_id int not null,
    skill_name varchar(30),
    primary key (pokemon_id, skill_name)
);

create table skilltype(
    name varchar(30),
    type varchar(10),
    primary key (name, type)
);

CREATE TABLE account(
    user_id varchar(20) NOT NULL UNIQUE PRIMARY KEY,
    pass_word VARCHAR(64) NOT NULL
);

create table user(
    user_id varchar(20) not null,
    pokemon_id int not null,
    pokemon_cp int not null,
    primary key (user_id, pokemon_id)
);

load data local infile './type.csv'
into table type
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile './pokemon.csv'
into table pokemon
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile './skill.csv'
into table skill
fields terminated by ','
enclosed by '"'
lines terminated by '\r\n'
ignore 1 lines;

load data local infile './skilltype.csv'
into table skilltype
fields terminated by ','
enclosed by '"'
lines terminated by '\r\n'
ignore 1 lines;
