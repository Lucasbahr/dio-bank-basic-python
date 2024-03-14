from datetime import datetime
from modules.contabancaria import ContaBancaria
from utils.ferramentas import verificar_senha


class OperacoesBancarias:
    def __init__(self, conta, senha=None):
        self.conta = ContaBancaria(**conta)
        self.senha = senha

    def criar_usuario(self):
        self.conta.criar_conta()

    def buscar_usuario(self):
        user = self.conta.usuario
        return user

    def fazer_login(self):
        user = self.conta.usuario
        validacao = verificar_senha(self.senha, user['senha'], user['papper'])
        return validacao

    def saque_conta(self, valor):
        data_atual = datetime.now().strftime("%Y-%m-%d")
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        elif valor > self.conta.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif data_atual != self.conta.data_saque.split()[0]:
            self.realizar_saque(valor, 0, valor)
        elif self.conta.limite_valor_saque < (self.conta.valor_saque_diario + valor):
            print("Operação falhou! Você já sacou o limite diário.")
        elif self.conta.numero_saques >= self.conta.limite_saques:
            print("Operação falhou! Você já realizou a quantidade máxima de saques por dia.")
        else:
            self.realizar_saque(valor,(self.conta.numero_saques + 1),(self.conta.valor_saque_diario + valor))

    def realizar_saque(self,valor,valor_saque_diario,numero_saque):
        self.conta.sacar(valor)
        self.conta.atualizar_data_saque()
        self.conta.atualizar_extrato("Saque", valor)
        self.conta.atualizar_numero_saques((valor_saque_diario))
        self.conta.atualizar_valor_saque_diario((numero_saque))
        print("Saque realizado com sucesso!")

    def depositar(self, valor):
        if valor > 0:
            self.conta.depositar(valor)
            self.conta.atualizar_extrato("Deposito", valor)
            self.conta.atualizar_data_deposito()
        else:
            print("Operação falhou! O valor informado é inválido.")

    def consultar_extrato(self):
        extrato = self.conta.extrato
        saldo = self.conta.saldo
        if not extrato:
            extrato_text = "Não foram realizadas movimentações."
        else:
            extrato_text = extrato.strip()

        extrato_info = f"""
        ================ EXTRATO ================
        {extrato_text}

        Saldo: R$ {saldo}
        ==========================================
        """
        print(extrato_info)


    def sair(self):
        del self.conta
