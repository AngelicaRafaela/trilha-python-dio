from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []  # Lista para armazenar as contas do cliente

    def realizar_transacao(self, conta, transacao):
        # Método para realizar uma transação em uma conta específica
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        # Método para adicionar uma nova conta à lista de contas do cliente
        self.contas.append(conta)


class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        # Inicializa uma nova Pessoa Fisica com as informações fornecidas
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.cliente = Cliente(endereco)  # Cria um objeto Cliente associado à pessoa física


class Conta:
    def __init__(self, numero, cliente):
        # Inicializa uma nova conta com o número e o cliente associados
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()  # Cria um histórico de transações associado à conta

    @classmethod
    def nova_conta(cls, cliente, numero):
        # Método de classe para criar uma nova conta com o cliente e o número especificados
        return cls(numero, cliente)

    @property
    def saldo(self):
        # Propriedade que retorna o saldo da conta
        return self._saldo

    @property
    def numero(self):
        # Propriedade que retorna o número da conta
        return self._numero

    @property
    def agencia(self):
        # Propriedade que retorna a agência da conta
        return self._agencia

    @property
    def cliente(self):
        # Propriedade que retorna o cliente associado à conta
        return self._cliente

    @property
    def historico(self):
        # Propriedade que retorna o histórico de transações da conta
        return self._historico

    def sacar(self, valor):
        # Método para sacar um valor da conta
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        # Método para depositar um valor na conta
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        # Inicializa uma nova conta corrente com o número, cliente e limites especificados
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        # Método para sacar um valor da conta corrente
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        # Método para retornar uma representação em string da conta corrente
        return f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}"


class Historico:
    def __init__(self):
        # Inicializa um novo histórico de transações
        self._transacoes = []

    @property
    def transacoes(self):
        # Propriedade que retorna a lista de transações do histórico
        return self._transacoes

    def adicionar_transacao(self, transacao):
        # Método para adicionar uma transação ao histórico
        self._transacoes.append(transacao)


class Transacao(ABC):
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        # Inicializa um novo saque com o valor especificado
        self._valor = valor

    @property
    def valor(self):
        # Propriedade que retorna o valor do saque
        return self._valor

    def registrar(self, conta):
        # Método para registrar um saque na conta
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        # Inicializa um novo depósito com o valor especificado
        self._valor = valor

    @property
    def valor(self):
        # Propriedade que retorna o valor do depósito
        return self._valor

    def registrar(self, conta):
        # Método para registrar um depósito na conta
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
