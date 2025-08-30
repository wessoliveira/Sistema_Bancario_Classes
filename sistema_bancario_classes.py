import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

LARGURA_PRINT = 80

def menu():

    menu = f"""
    {" Menu ".center(LARGURA_PRINT, "=")}
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    [u] Criar Usuário
    [l] Listar Usuários
    [c] Criar Conta
    [k] Listar Contas
    => """
    return input(textwrap.dedent(menu))

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
            print(f"\n@@@ Operação falhou! Número máximo de saques ({limite_saques}) atingido. @@@")
    else:
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. Informe um número maior que zero. @@@")
        elif valor > limite:
            print(f"\n@@@ Operação falhou! O valor máximo para saque é R$ {limite:.2f}. @@@")
        elif valor > saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        else:
            saldo -= valor
            extrato += f"Saque:\t\t R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
    return saldo, extrato, numero_saques

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\t R$ {valor:.2f}\n"
        print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. Informe um número maior que zero. @@@")
    return saldo, extrato

def mostrar_extrato(saldo, /, *, extrato):
    print("\n", " Extrato ".center(LARGURA_PRINT, "="), sep="")
    print("Sem movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\t R$ {saldo:.2f}")
    print("=" * LARGURA_PRINT)

def criar_usuario(lista_usuarios):
    usuario = {}
    usuario['cpf'] = input("Informe o CPF (apenas números): ")
    lista_busca = [u for u in lista_usuarios if u['cpf'] == usuario['cpf']]
    if lista_busca:
        print("\n@@@ Usuário já existe! @@@")
    else:
        usuario['nome'] = input("Informe o nome: ")
        usuario['data_nascimento'] = input("Informe a data de nascimento (dd/mm/aaaa): ")
        usuario['endereco'] = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        lista_usuarios.append(usuario)
        print("\n=== Usuário criado com sucesso! ===")
    # return lista_usuarios

def listar_usuarios(lista_usuarios):
    print("\n", " Lista de Usuários ".center(LARGURA_PRINT, "="), sep="")
    if not lista_usuarios:
        print("\nNenhum usuário cadastrado.")
    else:
        for u in lista_usuarios:
            info_usuario = f"""
            {"-" * (LARGURA_PRINT - 2)}
            CPF: {u['cpf']}
            Nome: {u['nome']}
            Data de Nascimento: {u['data_nascimento']}
            Endereço: {u['endereco']}"""
            print(textwrap.dedent(info_usuario))
    print("\n" + "=" * LARGURA_PRINT)

def criar_conta(lista_contas, lista_usuarios):
    agencia = "0001"
    numero_conta = len(lista_contas) + 1
    conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": None}
    cpf = input("Informe o CPF do usuário: ")
    lista_busca = [u for u in lista_usuarios if u['cpf'] == cpf]
    if lista_busca:
        conta['usuario'] = lista_busca[0]
        lista_contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")
        print(f"Agência: {agencia}")
        print(f"Número da Conta: {numero_conta}")
    else:
        print("\n@@@ Usuário não encontrado, por favor verifique o CPF informado. @@@")

def listar_contas(lista_contas):
    print("\n", " Lista de Contas ".center(LARGURA_PRINT, "="), sep="")
    if not lista_contas:
        print("\nNenhuma conta cadastrada.")
    else:
        for c in lista_contas:
            info_conta = f"""
            {"-" * (LARGURA_PRINT - 2)}
            Agência: {c['agencia']}
            Número da Conta: {c['numero_conta']}
            Cliente: {c['usuario']['nome']}
            CPF: {c['usuario']['cpf']}"""
            print(textwrap.dedent(info_conta))
    print("\n" + "=" * LARGURA_PRINT)

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    LIMITE_SAQUES = 3
    lista_usuarios = []
    lista_contas = []

    while True:

        opcao = menu()

        if opcao == "s":
            valor_saque = round(float(input("Informe o valor do saque: ")), 2)
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, 
                valor=valor_saque, 
                extrato=extrato, 
                limite=limite, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES
            )
        
        elif opcao == "d":
            valor_deposito = round(float(input("Informe o valor do depósito: ")), 2)
            saldo, extrato = depositar(saldo, valor_deposito, extrato)
        
        elif opcao == "e":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "u":
            # lista_usuarios = criar_usuario(lista_usuarios)
            criar_usuario(lista_usuarios)

        elif opcao == "l":
            listar_usuarios(lista_usuarios)

        elif opcao == "c":
            # lista_contas = criar_conta(lista_contas, lista_usuarios)
            criar_conta(lista_contas, lista_usuarios)

        elif opcao == "k":
            listar_contas(lista_contas)

        elif opcao == "q":
            print("Sair...")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# main()


