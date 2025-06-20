# TODO: enforce HTTPS
# TODO: rotate API keys
# TODO: add rate limiting
import os, time
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from .retriever import retrieve
from .llm_loader import stream
try:
    from clickhouse_connect import get_client
    ck = get_client(url=os.getenv("CLICKHOUSE_URL", "http://localhost:8123"))
    ck.command(
        "CREATE TABLE IF NOT EXISTS logs (q String, a String, ts DateTime) ENGINE=MergeTree ORDER BY ts"
    )
except Exception:  # pragma: no cover - optional DB
    class _Dummy:
        def insert(self, *a, **kw):
            pass

        def command(self, *a, **kw):
            pass

    ck = _Dummy()

API_KEY = os.getenv("API_KEY", "dev")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("fastapi_app/templates/index.html").read_text()


def auth(key: str | None):
    if key != API_KEY:
        raise HTTPException(status_code=401)


@app.post("/ask")
async def ask(req: Request, x_api_key: str = Header(None)):
    auth(x_api_key)
    q = (await req.json())["query"]
    docs = retrieve(q)
    prompt = q + "\n" + "\n".join(t for t, _ in docs)
    if "text/event-stream" in req.headers.get("accept", ""):
        async def gen():
            ans = ""
            for t in stream(prompt):
                ans += t
                yield f"data: {t}\n\n"
            yield "data: [DONE]\n\n"
            ck.insert("logs", [{"q": q, "a": ans, "ts": time.time()}])
        return StreamingResponse(gen(), media_type="text/event-stream")
    ans = "".join(stream(prompt))
    ck.insert("logs", [{"q": q, "a": ans, "ts": time.time()}])
    cites = [f"{i}:0" for _, i in docs]
    return {"answer": ans, "citations": cites}
