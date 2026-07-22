"""Generate the animated pixel Starry Night header into assets/ (run locally, commit output)."""
import math
import os
import random

from pixel import NIGHT, MUTED, GOLD, CROP_CSS, CROP_KINDS, crop

OUT = os.path.join("assets", "header.svg")
W, H = 830, 250
GRASS_Y = H - 26
HILL_Y = H - 52
CELL = 6
FLOW = 9.0

SWIRL_BLUES = ["#24407c", "#33569f", "#4f78c0", "#7fa3d8"]
CREAM = "#e6ddb8"
STAR_CORE = "#f7e7a0"
STAR_HALO = "#e3b94c"
rng = random.Random(20260722)

EXTRA_CSS = """
.fp{animation:fw 9s linear infinite}
@keyframes fw{0%,100%{opacity:.4}50%{opacity:1}}
.halo{animation:hp 5s ease-in-out infinite}
@keyframes hp{0%,100%{opacity:.22}50%{opacity:.7}}
.star{animation:tw 4s infinite}
@keyframes tw{0%,100%{opacity:.3}50%{opacity:1}}
.fly{animation:fl 6s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0);opacity:.2}25%{opacity:1}50%{transform:translateY(-9px);opacity:.5}75%{opacity:.9}}
.title{animation:fade 1.2s ease-out}
@keyframes fade{from{opacity:0}to{opacity:1}}
"""


