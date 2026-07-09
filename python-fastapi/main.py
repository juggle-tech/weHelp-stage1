from fastapi import FastAPI

app = FastAPI()     # FastAPI物件

# 建立網站首頁
@app.get("/")
def index():
    return {"x": 3, "y": 4}

# 啟動server > uvicorn {檔案名稱: 物件名稱 --reload}
# " py -m uvicorn main:app --reload " 
#  --reload: 更新檔案後會自動載入更新
# Ctrl+C 終止連線


# 改變埠號: py -m uvicorn main:app --reload --port 3000