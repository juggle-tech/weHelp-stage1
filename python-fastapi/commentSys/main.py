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
import json
from typing import Annotated
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()



# 建立後端 RESTful APIs
# 新增留言的 API
@app.post("/api/message")
def create_message(body = Body(None)):  # 告訴他要從請求文本獲得資訊
    # 預期前端透過 請求文本(Request Body) 傳遞{"author": "name", "content": "contents"}
    body = json.loads(body) # 請求文本的資訊是Json的形式
    author = body["author"]
    content = body["content"]

    # 連線到資料庫，將資料新增到資料表中
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO message(author, content) VALUES (%s, %s)",
        [author, content]
    )
    con.commit()
    return {"ok": True}


# 取得所有留言的 API
@app.get("/api/message")
def get_messages():
    # 連線到資料庫，取得留言傳回到前端
    cursor = con.cursor(dictionary=True) # 用 python 字典的形式把資料抓出來，預設是Tuple的形式
    cursor.execute("SELECT * FROM message ORDER BY id ASC")
    data = cursor.fetchall()
    return data


# 根據編號，刪除留言的 API
@app.delete("/api/message/{id}")
def delete_message(id: int):
    # 連線到資料庫，根據 id 的值，刪除留言資料
    cursor = con.cursor()
    cursor.execute("DELETE FROM message WHERE id=%s", [id])
    con.commit()
    return {"ok": True}

# 一定要放最後面，否則會讓 /api/message 系列全部失效
# 把目前資料夾掛載成靜態檔案來源
app.mount("/", StaticFiles(directory="static", html=True))
