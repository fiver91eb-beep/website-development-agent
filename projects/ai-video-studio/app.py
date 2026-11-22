import os, uuid, threading, traceback
from flask import Flask, request, jsonify, send_file
from renderer import render_video, make_storyboard

app=Flask(__name__,static_folder="static",static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"]=2*1024*1024
JOBS={}; LOCK=threading.Lock()
OUTPUT=os.path.join(os.path.dirname(__file__),"renders")
os.makedirs(OUTPUT,exist_ok=True)

@app.get("/")
def home(): return app.send_static_file("index.html")

@app.get("/health")
def health(): return jsonify({"ok":True,"service":"AI Video Studio","mode":"built-in prompt animation","api_required":False})

@app.post("/api/storyboards")
def storyboard():
    data=request.get_json(silent=True) or {}
    prompt=str(data.get("prompt","")).strip()
    if not prompt: return jsonify({"error":"Please describe your video first."}),400
    return jsonify(make_storyboard(prompt,data.get("style","Cartoon"),data.get("duration",8),data.get("mood","Happy")))

@app.post("/api/renders")
def create_render():
    data=request.get_json(silent=True) or {}
    if not str(data.get("prompt","")).strip(): return jsonify({"error":"A video prompt is required."}),400
    job_id=uuid.uuid4().hex[:12]
    with LOCK: JOBS[job_id]={"id":job_id,"status":"queued","progress":0,"message":"Waiting to render","file":None}
    threading.Thread(target=run_job,args=(job_id,data),daemon=True).start()
    return jsonify({"job_id":job_id,"status":"queued"}),202

def run_job(job_id,data):
    def update(progress,message):
        with LOCK:
            if job_id in JOBS: JOBS[job_id].update(progress=progress,message=message,status="rendering")
    try:
        path=render_video(data,OUTPUT,update)
        with LOCK: JOBS[job_id].update(status="completed",progress=100,message="Your video is ready",file=path)
    except Exception as exc:
        traceback.print_exc()
        with LOCK: JOBS[job_id].update(status="failed",message=str(exc),error="Render failed")

@app.get("/api/renders/<job_id>")
def render_status(job_id):
    with LOCK:
        job=JOBS.get(job_id)
        if not job: return jsonify({"error":"Render not found. Jobs may reset when the server restarts."}),404
        result={k:v for k,v in job.items() if k!="file"}
        if job.get("status")=="completed": result["download_url"]=f"/api/renders/{job_id}/download"
        return jsonify(result)

@app.get("/api/renders/<job_id>/download")
def download(job_id):
    with LOCK: job=JOBS.get(job_id); path=job.get("file") if job else None
    if not path or not os.path.exists(path): return jsonify({"error":"Video file is no longer available."}),404
    return send_file(path,as_attachment=True,download_name=f"ai-video-{job_id}.mp4",mimetype="video/mp4")

if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=False)
