
from tkinter import messagebox
from data_structures import Client


def add_new_client(bank, razao_social, CNPJ, account_type, initial_balance, password):
    if CNPJ in bank.clients:
        return False, "Client with this CNPJ already exists!"
    
    client = Client(razao_social, CNPJ, account_type, initial_balance, password)
    bank.add_client(client)
    return True, "Client added successfully!"

def delete_client(bank, CNPJ):
    if CNPJ not in bank.clients:
        return False, "No client with this CNPJ found!"
    
    del bank.clients[CNPJ]
    return True, "Client deleted successfully!"

def list_clients(bank):
    if not bank.clients:
        return "No clients to display."
    
    client_list = ""
    for client in bank.clients.values():
        client_list += f"Razao Social: {client.razao_social}, CNPJ: {client.CNPJ}, Balance: {client.balance}"
    
    return client_list

def debit_from_account(bank, CNPJ, password, amount):
    client = bank.get_client(CNPJ)
    if not client:
        return False, "Client not found!"
    
    if client.password != password:
        return False, "Incorrect password!"
    
    fee_percentage = 0.05 if client.account_type == "comum" else 0.03
    total_amount = amount + (amount * fee_percentage)
    
    if client.balance - total_amount < (-1000 if client.account_type == "comum" else -5000):
        return False, "Insufficient balance for the transaction!"
    
    client.balance -= total_amount
    client.add_transaction("Debit", -amount)
    client.add_transaction("Fee", -(amount * fee_percentage))
    
    return True, f"Debited R${amount}. Transaction fee: R${amount * fee_percentage}. New balance: R${client.balance}"

def deposit_to_account(bank, CNPJ, amount):
    client = bank.get_client(CNPJ)
    if not client:
        return False, "Client not found!"
    
    client.balance += amount
    client.add_transaction("Deposit", amount)
    
    return True, f"Deposited R${amount}. New balance: R${client.balance}"

def get_account_statement(bank, CNPJ, password):
    client = bank.get_client(CNPJ)
    if not client:
        return False, "Client not found!"
    
    if client.password != password:
        return False, "Incorrect password!"
    
    statement = f"Account Statement for {client.razao_social}:\n"
    statement += f"CNPJ: {client.CNPJ}\n"
    statement += f"Account Type: {client.account_type}\n"
    statement += f"Balance: R${client.balance}\n"
    statement += f"Password: {client.password}\n\n"
    statement += "Transactions:\n"
    
    for transaction in client.transactions:
        statement += f"{transaction['date']} - {transaction['description']}: R${transaction['amount']}\n"
    
    return True, statement

def transfer_between_accounts(bank, source_CNPJ, password, dest_CNPJ, amount):
    source_client = bank.get_client(source_CNPJ)
    if not source_client:
        return False, "Source client not found!"
    
    dest_client = bank.get_client(dest_CNPJ)
    if not dest_client:
        return False, "Destination client not found!"
    
    if source_client.password != password:
        return False, "Incorrect password!"
    
    if source_client.balance - amount < (-1000 if source_client.account_type == "comum" else -5000):
        return False, "Insufficient balance for the transfer!"
    
    source_client.balance -= amount
    dest_client.balance += amount
    
    source_client.add_transaction("Transfer to " + dest_CNPJ, -amount)
    dest_client.add_transaction("Transfer from " + source_CNPJ, amount)
    
    return True, f"Transferred R${amount} to {dest_CNPJ}. New balance: R${source_client.balance}"
