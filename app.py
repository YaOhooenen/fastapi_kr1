from fastapi import FastAPI

my_app = FastAPI()

@my_app.get("/")
def root():
    return {"message": "Авторелоад действительно работает"}