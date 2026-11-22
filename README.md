# Portfolio

A growing collection of independent web projects. Each project lives in its own folder under `projects/`.

**Projects listed: 5**

## Projects

1. **Sajji & Rice** — `projects/website-development-agent/`
2. **NEXA AI Productivity** — `projects/nexa-ai-productivity/`
3. **KaamFlow — Service Business Workspace** — `projects/kaamflow/`
   - Responsive frontend demo for service businesses, with jobs, quotes, customers, invoices, reports and browser-local demo persistence.
4. **New Mobile — Remote Browser Workspace** — `projects/new-mobile/`
   - A mobile-first remote browser workspace built with an HTML/CSS/JavaScript frontend and a Python FastAPI + Playwright backend.
   - Includes ON/OFF/NEW session controls, remote Chromium browsing, URL navigation, page interaction and browser-profile reset.
   - The MVP has been run and tested. It is a remote browser workspace, **not** a full Android emulator or a second physical phone; it does not provide a new IMEI, MAC address or phone IP.
   - Frontend: [Open New Mobile](https://fiver91eb-beep.github.io/website-development-agent/)
   - Backend health endpoint: [Check backend health](https://new-mobile-backend-production.up.railway.app/healthz)
   - Source: [New Mobile project folder](https://github.com/fiver91eb-beep/website-development-agent/tree/main/projects/new-mobile)

## Running the projects

Open static frontend projects' `index.html` directly. New Mobile additionally requires its Python FastAPI + Playwright backend on a host that supports Chromium browser execution.

## Portfolio note

The count above reflects the four projects currently listed in this repository. Project scope and completion level differ: KaamFlow is documented as a frontend prototype, while New Mobile is a deployed remote-browser MVP with known platform limitations and ongoing interaction refinements.


5. **AI Video Studio** — `projects/ai-video-studio/`
   - Mobile-first prompt-to-video creator with storyboard generation, animation rendering, progress tracking, browser preview and MP4 download.
   - Python Flask backend with Pillow + FFmpeg renderer; optional OpenRouter storyboard generation supports two server-side API keys with failover.
   - Railway deployment is configured separately for this folder; render files and in-memory jobs are MVP-only and need persistent storage/queue for production.
   - Source: [AI Video Studio project folder](https://github.com/fiver91eb-beep/website-development-agent/tree/main/projects/ai-video-studio)
