drop table if exists beacon;
create table beacon (
    id integer primary key,
    name text not null,
    identity_key blob not null,
    clock_offset integer not null,
    k integer not null
);

drop table if exists eid;
create table eid (
    eid blog primary key,
    clock integer not null,
    beacon_id integer not null
);
