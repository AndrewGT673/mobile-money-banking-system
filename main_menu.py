from zwg_wallet import run_zwg_wallet
from usd_wallet import run_usd_wallet


def main_menu():
    while True:
        print("=" * 40)
        print(" MOBILE MONEY BANKING SYSTEM")
        print("=" * 40)
        print("Please Select Your Currency")
        print("1. Zimbabwe Gold (ZWG)")
        print("2. United States Dollar (USD)")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_zwg_wallet()
        elif choice == "2":
            run_usd_wallet()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main_menu()