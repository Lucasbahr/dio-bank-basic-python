from utils.banco_de_dados import Database
from utils.ferramentas import gerar_numero_conta
from modules.cliente import Cliente


class ContaBancaria(Cliente):

    def __init__(self, tipo_conta=None, **kw):
        super().__init__(**kw)
        self.tipo_conta = tipo_conta
        self.database = Database()

    def criar_usuario(self):
        self.database.criar_usuario(self.cpf, self.email, self.nome)
        return True

    def criar_conta_bancaria(self, saldo, senha_hash, papper, extrato,
                             numero_saques, valor_saque_diario,
                             limite_valor_saque, limite_saques,
                             data_saque, data_deposito):
        id_conta = gerar_numero_conta()
        self.database.criar_conta(self.cpf, id_conta, self.tipo_conta, senha_hash, papper, saldo, extrato, numero_saques,
                    valor_saque_diario,
                    limite_valor_saque, limite_saques, data_saque, data_deposito)
        return True

    @property
    def usuario(self):
        usuario = self.database.buscar_usuario(self.cpf)
        return usuario

    @property
    def conta(self):
        conta = self.database.buscar_conta(self.cpf)
        return conta

    @property
    def saldo(self):
        return self.database.buscar_conta(self.cpf)['saldo']

    @property
    def numero_saques(self):
        return self.database.buscar_conta(self.cpf)['numero_saques']

    @property
    def limite_saques(self):
        return self.database.buscar_conta(self.cpf)['limite_saques']

    @property
    def valor_saque_diario(self):
        return self.database.buscar_conta(self.cpf)['valor_saque_diario']

    @property
    def extrato(self):
        return self.database.buscar_conta(self.cpf)['extrato']

    @property
    def limite_valor_saque(self):
        return self.database.buscar_conta(self.cpf)['limite_valor_saque']

    @property
    def data_saque(self):
        return self.database.buscar_conta(self.cpf)['data_saque']

    @property
    def data_deposito(self):
        return self.database.buscar_conta(self.cpf)['data_deposito']

    def sacar(self, valor):
        self.database.sacar(self.database.buscar_conta(self.cpf)['id_conta'], valor)

    def depositar(self, valor):
        self.database.depositar(self.database.buscar_conta(self.cpf)['id_conta'], valor)
        print("Depósito realizado com sucesso!")

    def atualizar_extrato(self, tipo, valor, data_atual):
        self.database.atualizar_extrato(self.database.buscar_conta(self.cpf)['id_conta'], tipo, valor, data_atual)

    def atualizar_data_saque(self, data):
        self.database.atualizar_data_saque(self.database.buscar_conta(self.cpf)['id_conta'], data)

    def atualizar_data_deposito(self, data):
        self.database.atualizar_data_deposito(self.database.buscar_conta(self.cpf)['id_conta'], data)

    def atualizar_numero_saques(self, valor):
        self.database.atualizar_numero_saques(self.database.buscar_conta(self.cpf)['id_conta'], valor)

    def atualizar_valor_saque_diario(self, valor):
        self.database.atualizar_valor_saque_diario(self.database.buscar_conta(self.cpf)['id_conta'], valor)

    def __del__(self):
        self.database.close()
