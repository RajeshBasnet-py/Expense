import csv
import json
from datetime import datetime

# Initialize data structures
expenses = []
budgets = {}
next_id = 1

# Helper functions
def add_expense(description, amount, category):
    global next_id
    expense = {
        "id": next_id,
        "description": description,
        "amount": amount,
        "category": category,
        "date": datetime.now()
    }
    expenses.append(expense)
    next_id += 1
    print("Expense added successfully!")

def update_expense(expense_id, description=None, amount=None, category=None):
    for expense in expenses:
        if expense["id"] == expense_id:
            if description:
                expense["description"] = description
            if amount:
                expense["amount"] = amount
            if category:
                expense["category"] = category
            print("Expense updated successfully!")
            return
    print("Expense not found.")

def delete_expense(expense_id):
    global expenses
    expenses = [expense for expense in expenses if expense["id"] != expense_id]
    print("Expense deleted successfully!")

def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return
    for expense in expenses:
        print(f"ID: {expense['id']}, Description: {expense['description']}, Amount: {expense['amount']}, Category: {expense['category']}, Date: {expense['date'].strftime('%Y-%m-%d')} ")

def view_summary():
    total = sum(expense["amount"] for expense in expenses)
    print(f"Total expenses: {total}")

def view_monthly_summary(month):
    monthly_expenses = [expense for expense in expenses if expense["date"].month == month and expense["date"].year == datetime.now().year]
    total = sum(expense["amount"] for expense in monthly_expenses)
    print(f"Total expenses for month {month}: {total}")

def set_budget(month, budget):
    budgets[month] = budget
    print(f"Budget for month {month} set to {budget}")

def check_budget(month):
    if month not in budgets:
        print("No budget set for this month.")
        return
    monthly_expenses = sum(expense["amount"] for expense in expenses if expense["date"].month == month and expense["date"].year == datetime.now().year)
    if monthly_expenses > budgets[month]:
        print(f"Warning: You have exceeded your budget for month {month} by {monthly_expenses - budgets[month]}")
    else:
        print(f"You are within your budget for month {month}")

def export_to_csv(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Description", "Amount", "Category", "Date"])
        for expense in expenses:
            writer.writerow([expense["id"], expense["description"], expense["amount"], expense["category"], expense["date"].strftime('%Y-%m-%d')])
    print(f"Expenses exported to {filename}")

def save_to_json(filename):
    data = {
        "expenses": [
            {
                "id": expense["id"],
                "description": expense["description"],
                "amount": expense["amount"],
                "category": expense["category"],
                "date": expense["date"].strftime('%Y-%m-%d')
            }
            for expense in expenses
        ],
        "budgets": budgets
    }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def load_from_json(filename):
    global expenses, budgets, next_id
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            expenses = [
                {
                    "id": expense["id"],
                    "description": expense["description"],
                    "amount": expense["amount"],
                    "category": expense["category"],
                    "date": datetime.strptime(expense["date"], '%Y-%m-%d')
                }
                for expense in data["expenses"]
            ]
            budgets = data["budgets"]
            next_id = max(expense["id"] for expense in expenses) + 1 if expenses else 1
        print(f"Data loaded from {filename}")
    except FileNotFoundError:
        print(f"{filename} not found. Starting with empty data.")
    except json.JSONDecodeError:
        print(f"Error reading {filename}. Starting with empty data.")

# Command-line interface
def main():
    load_from_json("expenses.json")  # Automatically load data on start
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. Update Expense")
        print("3. Delete Expense")
        print("4. View Expenses")
        print("5. View Summary")
        print("6. View Monthly Summary")
        print("7. Set Budget")
        print("8. Check Budget")
        print("9. Export to CSV")
        print("10. Save to JSON")
        print("11. Load from JSON")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter description: ")
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                add_expense(description, amount, category)
            except ValueError:
                print("Invalid input for amount. Please enter a number.")
        elif choice == "2":
            try:
                expense_id = int(input("Enter expense ID: "))
                description = input("Enter new description (leave blank to keep current): ")
                amount = input("Enter new amount (leave blank to keep current): ")
                amount = float(amount) if amount else None
                category = input("Enter new category (leave blank to keep current): ")
                update_expense(expense_id, description, amount, category)
            except ValueError:
                print("Invalid input for ID or amount. Please enter a number.")
        elif choice == "3":
            try:
                expense_id = int(input("Enter expense ID: "))
                delete_expense(expense_id)
            except ValueError:
                print("Invalid input for ID. Please enter a number.")
        elif choice == "4":
            view_expenses()
        elif choice == "5":
            view_summary()
        elif choice == "6":
            try:
                month = int(input("Enter month (1-12): "))
                if 1 <= month <= 12:
                    view_monthly_summary(month)
                else:
                    print("Invalid month. Please enter a value between 1 and 12.")
            except ValueError:
                print("Invalid input for month. Please enter a number.")
        elif choice == "7":
            try:
                month = int(input("Enter month (1-12): "))
                if 1 <= month <= 12:
                    budget = float(input("Enter budget: "))
                    set_budget(month, budget)
                else:
                    print("Invalid month. Please enter a value between 1 and 12.")
            except ValueError:
                print("Invalid input for month or budget. Please enter numbers.")
        elif choice == "8":
            try:
                month = int(input("Enter month (1-12): "))
                if 1 <= month <= 12:
                    check_budget(month)
                else:
                    print("Invalid month. Please enter a value between 1 and 12.")
            except ValueError:
                print("Invalid input for month. Please enter a number.")
        elif choice == "9":
            filename = input("Enter filename: ")
            export_to_csv(filename)
        elif choice == "10":
            save_to_json("expenses.json")
        elif choice == "11":
            load_from_json("expenses.json")
        elif choice == "12":
            save_to_json("expenses.json")  # Save data before exiting
            print("Exiting the program. Goodbye!")
            break  # Ends the loop and exits the program

if __name__ == "__main__":
    main()
