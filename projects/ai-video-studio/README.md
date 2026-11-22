# AI Video Studio — No-API Cartoon Animator

A prompt-driven cartoon animation MVP. It runs on its own Python backend and does not require OpenRouter keys or any paid AI API.

## What it does
- Enter a prompt; built-in keyword understanding identifies supported subjects (bird, cat, dog, butterfly, fish, person) and actions (fly, play, run, jump, sleep, swim, walk, dance).
- Mood words such as happy, sad, sleepy and angry influence the storyboard/mood label.
- Creates a multi-scene storyboard and renders an MP4 with moving cartoon characters, scene transitions by action, captions and optional play-ball/water effects.
- Landscape, portrait and square MP4; progress, preview and download.
- No API key is read, sent, or needed.

## Honest limitations
This is a self-contained procedural 2D cartoon animator, not a general-purpose AI video model. It understands a supported set of words and draws supported cartoon subjects/actions with code. It cannot accurately animate every arbitrary object, detailed plot, exact physical movement, or produce photorealistic footage. The app can render repeated videos without API quotas, but practical throughput is limited by Railway CPU, execution time, and available disk space.

## Run locally
Python 3.11+; install requirements with `pip install -r requirements.txt`, then `python app.py`; open http://localhost:5000.

## Railway
Root directory: `/projects/ai-video-studio`
Start command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 600 app:app`
Health check: `/health`
No environment variables/API keys required.
