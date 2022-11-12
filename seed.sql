-- insert into rates (carrier, freight_rate_min, freight_rate_unit, freight_rate_weight, fuel_rate, loading_port, discharging_port, valid_date) values ('Cosco', 35.5, 33.5, 25.5, 10.5, 'Hong Kong', 'Sydney', '2022-11-30');
-- insert into rates (carrier, freight_rate_min, freight_rate_unit, freight_rate_weight, fuel_rate, loading_port, discharging_port, valid_date) values ('Vanguard', 32.5, 32.5, 23.5, 8.5, 'Singapore', 'Melbourne', '2022-11-30');

-- INSERT INTO users (email, name) VALUES ('haden@example.com', 'haden Example');

-- ALTER TABLE users ADD COLUMN password_hash TEXT;

INSERT INTO users (email, name, password_hash) VALUES ('haden.liu@gmail.com', 'Haden Liu', '$2b$12$sSov.HTpDEWFq4FW2bJNaOu9dRPGmKlVZPCm1f/l7q8SEh53p15Ba');
