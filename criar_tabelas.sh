#!/bin/bash

##DEFINIR VARIAVEL DE AMBIENTE export PGPASSWORD=<senha_banco>

psql -h localhost -p 5432 -U docker -c "CREATE DATABASE contas_banco"


psql -h localhost -p 5432 -U docker  -d contas_banco -c "CREATE TABLE IF NOT EXISTS users (
    id_conta TEXT PRIMARY KEY,
    cpf BIGINT  UNIQUE,
    email TEXT,
    nome TEXT,
    tipo_conta TEXT,
    senha TEXT,
    papper TEXT
);"

psql -h localhost -p 5432 -U docker  -d contas_banco -c "CREATE TABLE IF NOT EXISTS bank (
    id_conta TEXT  PRIMARY KEY,
    saldo REAL,
    extrato TEXT,
    numero_saques INTEGER,
    valor_saque_diario INTEGER,
    limite_valor_saque INTEGER,
    limite_saques INTEGER,
    data_saque TEXT,
    data_deposito TEXT,
    FOREIGN KEY (id_conta) REFERENCES users(id_conta)
);"
