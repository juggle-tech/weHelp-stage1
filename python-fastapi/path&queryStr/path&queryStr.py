from fastapi import FastAPI

app = FastAPI()


## Path
# 路徑 / 的路由範例
@app.get("/")
def index():
    return {"data": "Home Page"}


# 路徑 /data 的路由範例
@app.get("/data")
def getData():
    return {"data": [2, 3, 1]}


@app.get("/user/{name}")
def getUser(name):
    return {"echo": "Hello " + name}


# Type Hint
@app.get("/square/{number}")
def square(number: int):
    return {"result": number * number}


@app.get("/square/{number}")
def square(number):
    number = int(number)  # 轉成整數型別
    return {"result": number * number}


## Query string
# 處理路徑 /hello?name=名字
@app.get("/hello")
def hello(name):
    message = "哈囉，" + name
    return {"message": message}


# 處理路徑 /multiply?n1=數字&n2=數字
@app.get("/multiply")
def multiply(n1, n2):
    n1 = int(n1)
    n2 = int(n2)
    result = n1 * n2
    return {"result": result}