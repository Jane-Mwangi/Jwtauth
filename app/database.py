# from pymongo import MongoClient
# from fastapi import Depends, HTTPException
# from decouple import config



# # Replace these with your actual MongoDB server URL and database name
# DB_URL = config("APP_DB_URL")
# DB_NAME = "YOUR_DB_NAME"

# client = MongoClient(DB_URL)
# db = client[DB_NAME]

# class Database:
#     def __init__(self, connection_string):
#         self.client = MongoClient(connection_string)
#         self.db = self.client.get_database()

#     def create_expense(self, user_email: str, expense: ExpenseCreate):
#         # Find the user
#         user = self.db.users.find_one({"email": user_email})

#         # Insert the expense with a reference to the user
#         expense_data = expense.dict()
#         expense_data["user_id"] = user["_id"]
#         expense_id = self.db.expenses.insert_one(expense_data).inserted_id

#         return self.db.expenses.find_one({"_id": expense_id})

#     def get_user_expenses(self, user_email: str):
#         # Find the user
#         user = db.users.find_one({"email": user_email})

#         # Get all expenses for the user
#         expenses = list(db.expenses.find({"user_id": user["_id"]}))
#         return expenses

#     def update_expense(self, user_email: str, expense_id: int, expense: ExpenseCreate):
#         # Find the user
#         user = db.users.find_one({"email": user_email})

#         # Update the expense
#         updated_expense = db.expenses.find_one_and_update(
#             {"_id": expense_id, "user_id": user["_id"]},
#             {"$set": expense.dict()},
#             return_document=True
#         )

#         if updated_expense:
#             return updated_expense
#         else:
#             raise HTTPException(status_code=404, detail="Expense not found")

#     def delete_expense(self, user_email: str, expense_id: int):
#         # Find the user
#         user = db.users.find_one({"email": user_email})

#         # Delete the expense
#         deleted_expense = db.expenses.find_one_and_delete(
#             {"_id": expense_id, "user_id": user["_id"]}
#         )

#         if deleted_expense:
#             return deleted_expense
#         else:
#             raise HTTPException(status_code=404, detail="Expense not found")

from pymongo import MongoClient
from fastapi import Depends
from decouple import config

# Replace these with your actual MongoDB server URL and database name
DB_URL = config("APP_DB_URL")
DB_NAME = "YOUR_DB_NAME"

client = MongoClient(DB_URL)
db = client[DB_NAME]

# Dependency to provide the MongoDB database connection
def get_db():
    try:
        yield db
    finally:
        client.close()