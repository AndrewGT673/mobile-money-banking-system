from datetime import datetime

from files_storage import load_zwg_wallet_data, save_zwg_wallet_data


#Initial Variables

PIN = "3267"

ZWG_balance = 1000.00

transactions = []

#Login Function



def login():
    attempts = 3

    while attempts > 0:
        pin = input("Please enter your PIN: ")

        if pin == PIN:
            print("Login successful.")
            return True

        attempts -= 1
        print(f"Incorrect PIN. Attempts left: {attempts}")

    return False


#Check balance function



def check_balance(currency, balance):
    print("\n===== BALANCE =====")
    print(f"{currency} Balance: {currency} {balance:.2f}")


#Send Money Function


def send_money(currency, balance):
    try:
        number = input("Enter recipient mobile number: ")

        if len(number) != 10 or not number.isdigit():
            print("Invalid mobile number.")
            return balance

        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return balance

        if amount > balance:
            print("Insufficient funds.")
            return balance

        balance -= amount

        transaction = (
            f"{datetime.now().strftime('%d/%m/%Y')} | "
            f"Send Money | {currency} {amount:.2f} | "
            f"Balance {currency} {balance:.2f}"
        )

        transactions.append(transaction)

        print("\nTransaction successful.")
        print(f"Amount Sent: {currency} {amount:.2f}")
        print(f"Recipient: {number}")
        print(f"New Balance: {currency} {balance:.2f}")

        return balance

    except ValueError:
        print("Invalid amount.")
        return balance


#Buy Airtime



def buy_airtime(currency, balance):
    try:
        number = input("Enter mobile number: ")
        amount = float(input("Enter airtime amount: "))

        if amount <= 0:
            print("Invalid amount.")
            return balance

        if amount > balance:
            print("Insufficient balance.")
            return balance

        balance -= amount

        transaction = (
            f"{datetime.now().strftime('%d/%m/%Y')} | "
            f"Airtime | {currency} {amount:.2f} | "
            f"Balance {currency} {balance:.2f}"
        )

        transactions.append(transaction)

        print("Airtime purchased successfully.")

        return balance

    except ValueError:
        print("Invalid amount.")
        return balance


def transaction_history(history):
    """Display the ZWG wallet transaction history."""
    print("\n===== TRANSACTION HISTORY =====")
    if not history:
        print("No transactions found.")
        return

    for transaction in history:
        print(transaction)


def zwg_wallet(data):
    """Run the ZWG wallet menu using the original wallet functions."""
    balance = data["balance"]
    global transactions
    transactions = data["history"]

    while True:
        print("\n========================================")
        print("             ZWG WALLET")
        print("========================================")
        print("1. Send Money")
        print("2. Buy Airtime")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            balance = send_money("ZWG", balance)
            data["balance"] = balance
            data["history"] = transactions
            save_zwg_wallet_data(data)
        elif choice == "2":
            balance = buy_airtime("ZWG", balance)
            data["balance"] = balance
            data["history"] = transactions
            save_zwg_wallet_data(data)
        elif choice == "3":
            check_balance("ZWG", balance)
        elif choice == "4":
            transaction_history(transactions)
        elif choice == "5":
            print("You have been logged out.")
            break
        else:
            print("Invalid choice.")


def run_zwg_wallet():
    """Entry point called by main_menu.py."""
    data = load_zwg_wallet_data()
    if login():
        zwg_wallet(data)


if __name__ == "__main__":
    run_zwg_wallet()
