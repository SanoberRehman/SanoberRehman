"""Generate an animated aurora pixel header into assets/ (run locally, commit output)."""
import math
import os
import random

from pixel import MUTED, GOLD, CROP_CSS, CROP_KINDS, crop

OUT = os.path.join("assets", "header.svg")
W, H = 830, 240
GRASS_Y = H - 26
CELL = 5

SKY_TOP = "#070b1c"
SKY_BOT = "#0d1430"
# Aurora ribbon gradient, bottom (green) -> top (violet).
AURORA = ["#43e08a", "#2fd6b0", "#22c7d6", "#5aa8e6", "#8b7ff0", "#b06fd8"]

rng = random.Random(20260723)

EXTRA_CSS = """
.au{animation:shimmer 6s ease-in-out infinite}
@keyframes shimmer{0%,100%{opacity:var(--o)}50%{opacity:calc(var(--o) * 1.9)}}
.star{animation:tw 4.5s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.2}50%{opacity:.95}}
.fly{animation:fl 6s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0);opacity:.2}25%{opacity:1}50%{transform:translateY(-8px);opacity:.5}75%{opacity:.9}}
.title{animation:fade 1.2s ease-out}
@keyframes fade{from{opacity:0}to{opacity:1}}
"""


def lerp(a, b, t):
    ar, ag, ab = (int(a[i:i + 2], 16) for i in (1, 3, 5))
    br, bg, bb = (int(b[i:i + 2], 16) for i in (1, 3, 5))
    return f"#{round(ar+(br-ar)*t):02x}{round(ag+(bg-ag)*t):02x}{round(ab+(bb-ab)*t):02x}"


def ramp(t):
    """t in [0,1] bottom->top through the aurora stops."""
    t = max(0.0, min(0.999, t))
    seg = t * (len(AURORA) - 1)
    i = int(seg)
    return lerp(AURORA[i], AURORA[i + 1], seg - i)


def aurora():
    """Three flowing vertical light curtains, brightest mid-height, fading at the ends."""
    out = []
    ribbons = [(0.0, 78, 74), (2.2, 96, 92), (4.1, 66, 62)]  # phase, center_y, height
    for phase, cy, hgt in ribbons:
        for x in range(0, W, CELL):
            sway = 20 * math.sin(x / 90 + phase) + 8 * math.sin(x / 34 + phase * 2)
            top = cy + sway - hgt / 2
            steps = int(hgt // CELL)
            for s in range(steps):
                y = top + s * CELL
                if y < 6 or y > GRASS_Y - 30:
                    continue
                t = s / steps                       # 0 top .. 1 bottom
                base = 0.16 + 0.42 * math.sin(math.pi * t)   # brightest mid
                delay = (x / 130 + phase)
                out.append(
                    f'<rect class="au" x="{x}" y="{y:.0f}" width="{CELL}" height="{CELL}" '
                    f'fill="{ramp(1 - t)}" style="--o:{base:.2f};animation-delay:{-delay:.2f}s"/>'
                )
    return "".join(out)


def stars():
    out = []
    for _ in range(20):
        x, y = rng.randint(12, W - 12), rng.randint(8, GRASS_Y - 60)
        s = rng.choice((2, 2, 3))
        out.append(
            f'<rect class="star" x="{x}" y="{y}" width="{s}" height="{s}" fill="#e8ecff" '
            f'style="animation-delay:{-rng.uniform(0, 4.5):.2f}s"/>'
        )
    return "".join(out)


def moon():
    cx, cy = 748, 44
    out = []
    for gx in range(cx - 14, cx + 15, 4):
        for gy in range(cy - 14, cy + 15, 4):
            if (gx - cx) ** 2 + (gy - cy) ** 2 > 13 ** 2:
                continue
            if (gx - cx - 6) ** 2 + (gy - cy + 2) ** 2 < 11 ** 2:
                continue
            out.append(f'<rect x="{gx}" y="{gy}" width="4" height="4" fill="#f2e6c0"/>')
    return "".join(out)


def hills():
    out = []
    for x in range(0, W, CELL):
        h = 14 + 9 * math.sin(x / 100) + 5 * math.sin(x / 43 + 2)
        y = GRASS_Y - int(h // CELL) * CELL
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{GRASS_Y - y}" fill="#0a1526"/>')
    return "".join(out)


def grass():
    out = [f'<rect x="0" y="{GRASS_Y}" width="{W}" height="{H - GRASS_Y}" fill="#16280f"/>']
    for gx in range(0, W, 6):
        if rng.random() < 0.5:
            color = "#274018" if rng.random() < 0.6 else "#3f6626"
            out.append(f'<rect x="{gx}" y="{GRASS_Y}" width="6" height="6" fill="{color}"/>')
    return "".join(out)


def crops():
    out = []
    for i, x in enumerate((150, 250, 590, 700)):
        out.append(crop(x, GRASS_Y + 2, CROP_KINDS[i % len(CROP_KINDS)], delay_s=i * 1.9, px=3))
    return "".join(out)


def fireflies():
    out = []
    for _ in range(7):
        x = rng.randint(30, W - 30)
        y = rng.randint(GRASS_Y - 38, GRASS_Y - 10)
        out.append(
            f'<rect class="fly" x="{x}" y="{y}" width="3" height="3" fill="#A6D583" '
            f'style="animation-delay:{-rng.uniform(0, 6):.2f}s"/>'
        )
    return "".join(out)


def title():
    x = W / 2
    o = f'stroke="{SKY_TOP}" stroke-width="6" paint-order="stroke" stroke-linejoin="round"'
    return (
        f'<g class="title" text-anchor="middle" font-weight="700">'
        f'<text x="{x}" y="132" fill="#ffffff" font-size="42" {o}>Sanober Rehman</text>'
        f'<text x="{x}" y="164" fill="{GOLD}" font-size="17" {o}>AI/ML Engineer &#183; LLM &amp; GenAI Developer</text>'
        f'<text x="{x}" y="190" fill="{MUTED}" font-size="13" {o}>Dubai, UAE</text>'
        f"</g>"
    )


def build():
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Courier New, monospace">'
        f"<style>{CROP_CSS}{EXTRA_CSS}</style>"
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{SKY_TOP}"/><stop offset="1" stop-color="{SKY_BOT}"/>'
        f"</linearGradient></defs>"
        f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
        + aurora() + stars() + moon() + hills() + grass() + crops() + fireflies() + title()
        + "</svg>"
    )


def main():
    os.makedirs("assets", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
