import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button, OptionMenu, Text, Scrollbar, Canvas
import os
from PIL import Image, ImageTk

from data_structures import Client, Bank
from file_handling import load_clients_from_file, save_clients_to_file
from operations import add_new_client, delete_client, list_clients, debit_from_account, deposit_to_account, get_account_statement, transfer_between_accounts, register_salary, register_auto_debit, calculate_transfer_fee, process_end_of_month_transactions, upgrade_account
bank = Bank()
process_end_of_month_transactions(bank)
load_clients_from_file(bank)

def centralize_window(window):
    window.update()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def on_new_client():
    window = Toplevel(root)
    window.title("New Client")
    window.geometry("500x500")

    Label(window, text="Company Name (Razão Social):").grid(row=0, column=0, padx=10, pady=10)
    razao_social_entry = Entry(window)
    razao_social_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(window, text="CNPJ:").grid(row=1, column=0, padx=10, pady=10)
    CNPJ_entry = Entry(window)
    CNPJ_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(window, text="Account Type:").grid(row=2, column=0, padx=10, pady=10)
    account_type_var = tk.StringVar(window)
    account_type_var.set("comum")
    account_types = ["comum", "especial"]
    account_type_dropdown = OptionMenu(window, account_type_var, *account_types)
    account_type_dropdown.grid(row=2, column=1, padx=10, pady=10)

    Label(window, text="Initial Balance:").grid(row=3, column=0, padx=10, pady=10)
    initial_balance_entry = Entry(window)
    initial_balance_entry.grid(row=3, column=1, padx=10, pady=10)

    Label(window, text="Password:").grid(row=4, column=0, padx=10, pady=10)
    password_entry = Entry(window, show="*")
    password_entry.grid(row=4, column=1, padx=10, pady=10)

    def submit():
        razao_social = razao_social_entry.get()
        CNPJ = CNPJ_entry.get()
        account_type = account_type_var.get()
        initial_balance = float(initial_balance_entry.get()) if initial_balance_entry.get() else 0.0
        password = password_entry.get()

        success, message = add_new_client(bank, razao_social, CNPJ, account_type, initial_balance, password)
        messagebox.showinfo("Info", message)
        if success:
            window.destroy()

    submit_button = Button(window, text="Submit", command=submit)
    submit_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
    centralize_window(window)

def on_delete_client():
    CNPJ = simpledialog.askstring("Delete Client", "Enter the CNPJ of the client to delete:")
    if not CNPJ:
        return
    success, message = delete_client(bank, CNPJ)
    messagebox.showinfo("Info", message)

def on_auto_debit():
    auto_debit_window = Toplevel(root)
    auto_debit_window.title("Auto-Debit Registration")

    # Fields for CNPJ, company, and amount
    Label(auto_debit_window, text="CNPJ:").grid(row=0, column=0)
    CNPJ_entry = Entry(auto_debit_window)
    CNPJ_entry.grid(row=0, column=1)

    Label(auto_debit_window, text="Company:").grid(row=1, column=0)
    company_entry = Entry(auto_debit_window)
    company_entry.grid(row=1, column=1)

    Label(auto_debit_window, text="Amount:").grid(row=2, column=0)
    amount_entry = Entry(auto_debit_window)
    amount_entry.grid(row=2, column=1)

    def submit_auto_debit():
        CNPJ = CNPJ_entry.get()
        company = company_entry.get()
        amount = float(amount_entry.get()) if amount_entry.get() else 0.0
        success, message = register_auto_debit(bank, CNPJ, company, amount)
        messagebox.showinfo("Info", message)
        if success:
            auto_debit_window.destroy()

    Button(auto_debit_window, text="Submit", command=submit_auto_debit).grid(row=3, column=0, columnspan=2)


def on_auto_debit():
    window = Toplevel(root)
    window.title("Auto Debit Registration")

    # Example fields: CNPJ, company, amount
    Label(window, text="CNPJ:").grid(row=0, column=0)
    CNPJ_entry = Entry(window)
    CNPJ_entry.grid(row=0, column=1)

    Label(window, text="Company:").grid(row=1, column=0)
    company_entry = Entry(window)
    company_entry.grid(row=1, column=1)

    Label(window, text="Amount:").grid(row=2, column=0)
    amount_entry = Entry(window)
    amount_entry.grid(row=2, column=1)

    def submit_auto_debit():
        CNPJ = CNPJ_entry.get()
        company = company_entry.get()
        amount = float(amount_entry.get()) if amount_entry.get() else 0.0
        # Call the function from operations.py to register the auto-debit
        success, message = register_auto_debit(bank, CNPJ, company, amount)
        messagebox.showinfo("Info", message)
        if success:
            window.destroy()

    Button(window, text="Submit", command=submit_auto_debit).grid(row=3, column=0, columnspan=2)


