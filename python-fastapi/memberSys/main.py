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
from fastapi import FastAPI, Body, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 準備 SessionMiddleware 管理使用者狀態
app.add_middleware(SessionMiddleware, secret_key = "jung_secret_key")

# 建立後端 RESTful API
# 註冊會員的 API
import json
@app.post("/api/member")
def signup(body = Body(None)): # 從請求文本接收資訊
    body = json.loads(body)
    name = body["name"]
    email = body["email"]
    password = body["password"]

    # 連動 DB
    # 檢查 email 是否重複
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE email = %s", [email])
    result = cursor.fetchone()
    if result == None:  # 代表 email 沒有重複，可註冊
        cursor.execute("INSERT INTO member(name, email, password) VALUES(%s, %s, %s)", [name, email, password])
        con.commit() # 執行 SQL
        return {"ok": True}
    else: # 代表 email 重複，不可註冊
        return {"ok": False}
    

# 登入會員的 API
@app.put("/api/member/auth")
def signin(request: Request, body = Body(None)):
    body = json.loads(body)
    email = body["email"]
    password = body["password"]

    # 根據前端輸入的 email 和 password 從資料庫取得對應的帳戶資料
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE email = %s AND password = %s", [email, password])
    result = cursor.fetchone()
    if result != None:  # DB 裡有相應資料，登入成功
        request.session["member"] = {"name": result[1], "email": result[2]}
        return {"ok": True}
    else:   # 登入失敗
        request.session["member"] = None
        return {"ok": False}


# 檢查登入狀態的 API
@app.get("/api/member/auth")
def check_status(request: Request):
    if "member" in request.session and request.session["member"] != None: # 已經登入
        member = request.session["member"]
        return {"ok": True, "name": member["name"], "email": member["email"]}
    else: # 沒有登入
        return {"ok": False}


# 靜態檔案處理，支援前端網頁呈現
app.mount("/", StaticFiles(directory="static", html=True))
