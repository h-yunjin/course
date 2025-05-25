from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    password: str  # hashedpassword


class User(BaseModel):
    id: int
    email: EmailStr


class UserHashedPsw(User):
    password: str  # hashedpassword
