# ExpenseTracker

### Objective:
The **ExpenseTracker** project is a Flask-based backend application that allows multiple users to manage and track their expenses. It provides functionalities to add expenses, view expenses, and generate summarized details, including visual representations such as bar charts and pie charts.

---

### Project File Details:

- **expense.py**: Manages the expense object, which includes details like the description, date, and amount of the expense.
- **tracker.py**: Handles the addition of expenses, displays all expenses for a user, and provides a summary of expenses. It includes visual charts such as:
  - Category-wise expense bar chart
  - Pie chart comparing current and previous month expenses
  - Total expenses for the current year, month, and day
- **users.py**: Manages user registration and login functionalities.
- **main.py**: Serves as the entry point and central hub for the entire application to run.
- **templates/**: Contains HTML files for the user interface.
  - **index.html**: Page for adding new expenses.
  - **signin.html**: Page for user sign-in.
  - **signup.html**: Page for user registration.
  - **expenses.html**: Page to view all expenses of the user.
  - **summary.html**: Page to view the summary of expenses.

---

### How to Set Up the App:

1. **Clone the repository** or download the ZIP file and extract it.
2. Ensure the file structure looks like this:
    ```
    - expense.py
    - tracker.py
    - users.py
    - main.py
    - templates/
        - expenses.html
        - index.html
        - signin.html
        - signup.html
        - summary.html
    ```
3. **Create a virtual environment** for best practices:
    ```bash
    python -m venv env
    ```
4. **Activate the virtual environment**:
    - For Windows (Command Line):
      ```bash
      env\Scripts\activate
      ```
5. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
6. **Run the application** by executing:
    ```bash
    python main.py
    ```

   After running, the app will start a Flask server on **localhost**. The default URL to access the app is:
   ```
   http://127.0.0.1:5000/
   ```

   Paste this URL into your browser to access the **ExpenseTracker** app.

---

### Features:

- **User Registration and Authentication**: New users can sign up, and existing users can sign in to track their expenses.
- **Expense Management**: Users can add, view, and categorize their expenses.
- **Expense Summary**: Includes visual charts summarizing monthly, category-wise, and year-to-date expenses.
  
---

### Dependencies:

- Flask
- MongoDB
- Additional libraries (listed in `requirements.txt`)

---

Enjoy managing your expenses with **ExpenseTracker**!