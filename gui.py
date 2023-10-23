import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, Entry, Button, OptionMenu, Text, Scrollbar, Canvas
import os
from PIL import Image, ImageTk

from data_structures import Client, Bank
from file_handling import load_clients_from_file, save_clients_to_file
from operations import add_new_client, delete_client, list_clients, debit_from_account, deposit_to_account, get_account_statement, transfer_between_accounts

bank = Bank()
load_clients_from_file(bank)

def on_new_client():
    window = Toplevel(root)
    window.title("New Client")

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

    Button(window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=20)

def on_delete_client():
    CNPJ = simpledialog.askstring("Delete Client", "Enter the CNPJ of the client to delete:")
    success, message = delete_client(bank, CNPJ)
    messagebox.showinfo("Info", message)

def on_list_clients():
    clients_data = list_clients(bank)
    messagebox.showinfo("Clients", clients_data)

def on_debit():
    CNPJ = simpledialog.askstring("Debit", "Enter your CNPJ:")
    password = simpledialog.askstring("Debit", "Enter your password:", show="*")
    amount = simpledialog.askfloat("Debit", "Enter the amount to debit:")
    success, message = debit_from_account(bank, CNPJ, password, amount)
    messagebox.showinfo("Debit", message)

def on_deposit():
    CNPJ = simpledialog.askstring("Deposit", "Enter the CNPJ of the account to deposit into:")
    amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
    success, message = deposit_to_account(bank, CNPJ, amount)
    messagebox.showinfo("Deposit", message)

def on_statement():
    CNPJ = simpledialog.askstring("Statement", "Enter your CNPJ:")
    password = simpledialog.askstring("Statement", "Enter your password:", show="*")
    success, statement = get_account_statement(bank, CNPJ, password)
    if success:
        messagebox.showinfo("Statement", statement)
    else:
        messagebox.showerror("Error", statement)

def on_transfer():
    source_CNPJ = simpledialog.askstring("Transfer", "Enter your CNPJ:")
    password = simpledialog.askstring("Transfer", "Enter your password:", show="*")
    dest_CNPJ = simpledialog.askstring("Transfer", "Enter the CNPJ of the destination account:")
    amount = simpledialog.askfloat("Transfer", "Enter the amount to transfer:")
    success, message = transfer_between_accounts(bank, source_CNPJ, password, dest_CNPJ, amount)
    messagebox.showinfo("Transfer", message)

def close_application():
    save_clients_to_file(bank)
    root.destroy()

root = tk.Tk()
root.title("Banking System")

root.attributes('-fullscreen', True)

canvas = Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

# bg_image = tk.PhotoImage(file="image/QuemPupaTem.png")

image = Image.open("image/QPM.jpg")
bg_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

btn_new_client = tk.Button(canvas, text="New Client", command=on_new_client, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 150, window=btn_new_client)

btn_delete_client = tk.Button(canvas, text="Delete Client", command=on_delete_client, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 250, window=btn_delete_client)

btn_list_clients = tk.Button(canvas, text="List Clients", command=on_list_clients, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 350, window=btn_list_clients)

btn_debit = tk.Button(canvas, text="Debit", command=on_debit, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 450, window=btn_debit)

btn_deposit = tk.Button(canvas, text="Deposit", command=on_deposit, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 550, window=btn_deposit)

btn_statement = tk.Button(canvas, text="Statement", command=on_statement, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 650, window=btn_statement)

btn_transfer = tk.Button(canvas, text="Transfer", command=on_transfer, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 750, window=btn_transfer)

btn_close = tk.Button(canvas, text="Close", command=close_application, width=20, height=2)
canvas.create_window(root.winfo_screenwidth() / 2, 850, window=btn_close)

root.mainloop()
