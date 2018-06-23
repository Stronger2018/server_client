create database dict_server;
use dict_server;
create table dict(name varchar(20) not null,passwd varchar(15) default "123456",primary key(name));
desc dict;


