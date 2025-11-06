import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.expenses = []
        self.categories = ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Other"]
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from CSV file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Convert amount to float
                        row['amount'] = float(row['amount'])
                        self.expenses.append(row)
                print(f"Loaded {len(self.expenses)} expenses from {self.filename}")
            except Exception as e:
                print(f"Error loading expenses: {e}")
                self.expenses = []
        else:
            print("No existing expense file found. Starting fresh.")
    
    def save_expenses(self):
        """Save expenses to CSV file"""
        try:
            with open(self.filename, 'w', newline='') as file:
                if self.expenses:
                    fieldnames = self.expenses[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.expenses)
                else:
                    # Create empty file with headers
                    writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
                    writer.writeheader()
            print(f"Expenses saved to {self.filename}")
        except Exception as e:
            print(f"Error saving expenses: {e}")
    
    def add_expense(self):
        """Add a new expense"""
        print("\n--- Add New Expense ---")
        
        # Get amount with error handling
        while True:
            try:
                amount = float(input("Enter expense amount: $"))
                if amount <= 0:
                    print("Amount must be positive. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        # Get category with validation
        print("\nAvailable categories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        
        while True:
            try:
                category_choice = int(input(f"Select category (1-{len(self.categories)}): "))
                if 1 <= category_choice <= len(self.categories):
                    category = self.categories[category_choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.categories)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get date with validation
        while True:
            date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date_str:
                date_str = datetime.now().strftime("%Y-%m-%d")
                break
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")
        
        # Get description
        description = input("Enter description (optional): ").strip()
        
        # Create expense dictionary
        expense = {
            'date': date_str,
            'category': category,
            'amount': amount,
            'description': description
        }
        
        self.expenses.append(expense)
        print(f"Expense of ${amount:.2f} added successfully!")
    
    def view_expenses(self):
        """View all expenses"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        
        print("\n--- All Expenses ---")
        print(f"{'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
        print("-" * 50)
        
        total = 0
        for expense in self.expenses:
            print(f"{expense['date']:<12} {expense['category']:<15} ${expense['amount']:<9.2f} {expense['description']}")
            total += expense['amount']
        
        print("-" * 50)
        print(f"{'Total':<27} ${total:<9.2f}")
    
    def generate_report(self):
        """Generate expense reports"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        
        print("\n--- Expense Report ---")
        
        # Total spending
        total_spent = sum(expense['amount'] for expense in self.expenses)
        print(f"Total Spending: ${total_spent:.2f}")
        
        # Spending by category
        print("\nSpending by Category:")
        print("-" * 30)
        category_totals = {}
        for category in self.categories:
            category_total = sum(expense['amount'] for expense in self.expenses if expense['category'] == category)
            category_totals[category] = category_total
            if category_total > 0:
                percentage = (category_total / total_spent) * 100
                print(f"{category:<15}: ${category_total:<8.2f} ({percentage:.1f}%)")
        
        # Highest expense
        if self.expenses:
            highest_expense = max(self.expenses, key=lambda x: x['amount'])
            print(f"\nHighest Expense: ${highest_expense['amount']:.2f} on {highest_expense['category']} ({highest_expense['date']})")
        
        # Monthly spending (if we have enough data)
        monthly_totals = {}
        for expense in self.expenses:
            month = expense['date'][:7]  # YYYY-MM
            monthly_totals[month] = monthly_totals.get(month, 0) + expense['amount']
        
        if len(monthly_totals) > 1:
            print("\nMonthly Spending:")
            for month, total in sorted(monthly_totals.items()):
                print(f"  {month}: ${total:.2f}")
        
        return category_totals
    
    def visualize_expenses(self):
        """Create visualizations of expenses"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        
        category_totals = {}
        for category in self.categories:
            category_total = sum(expense['amount'] for expense in self.expenses if expense['category'] == category)
            if category_total > 0:
                category_totals[category] = category_total
        
        if not category_totals:
            print("No expenses to visualize.")
            return
        
        # Create pie chart
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
        plt.title('Expense Distribution by Category')
        
        # Create bar chart
        plt.subplot(1, 2, 2)
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        plt.bar(categories, amounts, color=['red', 'blue', 'green', 'orange', 'purple', 'brown'])
        plt.title('Expenses by Category')
        plt.xlabel('Categories')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def run(self):
        """Main program loop"""
        print("=" * 50)
        print("    Welcome to Personal Expense Tracker!")
        print("=" * 50)
        
        while True:
            print("\nMain Menu:")
            print("1. Add an Expense")
            print("2. View All Expenses")
            print("3. Generate Report")
            print("4. Visualize Expenses")
            print("5. Save and Exit")
            
            try:
                choice = int(input("\nEnter your choice (1-5): "))
                
                if choice == 1:
                    self.add_expense()
                elif choice == 2:
                    self.view_expenses()
                elif choice == 3:
                    self.generate_report()
                elif choice == 4:
                    self.visualize_expenses()
                elif choice == 5:
                    self.save_expenses()
                    print("Thank you for using Personal Expense Tracker. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nProgram interrupted. Saving expenses...")
                self.save_expenses()
                break

# Main execution
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()