def snap(v):
    return int(v // CELL) * CELL


def flow_pixel(x, y, t_norm, color, opacity=1.0):
    op = f' fill-opacity="{opacity}"' if opacity < 1 else ""
    return (
        f'<rect class="fp" x="{snap(x)}" y="{snap(y)}" width="{CELL}" height="{CELL}" '
        f'fill="{color}"{op} style="animation-delay:{-t_norm * FLOW:.2f}s"/>'
    )


def spiral(cx, cy, turns, r0, dr, squash):
    out, seen = [], set()
    t_max = turns * 2 * math.pi
    for phase in (0.0, math.pi):
        t = 0.0
        while t < t_max:
            r = r0 + dr * t
            x = cx + r * math.cos(t + phase)
            y = cy + squash * r * math.sin(t + phase)
            key = (snap(x), snap(y))
            t += 0.35 / max(r * 0.02, 1)
            if key in seen or not (0 <= x < W and 8 <= y < HILL_Y - 12):
                continue
            seen.add(key)
            color = CREAM if rng.random() < 0.12 else SWIRL_BLUES[int(t * 2) % len(SWIRL_BLUES)]
            out.append(flow_pixel(x, y, t / t_max, color))
    return "".join(out)


def waves():
    out = []
    for y0 in (38, 74, 112, 146):
        for x in range(0, W, CELL):
            if rng.random() < 0.28:
                continue
            y = y0 + 9 * math.sin(x / 52 + y0 * 0.7)
            color = CREAM if rng.random() < 0.06 else SWIRL_BLUES[int(x / CELL + y0) % len(SWIRL_BLUES)]
            out.append(flow_pixel(x, y, (x / W + y0 / 200) % 1.0, color, opacity=0.75))
    return "".join(out)


def ring(cx, cy, radius, color, cls, delay, opacity):
    out = []
    steps = max(10, int(radius * 1.6))
    for i in range(steps):
        a = 2 * math.pi * i / steps
        x, y = cx + radius * math.cos(a), cy + radius * math.sin(a)
        out.append(
            f'<rect class="{cls}" x="{x:.0f}" y="{y:.0f}" width="3" height="3" fill="{color}" '
            f'fill-opacity="{opacity}" style="animation-delay:{-delay:.2f}s"/>'
        )
    return "".join(out)


def stars():
    out = []
    spots = [(95, 55), (215, 110), (415, 42), (555, 120), (645, 58), (330, 150), (770, 130)]
    for i, (x, y) in enumerate(spots):
        d = i * 0.9
        out.append(f'<rect class="star" x="{x - 2}" y="{y - 2}" width="5" height="5" fill="{STAR_CORE}" style="animation-delay:{-d:.2f}s"/>')
        out.append(ring(x, y, 7, STAR_HALO, "halo", d, 0.55))
        out.append(ring(x, y, 12, STAR_HALO, "halo", d + 1.2, 0.28))
    return "".join(out)


def moon():
    cx, cy = 758, 48
    out = []
    for gx in range(cx - 16, cx + 17, 4):
        for gy in range(cy - 16, cy + 17, 4):
            if (gx - cx) ** 2 + (gy - cy) ** 2 > 15 ** 2:
                continue
            if (gx - cx - 7) ** 2 + (gy - cy + 3) ** 2 < 12 ** 2:
                continue
            out.append(f'<rect x="{gx}" y="{gy}" width="4" height="4" fill="{STAR_CORE}"/>')
    out.append(ring(cx, cy, 22, STAR_HALO, "halo", 0.5, 0.3))
    return "".join(out)


def cypress():
    out = []
    base_x, rows = 66, 16
    for i in range(rows):
        y = GRASS_Y - (i + 1) * 6
        half = max(1, round(3.4 * (1 - i / rows)) + (1 if i % 3 == 0 and i < 10 else 0))
        for k in range(-half, half + 1):
            out.append(f'<rect x="{base_x + k * 5}" y="{y}" width="5" height="6" fill="#14301c"/>')
    return "".join(out)


def hills():
    out = []
    for x in range(0, W, CELL):
        h = 16 + 10 * math.sin(x / 95) + 6 * math.sin(x / 41 + 2)
        y = GRASS_Y - int(h // CELL) * CELL
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{GRASS_Y - y}" fill="#0c1524"/>')
    return "".join(out)


def grass():
    out = [f'<rect x="0" y="{GRASS_Y}" width="{W}" height="{H - GRASS_Y}" fill="#1a2e12"/>']
    for gx in range(0, W, 6):
        if rng.random() < 0.55:
            color = "#2d4a1e" if rng.random() < 0.6 else "#48732c"
            out.append(f'<rect x="{gx}" y="{GRASS_Y}" width="6" height="6" fill="{color}"/>')
        if rng.random() < 0.12:
            out.append(f'<rect x="{gx}" y="{GRASS_Y - 4}" width="3" height="4" fill="#48732c"/>')
    return "".join(out)


def crops():
    out = []
    for i, x in enumerate((148, 240, 596, 706)):
        out.append(crop(x, GRASS_Y + 2, CROP_KINDS[i % len(CROP_KINDS)], delay_s=i * 1.9, px=3))
    return "".join(out)


def fireflies():
    out = []
    for _ in range(8):
        x = rng.randint(30, W - 30)
        y = rng.randint(GRASS_Y - 40, GRASS_Y - 10)
        out.append(
            f'<rect class="fly" x="{x}" y="{y}" width="3" height="3" fill="#A6D583" '
            f'style="animation-delay:{-rng.uniform(0, 6):.2f}s"/>'
        )
    return "".join(out)


def title():
    x = W / 2
    outline = f'stroke="{NIGHT}" stroke-width="6" paint-order="stroke" stroke-linejoin="round"'
    return (
        f'<g class="title" text-anchor="middle" font-weight="700">'
        f'<text x="{x}" y="128" fill="#ffffff" font-size="42" {outline}>Sanober Rehman</text>'
        f'<text x="{x}" y="160" fill="{GOLD}" font-size="17" {outline}>AI/ML Engineer &#183; LLM &amp; GenAI Developer</text>'
        f'<text x="{x}" y="186" fill="{MUTED}" font-size="13" {outline}>Dubai, UAE</text>'
        f"</g>"
    )


def build():
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Courier New, monospace">'
        f"<style>{CROP_CSS}{EXTRA_CSS}</style>"
        f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>'
        + waves()
        + spiral(340, 92, 2.4, 8, 3.4, 0.55)
        + spiral(585, 128, 1.6, 6, 3.0, 0.5)
        + stars() + moon() + hills() + cypress() + grass() + crops() + fireflies() + title()
        + "</svg>"
    )


def main():
    os.makedirs("assets", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
