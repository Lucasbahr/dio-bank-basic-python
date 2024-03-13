import random
import hashlib
import secrets
import string

def gerar_numero_conta():
    numero_conta = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    digito_verificador = random.randint(0, 9)
    numero_conta_completo = f"{numero_conta}-{digito_verificador}"
    return numero_conta_completo

def validar_cpf(cpf):
    if not cpf.isdigit() or len(cpf) != 11:
        return False
    return True

def validar_email(email):
    if "@" not in email:
        return False
    return True

def validar_tipo_conta(tipo_conta):
    tipos_validos = ["normal", "premium", "universitario"]
    if tipo_conta.lower() not in tipos_validos:
        return False
    return True

def validar_senha(senha):
    if not senha.isdigit():
        return False
    if len(senha) != 6:
        return False
    return True

def hash_senha_e_papper(senha):
    papper = generate_pepper()
    senha_com_pepper = senha + papper
    hashed_senha = hashlib.sha256(senha_com_pepper.encode()).hexdigest()
    return hashed_senha , papper

def verificar_senha(senha, hashed_senha, pepper):
    senha_com_pepper = senha + pepper
    hashed_senha_input = hashlib.sha256(senha_com_pepper.encode()).hexdigest()
    return hashed_senha_input == hashed_senha

def generate_pepper(length=32):
    pepper_characters = string.ascii_letters + string.digits + string.punctuation
    pepper = ''.join(secrets.choice(pepper_characters) for _ in range(length))
    return pepper
