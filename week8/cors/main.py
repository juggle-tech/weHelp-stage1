from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

origins = [
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # 只有清單內的來源會被放行
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
def hello():
    return {
        "message": "Hello from FastAPI!",
        "note": "CORS configuration has successfully allowed this origin.",
    }

@app.get("/proxy/google")
async def proxy_google():
    # 這是伺服器對伺服器的呼叫，完全不受瀏覽器的 CORS 政策限制
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.google.com/")
        return {
            "status_code": response.status_code,
            "content_length": len(response.text),
            "note": "The backend proxies the request to google.com, so the frontend only talks to your backend.",
        }