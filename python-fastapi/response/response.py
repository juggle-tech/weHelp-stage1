from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse

app = FastAPI()

# 處理路徑 /
@app.get("/")
def index():
    return FileResponse("home.html")

# 處理路徑 /img/logo
@app.get("/img/logo")
def logo():
    return FileResponse("logo.png")

# 處理路徑 /member
@app.get("/member")
def member():
    return RedirectResponse("https://www.google.com/")