from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{"message": "Task Manager API is running"}

