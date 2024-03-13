from datetime import datetime
from modules.contabancaria import ContaBancaria
from utils.ferramentas import *

class OperacoesBancarias:
    def __init__(self, conta, senha=None):
        self.conta = ContaBancaria(**conta)
        self.senha = senha
    def criar_usuario(self):
        self.conta.criar_conta()

    def buscas_usuarios(self):
        user = self.conta.consultar_usuario()
        return  user
    def fazer_login(self):
        user = self.conta.consultar_usuario()
        validacao =  verificar_senha(self.senha, user['senha'], user['papper'])
        return validacao

    def saque_conta(self, valor):
        saldo_atual = self.conta.consultar_saldo()
        limite_valor_saque = self.conta.consultar_limite_valor_saque()
        numero_saques_hoje = self.conta.consultar_numero_saques()
        valor_saque_diario = self.conta.consultar_valor_saque_diario()
        limite_saques = self.conta.limite_saques()
        data_atual = datetime.now().strftime("%Y-%m-%d")
        data_ultimo_saque = self.conta.consultar_data_saque()
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        elif valor > saldo_atual:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif data_atual != data_ultimo_saque.split()[0]:
            self.conta.sacar(valor)
            self.conta.atualizar_extrato("Saque",valor)
            self.conta.atualizar_numero_saques(0)
            self.conta.atualizar_valor_saque_diario(valor)
            self.conta.atualizar_data_saque()
            print("Saque realizado com sucesso!")
        elif limite_valor_saque < (valor_saque_diario + valor):
            print("Operação falhou! Você já sacou o limite diário.")
        elif numero_saques_hoje >= limite_saques:
            print("Operação falhou! Você já realizou a quantidade máxima de saques por dia.")
        else:
            self.conta.sacar(valor)
            self.conta.atualizar_data_saque()
            self.conta.atualizar_extrato("Saque", valor)
            self.conta.atualizar_numero_saques((numero_saques_hoje + 1))
            self.conta.atualizar_valor_saque_diario((valor_saque_diario + valor))
            print("Saque realizado com sucesso!")
    def depositar(self, valor):
        if valor > 0:
            self.conta.depositar(valor)
            self.conta.atualizar_extrato("Deposito", valor)
            self.conta.atualizar_data_deposito()
        else:
            print("Operação falhou! O valor informado é inválido.")

    def consultar_extrato(self):
        extrato = self.conta.consultar_extrato()
        saldo = self.conta.consultar_saldo()
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo}")
        print("==========================================")
        return self.conta.consultar_extrato()

    def sair(self):
        self.conta.__del__()