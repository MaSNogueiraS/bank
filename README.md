# Bank
A college project.

## How to Use
Run `gui.py` to access the bank system. Ensure all necessary files are in the same folder. These include: 
- `data_structures.py`: Creates client and bank classes for system functionality and data handling.
- `file_handling.py`: Manages the `.json` file containing bank data, creating it if necessary.
- `operations.py`: Hosts main functions for background processing, data display in GUI, and input handling.

## Functions

### Add New Client
Click the "New Client" button to open a window for entering details like Company Name (or Razão Social), CNPJ, account type (common or special), initial balance, and password. A confirmation message appears upon successful addition. Attempting to add an existing CNPJ results in an error.

**Note:** The system checks for CNPJ uniqueness but not for empty entries.

### Delete Client
Accessible to all users (ideally for bank management only), this function prompts for the CNPJ of the account to be deleted.

**Note:** Implement additional security measures.

### List Clients
Displays a list of all registered clients, including name, CNPJ, and current balance.

**Note:** The display quality needs improvement.

### Debit
Requires your CNPJ, password, and the debit amount. A fee is applied based on account type.

**Note:** The debit fee isn't currently displayed; consider showing it or removing it altogether.

### Register Salary
Enter your CNPJ and the salary amount to be automatically deposited at month-end.

**Note:** No salary confirmation is required. The system automatically processes debts and deposits at month-end, avoiding duplication.

### Register Auto-Debit
Enter your CNPJ, the payee company (e.g., Netflix), and the monthly payment amount.

**Note:** Deletions of auto-debits or salaries must be done manually in the `.json` file.

### Deposit
Simply enter the CNPJ and deposit amount.

### Statement
After submitting your CNPJ and password, this function displays account details, including transactions, salaries, and auto-debts, for financial tracking.

**Note:** Data is lost if the `.json` file is deleted. No data filtering is currently implemented.

### Transfer
Enter your CNPJ, password, recipient's CNPJ, and transfer amount. A fee is displayed for confirmation.

### Upgrade Account
Change your account type, with a default upgrade cost set in `operations.py`.

**Note:** This feature is more for conceptual exploration.

### Close
Closes the program and saves data.

**Note:** While all operations are saved in real-time to the `.json` file, this acts as an additional confirmation step.

## Author's Notes

### Positives
The project's execution was successful, especially integrating functionalities with Tkinter. The creation of a basic logo adds a unique touch.

### Negatives
Improvements are possible, like centralizing windows, enhancing the client list display, fixing close button functionalities, implementing user feedback and customization options, and addressing the lack of empty CNPJ checks.

## Contact the Author

Mateus Scarpelli Nogueira da Silva
Email: mateus.scarpelli03@gmail.com
github: MaSNogueiraS