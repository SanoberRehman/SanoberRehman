"""Shared pixel-art helpers for the profile's generated SVGs."""

NIGHT = "#0e1633"
CARD = "#10162b"
FG = "#d8d0b8"
MUTED = "#9FB0D8"
GOLD = "#E8C170"
SPARK = "#F5D76E"
STEM = "#48732c"
LEAF = "#6FA344"

CROP_CSS = """
.s1{animation:k1 7.5s infinite}
.s2{animation:k2 7.5s infinite}
.s3{animation:k3 7.5s infinite}
.sp{animation:kp 7.5s infinite}
@keyframes k1{0%,32.9%{opacity:1}33%,100%{opacity:0}}
@keyframes k2{0%,32.9%{opacity:0}33%,65.9%{opacity:1}66%,100%{opacity:0}}
@keyframes k3{0%,65.9%{opacity:0}66%,100%{opacity:1}}
@keyframes kp{0%,69%{opacity:0}74%{opacity:1}80%{opacity:.15}88%{opacity:1}96%,100%{opacity:.2}}
"""

STAGES = [
    {"stem": [(2, 0), (2, 1)], "leaf": [(1, 1)], "fruit": []},
    {"stem": [(2, 0), (2, 1), (2, 2)], "leaf": [(1, 2), (3, 2)], "fruit": []},
    {"stem": [(2, 0), (2, 1), (2, 2), (2, 3)], "leaf": [(1, 2), (3, 2), (1, 3), (3, 3)], "fruit": [(2, 4)]},
]


def shade(hex_color, amount):
    """Blend a hex color toward white (amount > 0) or black (amount < 0)."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    target = 255 if amount > 0 else 0
    a = abs(amount)
    r, g, b = (round(v + (target - v) * a) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def crop(x, base_y, fruit_color, delay_s, px=3, sparkle=False):
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
            f'<rect x="{x + c * px:.0f}" y="{base_y - (r + 1) * px}" width="{px}" height="{px}" fill="{col}"/>'
            for c, r, col in pixels
        )
        if sparkle and i == 2:
            sx, sy = x + 4 * px, base_y - 6 * px
            rects += (
                f'<g class="sp">'
                f'<rect x="{sx:.0f}" y="{sy}" width="2" height="2" fill="{SPARK}"/>'
                f'<rect x="{sx - 3:.0f}" y="{sy + 4}" width="2" height="2" fill="{SPARK}"/>'
                f'<rect x="{sx + 3:.0f}" y="{sy - 4}" width="2" height="2" fill="{SPARK}"/>'
                f"</g>"
            )
        groups.append(f'<g class="s{i + 1}" style="animation-delay:{-delay_s:.2f}s">{rects}</g>')
    return "".join(groups)
