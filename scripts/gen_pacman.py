"""Generate an animated pixel Pac-Man banner into assets/ (run locally, commit output)."""
import os

OUT = os.path.join("assets", "pacman.svg")
W, H = 820, 92
PX = 4
MID = 44                      # vertical center for sprites
START, END = -48, W + 40      # pac-man travel range
T = 7.0                       # seconds per loop

Y = "#FFD23F"                 # pac-man
GHOSTS = ["#FF4B57", "#FFB8DE", "#4FE0E8", "#FFA94D"]  # Blinky, Pinky, Inky, Clyde
EYE, PUP = "#ffffff", "#2440c8"
PELLET = "#F5E6B3"
BG = "#0d1117"

PAC_OPEN = [
    "...YYYYY...",
    ".YYYYYYYY..",
    "YYYYYYYY...",
    "YYYYYYY....",
    "YYYYYY.....",
    "YYYYY......",
    "YYYYYY.....",
    "YYYYYYY....",
    "YYYYYYYY...",
    ".YYYYYYYY..",
    "...YYYYY...",
]
PAC_CLOSED = [
    "...YYYYY...",
    ".YYYYYYYYY.",
    "YYYYYYYYYYY",
    "YYYYYYYYYYY",
    "YYYYYYYYYY.",
    "YYYYYYYYY..",
    "YYYYYYYYYY.",
    "YYYYYYYYYYY",
    "YYYYYYYYYYY",
    ".YYYYYYYYY.",
    "...YYYYY...",
]
GHOST = [
    "..BBBBB..",
    ".BBBBBBB.",
    "BBBBBBBBB",
    "BwwBBwwBB",
    "BwpBBwpBB",
    "BwwBBwwBB",
    "BBBBBBBBB",
    "BBBBBBBBB",
    "BBBBBBBBB",
    "B.BB.BB.B",
]

CSS = f"""
.pac{{animation:move {T}s linear infinite}}
@keyframes move{{from{{transform:translateX({START}px)}}to{{transform:translateX({END}px)}}}}
.chomp1{{animation:c1 .34s steps(1) infinite}}
.chomp2{{animation:c2 .34s steps(1) infinite}}
@keyframes c1{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes c2{{0%,49%{{opacity:0}}50%,100%{{opacity:1}}}}
.bob{{animation:bob 1.6s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
.eat{{animation:eat {T}s linear infinite}}
@keyframes eat{{0%,92%{{opacity:1}}93%,100%{{opacity:0}}}}
"""


def sprite(rows, x, y, colors):
    out = []
    for r, line in enumerate(rows):
        c = 0
        while c < len(line):
            ch = line[c]
            if ch == ".":
                c += 1
                continue
            run = 1
            while c + run < len(line) and line[c + run] == ch:
                run += 1
            out.append(f'<rect x="{x + c * PX}" y="{y + r * PX}" width="{run * PX}" height="{PX}" fill="{colors[ch]}"/>')
            c += run
    return "".join(out)


def pacman_group():
    top = MID - len(PAC_OPEN) * PX // 2
    o = sprite(PAC_OPEN, 0, top, {"Y": Y})
    cl = sprite(PAC_CLOSED, 0, top, {"Y": Y})
    return (f'<g class="pac"><g class="chomp1">{o}</g><g class="chomp2">{cl}</g></g>')


def ghost_group(color, back_offset, delay):
    top = MID - len(GHOST) * PX // 2
    body = sprite(GHOST, 0, top, {"B": color, "w": EYE, "p": PUP})
    return (f'<g class="pac" style="animation-delay:0s">'
            f'<g class="bob" style="animation-delay:{delay:.2f}s;transform-box:fill-box">'
            f'<g transform="translate({back_offset},0)">{body}</g></g></g>')


def pellets():
    out = []
    step = 26
    for x in range(30, W - 20, step):
        f = (x - START) / (END - START)
        delay = (f - 0.925) * T
        out.append(
            f'<circle class="eat" cx="{x}" cy="{MID + 2}" r="3.2" fill="{PELLET}" '
            f'style="animation-delay:{delay:.2f}s"/>'
        )
    return "".join(out)


def build():
    # Ghosts trail behind Pac-Man (to its left) at increasing offsets.
    ghosts = "".join(
        ghost_group(GHOSTS[i], -34 * (i + 1) - 20, delay=i * 0.4)
        for i in range(len(GHOSTS))
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f"<style>{CSS}</style>"
        f'<rect width="{W}" height="{H}" rx="6" fill="{BG}"/>'
        + pellets() + ghosts + pacman_group()
        + "</svg>"
    )


def main():
    os.makedirs("assets", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
