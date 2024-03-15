import psycopg2

from utils.interface import *
from modules.operacoe_bancarias import OperacoesBancarias

def depositar(conta):
    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("Valor inválido. Por favor, insira um número válido.")
        return
    conta.depositar(valor)

def sacar(conta):
    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("Valor inválido. Por favor, insira um número válido.")
        return
    conta.saque_conta(valor)

def mostrar_extrato(conta):
    conta.consultar_extrato()

def sair(conta):
    conta.sair()

def main():
    conta = None
    login = input("Já possui conta? Digite 's'. Caso contrário, digite 'c':  ")
    if login == "c":
        while True:
            try:
                conta_dados = criar_usuario()
                conta = OperacoesBancarias(**conta_dados)
                conta.criar_usuario_e_conta()
                break
            except psycopg2.errors.UniqueViolation:
                print("CPF já está em uso. Por favor, refaça o cadastro.")
    elif login == "s":
        conta_dados = fazer_login()
        conta = OperacoesBancarias(**conta_dados)


    opcoes = {
        'd': depositar,
        's': sacar,
        'e': mostrar_extrato,
        'q': sair
    }

    while True:
        menu = """
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair

        => """
        opcao = input(menu)
        if opcao == "q":
            opcoes[opcao](conta)
            print("O banco agradece a preferência!")
            break
        if opcao in opcoes:
            opcoes[opcao](conta)
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
