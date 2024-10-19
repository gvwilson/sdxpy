drop table if exists person;
create table person(
    ident integer not null primary key,
    personal text not null,
    family text not null
);

insert into person(ident, personal, family) values
(14, 'Rupinder', 'Sangal'),
(18, 'Cheo', 'Liu'),
(31, 'Iskander', 'Purjant');
