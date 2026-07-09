# 準備 DB 連線
import mysql.connector
con = mysql.connector.connect(
    user = "root",
    password = "0000",
    host = "localhost",
    database = "fastapi"
)
print("Database Ready!")

# 準備網站後端系統
from typing import Annotated
from fastapi import FastAPI
app = FastAPI()

@app.get("/createMessage")
def createMessage (
    author: Annotated[str, None],
    content: Annotated[str, None]
):
    # 利用已建立的 DB 連線對 DB 下 SQL 指令
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO message(author, content) VALUES (%s, %s)",
        [author, content]
    )
    con.commit()
    return {"OK": True}
