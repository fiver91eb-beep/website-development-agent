# New Mobile — isolated browser MVP

This project is a **remote Chromium browser workspace**, not an Android emulator and not a physical-device identity generator.

## What it does
- ON starts a remote Chromium browser with its own persistent browser profile.
- OFF closes the running browser but keeps the profile directory so website sessions can resume.
- NEW deletes the old profile directory and creates a clean profile.
- Links are opened remotely; the phone receives screenshots and sends tap/scroll/text input.
- The browser's public egress IP belongs to the hosting server. This does not create a new physical phone, MAC address, IMEI, or iPhone identity.
- Websites may restrict remote browsers or automation; a website's full mobile-app functionality is not guaranteed.

## Backend
Python FastAPI + Playwright Chromium. See `requirements.txt` and `main.py`.

Environment:
- `NEW_MOBILE_DATA_DIR`: persistent data directory (default `./data`). Must survive app restarts if sessions are to persist.
- `NEW_MOBILE_ACCESS_KEY`: optional bearer key. Set this before exposing the API publicly.
- `CORS_ORIGINS`: comma-separated frontend origins (default `*`; set a specific origin for deployment).

Install Python dependencies, install Playright's Chromium browser and OS libraries for the host, then run:
`uvicorn main:app --host 0.0.0.0 --port 8000`

**Important deployment limitation:** The host must support running Chromium and persistent disk. Some free serverless/sleeping/ephemeral hosts will not reliably support browser sessions or preserve profiles. Replit account creation/deployment access was not confirmed in this build, so hosting is not configured.

## API
- `GET /api/v1/health`
- `POST /api/v1/session/start`
- `GET /api/v1/session/{id}`
- `POST /api/v1/session/{id}/stop`
- `POST /api/v1/session/{id}/reset`
- `POST /api/v1/session/{id}/navigate` body: `{"url":"https://example.com"}`
- `POST /api/v1/session/{id}/input`
- `GET /api/v1/session/{id}/frame`
- `GET /api/v1/session/{id}/history`

The backend blocks localhost/private-network destinations to reduce SSRF risk. It is still an MVP: do not expose it publicly without setting an access key, restricting CORS, and reviewing security.
