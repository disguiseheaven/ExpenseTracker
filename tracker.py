# tracker.py
from pymongo import MongoClient
from pymongo import DESCENDING
from expense import Expense
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')

# MongoDB Setup
client = MongoClient('mongodb+srv://rubisingh:U6kvda6pma!@cluster0.iv8cp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['ExpenseTracker']
expenses_collection = db['expenses']
today = datetime.today()

class Tracker:
    def __init__(self):
        self.expenses_collection = expenses_collection

    # Method to add expenses
    def add_expense(self, expense, user_id):
        """Add an expense for a specific user."""
        expense_data = {'description': expense.description, 'amount': expense.amount, 'date': expense.date, 'user_id': user_id}
        self.expenses_collection.insert_one(expense_data)

    # Method to display all expenses
    def display_all_expenses(self, user_id):
        """Display all expenses for a specific user."""
        expenses = self.expenses_collection.find({'user_id': user_id}).sort('date', DESCENDING)
        return [Expense.from_dict(expense) for expense in expenses]

    # Method to summarize expenses and create bar chart for categories
    def summarize_expenses(self, user_id):
        """Summarize all the expenses for a specific user and create a bar chart based on expense category."""
        # Fetch all expenses for the user from the database
        expenses_cursor = self.expenses_collection.find({'user_id': user_id})
        
        # Convert the cursor to a list of dictionaries and then to a pandas DataFrame
        expenses_list = list(expenses_cursor)
        df = pd.DataFrame(expenses_list)
        
        # Check for amount column to be numeric, to avoid errors
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        # Group by 'description' and sum the amounts for each category
        summary_df = df.groupby('description')['amount'].sum().reset_index()

        # Clear the previous plots from the memory
        plt.clf()

        # Create a bar chart
        plt.bar(summary_df['description'], summary_df['amount'])
        plt.xlabel('Expense Category')
        plt.ylabel('Total Amount')
        plt.title('Total Expenses by Category')

        # Convert the plot to PNG image to be displayed on the web page
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_data = base64.b64encode(img.getvalue()).decode('utf-8')
        img_url = f"data:image/png;base64,{img_data}" 

        # Return the chart URL to display it in the HTML
        return img_url

    def generate_monthly_expense_pie_chart(self, user_id):
        """Generate a pie chart comparing the total expenses of the current and previous months."""

        # Fetch all expenses for the user from the database
        expenses_cursor = self.expenses_collection.find({'user_id': user_id})
        
        # Convert the cursor to a list of dictionaries and then to a pandas DataFrame
        expenses_list = list(expenses_cursor)
        df = pd.DataFrame(expenses_list)
        
        # Ensure amount to be numeric 
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        # Calculate the total expenses for the current month and the previous month
        first_day_of_current_month = today.replace(day=1)
        first_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)

        # Filter expenses for the current month
        current_month_expenses = df[df['date'] >= first_day_of_current_month.strftime('%Y-%m-%d')]

        # Filter expenses for the previous month
        previous_month_expenses = df[(df['date'] >= first_day_of_previous_month.strftime('%Y-%m-%d')) &
                                      (df['date'] < first_day_of_current_month.strftime('%Y-%m-%d'))]

        # Calculate the total expenses for the current and previous months
        current_month_total = current_month_expenses['amount'].sum()
        previous_month_total = previous_month_expenses['amount'].sum()

        # Create a pie chart comparing the two months
        pie_data = [current_month_total, previous_month_total]
        pie_labels = ['Current Month', 'Previous Month']

        plt.clf()

        plt.figure(figsize=(6, 6))
        plt.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
        plt.title('Expenses for Current vs Previous Month')

        # Convert the pie chart to PNG image to be displayed on the web page
        pie_img = BytesIO()
        plt.savefig(pie_img, format='png')
        pie_img.seek(0)
        pie_img_data = base64.b64encode(pie_img.getvalue()).decode('utf-8')
        pie_img_url = f"data:image/png;base64,{pie_img_data}" 

        # Return the pie chart URL to display it in the HTML
        return pie_img_url
    
    def numerical_summary(self, user_id):
        """Summarize the total expenses for a user and display total for current month and day."""
    
        # Fetch all expenses for the user from the database
        expenses_cursor = self.expenses_collection.find({'user_id': user_id})
        
        # Convert the cursor to a list of dictionaries and then to a pandas DataFrame
        expenses_list = list(expenses_cursor)
        df = pd.DataFrame(expenses_list)
        
        # Check for amount column to be numeric, to avoid errors
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Get today's date and the current month
        current_month = today.month
        current_day = today.day
        current_year = today.year
        
        # Filter expenses for the current month and current day
        df['date'] = pd.to_datetime(df['date'])  # Convert 'date' column to datetime
        df_month = df[df['date'].dt.month == current_month]
        df_day = df[df['date'].dt.day == current_day]
        df_year = df[df['date'].dt.year == current_year]
        
        # Total expenses
        total_expenses = df_year['amount'].sum()
        total_expenses_month = df_month['amount'].sum()
        total_expenses_day = df_day['amount'].sum()
        
        # Display total expenses for the user
        result = {
            "total_expenses": total_expenses,
            "total_expenses_month": total_expenses_month,
            "total_expenses_day": total_expenses_day
        }
        return result