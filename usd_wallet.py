import json
import os
from datetime import datetime
# File for saving USD wallet information
DATA_FILE = "usd_wallet_data.json"
# Default USD account information
DEFAULT_DATA = {
    "pin": "1234",
    "balance": 500.00,
    "history": []
}
# Load saved account information
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Could not read saved data.")
    return DEFAULT_DATA.copy()
# Save account information
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
# PIN authentication
def login(data):

    print("          USD WALLET LOGIN")

    attempts = 3
    while attempts > 0:
        pin = input("Please enter your PIN: ")
        if pin == data["pin"]:
            print("Login successful.")
            return True
        attempts -= 1
        print("Incorrect PIN.")
        if attempts > 0:
            print("Attempts remaining:", attempts)
    print("Access denied.")
    return False
# Get a valid positive amount
def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
# Validate mobile number
def validate_mobile_number(number):
    return (
        number.isdigit()
        and len(number) == 10
        and number.startswith("07")
    )
# Add transaction to history
def add_transaction(data, transaction_type, amount):
    transaction = {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "type": transaction_type,
        "amount": amount,
        "balance": data["balance"]
    }
    data["history"].append(transaction)
# Send money
def send_money(data):
    while True:
        print("\n------------- SEND MONEY -------------")
        print("1. Send to Registered")
        print("2. Back to USD Wallet")
        choice = input("Enter your choice: ")
        if choice == "1":
            recipient = input("Enter recipient mobile number: ")
            if not validate_mobile_number(recipient):
                print("Invalid mobile number.")
                continue
            amount = get_amount()
            if amount > data["balance"]:
                print("Transaction failed.")
                print("Insufficient balance.")
                continue
            data["balance"] -= amount
            add_transaction(data, "Send Money", amount)
            save_data(data)
            print("\nTransaction successful.")
            print("Amount Sent: USD", f"{amount:.2f}")
            print("Recipient:", recipient)
            print("New Balance: USD", f"{data['balance']:.2f}")
        elif choice == "2":
            break
        else:
            print("Invalid choice.")
# Buy airtime
def buy_airtime(data):
    print("\n------------- BUY AIRTIME -------------")
    mobile = input("Enter mobile number: ")
    if not validate_mobile_number(mobile):
        print("Invalid mobile number.")
        return
    amount = get_amount()
    if amount > data["balance"]:
        print("Transaction failed.")
        print("Insufficient balance.")
        return
    data["balance"] -= amount
    add_transaction(data, "Airtime", amount)
    save_data(data)
    print("\nAirtime purchase successful.")
    print("Mobile Number:", mobile)
    print("Airtime Amount: USD", f"{amount:.2f}")
    print("New Balance: USD", f"{data['balance']:.2f}")
# Buy data bundle
def buy_data_bundle(data):
    print("\n------------- DATA BUNDLES -------------")
    print("1. 100 MB - USD 0.50")
    print("2. 500 MB - USD 1.00")
    print("3. 1 GB   - USD 2.00")
    print("4. 2 GB   - USD 3.50")
    print("5. 5 GB   - USD 7.00")
    print("6. Back")
    bundles = {
        "1": ("100 MB", 0.50),
        "2": ("500 MB", 1.00),
        "3": ("1 GB", 2.00),
        "4": ("2 GB", 3.50),
        "5": ("5 GB", 7.00)
    }
    choice = input("Select bundle: ")
    if choice == "6":
        return
    if choice not in bundles:
        print("Invalid bundle choice.")
        return
    bundle_name, price = bundles[choice]
    mobile = input("Enter mobile number: ")
    if not validate_mobile_number(mobile):
        print("Invalid mobile number.")
        return
    if price > data["balance"]:
        print("Transaction failed.")
        print("Insufficient balance.")
        return
    data["balance"] -= price
    add_transaction(data, "Data Bundle - " + bundle_name, price)
    save_data(data)
    print("\nData bundle purchase successful.")
    print("Bundle:", bundle_name)
    print("Mobile Number:", mobile)
    print("Price: USD", f"{price:.2f}")
    print("New Balance: USD", f"{data['balance']:.2f}")
# Airtime and bundles menu
def airtime_and_bundles(data):
    while True:
        print("\n--------- AIRTIME AND BUNDLES ---------")
        print("1. Buy Airtime")
        print("2. Buy Data Bundle")
        print("3. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            buy_airtime(data)
        elif choice == "2":
            buy_data_bundle(data)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
# Check balance
def check_balance(data):
    print("\n------------- CHECK BALANCE -------------")
    print("Current Balance: USD", f"{data['balance']:.2f}")
# Transaction history
def transaction_history(data):
    print("\n============= TRANSACTION HISTORY =============")
    if len(data["history"]) == 0:
        print("No transactions found.")
        return
    print(
        f"{'Date':<18}"
        f"{'Type':<25}"
        f"{'Amount':<15}"
        f"{'Balance':<15}"
    )
    print("-" * 73)
    for transaction in data["history"]:
        print(
            f"{transaction['date']:<18}"
            f"{transaction['type']:<25}"
            f"USD {transaction['amount']:<10.2f}"
            f"USD {transaction['balance']:<10.2f}"
        )
# USD wallet menu
def usd_wallet(data):
    while True:
        print("\n========================================")
        print("             USD WALLET")
        print("========================================")
        print("1. Send Money")
        print("2. Airtime and Bundles")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            send_money(data)
        elif choice == "2":
            airtime_and_bundles(data)
        elif choice == "3":
            check_balance(data)
        elif choice == "4":
            transaction_history(data)
        elif choice == "5":
            print("You have been logged out.")
            break
        else:
            print("Invalid choice.")
# Main program
def run_usd_wallet():
    """Entry point called by main_menu.py."""
    data = load_data()

    if login(data):
        usd_wallet(data)


def main():
    """Keep direct execution of this module working."""
    run_usd_wallet()

if __name__ == "__main__":
    main()
