"""Shared pixel-art helpers for the profile's generated SVGs."""

BG = "#0d1117"
FG = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#A6D583"
STEM = "#48732c"
LEAF = "#6FA344"

CROP_CSS = """
.s1{animation:k1 7.5s infinite}
.s2{animation:k2 7.5s infinite}
.s3{animation:k3 7.5s infinite}
@keyframes k1{0%,32.9%{opacity:1}33%,100%{opacity:0}}
@keyframes k2{0%,32.9%{opacity:0}33%,65.9%{opacity:1}66%,100%{opacity:0}}
@keyframes k3{0%,65.9%{opacity:0}66%,100%{opacity:1}}
"""

# (col, row) pixel maps per growth stage; row 0 sits on the baseline.
STAGES = [
    {"stem": [(2, 0), (2, 1)], "leaf": [(1, 1)], "fruit": []},
    {"stem": [(2, 0), (2, 1), (2, 2)], "leaf": [(1, 2), (3, 2)], "fruit": []},
    {"stem": [(2, 0), (2, 1), (2, 2), (2, 3)], "leaf": [(1, 2), (3, 2), (1, 3), (3, 3)], "fruit": [(2, 4)]},
]


def crop(x, base_y, fruit_color, delay_s, px=3):
    """An animated crop sprite cycling through three growth stages."""
    groups = []
    for i, stage in enumerate(STAGES):
        pixels = []
        for (c, r) in stage["stem"]:
            pixels.append((c, r, STEM))
        for (c, r) in stage["leaf"]:
            pixels.append((c, r, LEAF))
        for (c, r) in stage["fruit"]:
            pixels.append((c, r, fruit_color))
        rects = "".join(
            f'<rect x="{x + c * px}" y="{base_y - (r + 1) * px}" width="{px}" height="{px}" fill="{col}"/>'
            for c, r, col in pixels
        )
        groups.append(f'<g class="s{i + 1}" style="animation-delay:{-delay_s:.2f}s">{rects}</g>')
    return "".join(groups)
