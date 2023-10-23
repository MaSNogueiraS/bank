
import json
from data_structures import Client

FILENAME = "bank_data.json"

def save_clients_to_file(bank):
    data = []
    for client in bank.clients.values():
        client_data = {
            "razao_social": client.razao_social,
            "CNPJ": client.CNPJ,
            "account_type": client.account_type,
            "balance": client.balance,
            "password": client.password,
            "transactions": client.transactions
        }
        data.append(client_data)
    
    with open(FILENAME, 'w') as file:
        json.dump(data, file)

def load_clients_from_file(bank):
    try:
        with open(FILENAME, 'r') as file:
            data = json.load(file)
        
        for client_data in data:
            client = Client(
                client_data["razao_social"],
                client_data["CNPJ"],
                client_data["account_type"],
                client_data["balance"],
                client_data["password"]
            )
            client.transactions = client_data["transactions"]
            bank.add_client(client)
    except FileNotFoundError:
        pass
