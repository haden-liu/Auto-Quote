-- drop table if exists coloaders;
drop table if exists rates;

create table rates (
    id serial primary key,
    carrier varchar(50),
    freight_rate_min float(1),
    freight_rate_unit float(1),
    fuel_rate float(1),
    loading_port varchar(50),
    discharging_port varchar(50),
    valid_date date

)

-- alter table rates drop column coloader_ID
-- alter table rates add column freight_rate_weight float(1) not null
-- alter table rates drop column freight_rate_weight