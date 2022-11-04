# \venv\Scripts\activate.bat
# uvicorn app.main:app --reload
# 
# from app.dev_auth import db_driver, db_srv, db_user, db_pw, db_db, db_port
# import pyodbc
# 
# Azure connection
# while True:
#     try:
#         conn = pyodbc.connect(
#             'DRIVER='+db_driver+';'
#             'Server='+db_srv+';'
#             'Database='+db_db+';'
#             'UID='+db_user+';'
#             'PWD='+db_pw+';'
#         )

#         SQL_PUPPET = conn.cursor()
#         # cursor = conn.cursor()
#         print("Connected to database!")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(5)

#START: no database section
# my_data_storage = [
#     {"ID": 1, "title": "post1", "content": "content1", "category": "category1", "date": "Saturday, 15 October 2022 20:46:58", "published": True},
#     {"ID": 2, "title": "post2", "content": "content2", "category": "category2", "date": "Saturday, 16 October 2022 20:46:58", "published": True},
#     {"ID": 3, "title": "post3", "content": "content3", "category": "category3", "date": "Saturday, 17 October 2022 20:46:58", "published": True},
    
#     ]
#END: no database section

# def find_post(id: int):
#     # SQL_PUPPET.execute("SELECT * FROM Posts WHERE Id=?", (id))
#     SQL_PUPPET.execute("SELECT * FROM Posts WHERE Id=%s", (id))
#     find_post = SQL_PUPPET.fetchall()
#     return( f"{find_post}" )

# def find_post_index(id):
#     for i, p in enumerate(my_data_storage):
#         if p['Id'] == id:
#             return i

# SQL_QUERY = "SELECT * FROM Posts" # FOR JSON PATH
# SQL_PUPPET.execute("SELECT * FROM Posts FOR JSON AUTO")
# SQL_PUPPET.execute("INSERT INTO Posts (post_title, post_content, post_category, post_published) VALUES (?, ?, ?, ?)",(new_post.post_title, new_post.post_content, new_post.post_category, new_post.post_published))
