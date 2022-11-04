from app.config import *
import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        SQL_CONN = psycopg2.connect(
            host=f"{db_srv}",
            port=f"{db_port}",
            database=f"{db_db}",
            user=f"{db_user}",
            password=f"{db_pw}",
            cursor_factory=RealDictCursor
        )

        SQL_PUPPET = SQL_CONN.cursor()
        print("Connected to database!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(5)

@app.get("/")
def root():
    return { "message": "Robs_Vision's API v1.0" }

@app.get("/posts")
def get_posts():
    SQL_PUPPET.execute("SELECT * FROM posts ")
    SQL_RETURN = SQL_PUPPET.fetchall()
    return(SQL_RETURN)

@app.get("/posts/lastest")
def get_lastest_post():
    SQL_PUPPET.execute("SELECT * from posts WHERE Date = ")

@app.get("/posts/{id}")
def get_post_id(id: int):
    SQL_PUPPET.execute("SELECT * from posts WHERE id = %s ", (str(id),))
    SQL_RETURN = SQL_PUPPET.fetchone()
    if not SQL_RETURN:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    return( SQL_RETURN )

@app.get("/sqlalch")
def sql_alch_test(db: Session = Depends(get_db)):
    return({"status": "success"})


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def NEW_POST(new_post: Post):
    try:
        SQL_PUPPET.execute("INSERT INTO posts (post_title, post_content, post_category, post_published) VALUES (%s, %s, %s, %s) RETURNING * ",(new_post.post_title, new_post.post_content, new_post.post_category, new_post.post_published))
        SQL_RETURN = SQL_PUPPET.fetchone()
        SQL_CONN.commit()
        return({"Created new post!": SQL_RETURN})

    except Exception as error:
        print("Failed to add new post.")
        print("Error: ", error)
        return({ "message:": "Failed to add new post." })


@app.put("/posts/{id}")
def UPDATE_POST(id: int, update_post: Post):
    SQL_PUPPET.execute("UPDATE posts SET post_title = %s, post_content = %s, post_category = %s, post_published= %s WHERE id = %s RETURNING *", (update_post.post_title, update_post.post_content, update_post.post_category, update_post.post_published,str(id)))
    SQL_RETURN = SQL_PUPPET.fetchone()
    SQL_CONN.commit()
    if SQL_RETURN == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exists")
    
    return(SQL_RETURN)

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def DELETE_POST(id: int):
    SQL_PUPPET.execute("DELETE FROM Posts WHERE Id = %s RETURNING * ", (str(id),))
    SQL_RETURN = SQL_PUPPET.fetchone()
    SQL_CONN.commit()
    if SQL_RETURN == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exists")

    return({ f"Post with ID:{id} has been removed." })