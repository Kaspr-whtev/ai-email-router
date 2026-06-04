from pydantic import BaseModel, EmailStr


class MessageRequest(BaseModel):
    email: EmailStr
    message: str

class ClassificationRequest(BaseModel):
    message: str