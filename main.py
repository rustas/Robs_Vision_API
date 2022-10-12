from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Robs_Vision's API v4" }

@app.get("/posts")
def get_posts():
    return {"myData": "all my data"}
