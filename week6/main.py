import os
import query

from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine
from models import Member, Message
from starlette.middleware.sessions import SessionMiddleware


# Retrieve DB variables in .env
load_dotenv()  

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(mysql_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Simplify variable
SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = "templates")
# Session
app.add_middleware(SessionMiddleware, secret_key = "jung-secret-key")


## API
# home.html
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request = request, name = "home.html", context = {}
    )


@app.post("/login")
async def login(request: Request, session: SessionDep, 
                email: str = Form(""), pwd: str = Form("")):
    
    # Validate if the email and password match
    member = query.validate_login(session, email, pwd)
    if member:
        # Store user's name in session
        request.session["member_name"] = member.name
        return RedirectResponse(url = "/member", status_code = 303)
    else:
        msg = "帳號或密碼輸入錯誤"
        return RedirectResponse(url = f"/ohoh?msg={msg}", status_code = 303)


# member.html
@app.get("/member")
async def member(request: Request):
    return templates.TemplateResponse(request, "member.html", 
                context = {"name": request.session.get("member_name")
                })


# ohoh.html
@app.get("/ohoh")
async def error_msg(request: Request, msg: str = ""):
    return templates.TemplateResponse(request, "ohoh.html", {"msg": msg})


@app.post("/signup")
async def sign_up(request: Request, session: SessionDep,name: str = Form(""), 
                  email: str = Form(""), pwd: str = Form("")):
    if query.check_email(session, email):
        msg = "重複的電子郵件"
        return templates.TemplateResponse(request, "ohoh.html", {"msg": msg})
    else:
        member = Member(name=name, email=email, pwd=pwd)
        query.create_member(session, member)
        return RedirectResponse(url = "/", status_code = 303)
    

# logout.html
@app.get("/logout")
async def logout(request: Request):
    # Clear all stored session data
    request.session.clear()
    return RedirectResponse(url = "/", status_code = 303)