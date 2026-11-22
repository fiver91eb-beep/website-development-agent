import os, math, re, random
import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont

FPS = 20

def font(size, bold=False):
    paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def detect_subject(prompt):
    p = prompt.lower()
    choices = [("bird", ["bird","sparrow","parrot","eagle","چڑیا","پرندہ","chirya"]),
               ("cat", ["cat","kitten","بلی","billi"]),
               ("dog", ["dog","puppy","کتا","kutta"]),
               ("butterfly", ["butterfly","تتلی","titli"]),
               ("fish", ["fish","مچھلی","machli"]),
               ("person", ["boy","girl","child","person","man","woman","بچہ","لڑکا","لڑکی"])]
    for name, words in choices:
        if any(w in p for w in words): return name
    return "bird"

def detect_mood(prompt, chosen):
    p = (prompt + " " + str(chosen)).lower()
    for mood, words in [("sad",["sad","udaas","اداس"]),("sleepy",["sleepy","tired","نیند","so raha"]),
                        ("angry",["angry","غصہ"]),("happy",["happy","khush","خوش"])]:
        if any(w in p for w in words): return mood
    return "happy"

def detect_actions(prompt):
    p = prompt.lower()
    tests = [
      ("fly",["fly","flying","flies","ud","اڑ","اڑ رہی","اڑتا"]),
      ("play",["play","playing","khel","کھیل","گेंद","ball"]),
      ("run",["run","running"," दौڑ","dor","دوڑ"]),
      ("jump",["jump","jumping","چھلانگ","uchhal"]),
      ("sleep",["sleep","sleeping","so raha","سو رہی","سو رہا"]),
      ("swim",["swim","swimming","تیر","machli"]),
      ("walk",["walk","walking","چل رہی","چلتا"]),
      ("dance",["dance","dancing","ناچ","dance kar"])
    ]
    found = [action for action, words in tests if any(w in p for w in words)]
    if not found: found = ["fly"] if detect_subject(prompt) in ("bird","butterfly") else ["walk","play"]
    # Preserve a simple sequence; add contrasting actions if the prompt says "then/phir".
    return found[:4]

def make_storyboard(prompt, style="Cartoon", duration=8, mood="Happy"):
    subject = detect_subject(prompt)
    actions = detect_actions(prompt)
    labels = {"fly":"flies through the sky","play":"plays with a ball","run":"runs happily","jump":"jumps into the air",
              "sleep":"rests peacefully","swim":"swims through the water","walk":"walks along the path","dance":"dances"}
    scenes = []
    for i, action in enumerate(actions):
        scenes.append({"scene":i+1,"time":f"{i*duration/len(actions):.1f}–{(i+1)*duration/len(actions):.1f}s",
                       "title":action.title(),"description":f"The {subject} {labels[action]}."})
    return {"title":f"{subject.title()} animation","style":style,"duration":duration,"scenes":scenes,
            "subject":subject,"actions":actions,"mood":detect_mood(prompt,mood),"ai_generated":False}

def cloud(d, x, y, scale=1):
    d.ellipse((x,y+12*scale,x+54*scale,y+38*scale),fill=(245,250,255))
    d.ellipse((x+12*scale,y,x+40*scale,y+34*scale),fill=(245,250,255))
    d.ellipse((x+31*scale,y+8*scale,x+66*scale,y+38*scale),fill=(245,250,255))

def draw_bird(d,x,y,s,t,mood):
    wing = math.sin(t*13)*s*.42
    # tail, body, wing, head, beak, eye
    d.polygon([(x-s*.55,y),(x-s*1.05,y-s*.22),(x-s*.92,y+s*.22)],fill=(246,166,74))
    d.ellipse((x-s*.62,y-s*.30,x+s*.48,y+s*.36),fill=(255,184,82),outline=(125,76,45),width=max(1,int(s*.035)))
    d.ellipse((x+s*.18,y-s*.62,x+s*.78,y-.02*s),fill=(255,199,105),outline=(125,76,45),width=max(1,int(s*.03)))
    d.polygon([(x+s*.70,y-s*.34),(x+s*1.12,y-s*.18),(x+s*.70,y-s*.10)],fill=(255,119,64))
    d.ellipse((x+s*.52,y-s*.43,x+s*.59,y-s*.35),fill=(25,30,42))
    d.ellipse((x-s*.25,y-s*.25-wing,x+s*.32,y+s*.04-wing),fill=(225,126,62),outline=(125,76,45),width=max(1,int(s*.025)))
    d.line((x-s*.08,y+s*.28,x-s*.12,y+s*.52),fill=(110,78,52),width=max(2,int(s*.04)))
    d.line((x+s*.12,y+s*.28,x+s*.18,y+s*.52),fill=(110,78,52),width=max(2,int(s*.04)))

def draw_cat(d,x,y,s,t,mood):
    d.ellipse((x-s*.55,y-s*.35,x+s*.55,y+s*.48),fill=(245,154,105),outline=(105,68,55),width=3)
    d.ellipse((x-s*.42,y-s*.75,x+s*.42,y+s*.05),fill=(245,154,105),outline=(105,68,55),width=3)
    d.polygon([(x-s*.4,y-s*.48),(x-s*.45,y-s*.95),(x-s*.08,y-s*.66)],fill=(245,154,105))
    d.polygon([(x+s*.08,y-s*.66),(x+s*.45,y-s*.95),(x+s*.4,y-s*.48)],fill=(245,154,105))
    d.ellipse((x-s*.22,y-s*.48,x-s*.12,y-s*.36),fill=(20,25,35)); d.ellipse((x+s*.12,y-s*.48,x+s*.22,y-s*.36),fill=(20,25,35))
    d.arc((x-s*.13,y-s*.30,x+s*.13,y-s*.10),190,350,fill=(90,45,45),width=2)
    d.arc((x+s*.38,y-s*.15,x+s*.95,y+s*.55),180,300,fill=(245,154,105),width=5)

