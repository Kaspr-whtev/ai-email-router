from pydantic import BaseModel, EmailStr
from typing import Literal


class MessageRequest(BaseModel):
    email: EmailStr
    message: str

class ClassificationRequest(BaseModel):
    message: str

DepartmentEmail = Literal[
    "human-resources@example.com",
    "help-desk@example.com",
    "it@example.com",
    "kadry@example.com",
    "other@example.com",
]


class DepartmentResult(BaseModel):
    department: DepartmentEmail