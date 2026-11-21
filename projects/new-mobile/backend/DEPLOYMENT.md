# New Mobile backend deployment

This backend needs a host that can run Docker, Chromium, and a persistent writable disk.

## Required configuration

- `PORT`: supplied by many hosts; defaults to 8000.
- `NEW_MOBILE_DATA_DIR`: set to a persistent mounted directory (the Dockerfile defaults to `/data`).
- `NEW_MOBILE_ACCESS_KEY`: set a long, random secret before exposing the API publicly. The frontend sends it as a Bearer token.
- `CORS_ORIGINS`: set to the exact HTTPS origin serving the frontend. Do not leave the wildcard default for a public deployment.

Mount a persistent disk at `/data`. Without persistent storage, browser logins and cookies can be lost when the service restarts or is redeployed.

## Start locally with Docker

From this directory:

```bash
docker build -t new-mobile-backend .
docker run --rm -p 8000:8000 \
  -e NEW_MOBILE_ACCESS_KEY="replace-with-a-long-random-secret" \
  -e CORS_ORIGINS="http://localhost:8080" \
  -v new-mobile-data:/data \
  new-mobile-backend
```

Then check `http://localhost:8000/api/v1/health`. Configure the frontend's Settings with the backend base URL and the same access key.

## Deployment checklist

1. Deploy this Dockerfile to a container host that supports Chromium.
2. Attach a persistent disk at `/data`.
3. Set the environment variables above using the host's secret manager.
4. Restrict CORS to the frontend's exact origin.
5. Check the health endpoint.
6. Open the frontend, save the backend URL and access key, then test ON, navigation, OFF, and NEW.

## Important

- A running health endpoint does not by itself prove that Chromium can launch; test ON after deployment.
- Do not commit access keys, passwords, cookies, or browser profile data to GitHub.
- This is a remote web browser, not Android Runtime. It cannot install APKs or run native Android apps.
- Websites may block remote browser automation or limit their web versions.
- Review and harden authentication, rate limiting, and SSRF protections before public production use. The current backend remains an MVP.
