import os, math, textwrap, random, re
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio

W, H, FPS = 720, 405, 24

def font(size, bold=False):
    paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def make_storyboard(prompt, style="Cartoon", duration=8):
    duration = max(4, min(20, int(duration or 8)))
    words = re.findall(r"[A-Za-z0-9']+", prompt)
    subject = " ".join(words[:7]) or "Your story"
    beats = [
        ("Opening shot", f"Introduce {subject} with a clear establishing scene."),
        ("The moment", "Show the main action with expressive movement and a camera push-in."),
        ("The highlight", "Build to the most memorable moment with motion and visual contrast."),
        ("Ending", "Finish on a clean final frame with a gentle fade.")
    ]
    return {"title": subject[:48], "style": style, "duration": duration,
            "scenes": [{"scene": i+1, "time": f"{round(i*duration/4,1)}–{round((i+1)*duration/4,1)}s",
                        "title": title, "description": desc} for i,(title,desc) in enumerate(beats)]}

def render_video(data, output_dir, update):
    prompt = str(data.get("prompt", "A little adventure")).strip()
    style = str(data.get("style", "Cartoon"))
    ratio = str(data.get("ratio", "16:9"))
    duration = max(4, min(20, int(data.get("duration", 8))))
    width, height = (720,405) if ratio == "16:9" else ((405,720) if ratio == "9:16" else (540,540))
    mood = str(data.get("mood", "Happy")).lower()
    seed = sum(ord(c) for c in prompt) % 997
    random.seed(seed)
    out = os.path.join(output_dir, f"video-{os.urandom(6).hex()}.mp4")
    total = duration * FPS
    writer = imageio.get_writer(out, fps=FPS, codec="libx264", quality=7, macro_block_size=16,
                                ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"])
    try:
        for frame_no in range(total):
            t = frame_no / FPS
            im = Image.new("RGB", (width,height), (17,24,48))
            d = ImageDraw.Draw(im)
            # layered sky and ground
            for y in range(height):
                k = y / max(1,height)
                d.line((0,y,width,y), fill=(int(17+20*k),int(25+22*k),int(52+34*k)))
            horizon = int(height*.72)
            d.ellipse((int(width*.72),int(height*.10),int(width*.86),int(height*.10)+int(width*.14)), fill=(255,205,112))
            d.rectangle((0,horizon,width,height), fill=(25,65,65))
            for j in range(7):
                x=(j*137-int(t*35))%(width+100)-50
                d.ellipse((x,horizon-45,x+100,horizon+25), fill=(22,56,59))
            # cute animated character
            cx=int(width*.5 + math.sin(t*1.2)*width*.18)
            cy=int(height*.57 + math.sin(t*4)*8)
            bob=math.sin(t*5)*3
            r=max(26,int(min(width,height)*.085))
            d.ellipse((cx-r,cy-r+ bob,cx+r,cy+r+bob), fill=(255,181,91), outline=(255,226,180), width=4)
            d.ellipse((cx-r*.62,cy-r*.22+bob,cx-r*.40,cy-r*.02+bob), fill=(25,30,45))
            d.ellipse((cx+r*.40,cy-r*.22+bob,cx+r*.62,cy-r*.02+bob), fill=(25,30,45))
            if mood in ("sad","sleepy"):
                d.arc((cx-r*.35,cy+r*.05+bob,cx+r*.35,cy+r*.42+bob), 190,350, fill=(65,35,40), width=3)
            else:
                d.arc((cx-r*.3,cy+r*.03+bob,cx+r*.3,cy+r*.43+bob), 10,170, fill=(65,35,40), width=3)
            # simple arms and feet
            d.line((cx-r*.75,cy+r*.15,cx-r*1.25,cy+r*.55), fill=(255,181,91), width=9)
            d.line((cx+r*.75,cy+r*.15,cx+r*1.25,cy+r*.55), fill=(255,181,91), width=9)
            d.line((cx-r*.3,cy+r*.8,cx-r*.48,cy+r*1.12), fill=(255,181,91), width=10)
            d.line((cx+r*.3,cy+r*.8,cx+r*.48,cy+r*1.12), fill=(255,181,91), width=10)
            # scene label and prompt caption
            d.rounded_rectangle((18,16,width-18,70), radius=16, fill=(8,13,30))
            d.text((34,29), "AI VIDEO STUDIO  •  " + style.upper(), font=font(16,True), fill=(153,224,255))
            caption = prompt[:76] + ("…" if len(prompt)>76 else "")
            d.rounded_rectangle((18,height-66,width-18,height-16), radius=14, fill=(8,13,30))
            d.text((32,height-51), caption, font=font(max(12,int(width*.022))), fill=(255,255,255))
            # progress marker
            d.rectangle((0,height-4,int(width*(frame_no+1)/total),height), fill=(89,206,255))
            writer.append_data(__import__("numpy").array(im))
            if frame_no % max(1,FPS//2) == 0:
                update(int((frame_no+1)*100/total), f"Rendering frame {frame_no+1} of {total}")
    finally:
        writer.close()
    return out
