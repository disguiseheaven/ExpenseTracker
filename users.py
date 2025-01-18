# users.py
from bcrypt import hashpw, gensalt, checkpw
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient('mongodb+srv://rubisingh:U6kvda6pma!@cluster0.iv8cp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['ExpenseTracker']
users_collection = db['users']

def register_user(username, password):
    """Register a new user with a hashed password."""
    if users_collection.find_one({'username': username}):
        return False  # User already exists
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    users_collection.insert_one({'username': username, 'password': hashed_password})
    return True

def login_user(username, password):
    """Verify user's credentials."""
    user = users_collection.find_one({'username': username})
    if user and checkpw(password.encode('utf-8'), user['password']):
        return str(user['_id'])  # Return user ID
    return None
