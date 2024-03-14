from utils.ferramentas import *
from modules.operacoesbancarias import OperacoesBancarias
def criar_usuario():
    cpf = input("Informe seu CPF somente números: ")
    while not validar_cpf(cpf):
        cpf = input("CPF inválido. Por favor, informe seu CPF somente números: ")

    nome = input("Informe seu nome: ")

    email = input("Informe seu email: ")
    while not validar_email(email):
        email = input("Email inválido. Por favor, informe seu email: ")

    tipo_conta = input("Informe seu tipo de conta (normal/premium/universitario): ")
    while not validar_tipo_conta(tipo_conta):
        tipo_conta = input(
            "Tipo de conta inválido. Por favor, informe seu tipo de conta (normal/premium/universitario): ")
    senha = input("Digite sua senha de 6 digitos numericos: ")
    while not validar_senha(senha):
        senha = input(
            "Senha nao atende os requisitos ! . Por favor, tente outra senha: ")
    id_conta = gerar_numero_conta()
    conta_dados = {
        'id_conta':id_conta,
        'cpf': cpf,
        'nome': nome,
        'email': email,
        'tipo_conta': tipo_conta,
        'senha': senha
    }

    return conta_dados

def fazer_login():
    tentativas = 0
    while tentativas < 3:
        cpf = input("Informe seu CPF somente números: ")
        senha = input("Digite sua senha de 6 digitos numericos: ")
        conta_dados = {
            'id_conta': 'id_conta',
            'cpf': cpf,
            'nome': 'nome',
            'email': 'email',
            'tipo_conta':'' ,
            'senha':' '
        }
        operacao = OperacoesBancarias(conta_dados, senha=senha)
        conta = operacao.buscar_usuario()
        login = operacao.fazer_login()
        if login:
            user = {
                'id_conta': conta['id_conta'],
                'cpf': cpf,
                'email': conta['email'],
                'nome': conta['nome'],
                'tipo_conta': conta['tipo_conta'],
            }
            return user
        else:
            print("CPF ou senha incorretos. Tente novamente.")
            tentativas += 1
    print("Você excedeu o número máximo de tentativas. O programa será encerrado.")
    exit()