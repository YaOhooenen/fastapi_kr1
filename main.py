from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from models import User
import re

app = FastAPI()

# 1.2
@app.get("/")
def read_root():
    return FileResponse("index.html")

# 1.3
class CalcInput(BaseModel):
    num1: float
    num2: float

@app.post("/calculate")
def calculate(data: CalcInput):
    return {"result": data.num1 + data.num2}

# 1.4
user = User(name="Твоё Имя Фамилия", id=1)

@app.get("/users")
def get_user():
    return user

# 1.5
class UserAge(BaseModel):
    name: str
    age: int

@app.post("/user")
def check_user(u: UserAge):
    return {
        "name": u.name,
        "age": u.age,
        "is_adult": u.age >= 18
    }

# 2.1 / 2.2
feedbacks = []

BAD_WORDS = ["кринж", "рофл", "вайб"]

class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def check_bad_words(cls, v):
        for word in BAD_WORDS:
            if re.search(word, v, re.IGNORECASE):
                raise ValueError("Использование недопустимых слов")
        return v

@app.post("/feedback")
def post_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}