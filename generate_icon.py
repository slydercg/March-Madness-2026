"""
Hornet-on-Basketball icon v5
Layout:
 - Large basketball fills lower ~45% (clearly visible)
 - Hornet is compact, sitting on top of the ball
 - Wings HUGE, sweeping far out to both sides past the head
"""
from PIL import Image, ImageDraw
import math

SIZE = 1024
S    = 2
W = H = SIZE * S
img  = Image.new("RGBA", (W, H), (0,0,0,0))
d    = ImageDraw.Draw(img)

# ── colours ──────────────────────────────────────────────────────────────────
GREEN    = (26,  88,  46)
GREEN_HI = (48, 122,  70)
OUTLINE  = (8,   20,  12)
ORANGE   = (228, 113,  22)
WING_F   = (200, 238, 210, 150)
WING_S   = (20,  60,  30)
WHITE    = (255, 255, 255, 255)
DARK_EYE = (10,  10,  10)

def sc(v): return int(round(v * S))

def ell(cx,cy,rx,ry,fill=None,outline=None,lw=1):
    d.ellipse([sc(cx-rx),sc(cy-ry),sc(cx+rx),sc(cy+ry)],
              fill=fill,outline=outline,width=sc(lw))

def circ(cx,cy,r,**kw): ell(cx,cy,r,r,**kw)

def poly(pts,**kw):
    d.polygon([(sc(x),sc(y)) for x,y in pts],**kw)

def arc(cx,cy,rx,ry,s,e,color,lw):
    d.arc([sc(cx-rx),sc(cy-ry),sc(cx+rx),sc(cy+ry)],
          start=s,end=e,fill=color,width=sc(lw))

def bezier(p0,p1,p2,p3,n=80):
    pts=[]
    for i in range(n+1):
        t=i/n; u=1-t
        pts.append((u**3*p0[0]+3*u**2*t*p1[0]+3*u*t**2*p2[0]+t**3*p3[0],
                    u**3*p0[1]+3*u**2*t*p1[1]+3*u*t**2*p2[1]+t**3*p3[1]))
    return pts

def curve_line(pts,color,lw):
    d.line([(sc(x),sc(y)) for x,y in pts],fill=color,width=sc(lw))

# ════════════════════════════════════════════════════════════════════════
# BASKETBALL  — large, centered, fills lower portion
# ════════════════════════════════════════════════════════════════════════
BCX,BCY,BR = 512, 840, 260
for r in range(sc(BR),0,-max(1,sc(3))):
    ratio=r/sc(BR)
    d.ellipse([sc(BCX)-r,sc(BCY)-r,sc(BCX)+r,sc(BCY)+r],
              fill=(int(228-60*(1-ratio)),int(113-50*(1-ratio)),int(22-12*(1-ratio)),255))
circ(BCX,BCY,BR,outline=OUTLINE,lw=6)
# seam lines
arc(BCX,BCY,BR-4,90, 180,360,OUTLINE,8)
arc(BCX,BCY,BR-4,90,   0,180,OUTLINE,8)
arc(BCX,BCY,90,BR-4, 270, 90,OUTLINE,8)
arc(BCX,BCY,90,BR-4,  90,270,OUTLINE,8)

# ════════════════════════════════════════════════════════════════════════
# WINGS — drawn first, behind everything, sweep FAR out
# Wing roots attach at thorax sides (~y=430)
# Tips reach near the canvas edges
# ════════════════════════════════════════════════════════════════════════

# --- Upper-left wing ---
# outer edge curves up and left to tip
ul_outer = bezier((440,435), (280,310), (90,170), (30,110))
# inner (trailing) edge curves back to root
ul_inner = bezier((30,110),  (110,240), (300,390), (400,455))
ul_wing   = ul_outer + ul_inner
d.polygon([(sc(x),sc(y)) for x,y in ul_wing],
          fill=WING_F, outline=(*WING_S,255), width=sc(3))
# wing veins
curve_line(bezier((440,435),(240,310),(80,180),(38,125)), (*WING_S,170), 3)
curve_line(bezier((420,445),(270,348),(160,270),(120,220)), (*WING_S,110), 2)
curve_line(bezier((400,453),(310,385),(220,330),(185,300)), (*WING_S, 80), 2)

# --- Upper-right wing ---
ur_outer = bezier((584,435),(744,310),(934,170),(994,110))
ur_inner = bezier((994,110),(914,240),(724,390),(624,455))
d.polygon([(sc(x),sc(y)) for x,y in ur_outer+ur_inner],
          fill=WING_F, outline=(*WING_S,255), width=sc(3))
curve_line(bezier((584,435),(784,310),(944,180),(986,125)), (*WING_S,170), 3)
curve_line(bezier((604,445),(754,348),(864,270),(904,220)), (*WING_S,110), 2)
curve_line(bezier((624,453),(714,385),(804,330),(839,300)), (*WING_S, 80), 2)

# --- Lower-left wing (smaller, below upper) ---
ll_outer = bezier((415,490),(290,490),(200,540),(215,605))
ll_inner = bezier((215,605),(285,565),(370,525),(440,510))
d.polygon([(sc(x),sc(y)) for x,y in ll_outer+ll_inner],
          fill=(200,238,210,105), outline=(*WING_S,170), width=sc(2))

