# AI Video Studio

A mobile-first prompt-to-video web application. This MVP creates short animated MP4 videos locally using Pillow + FFmpeg and provides storyboard generation, render progress, preview, and download.

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

- GET /health — health check
- POST /api/storyboards — create a 4-scene storyboard from a prompt
- POST /api/renders — queue a video render
- GET /api/renders/{job_id} — poll render progress
- GET /api/renders/{job_id}/download — download MP4

Render request JSON: `{"prompt":"A cat explores a magical forest","style":"Cartoon","mood":"Happy","ratio":"16:9","duration":8}`.

## Deployment on Railway

Set the service root directory to `/projects/ai-video-studio`, builder to Railpack, start command to `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 600 app:app`, and health check path to `/health`.

The application uses FFmpeg through the `imageio-ffmpeg` package. The built-in renderer works without API keys. Optional OpenRouter integration can be added using server-side Railway variables only; never commit API keys to GitHub or frontend JavaScript.

## Current MVP limits

The renderer produces stylized animated scenes, not photorealistic generative video. Jobs are held in process memory and output MP4 files are written to the service filesystem. For durable production use, add a persistent volume, external job queue, and object storage. A single worker is configured to avoid multiple in-memory job registries.
