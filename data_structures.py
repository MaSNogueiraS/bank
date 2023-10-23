
import datetime

class Client:
    def __init__(self, razao_social, CNPJ, account_type, balance=0.0, password=""):
        self.razao_social = razao_social
        self.CNPJ = CNPJ
        self.account_type = account_type
        self.balance = balance
        self.password = password
        self.transactions = []

    def add_transaction(self, description, amount):
        transaction = {
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "description": description,
            "amount": amount
        }
        self.transactions.append(transaction)

class Bank:
    def __init__(self):
        self.clients = {}

    def add_client(self, client):
        self.clients[client.CNPJ] = client

    def get_client(self, CNPJ):
        return self.clients.get(CNPJ)
