import os, uuid, threading, traceback, requests, json
from flask import Flask, request, jsonify, send_file
from renderer import render_video, make_storyboard

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
JOBS = {}
LOCK = threading.Lock()
OUTPUT = os.path.join(os.path.dirname(__file__), "renders")
os.makedirs(OUTPUT, exist_ok=True)

@app.get("/")
def home():
    return app.send_static_file("index.html")

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "AI Video Studio", "renderer": "Pillow + FFmpeg"})

def ai_storyboard(prompt, style, duration):
    keys = [os.getenv("OPENROUTER_API_KEY_1"), os.getenv("OPENROUTER_API_KEY_2")]
    keys = [k for k in keys if k]
    for key in keys:
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", timeout=35,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                         "HTTP-Referer": os.getenv("APP_URL", "https://railway.app"),
                         "X-Title": "AI Video Studio"},
                json={"model": "openrouter/auto", "messages": [
                    {"role": "system", "content": "You are a concise video creative director. Return only valid JSON with keys title and scenes. scenes must be an array of exactly 4 objects, each with scene, time, title, description."},
                    {"role": "user", "content": f"Create a {duration}-second {style} video storyboard for: {prompt}. Make four sequential visual scenes."}
                ], "temperature": 0.7})
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            content = content.strip().removeprefix("```json").removesuffix("```").strip()
            result = json.loads(content)
            if isinstance(result.get("scenes"), list) and result["scenes"]:
                return {"title": result.get("title", prompt[:48]), "style": style,
                        "duration": duration, "scenes": result["scenes"][:4], "ai_generated": True}
        except Exception:
            continue
    return None

@app.post("/api/storyboards")
def storyboard():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    if not prompt:
        return jsonify({"error": "Please describe your video first."}), 400
    style = data.get("style", "Cartoon")
    duration = max(4, min(20, int(data.get("duration", 8))))
    result = ai_storyboard(prompt, style, duration) or make_storyboard(prompt, style, duration)
    result["ai_generated"] = result.get("ai_generated", False)
    return jsonify(result)

@app.post("/api/renders")
def create_render():
    data = request.get_json(silent=True) or {}
    prompt = str(data.get("prompt", "")).strip()
    if not prompt:
        return jsonify({"error": "A video prompt is required."}), 400
    job_id = uuid.uuid4().hex[:12]
    with LOCK:
        JOBS[job_id] = {"id": job_id, "status": "queued", "progress": 0, "message": "Waiting to render", "file": None}
    thread = threading.Thread(target=run_job, args=(job_id, data), daemon=True)
    thread.start()
    return jsonify({"job_id": job_id, "status": "queued"}), 202

def run_job(job_id, data):
    def update(progress, message):
        with LOCK:
            if job_id in JOBS:
                JOBS[job_id].update(progress=progress, message=message, status="rendering")
    try:
        path = render_video(data, OUTPUT, update)
        with LOCK:
            JOBS[job_id].update(status="completed", progress=100, message="Your video is ready", file=path)
    except Exception as exc:
        traceback.print_exc()
        with LOCK:
            JOBS[job_id].update(status="failed", message=str(exc), error="Render failed")

@app.get("/api/renders/<job_id>")
def render_status(job_id):
    with LOCK:
        job = JOBS.get(job_id)
        if not job:
            return jsonify({"error": "Render not found. Jobs may reset when the server restarts."}), 404
        result = {k:v for k,v in job.items() if k != "file"}
        if job.get("status") == "completed":
            result["download_url"] = f"/api/renders/{job_id}/download"
        return jsonify(result)

@app.get("/api/renders/<job_id>/download")
def download(job_id):
    with LOCK:
        job = JOBS.get(job_id)
        path = job.get("file") if job else None
    if not path or not os.path.exists(path):
        return jsonify({"error": "Video file is no longer available."}), 404
    return send_file(path, as_attachment=True, download_name=f"ai-video-{job_id}.mp4", mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
