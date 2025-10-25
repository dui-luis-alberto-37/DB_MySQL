CREATE DATABASE IF NOT EXISTS Postals;
USE Postals;

CREATE TABLE cod_post (
   d_codigo INT,
   d_asenta VARCHAR(60),
   d_tipo_asenta VARCHAR(60),
   D_mnpio VARCHAR(60),
   d_estado VARCHAR(60),
   d_ciudad VARCHAR(60),
   d_CP INT,
   c_estado INT,
   c_oficina INT,
   c_CP FLOAT,
   c_tipo_asenta INT,
   c_mnpio INT,
   id_asenta_cpcons INT,
   d_zona VARCHAR(60),
   c_cve_ciudad FLOAT
);

LOAD DATA LOCAL INFILE '/docker-entrypoint-initdb.d/db/postals_db.txt'
INTO TABLE cod_post
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(
   d_codigo,
   d_asenta,
   d_tipo_asenta,
   D_mnpio,
   d_estado,
   d_ciudad,
   d_CP,
   c_estado,
   c_oficina,
   c_CP,
   c_tipo_asenta,
   c_mnpio,
   id_asenta_cpcons,
   d_zona,
   c_cve_ciudad
);