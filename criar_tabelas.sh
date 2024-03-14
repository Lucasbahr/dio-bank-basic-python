#!/bin/bash

##DEFINIR VARIAVEL DE AMBIENTE export PGPASSWORD=<senha_banco>

psql -h localhost -p 5432 -U docker -c "CREATE DATABASE contas_banco"


psql -h localhost -p 5432 -U docker  -d contas_banco -c "CREATE TABLE IF NOT EXISTS clientes (
    cpf BIGINT PRIMARY KEY,
    email TEXT,
    nome TEXT
);"

psql -h localhost -p 5432 -U docker  -d contas_banco -c "CREATE TABLE IF NOT EXISTS contas_bancarias (
    id_conta TEXT PRIMARY KEY,
    cpf_cliente BIGINT,
    tipo_conta TEXT,
    saldo REAL,
    extrato TEXT,
    numero_saques INTEGER,
    valor_saque_diario INTEGER,
    limite_valor_saque INTEGER,
    limite_saques INTEGER,
    data_saque TEXT,
    data_deposito TEXT,
    senha_hash TEXT,
    papper TEXT,
    FOREIGN KEY (cpf_cliente) REFERENCES clientes(cpf)
);"
