from pydantic import BaseModel, EmailStr


class MessageRequest(BaseModel):
    email: EmailStr
    message: str