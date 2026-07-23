"""Generate swaying Stardew-style wooden section signs into assets/ (run locally, commit)."""
import os

from pixel import CROP_CSS, crop

W, H = 520, 78
BOARD_X, BOARD_Y, BOARD_W, BOARD_H = 70, 20, 380, 46

CSS = """
.sway{animation:sway 4.5s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 2px}
@keyframes sway{0%,100%{transform:rotate(-1.6deg)}50%{transform:rotate(1.6deg)}}
.fly{animation:fl 5s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0);opacity:.25}30%{opacity:1}50%{transform:translateY(-6px);opacity:.6}70%{opacity:.95}}
.rope{stroke:#5a3a1e;stroke-width:3}
"""

SIGNS = [
    ("about", "About"),
    ("stack", "Tech Stack"),
    ("projects", "Projects"),
    ("experience", "Experience"),
    ("github", "GitHub Stats"),
]


def board(title):
    x, y, bw, bh = BOARD_X, BOARD_Y, BOARD_W, BOARD_H
    gold = "#D9A441"
    planks = "".join(
        f'<line x1="{x + 4}" y1="{y + 6 + i * 12}" x2="{x + bw - 4}" y2="{y + 6 + i * 12}" '
        f'stroke="#5A3A1E" stroke-width="1" opacity="0.5"/>'
        for i in range(1, bh // 12)
    )
    studs = "".join(
        f'<rect x="{sx}" y="{sy}" width="5" height="5" fill="{gold}"/>'
        for sx, sy in ((x + 3, y + 3), (x + bw - 8, y + 3), (x + 3, y + bh - 8), (x + bw - 8, y + bh - 8))
    )
    cx = x + bw / 2
    return (
        f'<g class="sway">'
        f'<line class="rope" x1="{x + 26}" y1="0" x2="{x + 26}" y2="{y}"/>'
        f'<line class="rope" x1="{x + bw - 26}" y1="0" x2="{x + bw - 26}" y2="{y}"/>'
        f'<rect x="{x - 2}" y="{y - 2}" width="{bw + 4}" height="{bh + 4}" rx="5" fill="#2a1c0e"/>'
        f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="4" fill="#7a4e28"/>'
        f'<rect x="{x + 3}" y="{y + 3}" width="{bw - 6}" height="{bh - 6}" rx="3" fill="#8a5a30"/>'
        f"{planks}{studs}"
        f'<text x="{cx}" y="{y + bh / 2 + 6}" text-anchor="middle" fill="#f3e2b8" '
        f'font-family="Courier New, monospace" font-size="20" font-weight="700">{title}</text>'
        f"</g>"
    )


def decorations():
    # a small growing crop on the left, a couple of fireflies drifting near the sign
    out = [crop(24, H - 8, "parsnip", delay_s=0.0, px=3)]
    for i, (fx, fy, d) in enumerate([(BOARD_X + 40, 12, 0.0), (W - 40, 24, 1.6), (W - 24, 44, 3.1)]):
        out.append(
            f'<rect class="fly" x="{fx}" y="{fy}" width="3" height="3" fill="#A6D583" '
            f'style="animation-delay:{-d:.2f}s"/>'
        )
    return "".join(out)


def build(title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f"<style>{CROP_CSS}{CSS}</style>"
        f"{decorations()}{board(title)}"
        "</svg>"
    )


def main():
    os.makedirs("assets", exist_ok=True)
    for slug, title in SIGNS:
        with open(os.path.join("assets", f"sign-{slug}.svg"), "w", encoding="utf-8") as f:
            f.write(build(title))
        print(f"wrote assets/sign-{slug}.svg")


if __name__ == "__main__":
    main()
