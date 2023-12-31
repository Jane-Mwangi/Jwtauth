
# import uvicorn
# from fastapi import FastAPI
# from app.model  import PostSchema
# from fastapi import FastAPI, Body,Depends

# from app.model import PostSchema, UserSchema, UserLoginSchema,ExpenseCreate
# from app.auth.jwt_handler import signJWT
# from app.auth.jwt_bearer import jwtBearer
# from utils import verify_password
# from app.database import get_db,Database
# from fastapi import HTTPException
# from app.model import ExpenseDB
# from typing import List


# from fastapi.middleware.cors import CORSMiddleware



# app = FastAPI()

# #CORS MIDDLEWARE

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins during development
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )



# def get_db():
#     db = Database(config("APP_DB_URL"))  # Assuming Database is your MongoDB connection class
#     try:
#         yield db
#     finally:
#         db.client.close()  # Close the MongoClient connection


# posts = [
#     {
#         "id": 1,
#         "title": "Penguins ",
#         "text": "Penguins are a group of aquatic flightless birds."
#     },
#     {
#         "id": 2,
#         "title": "Tigers ",
#         "text": "Tigers are the largest living cat species and a memeber of the genus panthera."
#     },
#     {
#         "id": 3,
#         "title": "Koalas ",
#         "text": "Koala is arboreal herbivorous maruspial native to Australia."
#     },
# ]

# users = []



# def check_user(data: UserLoginSchema):
#     # Convert UserLoginSchema to a dictionary for comparison
#     user_data = data.dict()

#     for user in users:
#         # Convert user to a dictionary for comparison
#         user_dict = user.dict()

#         print(f"Comparing user data: {user_data}")
#         print(f"with existing user: {user_dict}")

#         # Create an instance of UserLoginSchema for comparison
#         user_login_instance = UserLoginSchema(**user_data)

#         # Compare user data
#         if user_dict == user_login_instance.dict():
#             print("Login successful")
#             return True

#     print("Login failed")
#     return False

# # Get Posts
# @app.get("/posts", tags=["posts"])
# def get_posts():
#     return { "data": posts }


# @app.get("/posts/{id}", tags=["posts"])
# def get_single_post(id: int):
#     if id > len(posts):
#         return {
#             "error": "No such post with the supplied ID."
#         }

#     for post in posts:
#         if post["id"] == id:
#             return {
#                 "data": post
#             }


# @app.post("/posts", dependencies=[Depends(jwtBearer())],tags=["posts"])
# def add_post(post: PostSchema):
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }
    
# # @app.post("/user/signup", tags=["user"])
# # def create_user(user: UserSchema = Body(...)):
# #     users.append(user) # replace with db call, making sure to hash the password first
# #     return signJWT(user.email)

# # @app.post("/user/signup", tags=["user"])
# # def create_user(user: UserSchema = Body(...), db=Depends(get_db)):
# #     # Convert UserSchema to dictionary
# #     user_dict = user.dict()

# #     # Hash the password before storing it
# #     user_dict["password"] = hash_password(user_dict["password"])

# #     # Insert the user into MongoDB
# #     db.users.insert_one(user_dict)

# #     return signJWT(user_dict["email"])



# # @app.post("/user/login", tags=["user"])
# # def user_login(user: UserLoginSchema = Body(...)):
# #     print(f"Attempting login with user: {user}")
# #     if check_user(user):
# #         return signJWT(user.email)
# #     print("Login failed")
# #     raise HTTPException(status_code=401, detail="Wrong login details!")


# @app.post("/user/signup", tags=["user"])
# def create_user(user: UserSchema = Body(...), db=Depends(get_db)):
#     # Convert UserSchema to dictionary
#     user_dict = user.dict()

#     # Hash the password before storing it
#     user_dict["password"] = hash_password(user_dict["password"])

#     # Insert the user into MongoDB
#     db.users.insert_one(user_dict)

#     # You can return a success message or any other specific status code here
#     return {"message": "User created successfully"}

# @app.post("/user/login", tags=["user"])
# def user_login(user: UserLoginSchema = Body(...), db=Depends(get_db)):
#     # Check if the user exists and the password is correct
#     if check_user(user, db):
#         # If successful, return the token
#         return signJWT(user.email)
#     else:
#         # If login fails, return a 401 Unauthorized status code
#         raise HTTPException(status_code=401, detail="Wrong login details!")

# def check_user(data: UserLoginSchema, db):
#     # Convert UserLoginSchema to a dictionary for comparison
#     user_data = data.dict()

#     # Retrieve the user from the database based on the email
#     user_from_db = db.users.find_one({"email": user_data["email"]})

#     if user_from_db:
#         # Check if the hashed password in the database matches the input
#         if verify_password(user_data["password"], user_from_db["password"]):
#             return True

#     return False

# #EXPENSE
# @app.post("/expenses/{user_email}", response_model=ExpenseDB, tags=["expenses"])
# def create_expense(user_email: str, expense: ExpenseCreate, db=Depends(get_db)):
#     return db.create_expense(user_email, expense)

