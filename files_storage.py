import json
import os
from datetime import datetime

# File names for persistence
BALANCE_FILE = "balances.txt"
HISTORY_FILE = "history.txt"

# Initial Data
zwg_balance = 1000.00
usd_balance = 500.00
transactions = [] # list of dicts

# === FILE HANDLING ===
def load_data():
    global zwg_balance, usd_balance, transactions
    try:
        if os.path.exists(BALANCE_FILE):
            with open(BALANCE_FILE, "r") as f:
                lines = f.readlines()
                zwg_balance = float(lines[0].strip())
                usd_balance = float(lines[1].strip())
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                for line in f:
                    transactions.append(eval(line.strip()))
    except:
        pass # If files don't exist, use default balances

def save_data():
    try:
        with open(BALANCE_FILE, "w") as f:
            f.write(f"{zwg_balance}\n{usd_balance}\n")
        with open(HISTORY_FILE, "w") as f:
            for t in transactions:
                f.write(f"{t}\n")
    except Exception as e:
        print(f"Error saving data: {e}")

def add_transaction(t_type, amount, currency, balance):
    date = datetime.now().strftime("%d/%m/%y")
    transactions.append({
        "date": date,
        "type": t_type,
        "amount": amount,
        "currency": currency,
        "balance": balance
    })
    save_data()


# === ZWG WALLET FILE HANDLING ===
# These functions are used by zwg_wallet.py.  They are separate from the
# original balances/history files above, so the two storage formats do not
# overwrite one another.
ZWG_DATA_FILE = "zwg_wallet_data.json"
ZWG_DEFAULT_DATA = {
    "balance": 1000.00,
    "history": []
}


def load_zwg_wallet_data():
    """Return saved ZWG wallet data, or the original default values."""
    if os.path.exists(ZWG_DATA_FILE):
        try:
            with open(ZWG_DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Could not read saved ZWG wallet data.")

    return {
        "balance": ZWG_DEFAULT_DATA["balance"],
        "history": []
    }


def save_zwg_wallet_data(data):
    """Save ZWG wallet data supplied by zwg_wallet.py."""
    with open(ZWG_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
