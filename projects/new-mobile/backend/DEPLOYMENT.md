# New Mobile backend deployment

This backend needs a host that can run Docker, Chromium, and a writable filesystem. A persistent disk is optional: use one only if browser logins must survive server restarts or redeploys.

## Required configuration

- `PORT`: supplied by many hosts; defaults to 8000.
- `NEW_MOBILE_DATA_DIR`: writable directory for the temporary browser profile (the Dockerfile defaults to `/data`).
- `NEW_MOBILE_ACCESS_KEY`: set a long, random secret before exposing the API publicly. The frontend sends it as a Bearer token.
- `CORS_ORIGINS`: set to the exact HTTPS origin serving the frontend. Do not leave the wildcard default for a public deployment.

For the requested temporary-use setup, do **not** attach a persistent volume. The profile exists only on the running service filesystem: OFF then ON can reuse it while the service stays alive, and NEW deletes it. A service restart or redeploy may erase the profile and logins. Attach a persistent disk at `/data` only if that behavior is later desired.

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

## Deploy with Railway

The repository includes `railway.json` for the backend service. In Railway, create a project from the GitHub repository `fiver91eb-beep/website-development-agent`, then set the service root directory to `/projects/new-mobile/backend`. Railway will build the included Dockerfile and use `/healthz` for its container health check.

Before exposing the service:

1. Do not add a Railway Volume for the temporary-use setup (a volume is optional only for retaining sessions across service restarts).
2. Set `NEW_MOBILE_DATA_DIR=/data`.
3. Set `NEW_MOBILE_ACCESS_KEY` to a long random secret in Railway Variables.
4. Set `CORS_ORIGINS` to the exact HTTPS origin of the published New Mobile frontend (no trailing slash).
5. Generate a public HTTPS domain for the service.
6. Open `https://YOUR-DOMAIN/healthz` and confirm it returns `{\"ok\":true}`.
7. Open `https://YOUR-DOMAIN/api/v1/health` with the Bearer access key and confirm `runtime_available=true`.
8. In the frontend Settings, enter the service base URL and access key; then test ON, navigate to a public website, OFF, ON again, and NEW.

The deployment is not complete until Chromium starts successfully and all browser controls are tested. For temporary use, no persistent volume is required; browser data can disappear after a service restart or redeploy. Railway account connection, project creation, volume provisioning, variables, and domain generation require authorization in the user's Railway workspace.
