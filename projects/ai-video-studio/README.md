# AI Video Studio

A mobile-first prompt-to-video web app. It creates short animated MP4 videos and includes optional OpenRouter-powered storyboard generation.

## Current capabilities

- Prompt-based 4-scene storyboard generation.
- Optional OpenRouter integration using server-side environment variables.
- Built-in animated MP4 renderer with Cartoon, Storybook, Minimal and Neon style choices in the UI (the renderer currently uses a procedural cartoon animation pipeline).
- Landscape (16:9), portrait (9:16), and square (1:1) output.
- Render progress, in-browser preview, and MP4 download.
- Flask JSON API and health endpoint.

**Important:** This version does not generate photorealistic AI video frames. OpenRouter is used for storyboard text only; the MP4 is rendered by the built-in Pillow + FFmpeg animation renderer. A dedicated video-generation provider/API is required for true generative text-to-video output.

## Run locally

Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000.

## API

- GET /health
- POST /api/storyboards
- POST /api/renders
- GET /api/renders/{job_id}
- GET /api/renders/{job_id}/download

Render request JSON:
```json
{"prompt":"A cat explores a magical forest","style":"Cartoon","mood":"Happy","ratio":"16:9","duration":8}
```

## Railway deployment

Set the service root directory to `/projects/ai-video-studio`, builder to Railpack, start command to:

```bash
gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 600 app:app
```

Health check path: `/health`.

Optional server-side variables:
- `OPENROUTER_API_KEY_1`
- `OPENROUTER_API_KEY_2`

Never put API keys in frontend JavaScript or commit them to GitHub. The app tries the first key, then the second if needed.

## MVP deployment notes

Render jobs and status are held in process memory; rendered MP4 files are written to the service filesystem. Jobs/files may be lost on restart or redeploy. For production, add a persistent volume, external job queue, and object storage. A single Gunicorn worker is configured for the in-memory job registry.
