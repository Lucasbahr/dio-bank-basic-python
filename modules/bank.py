import sqlite3
from datetime import datetime

class ContaBancaria:
    def __init__(self, id_conta):
        self.conn = sqlite3.connect(".\\repository\\contas_bank.db")
        self.cursor = self.conn.cursor()
        self._create_table()
        self.id_conta = id_conta
        self._checar_e_criar_conta()

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bank (
                                id INTEGER PRIMARY KEY,
                                id_conta INTEGER,
                                saldo REAL,
                                limite REAL,
                                extrato TEXT,
                                numero_saques INTEGER,
                                saque_diario INTEGER,
                                limite_valor_saque INTEGER,
                                limite_saques INTEGER,
                                data_saque TEXT)''')
        self.conn.commit()

    def _checar_e_criar_conta(self):
        self.cursor.execute("SELECT id FROM bank WHERE id_conta = ?", (self.id_conta,))
        resultado = self.cursor.fetchone()
        if resultado is None:
            self.cursor.execute('''INSERT INTO bank (id_conta, saldo, limite, extrato, numero_saques, limite_saques, limite_valor_saque, saque_diario)
                                    VALUES (?, 0.0, 0.0, '', 0, 3, 500, 0)''', (self.id_conta,))

            self.conn.commit()
            self.atualizar_data()
            print(f"Conta {self.id_conta} criada com sucesso!")
        else:
            print(f"Conta {self.id_conta} encontrada.")

    def depositar(self, valor):
        if valor > 0:
            self.cursor.execute('''UPDATE bank 
                                   SET saldo = saldo + ?, extrato = extrato || ?
                                   WHERE id_conta = ?''', (valor, f"Depósito: R$ {valor:.2f}\n", self.id_conta))
            self.conn.commit()
        else:
            print("Operação falhou! O valor informado é inválido.")

    def sacar(self, valor):
        self.cursor.execute(
            "SELECT saldo, numero_saques, limite_saques, data_saque, limite_valor_saque, saque_diario FROM bank WHERE id_conta = ?",
            (self.id_conta,))
        saldo_atual, numero_saques, limite_saques, data_saque , limite_valor_saque, saque_diario = self.cursor.fetchone()
        data_atual = datetime.now().strftime("%Y-%m-%d")
        data_operacao_formatada = datetime.strptime(data_saque, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        if valor > 0:
            excedeu_saldo = valor > saldo_atual
            if data_operacao_formatada != data_atual:
                self.cursor.execute('''UPDATE bank 
                                       SET limite_valor_saque = 0 ,
                                       numero_saques = 0     
                                       WHERE id_conta = ?''', (self.id_conta,))
                self.conn.commit()
            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif data_operacao_formatada == data_atual and limite_valor_saque <= saque_diario:
                print("Operação falhou! Você ja sacou o limite diario.")
            elif data_operacao_formatada == data_atual and numero_saques >= limite_saques:
                print("Operação falhou! Você já realizou a quantidade máxima de saques por dia.")
            else:
                self.cursor.execute('''UPDATE bank 
                                       SET saldo = saldo - ?, extrato = extrato || ?,
                                       numero_saques = numero_saques + 1 ,
                                       saque_diario = saque_diario + ?
                                       WHERE id_conta = ?''', (valor, f"Saque: R$ {valor:.2f}\n",valor, self.id_conta))
                self.conn.commit()
                self.atualizar_data()
        else:
            print("Operação falhou! O valor informado é inválido.")

    def mostrar_extrato(self):
        self.cursor.execute("SELECT extrato, saldo FROM bank WHERE id_conta = ?", (self.id_conta,))
        extrato, saldo = self.cursor.fetchone()
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    def atualizar_data(self):
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''UPDATE bank 
                               SET data_saque = ?
                               WHERE id_conta = ?''', (data_atual, self.id_conta))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
