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
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Joe Doe",
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