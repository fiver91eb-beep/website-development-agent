# New Mobile

A mobile-first, remote isolated browser workspace. This is **not an Android emulator** and does not create a physical second phone.

## Project structure
- `frontend/index.html` — phone-friendly browser workspace UI
- `backend/main.py` — Python FastAPI API with Playwright persistent Chromium profile
- `backend/requirements.txt` — Python dependencies
- `backend/README.md` — backend setup and API details

## Controls
- **ON**: start or resume the remote browser profile
- **OFF**: close the browser while keeping its profile in the running service's temporary filesystem
- **NEW**: delete the old profile and create a fresh one

## Important limitations
- Sites run in remote Chromium, not in the phone's local Chrome.
- The server's public IP is used; there is no unique phone IP, MAC address, IMEI, or iPhone identity.
- Sites may block remote browsing or automation; not every app feature is available on the web.
- The profile is temporary: it normally remains available while the Railway service process stays alive, but a restart or redeploy can erase it. No persistent volume is attached.
- Set a backend access key and restrict CORS before public deployment.
- The backend is configured on Railway. Confirm its public health endpoint and test ON/NEW in the browser before relying on it.

## Run
Serve `frontend/index.html` as a static page. Run the backend according to `backend/README.md`, then set the backend API base URL in the frontend's Settings.
