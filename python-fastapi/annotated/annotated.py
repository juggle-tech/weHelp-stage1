from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

# 處理路徑 /square/數字
@app.get("/square/{number}")
def square(number: Annotated[int, Path(ge=1)]):
    number = int(number)
    result = number * number
    return {"result": result}


# 處理路徑 /user/帳號
@app.get("/user/{account}")
def user(
  account: Annotated[str, Path(
    min_length=2, max_length=8
  )]
):
  return {"message": "Hello, " + account}


# 處理路徑 /multiply?n1=數字&n2=數字
@app.get("/multiply")
def multiply( 
  n1: Annotated[int, Query(ge=0, le=10)],
  n2: Annotated[int, Query(ge=0, le=10)]
):
  n1 = int(n1)
  n2 = int(n2)
  result = n1 * n2
  return {"result": result}


@app.get("/multiply")
def hello(
  n1: Annotated[int, Query(ge=-10, le=10)],
  n2: Annotated[int, Query(ge=-10, le=10)]
):
  n1 = int(n1)
  n2 = int(n2)
  return {"result": n1 * n2}


@app.get("/echo/{name}")
def echo(name: Annotated[str, Path(min_length=2, max_length=30)]):
    return {"message": "Hello " + name}

@app.get("/hello")
def hello(name: Annotated[str, Query(min_length=3)]):
    return {"message": "Hello " + name}