# @app.get("/expenses/{user_email}", response_model=List[ExpenseDB], tags=["expenses"])
# def get_user_expenses(user_email: str, db=Depends(get_db)):
#     return db.get_user_expenses(user_email)

# @app.put("/expenses/{user_email}/{expense_id}", response_model=ExpenseDB, tags=["expenses"])
# def update_expense(user_email: str, expense_id: int, expense: ExpenseCreate, db=Depends(get_db)):
#     return db.update_expense(user_email, expense_id, expense)

# @app.delete("/expenses/{user_email}/{expense_id}", response_model=ExpenseDB, tags=["expenses"])
# def delete_expense(user_email: str, expense_id: int, db=Depends(get_db)):
#     return db.delete_expense(user_email, expense_id)


# if __name__ == "__main__":
#     # This block ensures that the MongoDB client is properly closed when the FastAPI app shuts down
#     import atexit

#     @atexit.register
#     def shutdown():
#         from app.database import Database
#         db = Database(config("APP_DB_URL"))  # Initialize the Database class with your connection string
#         if hasattr(db, 'client') and db.client:
#             db.client.close()  # Close the MongoClient connection

#     uvicorn.run(app, host="127.0.0.1", port=8000)

import uvicorn
from fastapi import FastAPI
from app.model  import PostSchema
from fastapi import FastAPI, Body,Depends

from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from utils import verify_password
from app.database import get_db 
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware
import bcrypt 

def hash_password(password: str) -> str:
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

app = FastAPI()

#CORS MIDDLEWARE

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



posts = [
    {
        "id": 1,
        "title": "Penguins ",
        "text": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "Tigers ",
        "text": "Tigers are the largest living cat species and a memeber of the genus panthera."
    },
    {
        "id": 3,
        "title": "Koalas ",
        "text": "Koala is arboreal herbivorous maruspial native to Australia."
    },
]

users = []



def check_user(data: UserLoginSchema):
    # Convert UserLoginSchema to a dictionary for comparison
    user_data = data.dict()

    for user in users:
        # Convert user to a dictionary for comparison
        user_dict = user.dict()

        print(f"Comparing user data: {user_data}")
        print(f"with existing user: {user_dict}")

        # Create an instance of UserLoginSchema for comparison
        user_login_instance = UserLoginSchema(**user_data)

        # Compare user data
        if user_dict == user_login_instance.dict():
            print("Login successful")
            return True

    print("Login failed")
    return False

# Get Posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return { "data": posts }


@app.get("/posts/{id}", tags=["posts"])
def get_single_post(id: int):
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


@app.post("/posts", dependencies=[Depends(jwtBearer())],tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }
    
# @app.post("/user/signup", tags=["user"])
# def create_user(user: UserSchema = Body(...)):
#     users.append(user) # replace with db call, making sure to hash the password first
#     return signJWT(user.email)

# @app.post("/user/signup", tags=["user"])
# def create_user(user: UserSchema = Body(...), db=Depends(get_db)):
#     # Convert UserSchema to dictionary
#     user_dict = user.dict()

#     # Hash the password before storing it
#     user_dict["password"] = hash_password(user_dict["password"])

#     # Insert the user into MongoDB
#     db.users.insert_one(user_dict)

#     return signJWT(user_dict["email"])



# @app.post("/user/login", tags=["user"])
# def user_login(user: UserLoginSchema = Body(...)):
#     print(f"Attempting login with user: {user}")
#     if check_user(user):
#         return signJWT(user.email)
#     print("Login failed")
#     raise HTTPException(status_code=401, detail="Wrong login details!")


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...), db=Depends(get_db)):
    # Convert UserSchema to dictionary
    user_dict = user.dict()

    # Hash the password before storing it
    user_dict["password"] = hash_password(user_dict["password"])

    # Insert the user into MongoDB
    db.users.insert_one(user_dict)

    # You can return a success message or any other specific status code here
    return {"message": "User created successfully"}

@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...), db=Depends(get_db)):
    # Check if the user exists and the password is correct
    if check_user(user, db):
        # If successful, return the token
        return signJWT(user.email)
    else:
        # If login fails, return a 401 Unauthorized status code
        raise HTTPException(status_code=401, detail="Wrong login details!")

def check_user(data: UserLoginSchema, db):
    # Convert UserLoginSchema to a dictionary for comparison
    user_data = data.dict()

    # Retrieve the user from the database based on the email
    user_from_db = db.users.find_one({"email": user_data["email"]})

    if user_from_db:
        # Check if the hashed password in the database matches the input
        if verify_password(user_data["password"], user_from_db["password"]):
            return True

    return False


if __name__ == "__main__":
    # This block ensures that the MongoDB client is properly closed when the FastAPI app shuts down
    import atexit

    @atexit.register
    def shutdown():
        from app.database import client
        if client and client.server_info():
            client.close()

    uvicorn.run(app, host="127.0.0.1", port=8000)