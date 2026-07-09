from typing import Annotated
from fastapi import FastAPI, Path, Query
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()  # 產生 FastAPI 物件

# 非靜態檔案處理的路由，擺在上方
@app.get("/square")
def square(num: Annotated[int, None]):
    result = num * num
    return {"data": result}

@app.get("/member")
def member():
    return RedirectResponse("/")

# 統一處理靜態檔案，擺在下方，才不會影響其他路由
app.mount("/", StaticFiles(directory="public", html=True))