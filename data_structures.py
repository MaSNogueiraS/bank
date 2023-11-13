
import datetime

class Client:
    #This sets the clients and all the infos it have, this is super important for the operations to work
    def __init__(self, razao_social, CNPJ, account_type, balance=0.0, password=""):
        self.razao_social = razao_social
        self.CNPJ = CNPJ
        self.account_type = account_type
        self.balance = balance
        self.password = password
        self.transactions = []
        self.auto_debits = {}  
        self.set_overdraft_limit()  
        self.last_processed_month = None
        self.last_processed_year = None
        self.salary = 0
        
    def set_overdraft_limit(self):
        if self.account_type == "Plus":
            self.overdraft_limit = -5000.0
        else:  
            self.overdraft_limit = -1000.0

    def set_salary(self, amount):
        self.salary = amount

    def calculate_debit_fee(self, amount):
        if self.account_type == "Plus":
            return amount * 0.03
        else:  
            return amount * 0.05

    def add_transaction(self, description, amount):
        transaction = {
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "description": description,
            "amount": amount
        }
        self.transactions.append(transaction)

class Bank:
    #This is a simple class that i use to navigate between the clients basically
    def __init__(self):
        self.clients = {}

    def add_client(self, client):
        self.clients[client.CNPJ] = client

    def get_client(self, CNPJ):
        return self.clients.get(CNPJ)
