from __future__ import annotations

import asyncio
import ipaddress
import json
import os
import shutil
import socket
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from fastapi import Depends, FastAPI, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from playwright.async_api import async_playwright, BrowserContext, Page, Route

DATA_DIR = Path(os.getenv("NEW_MOBILE_DATA_DIR", "./data"))
PROFILE_DIR = DATA_DIR / "browser-profile"
STATE_FILE = DATA_DIR / "session.json"
ACCESS_KEY = os.getenv("NEW_MOBILE_ACCESS_KEY", "").strip()
ALLOWED_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(",") if x.strip()]

playwright_manager: Any = None
context: BrowserContext | None = None
page: Page | None = None
lock = asyncio.Lock()
history: list[dict[str, str]] = []
session_id = str(uuid.uuid4())
profile_id = str(uuid.uuid4())
state = "stopped"
current_url: str | None = None
created_at = datetime.now(timezone.utc).isoformat()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def persist() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "session_id": session_id, "profile_id": profile_id,
        "state": state, "current_url": current_url,
        "history": history, "updated_at": now()
    }, indent=2), encoding="utf-8")


def require_key(authorization: str | None = Header(default=None)) -> None:
    if ACCESS_KEY and authorization != f"Bearer {ACCESS_KEY}":
        raise HTTPException(status_code=401, detail="Invalid access key")


async def public_http_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise HTTPException(status_code=400, detail="Only http and https links are supported")
    host = parsed.hostname
    if host.lower() in {"localhost", "localhost.localdomain"}:
        raise HTTPException(status_code=400, detail="Local and private network addresses are blocked")
    try:
        records = await asyncio.get_running_loop().getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)
        addresses = {ipaddress.ip_address(row[4][0]) for row in records}
        if not addresses or any(not address.is_global for address in addresses):
            raise HTTPException(status_code=400, detail="Private or local network destinations are blocked")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Could not resolve destination host")
    return value


async def guard_route(route: Route) -> None:
    try:
        await public_http_url(route.request.url)
        await route.continue_()
    except HTTPException:
        await route.abort("blockedbyclient")
    except Exception:
        await route.abort("failed")


async def close_context() -> None:
    global context, page
    if context:
        await context.close()
    context = None
    page = None


async def launch_context() -> None:
    global context, page, state
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    context = await playwright_manager.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=True,
        viewport={"width": 390, "height": 844},
        device_scale_factor=1,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    context.set_default_timeout(15000)
    await context.route("**/*", guard_route)
    page = context.pages[0] if context.pages else await context.new_page()
    page.on("framenavigated", lambda frame: _record_navigation(frame.url) if frame == page.main_frame else None)
    state = "running"
    persist()


def _record_navigation(url: str) -> None:
    global current_url
    if url.startswith(("http://", "https://")):
        current_url = url
        history.append({"url": url, "title": "", "visited_at": now()})
        del history[:-100]
        persist()


def session_info() -> dict[str, Any]:
    return {
        "session_id": session_id, "state": state, "profile_id": profile_id,
        "current_url": current_url, "runtime_available": True,
        "viewport": {"width": 390, "height": 844}, "updated_at": now()
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    global playwright_manager, session_id, profile_id, state, current_url
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            saved = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            session_id = saved.get("session_id", session_id)
            profile_id = saved.get("profile_id", profile_id)
            current_url = saved.get("current_url")
            history.extend(saved.get("history", []))
        except Exception:
            pass
    playwright_manager = await async_playwright().start()
    yield
    await close_context()
    await playwright_manager.stop()


app = FastAPI(title="New Mobile API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=False, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/api/v1/health")
async def health(_: None = Depends(require_key)):
    return {"ok": True, "runtime_available": True, "runtime": "remote Chromium browser"}


@app.post("/api/v1/session/start")
async def start(_: None = Depends(require_key)):
    global state
    async with lock:
        if context is None:
            try:
                await launch_context()
            except Exception as exc:
                state = "unavailable"
                raise HTTPException(status_code=503, detail=f"Browser runtime could not start: {type(exc).__name__}")
        else:
            state = "running"
        persist()
        return session_info()


@app.get("/api/v1/session/{sid}")
async def get_status(sid: str, _: None = Depends(require_key)):
    if sid != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_info()


@app.post("/api/v1/session/{sid}/stop")
async def stop(sid: str, _: None = Depends(require_key)):
    global state
    if sid != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    async with lock:
        await close_context()
        state = "stopped"
        persist()
        return session_info()


@app.post("/api/v1/session/{sid}/reset")
async def reset(sid: str, _: None = Depends(require_key)):
    global session_id, profile_id, current_url, state
    if sid != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    async with lock:
        await close_context()
        shutil.rmtree(PROFILE_DIR, ignore_errors=True)
        history.clear()
        session_id = str(uuid.uuid4())
        profile_id = str(uuid.uuid4())
        current_url = None
        state = "stopped"
        persist()
        await launch_context()
        return session_info()


class NavigateBody(BaseModel):
    url: str = Field(min_length=4, max_length=2048)


@app.post("/api/v1/session/{sid}/navigate")
async def navigate(sid: str, body: NavigateBody, _: None = Depends(require_key)):
    global current_url
    if sid != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    if context is None or page is None:
        raise HTTPException(status_code=409, detail="Tap ON to start the browser first")
    url = await public_http_url(body.url)
    async with lock:
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            current_url = page.url
            title = await page.title()
            if history and history[-1]["url"] == current_url:
                history[-1]["title"] = title
            persist()
            return session_info()
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Website navigation failed: {type(exc).__name__}")


class InputBody(BaseModel):
    type: str
    x: int | None = None
    y: int | None = None
    dx: int = 0
    dy: int = 0
    text: str | None = Field(default=None, max_length=4000)
    key: str | None = None


@app.post("/api/v1/session/{sid}/input", status_code=204)
async def input_event(sid: str, body: InputBody, _: None = Depends(require_key)):
    if sid != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    if page is None:
        raise HTTPException(status_code=409, detail="Browser is stopped")
    if body.type == "tap":
        await page.mouse.click(body.x or 0, body.y or 0)
    elif body.type == "scroll":
        await page.mouse.wheel(body.dx, body.dy)
    elif body.type == "text":
        await page.keyboard.insert_text(body.text or "")
    elif body.type == "key":
        allowed = {"Enter", "Backspace", "Tab", "Escape"}
        if body.key not in allowed:
            raise HTTPException(status_code=400, detail="Unsupported key")
        await page.keyboard.press(body.key)
    elif body.type == "back":
        await page.go_back(wait_until="domcontentloaded")
    elif body.type == "forward":
        await page.go_forward(wait_until="domcontentloaded")
    elif body.type == "reload":
        await page.reload(wait_until="domcontentloaded")
    else:
        raise HTTPException(status_code=400, detail="Unsupported input event")
    return Response(status_code=204)


@app.get("/api/v1/session/{sid}/frame")
async def frame(sid: str, _: None = Depends(require_key)):
    if sid != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    if page is None:
        raise HTTPException(status_code=409, detail="Browser is stopped")
    data = await page.screenshot(type="jpeg", quality=70, full_page=False)
    return Response(content=data, media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@app.get("/api/v1/session/{sid}/history")
async def get_history(sid: str, _: None = Depends(require_key)):
    if sid != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    return history
