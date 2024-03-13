import psycopg2
from datetime import datetime
from utils.ferramentas import hash_senha_e_papper
from dotenv import load_dotenv
import os

load_dotenv()
dbname = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")



class ContaBancaria:
    def __init__(self, cpf, nome=None, email=None, tipo_conta=None, senha=None,id_conta=0):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cpf = cpf
        self.id_conta = id_conta
        self.email = email
        self.nome = nome
        self.senha = senha
        self.tipo_conta = tipo_conta
        self.cursor = self.conn.cursor()

    def criar_conta(self):
        senha, papper = hash_senha_e_papper(str(self.senha))
        self.cursor.execute('''INSERT INTO users (cpf, id_conta, email, nome, tipo_conta, senha, papper)
                                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_conta''',
                            (self.cpf, self.id_conta, self.email, self.nome, self.tipo_conta, senha,papper))
        id_conta = self.cursor.fetchone()[0]
        self.cursor.execute('''INSERT INTO bank (id_conta, saldo, extrato, numero_saques, limite_saques, limite_valor_saque, valor_saque_diario)
                                VALUES (%s, 0.0, '', 0, 3, 500, 0)''', (id_conta,))
        self.conn.commit()
        print(f"Conta {self.id_conta} criada com sucesso!")

    def consultar_usuario(self):
        self.cursor.execute("SELECT id_conta, email, nome, tipo_conta, senha, papper FROM users WHERE cpf = %s", (self.cpf,))
        id_conta, email, nome, tipo_conta, senha, papper = self.cursor.fetchone()
        conta = {
            'id_conta': id_conta,
            'email': email,
            'nome': nome,
            'tipo_conta': tipo_conta,
            'senha': senha,
            'papper': papper
        }
        return conta

    def consultar_saldo(self):
        self.cursor.execute("SELECT saldo FROM bank WHERE id_conta = %s", (self.id_conta,))
        saldo = self.cursor.fetchone()
        return saldo[0] if saldo else None

    def limite_saques(self):
        self.cursor.execute("SELECT limite_saques FROM bank WHERE id_conta = %s", (self.id_conta,))
        limite_saques = self.cursor.fetchone()
        return limite_saques[0] if limite_saques else None

    def consultar_extrato(self):
        self.cursor.execute("SELECT extrato FROM bank WHERE id_conta = %s", (self.id_conta,))
        extrato = self.cursor.fetchone()
        return extrato[0] if extrato else None

    def consultar_numero_saques(self):
        self.cursor.execute("SELECT numero_saques FROM bank WHERE id_conta = %s", (self.id_conta,))
        numero_saques = self.cursor.fetchone()
        return numero_saques[0] if numero_saques else None

    def consultar_valor_saque_diario(self):
        self.cursor.execute("SELECT valor_saque_diario FROM bank WHERE id_conta = %s", (self.id_conta,))
        saque_diario = self.cursor.fetchone()
        return saque_diario[0] if saque_diario else None

    def consultar_limite_valor_saque(self):
        self.cursor.execute("SELECT limite_valor_saque FROM bank WHERE id_conta = %s", (self.id_conta,))
        limite_valor_saque = self.cursor.fetchone()
        return limite_valor_saque[0] if limite_valor_saque else None

    def consultar_data_saque(self):
        self.cursor.execute("SELECT data_saque FROM bank WHERE id_conta = %s", (self.id_conta,))
        data_saque = self.cursor.fetchone()
        return data_saque[0] if data_saque else None

    def consultar_data_deposito(self):
        self.cursor.execute("SELECT data_deposito FROM bank WHERE id_conta = %s", (self.id_conta,))
        data_deposito = self.cursor.fetchone()
        return data_deposito[0] if data_deposito else None

    def sacar(self, valor):
        self.cursor.execute('''UPDATE bank 
                               SET saldo = saldo - %s
                               WHERE id_conta = %s''', (valor, self.id_conta, ))
        self.conn.commit()

    def depositar(self, valor):
        self.cursor.execute('''UPDATE bank 
                               SET saldo = saldo + %s
                               WHERE id_conta = %s''', (valor, self.id_conta, ))
        self.conn.commit()
        self.atualizar_data_saque()
        print("Depósito realizado com sucesso!")

    def atualizar_extrato(self,tipo, valor):
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute('''UPDATE bank 
                                   SET extrato = extrato || %s
                                   WHERE id_conta = %s''', (f"{tipo}: R$ {valor:.2f}  - Data: {data_atual}\n", self.id_conta, ))
            self.conn.commit()
            print("Extrato atualizado com sucesso!")
        except psycopg2.Error as e:
            print("Erro ao atualizar extrato:", e)

    def atualizar_data_saque(self):
        try:
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''UPDATE bank 
                                   SET data_saque = %s
                                   WHERE id_conta = %s''', (data_atual, self.id_conta, ))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Erro ao atualizar data:", e)

    def atualizar_data_deposito(self):
        try:
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''UPDATE bank 
                                   SET data_deposito = %s
                                   WHERE id_conta = %s''', (data_atual, self.id_conta, ))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Erro ao atualizar data:", e)


    def atualizar_numero_saques(self,valor):
        self.cursor.execute('''UPDATE bank 
                               SET numero_saques = %s     
                               WHERE id_conta = %s''', (valor,self.id_conta, ))
        self.conn.commit()

    def atualizar_valor_saque_diario(self, valor):
        self.cursor.execute('''UPDATE bank 
                               SET valor_saque_diario = %s    
                               WHERE id_conta = %s''', (valor, self.id_conta, ))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
