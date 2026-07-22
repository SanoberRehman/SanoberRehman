"""Shared pixel-art helpers: Stardew-style crop sprites drawn from pixel maps."""

NIGHT = "#0e1633"
CARD = "#10162b"
FG = "#d8d0b8"
MUTED = "#9FB0D8"
GOLD = "#E8C170"
SPARK = "#F5D76E"

COLORS = {
    "g": "#5ca933",  # leaf mid green
    "G": "#3e7d23",  # leaf dark green
    "h": "#8fd14f",  # leaf light green
    "c": "#e8d9a8",  # parsnip root cream
    "m": "#6b4a2b",  # soil mound
    "t": "#7a5230",  # woody stem
    "b": "#4a72c4",  # blueberry
    "B": "#7ea0e0",  # blueberry highlight
    "P": "#d8862c",  # pumpkin body
    "p": "#e8a84c",  # pumpkin highlight
    "D": "#a85e1c",  # pumpkin rib shadow
    "u": "#7da03c",  # unripe green
    "s": "#6b8f2e",  # vine
}

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

# Each crop: three growth stages as pixel maps ('.' = empty), drawn bottom-anchored.
SPRITES = {
    "parsnip": [
        [
            "..h.h..",
            "...g...",
        ],
        [
            ".g.h.g.",
            "..ghg..",
            ".ghghg.",
            "...g...",
        ],
        [
            ".h..g..h.",
            ".ghggh.g.",
            "..hgGgh..",
            "...gGg...",
            "....G....",
            "..mmmmm..",
            ".mmcccmm.",
        ],
    ],
    "blueberry": [
        [
            "..gh..",
            "..t...",
        ],
        [
            "..ggg..",
            ".ggGgg.",
            "..gtg..",
            "...t...",
        ],
        [
            "..gggg...",
            ".gBgggb..",
            "ggbgGgbg.",
            "gGgbggGg.",
            ".gbgGbg..",
            "..gggg...",
            "...tt....",
        ],
    ],
    "pumpkin": [
        [
            "..sh..",
            "..s...",
        ],
        [
            ".h.s...",
            ".shss..",
            "..uu...",
            "..uu...",
        ],
        [
            "...tt....",
            "h..tt..h.",
            ".ppPDPp..",
            "pPPDPPDp.",
            "pPPDPPDp.",
            ".pPDPPD..",
            "..DDDD...",
        ],
    ],
}

CROP_KINDS = list(SPRITES.keys())


def render_map(rows, x, base_y, px):
    """Render a pixel map bottom-anchored at (x, base_y), run-length encoding rows."""
    out = []
    n = len(rows)
    for r, row in enumerate(rows):
        y = base_y - (n - r) * px
        col = 0
        while col < len(row):
            ch = row[col]
            if ch == ".":
                col += 1
                continue
            run = 1
            while col + run < len(row) and row[col + run] == ch:
                run += 1
            out.append(
                f'<rect x="{x + col * px:.0f}" y="{y}" width="{run * px}" height="{px}" fill="{COLORS[ch]}"/>'
            )
            col += run
    return "".join(out)


def crop(x, base_y, kind, delay_s, px=3, sparkle=True):
    """An animated crop sprite cycling through three growth stages."""
    stages = SPRITES[kind]
    groups = []
    for i, rows in enumerate(stages):
        body = render_map(rows, x, base_y, px)
        if sparkle and i == 2:
            sx, sy = x + len(rows[0]) * px, base_y - (len(rows) + 1) * px
            body += (
                f'<g class="sp">'
                f'<rect x="{sx:.0f}" y="{sy}" width="2" height="2" fill="{SPARK}"/>'
                f'<rect x="{sx - 4:.0f}" y="{sy + 5}" width="2" height="2" fill="{SPARK}"/>'
                f'<rect x="{sx + 3:.0f}" y="{sy - 4}" width="2" height="2" fill="{SPARK}"/>'
                f"</g>"
            )
        groups.append(f'<g class="s{i + 1}" style="animation-delay:{-delay_s:.2f}s">{body}</g>')
    return "".join(groups)


def shade(hex_color, amount):
    """Blend a hex color toward white (amount > 0) or black (amount < 0)."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    target = 255 if amount > 0 else 0
    a = abs(amount)
    r, g, b = (round(v + (target - v) * a) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"
