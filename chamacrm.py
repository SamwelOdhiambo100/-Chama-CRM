import json
import os

def chama_manager():
    """Manages chama (informal savings group) operations with persistent storage."""

    data_file = "chama_data.json"

    def load_data():
        """Loads data from the JSON file."""
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                return json.load(f)
        else:
            return {"members": {}, "contributions": []}

    def save_data(data):
        """Saves data to the JSON file."""
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)

    data = load_data()
    members = data["members"]
    contributions = data["contributions"]

    def add_member(name):
        """Adds a new member to the chama."""
        if name not in members:
            members[name] = 0
            print(f"{name} added to the chama.")
            save_data(data)
        else:
            print(f"{name} is already a member.")

    def record_contribution(name, amount, date):
        """Records a member's contribution."""
        if name in members:
            members[name] += amount
            contributions.append({"member": name, "amount": amount, "date": date})
            print(f"{name} contributed {amount}. New balance: {members[name]}")
            save_data(data)
        else:
            print(f"{name} is not a member.")

    def view_balance(name):
        """Views a member's balance."""
        if name in members:
            print(f"{name}'s balance: {members[name]}")
        else:
            print(f"{name} is not a member.")

    def view_all_balances():
        """Views all members balances"""
        if not members:
            print("No members in the chama.")
        else:
            for name, balance in members.items():
                print(f"{name}'s balance: {balance}")

    def display_menu():
        """Displays the menu of options."""
        print("\nChama Manager Menu:")
        print("1. Add Member")
        print("2. Record Contribution")
        print("3. View Balance")
        print("4. View All Balances")
        print("5. Exit")

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter member name: ")
            add_member(name)
        elif choice == "2":
            name = input("Enter member name: ")
            amount = float(input("Enter contribution amount: "))
            date = input("Enter contribution date: ")
            record_contribution(name, amount, date)
        elif choice == "3":
            name = input("Enter member name: ")
            view_balance(name)
        elif choice == "4":
            view_all_balances()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    chama_manager()

