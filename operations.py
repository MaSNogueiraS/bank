
from tkinter import messagebox
from data_structures import Client
import datetime

# Here is where all the actual calculations and process of inputs happen
# Basically it reads the client data, and with the input it perform a function

#this add the new client
def add_new_client(bank, razao_social, CNPJ, account_type, initial_balance, password):
    #This checks if the cnpj already exists in the clients bank
    if CNPJ in bank.clients:
        return False, "Client with this CNPJ already exists!"
    
    client = Client(razao_social, CNPJ, account_type, initial_balance, password)
    bank.add_client(client)
    return True, "Client added successfully!"

#this one deletes a client
def delete_client(bank, CNPJ):
    if CNPJ not in bank.clients:
        return False, "No client with this CNPJ found!"
    
    del bank.clients[CNPJ]
    return True, "Client deleted successfully!"

#This one list the clients
def list_clients(bank):
    if not bank.clients:
        return "No clients to display."
    
    client_list = []
    #because i save the clients this way i can check the type of what is return to perform differnts displays, the way i did in the beggining was a mess, you can check in my git MaSNogueiraS on the bank rep, dev branch, see the comits history
    for client in bank.clients.values():
        client_list.append(f"Razao Social: {client.razao_social}, CNPJ: {client.CNPJ}, Balance: {client.balance}") 
    
    return client_list

#This debits from an account
def debit_from_account(bank, CNPJ, password, amount):
    client = bank.get_client(CNPJ)
    if not client:
        return False, "Client not found!"
    
    if client.password != password:
        return False, "Incorrect password!"
    
    # here i calculate the fee based on the ammount of money to debit and the account type
    fee_percentage = 0.05 if client.account_type == "comum" else 0.03
    total_amount = amount + (amount * fee_percentage)

    #This checks the limits for the account type, so it do not pass the minimum an account can have
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
    
#this function is used by the gui to display the fee for the transfer so the client can confirm it our cancel if the fee is to high
def calculate_transfer_fee(bank, source_CNPJ, amount):
    client = bank.get_client(source_CNPJ)
    if client:
        fee = client.calculate_debit_fee(amount)
        return fee
    else:
        return 0  # Return 0 if client not found
    
#This register in the client an debt, with the name of the company to debt
    
def register_auto_debit(bank, CNPJ, company, amount):
    client = bank.get_client(CNPJ)
    if client:
        if company in client.auto_debits:
            client.auto_debits[company] += amount  
        else:
            client.auto_debits[company] = amount  
        return True, f"Auto-debit of {amount} for {company} registered for CNPJ {CNPJ}."
    else:
        return False, "Client not found."
    

#This just add a salary that will be add at the end of the month
def register_salary(bank, CNPJ, salary_amount):
    client = bank.get_client(CNPJ)
    if client:
        client.set_salary(salary_amount)
        return True, f"Salary of {salary_amount} registered for CNPJ {CNPJ}."
    else:
        return False, "Client not found."
    

#this deposit to the account
def deposit_to_account(bank, CNPJ, amount):
    client = bank.get_client(CNPJ)
    if not client:
        return False, "Client not found!"
    
    client.balance += amount
    #also, this function, that i created in the client class, is the one that writes the moviments in the account, it is used in other parts of the codes as well, to keep track of things
    client.add_transaction("Deposit", amount)
    
    return True, f"Deposited R${amount}. New balance: R${client.balance}"

#This return the account statement to be displayed in the gui
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

    statement += "Upcoming Auto-Debits and Salary:\n"
    for company, amount in client.auto_debits.items():
        statement += f"Auto-debit to {company}: -R${amount}\n"
    if client.salary:
        if client.salary > 0:
            statement += f"Salary credit: +R${client.salary}\n\n"
    
    statement += "Transaction History:\n"
    for transaction in client.transactions:
        statement += f"{transaction['date']} - {transaction['description']}: R${transaction['amount']}\n"
    
    return True, statement
#statement could be a list, i made this way because it was the way i did everything, the client list was a str hehe (have to mod it :p)


# this transfer between the accounts, use the calculos of the fee i mention earlyer
def transfer_between_accounts(bank, source_CNPJ, password, dest_CNPJ, amount):
    source_client = bank.get_client(source_CNPJ)
    dest_client = bank.get_client(dest_CNPJ)
    # in the gui will be a confirmation 
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
    
#This function made the debits and salary work, i know that it probably wont be tested but it checks the day and then chack all the clients debits and salaries, then it perform the intended operations and save on the client the month and year so it perform the operations only one time
def process_end_of_month_transactions(bank):
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    for CNPJ, client in bank.clients.items():
        if (client.last_processed_month == current_month and client.last_processed_year == current_year):
            continue  

        for company, amount in client.auto_debits.items():
            if client.balance - amount >= client.overdraft_limit:
                client.balance -= amount
                client.add_transaction(f"Auto-debit to {company}", -amount)
            else:
                client.add_transaction(f"Failed auto-debit to {company}", 0)

        if client.salary > 0:
            client.balance += client.salary
            client.add_transaction("Salary deposit", client.salary)
        #this sets the month and year
        client.last_processed_month = current_month
        client.last_processed_year = current_year


#This upgrades the account type
def upgrade_account(bank, CNPJ, password):
    client = bank.get_client(CNPJ)
    if not client:
        return False, "Client not found!"

    if client.password != password:
        return False, "Incorrect password!"
    #you can change the cost here 
    upgrade_cost = 100000  

    if client.balance < upgrade_cost:
        return False, "Insufficient balance for account upgrade."

    if client.account_type == "Plus":
        return False, "Account is already a Plus account."

    client.balance -= upgrade_cost
    client.account_type = "Plus"
    client.add_transaction("Account upgrade", -upgrade_cost)
    return True, "Account upgraded to Plus successfully."

# So basically the real code is here, therefore it depends on the other parts i consider this the most important part