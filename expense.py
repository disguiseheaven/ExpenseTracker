from datetime import datetime

class Expense:
    def __init__(self, description, amount, date=None):
        self.description = description
        self.amount = amount
        # If date is not provided, use the current date.
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def from_dict(data):
        """Create an Expense object from a MongoDB document."""
        return Expense(
            description=data['description'],
            amount=data['amount'],
            date=data['date']
        )