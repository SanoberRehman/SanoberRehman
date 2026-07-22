"""Generate the animated pixel-art header banner into assets/ (run locally, commit output)."""
import os
import random

from pixel import BG, FG, MUTED, ACCENT, CROP_CSS, crop

OUT = os.path.join("assets", "header.svg")
W, H = 830, 210
GRASS_Y = H - 26
PALETTE = ["#6FA344", "#4E93C9", "#B08428", "#8E5FA8", "#A9603A"]

rng = random.Random(20260722)

EXTRA_CSS = """
.star{animation:tw 4s infinite}
@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}
.fly{animation:fl 6s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0);opacity:.2}25%{opacity:1}50%{transform:translateY(-9px);opacity:.5}75%{opacity:.9}}
.title{animation:fade 1.2s ease-out}
@keyframes fade{from{opacity:0}to{opacity:1}}
"""


def stars():
    out = []
    for _ in range(16):
        x, y = rng.randint(15, W - 15), rng.randint(12, 95)
        d = rng.uniform(0, 4)
        out.append(
            f'<rect class="star" x="{x}" y="{y}" width="2" height="2" fill="#ffffff" '
            f'style="animation-delay:{-d:.2f}s"/>'
        )
    return "".join(out)


def fireflies():
    out = []
    for _ in range(7):
        x = rng.randint(30, W - 30)
        y = rng.randint(GRASS_Y - 45, GRASS_Y - 12)
        d = rng.uniform(0, 6)
        out.append(
            f'<rect class="fly" x="{x}" y="{y}" width="3" height="3" fill="{ACCENT}" '
            f'style="animation-delay:{-d:.2f}s"/>'
        )
    return "".join(out)


def grass():
    out = [f'<rect x="0" y="{GRASS_Y}" width="{W}" height="{H - GRASS_Y}" fill="#1a2e12"/>']
    for gx in range(0, W, 6):
        if rng.random() < 0.55:
            shade = "#2d4a1e" if rng.random() < 0.6 else "#48732c"
            out.append(f'<rect x="{gx}" y="{GRASS_Y}" width="6" height="6" fill="{shade}"/>')
        if rng.random() < 0.12:
            out.append(f'<rect x="{gx}" y="{GRASS_Y - 4}" width="3" height="4" fill="#48732c"/>')
    return "".join(out)


def crops():
    out = []
    xs = [60, 175, 640, 755]
    for i, x in enumerate(xs):
        out.append(crop(x, GRASS_Y + 2, PALETTE[i % len(PALETTE)], delay_s=i * 1.9, px=4))
    return "".join(out)


def build():
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Courier New, monospace">'
        f"<style>{CROP_CSS}{EXTRA_CSS}</style>"
        f'<rect width="{W}" height="{H}" fill="{BG}"/>'
        + stars() + grass() + crops() + fireflies() +
        f'<g class="title" text-anchor="middle">'
        f'<text x="{W / 2}" y="92" fill="#ffffff" font-size="40" font-weight="700">Sanober Rehman</text>'
        f'<text x="{W / 2}" y="122" fill="{ACCENT}" font-size="16">AI/ML Engineer &#183; LLM &amp; GenAI Developer</text>'
        f'<text x="{W / 2}" y="146" fill="{MUTED}" font-size="13">Dubai, UAE</text>'
        f"</g></svg>"
    )


def main():
    os.makedirs("assets", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
