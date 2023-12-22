import uvicorn
from fastapi import FastAPI
from app.model  import PostSchema
from fastapi import FastAPI, Body,Depends

from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from utils import hash_password
from app.database import get_db 
from fastapi import HTTPException



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

app = FastAPI()

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

@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...), db=Depends(get_db)):
    # Convert UserSchema to dictionary
    user_dict = user.dict()

    # Hash the password before storing it
    user_dict["password"] = hash_password(user_dict["password"])

    # Insert the user into MongoDB
    db.users.insert_one(user_dict)

    return signJWT(user_dict["email"])



@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    print(f"Attempting login with user: {user}")
    if check_user(user):
        return signJWT(user.email)
    print("Login failed")
    raise HTTPException(status_code=401, detail="Wrong login details!")





if __name__ == "__main__":
    # This block ensures that the MongoDB client is properly closed when the FastAPI app shuts down
    import atexit

    @atexit.register
    def shutdown():
        from app.database import client
        client.close()

    uvicorn.run(app, host="127.0.0.1", port=8000)