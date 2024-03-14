import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

dbname = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")


class Database:
    def __init__(self):
        self.dbname = os.getenv("DATABASE_NAME")
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.host = os.getenv("DATABASE_HOST")
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        self.cursor = self.conn.cursor()

    def criar_usuario(self, cpf, email, nome):
        self.cursor.execute('''INSERT INTO clientes (cpf, email, nome)
                          VALUES (%s, %s, %s)''',
                       (cpf, email, nome,))
        self.conn.commit()


    def buscar_usuario(self, cpf):
        self.cursor.execute("SELECT cpf, email, nome FROM clientes WHERE cpf = %s", (cpf,))
        cpf, email, nome = self.cursor.fetchone()
        return {
            'cpf': cpf,
            'email': email,
            'nome': nome
        }


    def criar_conta(self, cpf, id_conta, tipo_conta, senha_hash, papper, saldo, extrato, numero_saques, valor_saque_diario,
                    limite_valor_saque, limite_saques, data_saque, data_deposito):

        self.cursor.execute('''INSERT INTO contas_bancarias (id_conta, cpf_cliente, tipo_conta, saldo, extrato, 
                        numero_saques, valor_saque_diario, limite_valor_saque, limite_saques, data_saque, 
                        data_deposito, senha_hash, papper)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
                             id_conta, cpf, tipo_conta, saldo, extrato,
                             numero_saques, valor_saque_diario,
                             limite_valor_saque, limite_saques,
                             data_saque, data_deposito, senha_hash, papper))
        self.conn.commit()

    def buscar_conta(self, cpf):
        self.cursor.execute("SELECT id_conta, cpf_cliente, tipo_conta, saldo,"
                       " extrato, numero_saques, "
                       "valor_saque_diario, limite_valor_saque,"
                       " limite_saques, data_saque, data_deposito, "
                       "senha_hash, papper FROM contas_bancarias WHERE cpf_cliente = %s",
                       (cpf,))
        result = self.cursor.fetchone()
        if result:
            id_conta, cpf_cliente, tipo_conta, saldo, extrato, numero_saques, valor_saque_diario, limite_valor_saque, \
                limite_saques, data_saque, data_deposito, senha_hash, papper = result
            return {
                'id_conta': id_conta,
                'cpf_cliente': cpf_cliente,
                'tipo_conta': tipo_conta,
                'saldo': saldo,
                'extrato': extrato,
                'numero_saques': numero_saques,
                'valor_saque_diario': valor_saque_diario,
                'limite_valor_saque': limite_valor_saque,
                'limite_saques': limite_saques,
                'data_saque': data_saque,
                'data_deposito': data_deposito,
                'senha_hash': senha_hash,
                'papper': papper
            }
        else:
            return None

    def saldo(self, id_conta):
        self.cursor.execute("SELECT saldo FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        saldo = self.cursor.fetchone()
        return saldo[0] if saldo else None

    def numero_saques(self, id_conta):
        self.cursor.execute("SELECT numero_saques FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        numero_saques = self.cursor.fetchone()
        return numero_saques[0] if numero_saques else None

    def limite_saques(self, id_conta):
        self.cursor.execute("SELECT limite_saques FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        limite_saques = self.cursor.fetchone()
        return limite_saques[0] if limite_saques else None

    def valor_saque_diario(self, id_conta):
        self.cursor.execute("SELECT valor_saque_diario FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        saque_diario = self.cursor.fetchone()
        return saque_diario[0] if saque_diario else None

    def extrato(self, id_conta):
        self.cursor.execute("SELECT extrato FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        extrato = self.cursor.fetchone()
        return extrato[0] if extrato else None

    def limite_valor_saque(self, id_conta):
        self.cursor.execute("SELECT limite_valor_saque FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        limite_valor_saque = self.cursor.fetchone()
        return limite_valor_saque[0] if limite_valor_saque else None

    def data_saque(self, id_conta):
        self.cursor.execute("SELECT data_saque FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        data_saque = self.cursor.fetchone()
        return data_saque[0] if data_saque else None

    def data_deposito(self, id_conta):
        self.cursor.execute("SELECT data_deposito FROM contas_bancarias WHERE id_conta = %s", (id_conta,))
        data_deposito = self.cursor.fetchone()
        return data_deposito[0] if data_deposito else None

    def sacar(self, id_conta, valor):
        self.cursor.execute('''UPDATE contas_bancarias 
                           SET saldo = saldo - %s
                           WHERE id_conta = %s''', (valor, id_conta,))
        self.conn.commit()

    def depositar(self, id_conta, valor):
        self.cursor.execute('''UPDATE contas_bancarias 
                           SET saldo = saldo + %s
                           WHERE id_conta = %s''', (valor, id_conta,))
        self.conn.commit()

    def atualizar_extrato(self, id_conta, tipo, valor,data_atual):
        try:
            self.cursor.execute('''UPDATE contas_bancarias 
                               SET extrato = extrato || %s
                               WHERE id_conta = %s''',
                            (f"{tipo}: R$ {valor:.2f}  - Data: {data_atual}\n", id_conta,))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Erro ao atualizar extrato:", e)

    def atualizar_data_saque(self, id_conta,data_atual):
        try:
            self.cursor.execute('''UPDATE contas_bancarias 
                               SET data_saque = %s
                               WHERE id_conta = %s''', (data_atual, id_conta,))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Erro ao atualizar data:", e)

    def atualizar_data_deposito(self, id_conta,data_atual):
        try:
            self.cursor.execute('''UPDATE contas_bancarias 
                               SET data_deposito = %s
                               WHERE id_conta = %s''', (data_atual, id_conta,))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Erro ao atualizar data:", e)

    def atualizar_numero_saques(self, id_conta, numero_saques):
        self.cursor.execute('''UPDATE contas_bancarias 
                           SET numero_saques = %s     
                           WHERE id_conta = %s''', (numero_saques, id_conta,))
        self.conn.commit()

    def atualizar_valor_saque_diario(self, id_conta, valor_saque_diario):
        self.cursor.execute('''UPDATE contas_bancarias 
                           SET valor_saque_diario = %s    
                           WHERE id_conta = %s''', (valor_saque_diario, id_conta,))
        self.conn.commit()

    def close(self):
        self.conn.close()
