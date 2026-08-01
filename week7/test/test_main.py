"""
main.py 測試檔
----------------------------------
針對 main.py 的路由(login / signup / member / message API / token API)
透過 TestClient 打 API,確認整體串接(路由 + query.py + session)是否正常。

重要提醒:
main.py 開頭 `import query`,而 query.py 在 import 的當下就會連線 MySQL
(執行 create_database_if_not_exists())。這代表要讓這份測試檔案跑起來,
你的 .env 必須指向一個真的連得到的 MySQL 伺服器,否則在 import main 這一步
就會直接失敗,不會進到任何測試案例。

DB 邏輯本身(query.py)的正確性請看 test_query.py,那邊測試不會經過 HTTP,
失敗時比較好定位是哪一層的問題。這份檔案著重在「路由邏輯」跟「串接是否正確」。
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

import main, query
from main import app, get_session
from models import Member, Message


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """覆寫 get_session,讓 API 呼叫使用測試用的記憶體資料庫"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def existing_member(session: Session):
    """預先塞一筆會員資料,方便測試登入相關功能"""
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def _login(client: TestClient, member: Member):
    """共用小工具:模擬登入,讓後續請求帶有 session"""
    client.post("/login", data={"email2": member.email, "pwd2": member.password})


# ---------- 首頁 / 頁面路由 ----------

def test_home_page(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_member_page_without_login_redirects_to_home(client: TestClient):
    response = client.get("/member", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/"


def test_member_page_with_login_shows_member_page(client: TestClient, existing_member: Member):
    _login(client, existing_member)
    response = client.get("/member")
    assert response.status_code == 200

    # response.text only captures values like {{ name }} after they have been rendered into the HTML.
    # If it isn't rendered to the frontend, the assertion will fail.
    assert existing_member.name in response.text


# ---------- 登入 / 註冊 / 登出 ----------

def test_signup_success(client: TestClient, session: Session):
    response = client.post("/signup", data={
        "name": "Ming",
        "email1": "ming@test.com",
        "pwd1": "abc123",
    }, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"

    # 額外驗證:資料真的寫進去了
    created = query.check_email(session, "ming@test.com")
    assert created is not None
    assert created.name == "Ming"


def test_signup_duplicate_email(client: TestClient, existing_member: Member):
    response = client.post("/signup", data={
        "name": "Duplicate member",
        "email1": existing_member.email,
        "pwd1": "xxxxx",
    })
    assert response.status_code == 200
    assert "重複的電子郵件" in response.text


def test_login_success(client: TestClient, existing_member: Member):
    response = client.post("/login", data={
        "email2": existing_member.email,
        "pwd2": existing_member.password,
    }, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/member"


def test_login_wrong_password(client: TestClient, existing_member: Member):
    response = client.post("/login", data={
        "email2": existing_member.email,
        "pwd2": "錯誤密碼",
    }, follow_redirects=False)
    assert response.status_code == 303
    assert "/ohoh" in response.headers["location"]


def test_logout_then_member_page_redirects_to_home(client: TestClient, existing_member: Member):
    _login(client, existing_member)
    logout_response = client.get("/logout", follow_redirects=False)
    assert logout_response.status_code == 303

    member_response = client.get("/member", follow_redirects=False)
    assert member_response.status_code == 302
    assert member_response.headers["location"] == "/"


# ---------- 留言 API (/api/message) ----------

def test_create_message_without_login_returns_error(client: TestClient):
    response = client.post("/api/message", json={"content": "測試留言"})
    assert response.status_code == 200
    assert response.json() == {"error": True}


def test_create_message_success(client: TestClient, existing_member: Member):
    _login(client, existing_member)
    response = client.post("/api/message", json={"content": "今天天氣不錯"})
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_get_message_empty_returns_error(client: TestClient, existing_member: Member):
    _login(client, existing_member)
    response = client.get("/api/message")
    assert response.json() == {"error": True}


def test_get_message_after_creating(client: TestClient, existing_member: Member):
    _login(client, existing_member)
    client.post("/api/message", json={"content": "第一則留言"})

    response = client.get("/api/message")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["self"] is True
    assert body["data"][0]["name"] == existing_member.name


def test_delete_message_by_owner(client: TestClient, existing_member: Member, session: Session):
    _login(client, existing_member)
    client.post("/api/message", json={"content": "要被刪除的留言"})
    message = session.exec(select(Message)).first()

    response = client.delete(f"/api/message/{message.id}")
    assert response.json() == {"ok": True}


def test_delete_message_by_non_owner_fails(client: TestClient, existing_member: Member, session: Session):
    _login(client, existing_member)
    client.post("/api/message", json={"content": "別人的留言"})
    message = session.exec(select(Message)).first()

    other = Member(name="別人", email="other@test.com", password="xxxxx")
    session.add(other)
    session.commit()
    session.refresh(other)

    client.get("/logout")
    _login(client, other)

    response = client.delete(f"/api/message/{message.id}")
    assert response.json() == {"error": True}


def test_delete_message_without_login_returns_error(client: TestClient, existing_member: Member, session: Session):
    # 先用登入狀態建立一則留言,再登出後嘗試刪除
    _login(client, existing_member)
    client.post("/api/message", json={"content": "留言"})
    message = session.exec(select(Message)).first()
    client.get("/logout")
 
    response = client.delete(f"/api/message/{message.id}")
    assert response.status_code == 200
    assert response.json() == {"error": True}


# ---------- Token API ----------

def test_update_token_without_login_returns_error(client: TestClient):
    response = client.put("/api/token")
    assert response.json() == {"error": True}


def test_update_token_success(client: TestClient, existing_member: Member):
    _login(client, existing_member)

    response = client.put("/api/token")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert len(body["token"]) == 64   # sha256 hexdigest
