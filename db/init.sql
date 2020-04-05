create database rt_share;
use rt_share;

create table servers
(
    id varchar(20)
  , ip_addr varchar(30)
  , port int

  , primary key (id)
);

create table sessions
(
    id varchar(5)
  , server_id varchar(20)

  , primary key (id)
  , foreign key (server_id) references servers (id) on delete cascade on update cascade
);

create table clients
(
    id varchar(50)
  , session_id varchar(5)

  , primary key (id, session_id)
  , foreign key (session_id) references sessions (id) on delete cascade on update cascade
);

insert into servers (id, ip_addr, port) values ('test', '172.16.100.3', 5000);
