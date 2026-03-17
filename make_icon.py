"""
Hornet app icon — just the logo, centered, no basketball.
Flood-fill background removal with safe threshold (bee body dist ~54+ from bg).
"""
from PIL import Image, ImageDraw
import math
from collections import deque

SIZE = 1024
BG   = (40, 92, 57)

def cdist(a, b=BG):
    return math.sqrt(sum((int(a[i])-int(b[i]))**2 for i in range(3)))

# ── Load & remove background ─────────────────────────────────────────────────
src = Image.open(
    '/Users/markslyder/Claude Code Applications/March Madness 2026/hornet-logo.png'
).convert('RGBA')
w, h = src.size
px   = src.load()

# Flood-fill from all edges — threshold 38 (bee body closest pixel is ~54)
THRESHOLD = 38
visited   = [[False]*h for _ in range(w)]
queue     = deque()
for x in range(w):
    for y in (0, h-1):
        if not visited[x][y] and cdist(px[x,y]) < THRESHOLD:
            visited[x][y] = True
            queue.append((x, y))
for y in range(h):
    for x in (0, w-1):
        if not visited[x][y] and cdist(px[x,y]) < THRESHOLD:
            visited[x][y] = True
            queue.append((x, y))

while queue:
    x, y = queue.popleft()
    if cdist(px[x,y]) < THRESHOLD:
        px[x,y] = (0, 0, 0, 0)
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny))

# ── Crop tightly to bee ───────────────────────────────────────────────────────
# Bee occupies x=60..128, y=21..110 — add padding
PAD  = 6
crop = src.crop((60-PAD, 21-PAD, 128+PAD, 110+PAD))   # ~84×95 px

# ── Scale to fill icon (with margin) ─────────────────────────────────────────
MARGIN   = 80
TARGET_H = SIZE - 2*MARGIN
TARGET_W = int(crop.width * TARGET_H / crop.height)
if TARGET_W > SIZE - 2*MARGIN:
    TARGET_W = SIZE - 2*MARGIN
    TARGET_H = int(crop.height * TARGET_W / crop.width)

hornet = crop.resize((TARGET_W, TARGET_H), Image.LANCZOS)

# ── Canvas — rounded-square background matching the logo ─────────────────────
canvas = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
d      = ImageDraw.Draw(canvas)
d.rounded_rectangle([0, 0, SIZE, SIZE], radius=180, fill=(*BG, 255))

# Centre hornet on canvas
px_off = (SIZE - TARGET_W) // 2
py_off = (SIZE - TARGET_H) // 2
canvas.paste(hornet, (px_off, py_off), hornet)

out = '/Users/markslyder/Claude Code Applications/March Madness 2026/icon.png'
canvas.save(out, 'PNG')
print(f'Saved {TARGET_W}×{TARGET_H} hornet → {out}')
