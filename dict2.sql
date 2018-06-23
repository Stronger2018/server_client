use dict_server;
create table history(word varchar(20) not null,explaining varchar(150) not null,time datetime not null,name varchar(20) not null,foreign key(name) references dict(name));
