from pydantic import BaseModel,Field,EmailStr


class PostSchema(BaseModel):
    id : int = Field(default = None)
    title : str = Field(default = None)
    content : str = Field(default = None)
    class Config :
        schema_extra = {
            "post_demo" :{
                 "title": "some title",
                "content":"some content"
            }
        }



class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        } 


class ExpenseSchema(BaseModel):
    name: str
    amount: float

class ExpenseDB(ExpenseSchema):
    id: int

class ExpenseCreate(ExpenseSchema):
    pass


