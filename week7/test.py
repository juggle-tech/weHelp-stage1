
import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8000/mcp/",
            headers={
                "Authorization": "Bearer 3db7e13967291d3a8d40578e2be758f98032261ce1d9891129380991ad7203d9",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "id": 1,
                "params": {},
            },
        )
        print(resp.status_code)
        print(resp.text[:500])

asyncio.run(test())