# --- Lower-right wing ---
lr_outer = bezier((609,490),(734,490),(824,540),(809,605))
lr_inner = bezier((809,605),(739,565),(654,525),(584,510))
d.polygon([(sc(x),sc(y)) for x,y in lr_outer+lr_inner],
          fill=(200,238,210,105), outline=(*WING_S,170), width=sc(2))

# ════════════════════════════════════════════════════════════════════════
# BACK LEGS
# ════════════════════════════════════════════════════════════════════════
curve_line(bezier((350,645),(265,688),(205,742),(175,795)),OUTLINE,10)
curve_line(bezier((674,645),(759,688),(819,742),(849,795)),OUTLINE,10)

# ════════════════════════════════════════════════════════════════════════
# ABDOMEN  — the biggest, roundest body part
# ════════════════════════════════════════════════════════════════════════
ABX,ABY,ABW,ABH = 512, 625, 175, 200
ell(ABX,ABY,ABW,ABH,fill=GREEN,outline=OUTLINE,lw=8)
for sy,sh in [(ABY-148,36),(ABY-92,40),(ABY-34,40),(ABY+24,38),(ABY+80,32)]:
    mid=sy+sh/2; dy=abs(mid-ABY)
    if dy<ABH:
        rx=ABW*math.sqrt(max(0,1-(dy/ABH)**2))
        d.rectangle([sc(ABX-rx+5),sc(sy),sc(ABX+rx-5),sc(sy+sh)],fill=OUTLINE)
ell(ABX,ABY,ABW,ABH,fill=None,outline=OUTLINE,lw=8)
# stinger
poly([(ABX-15,ABY+ABH-5),(ABX+15,ABY+ABH-5),(ABX,ABY+ABH+38)],fill=OUTLINE)

# ════════════════════════════════════════════════════════════════════════
# THORAX
# ════════════════════════════════════════════════════════════════════════
THX,THY,THW,THH = 512, 418, 95, 80
ell(THX,THY,THW,THH,fill=GREEN,outline=OUTLINE,lw=7)
arc(THX,THY,THW-14,THH//2,205,335,GREEN_HI,5)

# MIDDLE LEGS
curve_line(bezier((402,482),(305,522),(245,568),(210,620)),OUTLINE,10)
curve_line(bezier((622,482),(719,522),(779,568),(814,620)),OUTLINE,10)

# ════════════════════════════════════════════════════════════════════════
# HEAD
# ════════════════════════════════════════════════════════════════════════
HCX,HCY,HR = 512, 262, 132
circ(HCX,HCY,HR,fill=GREEN,outline=OUTLINE,lw=9)
arc(HCX,HCY,95,65,218,322,GREEN_HI,6)

# ════════════════════════════════════════════════════════════════════════
# COMPOUND EYES  — massive, dominate the face
# ════════════════════════════════════════════════════════════════════════
def eye(cx,cy,rx,ry):
    ell(cx,cy,rx,ry,fill=DARK_EYE,outline=OUTLINE,lw=7)
    ell(cx,cy,rx-9,ry-9,fill=(16,52,25))
    ell(cx,cy,rx-26,ry-26,fill=(5,5,5))
    # big bright highlight
    ell(cx-rx//3+2,cy-ry//3+2,rx//5+2,ry//5+2,fill=WHITE)
    # small secondary glint
    ell(cx+rx//4,cy-ry//7,rx//9,ry//9,fill=(255,255,255,165))
    ell(cx,cy,rx,ry,fill=None,outline=OUTLINE,lw=7)

eye(380,256, 96,112)
eye(644,256, 96,112)

# ════════════════════════════════════════════════════════════════════════
# MANDIBLES
# ════════════════════════════════════════════════════════════════════════
arc(HCX,HCY+52,78,34,10,170,OUTLINE,9)
d.line([sc(380),sc(370),sc(346),sc(400)],fill=OUTLINE,width=sc(8))
d.line([sc(644),sc(370),sc(678),sc(400)],fill=OUTLINE,width=sc(8))

# ════════════════════════════════════════════════════════════════════════
# FRONT LEGS  — raised in aggressive pose
# ════════════════════════════════════════════════════════════════════════
curve_line(bezier((386,360),(285,305),(222,258),(182,232)),OUTLINE,11)
curve_line(bezier((638,360),(739,305),(802,258),(842,232)),OUTLINE,11)

# ════════════════════════════════════════════════════════════════════════
# ANTENNAE
# ════════════════════════════════════════════════════════════════════════
curve_line(bezier((460,132),(412,72),(365,38),(330,18)),OUTLINE,9)
circ(323,12,18,fill=OUTLINE)
curve_line(bezier((564,132),(612,72),(659,38),(694,18)),OUTLINE,9)
circ(701,12,18,fill=OUTLINE)

# ════════════════════════════════════════════════════════════════════════
img = img.resize((SIZE,SIZE),Image.LANCZOS)
img.save("/Users/markslyder/Claude Code Applications/March Madness 2026/icon.png","PNG")
print("Done.")
