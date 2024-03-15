from datetime import datetime
from modules.conta_bancaria import ContaBancaria
from utils.ferramentas import verificar_senha, hash_senha_e_papper


class OperacoesBancarias:
    def __init__(self, cpf,email=None,nome=None,tipo_conta=None, senha=None):
        self._conta = ContaBancaria(tipo_conta=tipo_conta, cpf=cpf, email=email, nome=nome)
        self._senha = senha
        self._tipo_conta = tipo_conta

    def criar_usuario_e_conta(self):
        data_formatada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saldo = 0.0
        extrato = ''
        numero_saques = 0
        valor_saque_diario = 0
        limite_valor_saque = 500
        limite_saques = 3
        data_saque = data_formatada
        data_deposito = data_formatada
        senha_hash, papper = hash_senha_e_papper(str(self._senha))

        self._conta.criar_usuario()

        self._conta.criar_conta_bancaria(saldo=saldo, extrato=extrato, numero_saques=numero_saques,
                                         valor_saque_diario=valor_saque_diario,
                                         limite_valor_saque=limite_valor_saque,limite_saques=limite_saques,
                                         data_saque=data_saque,data_deposito=data_deposito,
                                         senha_hash=senha_hash,papper=papper)

    def buscar_usuario(self):
        user = self._conta.usuario
        return user

    def buscar_conta_usuario(self):
        conta = self._conta.conta
        return conta

    def fazer_login(self):
        conta = self._conta.conta
        print(conta)
        validacao = verificar_senha(self._senha, conta['senha_hash'], conta['papper'])
        return validacao

    def saque_conta(self, valor):
        data_formatada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_atual = datetime.now().strftime("%Y-%m-%d")
        print(self._conta.limite_valor_saque)
        print((self._conta.valor_saque_diario + valor))
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        elif valor > self._conta.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif data_atual != self._conta.data_saque.split()[0]:
            self.realizar_saque(valor, 0, valor, data_formatada)
        elif self._conta.limite_valor_saque < (self._conta.valor_saque_diario + valor):
            print("Operação falhou! Você já sacou o limite diário.")
        elif self._conta.numero_saques >= self._conta.limite_saques:
            print("Operação falhou! Você já realizou a quantidade máxima de saques por dia.")
        else:
            self.realizar_saque(valor, (self._conta.numero_saques + 1), (self._conta.valor_saque_diario + valor),
                                data_formatada)

    def realizar_saque(self, valor, valor_saque_diario, numero_saque, data_formatada):
        self._conta.sacar(valor)
        self._conta.atualizar_data_saque(data_formatada)
        self._conta.atualizar_extrato("Saque", valor,data_formatada)
        self._conta.atualizar_numero_saques(valor_saque_diario)
        self._conta.atualizar_valor_saque_diario(numero_saque)
        print("Saque realizado com sucesso!")

    def depositar(self, valor):
        data_formatada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if valor > 0:
            self._conta.depositar(valor)
            self._conta.atualizar_extrato("Deposito", valor, data_formatada)
            self._conta.atualizar_data_deposito(data_formatada)
        else:
            print("Operação falhou! O valor informado é inválido.")

    def consultar_extrato(self):
        extrato = self._conta.extrato
        saldo = self._conta.saldo
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
        del self._conta


