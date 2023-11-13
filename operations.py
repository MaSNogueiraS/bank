
from tkinter import messagebox
from data_structures import Client
import datetime


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
    
    client_list = []
    for client in bank.clients.values():
        client_list.append(f"Razao Social: {client.razao_social}, CNPJ: {client.CNPJ}, Balance: {client.balance}") 
    
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
    fee = client.calculate_debit_fee(amount)
    total_amount = amount + fee

    if client.balance - total_amount >= client.overdraft_limit:
        return True, f"Debit of {amount} successful."
    else:
        return False, "Insufficient funds or overdraft limit reached."
    
def calculate_transfer_fee(bank, source_CNPJ, amount):
    client = bank.get_client(source_CNPJ)
    if client:
        # Use the method from the Client class to calculate the fee
        fee = client.calculate_debit_fee(amount)
        return fee
    else:
        return 0  # Return 0 or handle the error as you see fit
    
def register_auto_debit(bank, CNPJ, company, amount):
    client = bank.get_client(CNPJ)
    if client:
        # Assuming 'auto_debits' is a dictionary in the Client class to store auto-debit info
        if company in client.auto_debits:
            client.auto_debits[company] += amount  # Update existing auto-debit
        else:
            client.auto_debits[company] = amount  # Add new auto-debit
        return True, f"Auto-debit of {amount} for {company} registered for CNPJ {CNPJ}."
    else:
        return False, "Client not found."
    

def register_salary(bank, CNPJ, salary_amount):
    client = bank.get_client(CNPJ)
    if client:
        client.set_salary(salary_amount)
        return True, f"Salary of {salary_amount} registered for CNPJ {CNPJ}."
    else:
        return False, "Client not found."
    

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

    # Add upcoming auto-debits and salary
    statement += "Upcoming Auto-Debits and Salary:\n"
    for company, amount in client.auto_debits.items():
        statement += f"Auto-debit to {company}: -R${amount}\n"
    if client.salary > 0:
        statement += f"Salary credit: +R${client.salary}\n\n"
    
    statement += "Transaction History:\n"
    for transaction in client.transactions:
        statement += f"{transaction['date']} - {transaction['description']}: R${transaction['amount']}\n"
    
    return True, statement



def transfer_between_accounts(bank, source_CNPJ, password, dest_CNPJ, amount):
    source_client = bank.get_client(source_CNPJ)
    dest_client = bank.get_client(dest_CNPJ)

    if source_client and dest_client and source_client.password == password:
        fee = source_client.calculate_debit_fee(amount)
        total_amount = amount + fee

        if source_client.balance - total_amount >= source_client.overdraft_limit:
            source_client.balance -= total_amount
            source_client.add_transaction(f"Transfer to {dest_CNPJ} and fee", -total_amount)

            dest_client.balance += amount
            dest_client.add_transaction(f"Transfer from {source_CNPJ}", amount)

            return True, "Transfer successful."
        else:
            return False, "Insufficient funds or overdraft limit reached."
    else:
        return False, "Invalid CNPJ or password."
    

import datetime

def process_end_of_month_transactions(bank):
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    for CNPJ, client in bank.clients.items():
        # Check if transactions for the current month and year have already been processed
        if (client.last_processed_month == current_month and client.last_processed_year == current_year):
            continue  # Skip if already processed this month and year

        # Process auto-debits
        for company, amount in client.auto_debits.items():
            if client.balance - amount >= client.overdraft_limit:
                client.balance -= amount
                client.add_transaction(f"Auto-debit to {company}", -amount)
            else:
                client.add_transaction(f"Failed auto-debit to {company}", 0)

        # Process salary
        if client.salary > 0:
            client.balance += client.salary
            client.add_transaction("Salary deposit", client.salary)

        # Update the last processed month and year
        client.last_processed_month = current_month
        client.last_processed_year = current_year


def upgrade_account(bank, CNPJ, password):
    client = bank.get_client(CNPJ)
    if not client:
        return False, "Client not found!"

    if client.password != password:
        return False, "Incorrect password!"

    upgrade_cost = 100000  # Set the upgrade cost

    if client.balance < upgrade_cost:
        return False, "Insufficient balance for account upgrade."

    if client.account_type == "Plus":
        return False, "Account is already a Plus account."

    # Deduct the upgrade cost and change the account type
    client.balance -= upgrade_cost
    client.account_type = "Plus"
    return True, "Account upgraded to Plus successfully."

