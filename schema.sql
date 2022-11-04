-- drop table if exists coloaders;
-- drop table if exists rates;

-- create table rates (
--     id serial primary key,
--     carrier varchar(50) not null,
--     freight_rate_min float(1) not null,
--     freight_rate_unit float(1) not null,
--     fuel_rate float(1),
--     loading_port varchar(50) not null,
--     discharging_port varchar(50) not null,
--     valid_date date not null,
--     coloader_ID integer
-- )

-- alter table rates drop column coloader_ID
alter table rates add column freight_rate_weight float(1) not null