def on_list_clients():
    clients_data = list_clients(bank)

    # Estimate the width based on the longest client string
    # max_length = max(len(client_info) for client_info in clients_data)
    # estimated_width = min(1200, max(400, max_length * 7))  # Adjust the multiplier as needed # Do not work as intended
    estimated_width = 800

    client_window = Toplevel(root)
    client_window.title("List of Clients")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (estimated_width // 2)
    y = (screen_height // 2) - 300  
    client_window.geometry(f"{estimated_width}x600+{x}+{y}")  

    text = Text(client_window, wrap="word")
    scrollbar = Scrollbar(client_window, command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)

    text.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    separator = "-" * 100  # Separator to make the output more readable
    if type(clients_data) != str:
        for client_info in clients_data:
            text.insert("end", client_info + "\n" + separator + "\n\n")
        text.config(state="disabled")
    else:
        text.insert("end", "Error: "+clients_data)
        text.config(state="disabled")




def on_debit():
    CNPJ = simpledialog.askstring("Debit", "Enter your CNPJ:")
    if not CNPJ:
        return
    password = simpledialog.askstring("Debit", "Enter your password:", show="*")
    if not password:
        return
    amount = simpledialog.askfloat("Debit", "Enter the amount to debit:")
    if not amount:
        return
    success, message = debit_from_account(bank, CNPJ, password, amount)
    messagebox.showinfo("Debit", message)

def on_deposit():
    CNPJ = simpledialog.askstring("Deposit", "Enter the CNPJ of the account to deposit into:")
    if not CNPJ:
        return
    amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
    if not amount:
        return
    success, message = deposit_to_account(bank, CNPJ, amount)
    messagebox.showinfo("Deposit", message)

def on_statement():
    CNPJ = simpledialog.askstring("Statement", "Enter your CNPJ:")
    if not CNPJ:
        return
    password = simpledialog.askstring("Statement", "Enter your password:", show="*")
    if not password:
        return
    success, statement = get_account_statement(bank, CNPJ, password)
    if success:
        messagebox.showinfo("Statement", statement)
    else:
        messagebox.showerror("Error", statement)

def on_transfer():
    source_CNPJ = simpledialog.askstring("Transfer", "Enter your CNPJ:")
    if not source_CNPJ:
        return
    password = simpledialog.askstring("Transfer", "Enter your password:", show="*")
    if not password:
        return
    dest_CNPJ = simpledialog.askstring("Transfer", "Enter the CNPJ of the destination account:")
    if not dest_CNPJ:
        return
    amount = simpledialog.askfloat("Transfer", "Enter the amount to transfer:")

    fee = calculate_transfer_fee(bank, source_CNPJ, amount)
    total_amount = amount + fee

    def perform_transfer():
        success, message = transfer_between_accounts(bank, source_CNPJ, password, dest_CNPJ, amount)
        messagebox.showinfo("Transfer", message)

    confirm_window = Toplevel(root)
    confirm_window.title("Confirm Transfer")
    Label(confirm_window, text=f"Transfer Amount: {amount}\nFee: {fee}\nTotal: {total_amount}").grid(row=0, column=0, columnspan=2)
    Button(confirm_window, text="Confirm", command=lambda: [perform_transfer(), confirm_window.destroy()]).grid(row=1, column=0)
    Button(confirm_window, text="Cancel", command=confirm_window.destroy).grid(row=1, column=1)

def on_salary():
    salary_window = Toplevel(root)
    salary_window.title("Salary Registration")

    Label(salary_window, text="CNPJ:").grid(row=0, column=0)
    CNPJ_entry = Entry(salary_window)
    CNPJ_entry.grid(row=0, column=1)

    Label(salary_window, text="Salary Amount:").grid(row=1, column=0)
    amount_entry = Entry(salary_window)
    amount_entry.grid(row=1, column=1)

    def submit_salary():
        CNPJ = CNPJ_entry.get()
        amount = float(amount_entry.get()) if amount_entry.get() else 0.0
        success, message = register_salary(bank, CNPJ, amount)
        messagebox.showinfo("Info", message)
        if success:
            salary_window.destroy()

    Button(salary_window, text="Submit", command=submit_salary).grid(row=2, column=0, columnspan=2)


def on_account_upgrade():
    CNPJ = simpledialog.askstring("Account Upgrade, 100k cost", "Enter your CNPJ:")
    password = simpledialog.askstring("Account Upgrade, 100k cost", "Enter your password:", show="*")
    success, message = upgrade_account(bank, CNPJ, password)
    messagebox.showinfo("Account Upgrade", message)

def close_application():
    save_clients_to_file(bank)
    root.destroy()

root = tk.Tk()
root.title("Banking System")

root.attributes('-fullscreen', True)

canvas = Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

# bg_image = tk.PhotoImage(file="image/QuemPupaTem.png")

image = Image.open("image/QuemPoupaTemRevisado.png")
bg_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)


btn_new_client = tk.Button(canvas, text="New Client", command=on_new_client, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 250, window=btn_new_client)

btn_delete_client = tk.Button(canvas, text="Delete Client", command=on_delete_client, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 300, window=btn_delete_client)

btn_list_clients = tk.Button(canvas, text="List Clients", command=on_list_clients, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 350, window=btn_list_clients)

btn_debit = tk.Button(canvas, text="Debit", command=on_debit, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 400, window=btn_debit)

btn_salary = tk.Button(root, text="Register Salary", command=on_salary, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 450, window=btn_salary)

btn_auto_debit = tk.Button(root, text="Register Auto-Debit", command=on_auto_debit, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 500, window=btn_auto_debit)

btn_deposit = tk.Button(canvas, text="Deposit", command=on_deposit, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 550, window=btn_deposit)

btn_statement = tk.Button(canvas, text="Statement", command=on_statement, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 600, window=btn_statement)

btn_transfer = tk.Button(canvas, text="Transfer", command=on_transfer, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 650, window=btn_transfer)

btn_close = tk.Button(canvas, text="Close", command=close_application, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 800, window=btn_close)

btn_upgrade_account = tk.Button(canvas, text="Upgrade Account", command=on_account_upgrade, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 700, window=btn_upgrade_account)

root.mainloop()


