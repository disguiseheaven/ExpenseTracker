from flask import Flask, render_template, request, redirect, url_for, session
from tracker import Tracker
from expense import Expense
from users import register_user, login_user

# Set the flask app
app = Flask(__name__)
app.secret_key = 'ExpenseTracker'  

tracker = Tracker()

# Route for handling the expense page for logged in user
@app.route('/')
def index():
    # Get the add expense page if user logged in
    if 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('signin'))


# Route for user to signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if register_user(username, password):
            return redirect(url_for('signin'))
        else:
            return "Username already exists. Please choose a different one.", 400

    return render_template('signup.html')

# Route for user to signin 
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_id = login_user(username, password)
        # Store user_id and username in session
        if user_id:
            session['user_id'] = user_id  
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again.", 400

    return render_template('signin.html')

#Route to add expenses and save it in database
@app.route('/add_expense', methods=['POST'])
def add_expense():
    """Add a new expense (user-specific)."""
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    date = request.form.get('date')

    if not description or not amount:
        return "Description and amount are required", 400

    # Create Expense object and add to the tracker (user-specific)
    expense = Expense(description, amount, date)
    tracker.add_expense(expense, session['user_id'])

    return redirect(url_for('index'))

# Route to get all the expenses list
@app.route('/expenses')
def expenses():
    """Display all expenses for the logged-in user."""
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    expenses = tracker.display_all_expenses(session['user_id'])
    expenses_list = [{"description": expense.description, "amount": expense.amount, "date": expense.date}
                     for expense in expenses]
    
    return render_template('expenses.html', expenses=expenses_list)

# Route to get the summary of expenses 
@app.route("/expense_summary", methods=["GET"])
def expense_summary():
    # Assuming you have the user_id available from session or other means
    user_id = session['user_id']  

    # Get the chart image URL
    chart_url = tracker.summarize_expenses(user_id)
    pie_chart_url = tracker.generate_monthly_expense_pie_chart(user_id)
    expense_numerical_summary = tracker.numerical_summary(user_id)

    # Render the HTML page and pass the chart URL
    return render_template("summary.html", chart_url=chart_url, pie_chart_url=pie_chart_url, **expense_numerical_summary)

# Route to log out the user
@app.route('/logout')
def logout():
    """Log the user out and remove from session."""
    session.pop('user_id', None)
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)
