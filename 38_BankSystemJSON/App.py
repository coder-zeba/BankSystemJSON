import random
import time
import json
import os


class BankSystem:
    class Account:
        def __init__(self, account_number, name, balance=0.0):
            self.account_number = account_number
            self.name = name
            self.balance = balance

    def __init__(self):
        self.file_name = "accounts.json"
        self.accounts = []
        self.load_accounts()

    def load_accounts(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as file:
                    data = json.load(file)

                    for acc in data:
                        account = self.Account(
                            acc["account_number"],
                            acc["name"],
                            acc["balance"])
                        self.accounts.append(account)
            except (json.JSONDecodeError, FileNotFoundError):
                self.accounts = []
        self.total_accounts = len(self.accounts)

    def save_accounts(self):
        data = []
        for acc in self.accounts:
            data.append({
                "account_number": acc.account_number,
                "name": acc.name,
                "balance": acc.balance
            })
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def find_account(self, acc_no):
        for i in range(self.total_accounts):
            if self.accounts[i].account_number == acc_no:
                return i
        return -1

    def generate_account_number(self):
        while True:
            acc_no = random.randint(10000000, 99999999)
            exists = False

            for acc in self.accounts:
                if acc.account_number == acc_no:
                    exists = True
                    break

            if not exists:
                return acc_no

    def create_account(self):
        if self.total_accounts >= 1000:
            print("Bank account storage full.")
            return

        name = input("Enter candidate name: ")

        new_acc_no = self.generate_account_number()

        new_account = self.Account(new_acc_no, name, 0.0)
        self.accounts.append(new_account)
        self.total_accounts += 1
        self.save_accounts()

        print("\nAccount created successfully!")
        print("Account Holder Name :", new_account.name)
        print("Account Number      :", new_account.account_number)
        print("Balance             : Rs.", new_account.balance)

    def view_account(self):
        acc_no = int(input("Enter account number: "))

        i = self.find_account(acc_no)
        if i == -1:
            print("Account not found.")
            return

        account = self.accounts[i]
        print("\n******** Account Details ********")
        print("Account Holder Name :", account.name)
        print("Account Number      :", account.account_number)
        print("Balance             : Rs.", account.balance)

    def deposit(self):
        acc_no = int(input("Enter account number: "))
        i = self.find_account(acc_no)

        if i == -1:
            print("Account not found.")
            return

        amount = float(input("Enter amount to deposit: "))

        if amount <= 0:
            print("Invalid amount.")
            return

        self.accounts[i].balance += amount
        self.save_accounts()

        print(f"Rs. {amount} deposited successfully.")
        print("Updated balance: Rs.", self.accounts[i].balance)

    def withdraw(self):
        acc_no = int(input("Enter account number: "))
        i = self.find_account(acc_no)

        if i == -1:
            print("Account not found.")
            return

        amount = float(input("Enter amount to withdraw: "))

        if amount <= 0:
            print("Invalid amount.")
            return

        if amount > self.accounts[i].balance:
            print("Insufficient balance.")
            return

        self.accounts[i].balance -= amount
        self.save_accounts()

        print(f"Rs. {amount} withdrawn successfully.")
        print("Remaining balance: Rs.", self.accounts[i].balance)

    def show_all_accounts(self):
        if self.total_accounts == 0:
            print("No accounts created yet.")
            return

        print("\n===== All Bank Accounts =====")
        for i in range(self.total_accounts):
            account = self.accounts[i]
            print(f"\nAccount {i + 1}")
            print("Name           :", account.name)
            print("Account Number :", account.account_number)
            print("Balance        : Rs.", account.balance)


random.seed(time.time())

bank = BankSystem()

while True:
    print("\n********** Banking Management System **********")
    print("1. Open New Account")
    print("2. View Account Details")
    print("3. Deposit Amount")
    print("4. Withdraw Amount")
    print("5. Show All Accounts")
    print("6. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        bank.create_account()
    elif choice == 2:
        bank.view_account()
    elif choice == 3:
        bank.deposit()
    elif choice == 4:
        bank.withdraw()
    elif choice == 5:
        bank.show_all_accounts()
    elif choice == 6:
        print("Logged out successfully.")
        break
    else:
        print("Invalid choice.")