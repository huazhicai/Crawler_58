drop table exists `zjtb_kefu`;

create table `zjtb_kefu`(
id int(11) unsigned not null auto_increment,
title varchar(128) null,
salary varchar(128) null,
company varchar(128) null,
scale varchar(255) null,
industry varchar(255) null,
contacts varchar(255) null,
phone  varchar(255) null,
website varchar(255) null,
address varchar(255) null,
primary key (`id`),
unique key (`website`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;