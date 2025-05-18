from expense import Expense
import calendar
import datetime


def main():
    print("Expense Tracker")
    path = "Expense_tracker/expenses.csv"
    budget = 2000

    while True:
        # Get input
        expense = user_expense()

        # Write expense to file
        save_expense(expense, path)

        # Read file and summarize expenses
        summarize_expense(path, budget)

        # Check if the user wants to quit
        should_quit = input("Type 'quit' to stop or press Enter to continue: ").strip().lower()
        if should_quit == 'quit':
            print("Exiting Expense Tracker. Goodbye!")
            break


def user_expense():
    print(f"Enter your expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = ["Food", "Rent", "Fun", "Work", "Misc"]

    while True:
        print(f"Select expense category from the following:")
        for i, category in enumerate(expense_categories):
            print(f"{i+1}. {category}")

        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input(f"Enter the number of your selected category{value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name = expense_name, category = selected_category, amount = expense_amount)
            return new_expense
        else:
            print("Invalid, try again")


def save_expense(expense: Expense, path):
    with open(path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expense(path, budget):
    print(f"Summarized expense")
    expenses: list[Expense] = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(name=expense_name, amount=float(expense_amount), category=expense_category)
            expenses.append(line_expense)

    for line_expense in expenses:
        print(f"Name: {line_expense.name}, Amount: {line_expense.amount}, Category: {line_expense.category}")

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses by Category")
    for key, amount in amount_by_category.items():
        print(f"{key}:${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"Total spent ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"Remaining budget ${remaining_budget:.2f}")

    now = datetime.datetime.now()

    days_in_month = calendar.monthrange(now.year, now.month)[1]

    remaining_days = days_in_month - now.day

    print("Remaining days in the month:", remaining_days)

    daily_budget = remaining_budget/remaining_days

    print(f"Budget per day ${daily_budget:.2f}")
if __name__ == "__main__":
    main()
