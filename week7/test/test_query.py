"""
query.py 測試檔
----------------------------------
這裡直接呼叫 query.py 裡的函式,不透過 HTTP、不透過 main.py 的路由,
專注測試資料庫邏輯本身是否正確,失敗時比較好定位問題。

重要提醒:
query.py 在被 import 的當下就會執行 create_database_if_not_exists(),
實際去連線 MySQL 伺服器。也就是說,光是這個檔案最上面的 `import query`,
就需要你的 .env 指向一個真的連得到的 MySQL,否則會在收集測試階段就報錯。
之後可以考慮把這段連線邏輯改成不要在 import 時就自動執行
(例如搬進 main.py 的 lifespan,或包成一個要手動呼叫的函式),
測試環境會單純很多。
"""

import query
from models import Member, Message


# ---------- check_email ----------

def test_check_email_found(session):
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()

    result = query.check_email(session, "jung@test.com")
    assert result is not None
    assert result.email == "jung@test.com"


def test_check_email_not_found(session):
    result = query.check_email(session, "nobody@test.com")
    assert result is None


# ---------- validate_login ----------

def test_validate_login_success(session):
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()

    result = query.validate_login(session, "jung@test.com", "12345")
    assert result is not None
    assert result.name == "Jung"


def test_validate_login_wrong_password(session):
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()

    result = query.validate_login(session, "jung@test.com", "錯誤密碼")
    assert result is None


# ---------- create_member ----------

def test_create_member(session):
    member = Member(name="小明", email="ming@test.com", password="abc123")
    result = query.create_member(session, member)

    assert result.id is not None
    assert result.follower_count == 0    # server_default = "0"
    assert result.time is not None       # server_default = CURRENT_TIMESTAMP


# ---------- message 相關 ----------

def test_create_message_and_get_author_id(session):
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()
    session.refresh(member)

    message = query.create_message(session, Message(member_id=member.id, content="測試留言"))

    assert query.get_author_id(session, message.id) == member.id


def test_get_all_messages_marks_self_correctly(session):
    me = Member(name="我", email="me@test.com", password="12345")
    other = Member(name="別人", email="other@test.com", password="12345")
    session.add(me)
    session.add(other)
    session.commit()
    session.refresh(me)
    session.refresh(other)

    query.create_message(session, Message(member_id=me.id, content="我的留言"))
    query.create_message(session, Message(member_id=other.id, content="別人的留言"))

    messages = query.get_all_messages(session, me.id)
    assert len(messages) == 2

    my_message = next(m for m in messages if m["content"] == "我的留言")
    others_message = next(m for m in messages if m["content"] == "別人的留言")

    assert my_message["self"] is True
    assert others_message["self"] is False
    assert my_message["name"] == "我"


def test_delete_message(session):
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()
    session.refresh(member)

    message = query.create_message(session, Message(member_id=member.id, content="要刪除的留言"))
    query.delete_message(session, message.id)

    assert session.get(Message, message.id) is None


# ---------- token 相關 ----------

def test_update_token_generates_new_token(session):
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()
    session.refresh(member)

    token = query.update_token(session, member.id)

    assert len(token) == 64          # sha256 hexdigest 固定長度
    assert member.token == token


def test_get_member_by_token(session):
    member = Member(name="Jung", email="jung@test.com", password="12345")
    session.add(member)
    session.commit()
    session.refresh(member)

    token = query.update_token(session, member.id)
    found = query.get_member_by_token(session, token)

    assert found is not None
    assert found.id == member.id
