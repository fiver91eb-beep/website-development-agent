# New Mobile

A mobile-first, remote isolated browser workspace. This is **not an Android emulator** and does not create a physical second phone.

## Project structure
- `frontend/index.html` — phone-friendly browser workspace UI
- `backend/main.py` — Python FastAPI API with Playwright persistent Chromium profile
- `backend/requirements.txt` — Python dependencies
- `backend/README.md` — backend setup and API details

## Controls
- **ON**: start or resume the remote browser profile
- **OFF**: close the browser while keeping its profile data on the backend's persistent disk
- **NEW**: delete the old profile and create a fresh one

## Important limitations
- Sites run in remote Chromium, not in the phone's local Chrome.
- The server's public IP is used; there is no unique phone IP, MAC address, IMEI, or iPhone identity.
- Sites may block remote browsing or automation; not every app feature is available on the web.
- Persistent logins require durable server storage. Ephemeral hosting can lose the profile.
- Set a backend access key and restrict CORS before public deployment.
- Replit app creation could not be authorized in this account during the initial setup; deployment has not been configured or tested.

## Run
Serve `frontend/index.html` as a static page. Run the backend according to `backend/README.md`, then set the backend API base URL in the frontend's Settings.
