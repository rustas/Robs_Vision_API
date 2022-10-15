from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class design(BaseModel):
    ID: int
    title: str
    content: str
    category: str
    date: str
    published: bool = False


@app.get("/")
def root():
    return { "message": "Robs_Vision's API v4" }

@app.get("/info")
def get_posts():
    return { "myData": "all my data"}

@app.post("/new_post")
def NEW_POST(new_post: design):
    # payLoad: dict = Body(...)
    return { "data": new_post
        # new_post.ID,
        # new_post.title,
        # new_post.content,
        # new_post.category,
        # new_post.date,
        # new_post.published
    }
    # return { "NEW_POST": f"ID: {payLoad['ID']}, title: {payLoad['title']}, content: {payLoad['content']}"}

@app.post("/update_post")
def UPDATE_POST():
    return { "UPDATE_POST": "updated post #ID"}

@app.post("/delete_post")
def DELETE_POST():
    return { "DELETE_POST": "deleted post #ID"}

