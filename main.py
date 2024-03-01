from modules.bank import ContaBancaria


def depositar(conta):
    valor = float(input("Informe o valor do depósito: "))
    conta.depositar(valor)


def sacar(conta):
    valor = float(input("Informe o valor do saque: "))
    conta.sacar(valor)


def mostrar_extrato(conta):
    conta.mostrar_extrato()


def sair(conta):
    conta.__del__()


def main():
    id_conta = input("Informe o ID da conta: ")
    conta = ContaBancaria(id_conta)

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
