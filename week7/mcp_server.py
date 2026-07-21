import query

from fastmcp import FastMCP
from sqlmodel import Session
from fastmcp.server.dependencies import get_http_request
from query import engine
from models import Message


mcp = FastMCP("Testing Message Website")

def get_member_id():
    # Get token
    request = get_http_request()
    auth = request.headers.get("authorization", "")

    if not auth.startswith("Bearer "):
        return None

    token = auth.removeprefix("Bearer ").strip()

    # Get member info
    with Session(engine) as session:
        member = query.get_member_by_token(session, token)

    if member:
        return member.id

    return None


@mcp.tool
def create_message(content: str) -> dict:
    """在 Message 網站建立一則留言。

    當使用者說「請幫我在 Message 網站留言」時使用。
    參數 content 是留言內容。
    成功後回傳已建立留言的確認訊息: 「content」。

    """
    member_id = get_member_id()

    if member_id is None:
        return {"error": True}

    # Create the new message
    with Session(engine) as session:
        result = query.create_message(
            session,
            Message(member_id=member_id, content=content),
        )

    if result is None:
        return {"error": True}

    return {"ok": True}

mcp_app = mcp.http_app(path="/")