class Cliente:
    def __init__(self, endereco, conta=None):
        self._endereco = endereco
        self._contas = []
        if conta:
            self._contas.append(conta)

    def adicionar_conta(self, conta):
        print(f"Adicionar conta {conta}:\n {self}")
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        print(f"Realizando transação \n{transacao}")
        transacao.registrar(conta)

    def __str__(self):
        return f"""{"Cliente".center(30, "-")}
        Endereço: {self._endereco}
        Contas: {len(self._contas)}"""

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco, conta=None):
        super().__init__(endereco, conta)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()

    def __str__(self):
        return f"""
        {"PessoaFisica".center(30, "-")}
        CPF: {self._cpf}
        Nome: {self._nome}
        Nascimento: {self._data_nascimento}
        Endereço: {self._endereco}
        Contas: {len(self._contas)}"""

class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def nova_conta(self, cliente, numero):
        conta = Conta(numero, "0001-01", cliente)
        cliente.adicionar_conta(conta)
        return conta
    
    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False
        self._saldo -= valor
        # self._historico += f"Saque:\t\t {valor}\n"
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor de depósito inválido.")
            return False
        self._saldo += valor
        # self._historico += f"Depósito:\t {valor}\n"
        return True

    def __str__(self):
        return f"""
        {"Conta".center(30, "-")}
        Saldo: {self.saldo}
        Número: {self._numero}
        Agência: {self._agencia}
        Cliente: {self._cliente}
        Histórico:\n {self._historico}"""
    
class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def __str__(self):
        return textwrap.dedent(f"""
        {"ContaCorrente".center(30, "-")}
        Saldo: {self.saldo}
        Número: {self._numero}
        Agência: {self._agencia}
        Cliente: {self._cliente}
        Histórico:\n {self._historico}
        Limite: {self._limite}
        Limite de Saques: {self._limite_saques}""")

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        print(f"Registrando depósito de {self.valor} na conta:\n{conta}")
        deposito_ok = conta.depositar(self.valor)
        if deposito_ok:
            print("Depósito realizado com sucesso.")
            conta._historico.adicionar_transacao(self)
        else:
            print("Falha ao realizar depósito.")
    
    def __str__(self):
        return f"Depósito:\t {self.valor}"

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        print(f"Registrando saque de {self.valor} na conta:\n{conta}")
        saque_ok = conta.sacar(self.valor)
        if saque_ok:
            print("Saque realizado com sucesso.")
            conta._historico.adicionar_transacao(self)
        else:
            print("Falha ao realizar saque.")

    def __str__(self):
        return f"Saque:\t\t {self.valor}"

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def __str__(self):
        return "\n".join(str(t) for t in self._transacoes)

# cli1 = Cliente("Rua A, 123")
# cli2 = Cliente("Rua B, 456")

# print(cli1)
# print(cli2)

pf1 = PessoaFisica("123.456.789-00", "João Silva", "01/01/1990", "Rua C, 789")
pf2 = PessoaFisica("987.654.321-00", "Maria Souza", "02/02/1985", "Rua D, 321")

print(pf1)
print(pf2)


# cli1.adicionar_conta(101)

# pf1.adicionar_conta(102)

# print(cli1)
# print(pf1)
cc1 = ContaCorrente(103, "0001-01", pf1)
print("cc1:\n", cc1)

pf1.adicionar_conta(cc1)
print("pf1:\n", pf1)

print("Saldo de pf1:", pf1._contas[0].saldo)
print("Historico de pf1:")
print(pf1._contas[0]._historico)

pf1.realizar_transacao(cc1, Deposito(100))

print("cc1:\n", cc1)

print("pf1:\n", pf1)

print("Saldo de pf1:", pf1._contas[0].saldo)
print("Historico de pf1:")
print(pf1._contas[0]._historico)

pf1.realizar_transacao(cc1, Saque(50))
print("Saldo de pf1:", pf1._contas[0].saldo)
print("Historico de pf1:")
print(pf1._contas[0]._historico)


# dep1 = Deposito(100)
# dep1.registrar(cc1)

# saq1 = Saque(50)
# saq1.registrar(cc1)

# print("Instancia Historico")
# hist1 = Historico()

# print("Imprimindo Historico")
# print(hist1)

# print("Adiciona Transacao")
# hist1.adicionar_transacao(dep1)

# print("Imprimindo Historico")
# print(hist1)

# print("Adiciona Transacao")
# hist1.adicionar_transacao(saq1)

# print("Imprimindo Historico")
# print(hist1)