def draw_dog(d,x,y,s,t,mood):
    d.ellipse((x-s*.5,y-s*.3,x+s*.55,y+s*.42),fill=(191,137,91),outline=(92,65,45),width=3)
    d.ellipse((x-s*.42,y-s*.72,x+s*.38,y+s*.05),fill=(207,153,105),outline=(92,65,45),width=3)
    d.ellipse((x-s*.48,y-s*.7,x-s*.15,y-s*.22),fill=(110,70,48)); d.ellipse((x+s*.12,y-s*.7,x+s*.45,y-s*.2),fill=(110,70,48))
    d.ellipse((x-s*.2,y-s*.45,x-s*.1,y-s*.34),fill=(20,25,35)); d.ellipse((x+s*.1,y-s*.45,x+s*.2,y-s*.34),fill=(20,25,35))
    d.ellipse((x-s*.06,y-s*.23,x+s*.12,y-s*.08),fill=(35,30,30))

def render_video(data, output_dir, update):
    prompt=str(data.get("prompt","A little bird flies across the sky")).strip()
    style=str(data.get("style","Cartoon")); ratio=str(data.get("ratio","16:9"))
    duration=max(4,min(20,int(data.get("duration",8))))
    width,height=(720,405) if ratio=="16:9" else ((405,720) if ratio=="9:16" else (540,540))
    board=make_storyboard(prompt,style,duration,data.get("mood","Happy"))
    subject,actions,mood=board["subject"],board["actions"],board["mood"]
    total=duration*FPS; out=os.path.join(output_dir,f"video-{os.urandom(6).hex()}.mp4")
    writer=imageio.get_writer(out,fps=FPS,codec="libx264",quality=7,macro_block_size=16,
                              ffmpeg_params=["-pix_fmt","yuv420p","-movflags","+faststart"])
    try:
      for frame in range(total):
        t=frame/FPS; scene=min(len(actions)-1,int(t/duration*len(actions))); action=actions[scene]
        im=Image.new("RGB",(width,height),(112,190,235)); d=ImageDraw.Draw(im)
        # soft sky, sun, clouds, distant landscape
        d.rectangle((0,int(height*.73),width,height),fill=(100,177,112))
        d.ellipse((width*.78,height*.08,width*.91,height*.21),fill=(255,220,120))
        for i in range(4): cloud(d,int((i*width*.31-t*12)%(width+100)-60),int(height*(.13+(i%2)*.15)),.7)
        d.ellipse((width*.08,height*.57,width*.42,height*.85),fill=(82,155,105))
        d.ellipse((width*.58,height*.56,width*.95,height*.87),fill=(74,146,100))
        progress=(t%(duration/len(actions)))/(duration/len(actions))
        if action=="fly" or subject in ("bird","butterfly"):
          x=int(width*(.18+.64*progress)); y=int(height*(.37+.10*math.sin(t*2.7)))
          if action=="fly": y-=int(height*.10*math.sin(progress*math.pi))
        else:
          x=int(width*(.15+.68*progress)); y=int(height*.65)
          if action=="jump": y-=int(height*.18*abs(math.sin(progress*math.pi*2)))
          elif action=="play": y-=int(height*.05*abs(math.sin(t*7)))
          elif action=="sleep": y=int(height*.66)
        s=min(width,height)*.105
        if subject=="cat": draw_cat(d,x,y,s,t,mood)
        elif subject=="dog": draw_dog(d,x,y,s,t,mood)
        else: draw_bird(d,x,y,s,t,mood)
        if action=="play":
          bx=int(width*(.72-.12*math.sin(t*6))); by=int(height*.66-abs(math.sin(t*6))*height*.13)
          d.ellipse((bx-12,by-12,bx+12,by+12),fill=(244,85,92),outline="white",width=2)
        if action=="swim":
          for k in range(3):
            xx=(int(width*.2+k*width*.3-t*40))%width
            d.arc((xx,height*.72,xx+60,height*.79),0,180,fill=(230,250,255),width=3)
        if mood=="sad":
          d.rounded_rectangle((width*.03,height*.03,width*.97,height*.15),radius=14,fill=(40,56,83))
          d.text((width*.06,height*.065),"A gentle, sad little story",font=font(max(12,int(width*.025))),fill=(230,238,255))
        else:
          d.rounded_rectangle((width*.03,height*.03,width*.97,height*.15),radius=14,fill=(24,49,66))
          d.text((width*.06,height*.065),f"{subject.title()} • {action.title()}",font=font(max(12,int(width*.027)),True),fill=(255,255,255))
        d.rounded_rectangle((width*.03,height*.86,width*.97,height*.97),radius=13,fill=(22,37,49))
        caption=f"Scene {scene+1}/{len(actions)}: {action.title()}"
        d.text((width*.06,height*.895),caption,font=font(max(12,int(width*.025))),fill=(255,255,255))
        writer.append_data(np.asarray(im))
        if frame%max(1,FPS//2)==0: update(int((frame+1)*100/total),f"Animating {action} · frame {frame+1}/{total}")
    finally: writer.close()
    return out
