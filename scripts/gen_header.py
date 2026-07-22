"""Generate the animated pixel galaxy header into assets/ (run locally, commit output)."""
import math
import os
import random

from pixel import MUTED, GOLD, CROP_CSS, CROP_KINDS, crop

OUT = os.path.join("assets", "header.svg")
W, H = 830, 250
GRASS_Y = H - 26
HILL_Y = H - 52
CELL = 6
FLOW = 9.0

SPACE = "#0b0c22"
GALAXY = ["#6b4a9e", "#8a7fd4", "#5c7fd4", "#c46fb0", "#4fa5b8"]
CORE = "#efe9f7"
STAR_WHITE = "#e8e8f5"
STAR_BLUE = "#9fb4e8"
STAR_WARM = "#f2d9a0"

rng = random.Random(20260722)

EXTRA_CSS = """
.fp{animation:fw 9s linear infinite}
@keyframes fw{0%,100%{opacity:.35}50%{opacity:1}}
.halo{animation:hp 5s ease-in-out infinite}
@keyframes hp{0%,100%{opacity:.2}50%{opacity:.65}}
.star{animation:tw 4s infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
.fly{animation:fl 6s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0);opacity:.2}25%{opacity:1}50%{transform:translateY(-9px);opacity:.5}75%{opacity:.9}}
.shoot1{animation:sh1 13s linear infinite}
@keyframes sh1{0%,62%{transform:translate(0,0);opacity:0}63%{opacity:1}70%{transform:translate(320px,110px);opacity:0}100%{opacity:0}}
.shoot2{animation:sh2 17s linear infinite}
@keyframes sh2{0%,29%{transform:translate(0,0);opacity:0}30%{opacity:1}38%{transform:translate(-280px,130px);opacity:0}100%{opacity:0}}
.title{animation:fade 1.2s ease-out}
@keyframes fade{from{opacity:0}to{opacity:1}}
"""


def snap(v):
    return int(v // CELL) * CELL


def flow_pixel(x, y, t_norm, color, opacity=1.0, size=CELL):
    op = f' fill-opacity="{opacity}"' if opacity < 1 else ""
    return (
        f'<rect class="fp" x="{snap(x)}" y="{snap(y)}" width="{size}" height="{size}" '
        f'fill="{color}"{op} style="animation-delay:{-t_norm * FLOW:.2f}s"/>'
    )


def spiral_galaxy(cx, cy):
    """A pixel spiral galaxy with a bright core and colored arms."""
    out, seen = [], set()
    turns, r0, dr, squash = 2.2, 4, 3.2, 0.42
    t_max = turns * 2 * math.pi
    for phase in (0.0, math.pi):
        t = 0.0
        while t < t_max:
            r = r0 + dr * t
            x = cx + r * math.cos(t + phase)
            y = cy + squash * r * math.sin(t + phase)
            key = (snap(x), snap(y))
            t += 0.35 / max(r * 0.02, 1)
            if key in seen or not (0 <= x < W and 8 <= y < HILL_Y - 20):
                continue
            seen.add(key)
            frac = r / (r0 + dr * t_max)
            if frac < 0.18:
                color, op = CORE, 1.0
            else:
                color = GALAXY[int(t * 2) % len(GALAXY)]
                op = 0.9 if rng.random() < 0.5 else 0.6
            out.append(flow_pixel(x, y, t / t_max, color, op))
    out.append(f'<rect x="{snap(cx)}" y="{snap(cy)}" width="{CELL}" height="{CELL}" fill="#ffffff"/>')
    return "".join(out)


def milky_way():
    """A diagonal band of dense faint pixels across the sky."""
    out = []
    for x in range(0, W, 3):
        center = 148 - 0.13 * x
        for _ in range(2):
            y = rng.gauss(center, 16)
            if not (8 <= y < HILL_Y - 24) or rng.random() < 0.3:
                continue
            color = STAR_WHITE if rng.random() < 0.5 else GALAXY[rng.randrange(len(GALAXY))]
            out.append(flow_pixel(x, y, (x / W + y / 300) % 1.0, color, opacity=rng.uniform(0.3, 0.7), size=3))
    return "".join(out)


def nebulae():
    out = []
    for cx, cy, color in ((120, 60, "#6b4a9e"), (690, 150, "#c46fb0"), (420, 45, "#4fa5b8")):
        x, y = cx, cy
        for _ in range(46):
            x += rng.randint(-9, 9)
            y += rng.randint(-7, 7)
            if not (8 <= y < HILL_Y - 26):
                y = cy
            out.append(
                f'<rect x="{snap(x)}" y="{snap(y)}" width="{CELL}" height="{CELL}" '
                f'fill="{color}" fill-opacity="{rng.uniform(0.15, 0.4):.2f}"/>'
            )
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
    for i in range(30):
        x, y = rng.randint(12, W - 12), rng.randint(10, HILL_Y - 30)
        color = rng.choice((STAR_WHITE, STAR_WHITE, STAR_BLUE, STAR_WARM))
        s = rng.choice((2, 2, 3))
        out.append(
            f'<rect class="star" x="{x}" y="{y}" width="{s}" height="{s}" fill="{color}" '
            f'style="animation-delay:{-rng.uniform(0, 4):.2f}s"/>'
        )
    for i, (x, y) in enumerate(((95, 52), (545, 118), (760, 95))):
        d = i * 1.3
        out.append(f'<rect class="star" x="{x - 2}" y="{y - 2}" width="5" height="5" fill="{STAR_WHITE}" style="animation-delay:{-d:.2f}s"/>')
        out.append(ring(x, y, 7, "#8a7fd4", "halo", d, 0.5))
    return "".join(out)


def shooting_stars():
    def comet(cls, x, y):
        tail = "".join(
            f'<rect x="{x - 5 - k * 5}" y="{y + (k * 2 if cls == "shoot2" else -k * 2) * 0 }" width="4" height="2" '
            f'fill="{STAR_WHITE}" fill-opacity="{0.7 - k * 0.15:.2f}"/>'
            for k in range(4)
        )
        return f'<g class="{cls}"><rect x="{x}" y="{y}" width="3" height="3" fill="#ffffff"/>{tail}</g>'

    return comet("shoot1", 70, 40) + comet("shoot2", 740, 30)


def moon():
    cx, cy = 758, 48
    out = []
    for gx in range(cx - 16, cx + 17, 4):
        for gy in range(cy - 16, cy + 17, 4):
            if (gx - cx) ** 2 + (gy - cy) ** 2 > 15 ** 2:
                continue
            if (gx - cx - 7) ** 2 + (gy - cy + 3) ** 2 < 12 ** 2:
                continue
            out.append(f'<rect x="{gx}" y="{gy}" width="4" height="4" fill="{STAR_WARM}"/>')
    return "".join(out)


def pine():
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
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{GRASS_Y - y}" fill="#0a1220"/>')
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
    outline = f'stroke="{SPACE}" stroke-width="6" paint-order="stroke" stroke-linejoin="round"'
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
        f'<rect width="{W}" height="{H}" fill="{SPACE}"/>'
        + nebulae() + milky_way() + spiral_galaxy(250, 82)
        + stars() + shooting_stars() + moon() + hills() + pine() + grass() + crops() + fireflies() + title()
        + "</svg>"
    )


def main():
    os.makedirs("assets", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
