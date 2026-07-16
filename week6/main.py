import os
import query

from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine
from models import Member, Message
from starlette.middleware.sessions import SessionMiddleware


## Database setup
load_dotenv()  # Retrieve DB variables in .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(mysql_url, echo=True)

# DB session dependency
def get_session():
    with Session(engine) as session:
        yield session

# Reusable type alias for the Session dependency
SessionDep = Annotated[Session, Depends(get_session)]

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


## App setup
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = "templates")
# Session
app.add_middleware(SessionMiddleware, secret_key = "jung-secret-key")


## RESTful API
# home.html
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request = request, name = "home.html", context = {}
    )


@app.post("/login")
def login(request: Request, session: SessionDep, 
                email2: str = Form(""), pwd2: str = Form("")):
    
    # Validate if the email and password match
    member = query.validate_login(session, email2, pwd2)
    if member:
        # Store user's name in session
        request.session["member_id"] = member.id
        request.session["member_name"] = member.name
        request.session["member_email"] = member.email
        return RedirectResponse(url = "/member", status_code = 303)
    else:
        msg = "電子郵件或密碼錯誤"
        return RedirectResponse(url = f"/ohoh?msg={msg}", status_code = 303)


@app.post("/signup")
def signup(request: Request, session: SessionDep, name: str = Form(""), 
                  email1: str = Form(""), pwd1: str = Form("")):
    if query.check_email(session, email1):
        msg = "重複的電子郵件"
        return templates.TemplateResponse(request, "ohoh.html", {"msg": msg})
    else:
        member = Member(name=name, email=email1, password=pwd1)
        query.create_member(session, member)
        return RedirectResponse(url = "/", status_code = 303)


# member.html
@app.get("/member")
def member(request: Request):
    
    if "member_id" not in request.session:
        return templates.TemplateResponse(request, "home.html")
    else:
        return templates.TemplateResponse(request, "member.html", 
                context = {"name": request.session.get("member_name")
                })


# ohoh.html
@app.get("/ohoh")
def error_msg(request: Request, msg: str = ""):
    return templates.TemplateResponse(request, "ohoh.html", {"msg": msg})


# logout.html
@app.get("/logout")
def logout(request: Request):
    # Clear all stored session data
    request.session.clear()
    return RedirectResponse(url = "/", status_code = 303)




## Fetch API
# Create Msg API
@app.post("/api/message")
def create_message(request: Request, session: SessionDep, body = Body(None)):
    
    id = request.session["member_id"]
    content = body["content"]
    message = Message(member_id=id, content=content)
    try:
        query.create_message(session, message)
        return {"ok": True}
    except Exception as e:
        return {"error": True}


# Get Msg API
@app.get("/api/message")
def get_message(request: Request, session: SessionDep):
    id = request.session["member_id"]
    messages = query.get_all_messages(session, id)
    if messages:
        return {"ok": True, "data": messages} 
    else:
        return {"error": True}


# Delete Msg API
@app.delete("/api/message/{id}")
def delete_message(request: Request, session: SessionDep, id: int):
    try:
        if (query.get_author_id(session, id) == request.session["member_id"]):
            query.delete_message(session, id)
            return {"ok": True}
        return {"error": True}
    except Exception as e:
        return {"error": True}