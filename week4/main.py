import json
import time

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from urllib import request as req


app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = "templates")
# Session
app.add_middleware(SessionMiddleware, secret_key = "jung-secret-key")


# index.html
@app.get("/")
async def home(request: Request):

    # Already logged in -> Redirect to the member page
    if request.session.get("logged_in"):
            return RedirectResponse(url = "/member", status_code = 303)
    
    return templates.TemplateResponse(
        request = request, name = "index.html", context = {}
    )


@app.post("/login")
async def login(request: Request, email: str = Form(""), pwd: str = Form("")):

        # email or password is empty
        if not email or not pwd: 
            msg = "請輸入信箱和密碼"
        elif email == "abc@abc.com" and pwd == "abc":
            request.session["logged_in"] = True
            return RedirectResponse(url = "/member", status_code = 303)
        else:   # wrong email or password
            msg = "帳號或密碼輸入錯誤"

        return RedirectResponse(
                url = f"/ohoh?msg={msg}", status_code = 303)
        

# member.html
@app.get("/member")
async def member(request: Request):
    return templates.TemplateResponse(request, "member.html")


# ohoh.html
@app.get("/ohoh")
async def error_msg(request: Request, msg: str = ""):
    return templates.TemplateResponse(request, "ohoh.html", {"msg": msg})


# logout.html
@app.get("/logout")
async def logout(request: Request):
    request.session["logged_in"] = False
    return RedirectResponse(url = "/", status_code = 303)


# hotel.html
@app.get("/hotel/{hotel_num}")
async def get_hotel(request: Request, hotel_num: int):

    # Get hotels data 
    hotels_data = retrieve_hotels_data()

    # Retrieve hotel info by its id
    if hotel_num in hotels_data:
        hotel_info = "、".join(hotels_data[hotel_num])
    else:
        hotel_info = "查詢不到相關資料"
    return templates.TemplateResponse(
        request = request, name = "hotel.html", context = {"hotel_info": hotel_info}
    )


# Sources of the hotel data
SRC_CN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
SRC_ENG = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

# Cache for hotels' info
hotels_cache = {}
cache_updated_at = 0
# Update data every 5 mins (Time To Live)
CACHE_TTL = 300
  
def retrieve_hotels_data():
    """ Retrieve and process hotel data and return a dict for all hotels
        and update the cache as needed when the required time has passed

    Returns:
        dict: A dict storing hotel info in required format
    """

    global hotels_cache, cache_updated_at

    if hotels_cache and (time.time() - cache_updated_at < CACHE_TTL):
        return hotels_cache

    try:
        # Process hotel data and extract into lists
        with req.urlopen(SRC_CN) as response:
            data_cn = json.load(response)

        with req.urlopen(SRC_ENG) as response:
            data_eng = json.load(response)

        h_list_cn = data_cn["list"]
        h_list_eng = data_eng["list"]


        # Temporary dict to hold freshly fetched data before replacing the cache
        new_data = {}

        # Store required data into dict
        for hotel in h_list_cn:
            if hotel["_id"] not in new_data:
                new_data[hotel["_id"]] = [hotel["旅宿名稱"]]

        for hotel in h_list_eng:
            if hotel["_id"] in new_data:
                new_data[hotel["_id"]] += [hotel["hotel name"], hotel["tel"]]


        # Update the hotel cache and its timestamp
        hotels_cache = new_data
        cache_updated_at = time.time()
    except Exception as e:
        print(f"Failed to fetch hotel data: {e}")
        # On failure, fall back to the existing cache (can be stale or empty)
        return hotels_cache

    return hotels_cache