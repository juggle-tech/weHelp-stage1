import query
from fastmcp import FastMCP
from sqlmodel import Session
from query import engine
from models import Message
from fastmcp.server.dependencies import get_http_headers
from fastmcp.exceptions import ToolError


mcp = FastMCP("Testing Message Website")

def get_member_id():
    headers = get_http_headers()
    print(f"DEBUG all headers = {headers}")
    auth = get_http_headers().get("authorization")
    if not auth:
        raise ToolError(auth)
    token = auth.removeprefix("Bearer ").strip()
    with Session(engine) as session:
        member = query.get_member_by_token(session, token)
        if member:
            return member.id
        raise ToolError("Invalid token, Check Authorization header")
    

@mcp.tool
def create_message(content: str) -> dict:
    # Get member id using token
    member_id = get_member_id()
    if not member_id:
        return {"error": True}
    
    # Create a new message
    message = Message(member_id=member_id, content=content)
    with Session(engine) as session:
        result = query.create_message(session, message)
        if result:
            return {"ok": True, "result": result.model_dump()}
        return {"error": True}

mcp_app = mcp.http_app(path="/")