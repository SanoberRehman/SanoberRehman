"""Generate an animated pixel Pac-Man banner into assets/ (run locally, commit output).

Pac-Man stays put and chomps a stream of pellets flowing in from the right, with the
four ghosts bobbing behind. Designed so the *static* first frame already reads as a
full Pac-Man scene (in case a renderer freezes CSS animation), with motion as a bonus.
"""
import os

OUT = os.path.join("assets", "pacman.svg")
W, H = 820, 92
PX = 4
MID = 44
PAC_X = 210
SPACING = 28

Y = "#FFD23F"
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
.chomp2{{animation:c2 .32s steps(1) infinite}}
@keyframes c2{{0%,49%{{opacity:0}}50%,100%{{opacity:1}}}}
.chomp1{{animation:c1 .32s steps(1) infinite}}
@keyframes c1{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.flow{{animation:flow .62s linear infinite}}
@keyframes flow{{from{{transform:translateX(0)}}to{{transform:translateX(-{SPACING}px)}}}}
.bob{{animation:bob 1.5s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
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


def pellets():
    top_y = MID + 2
    dots = "".join(
        f'<circle cx="{x}" cy="{top_y}" r="3.4" fill="{PELLET}"/>'
        for x in range(PAC_X + 40, W + SPACING, SPACING)
    )
    return f'<g class="flow">{dots}</g>'


def ghosts():
    top = MID - len(GHOST) * PX // 2
    out = []
    for i, color in enumerate(GHOSTS):
        gx = 26 + i * 42
        body = sprite(GHOST, 0, top, {"B": color, "w": EYE, "p": PUP})
        out.append(f'<g class="bob" style="animation-delay:{-i * 0.35:.2f}s;transform-box:fill-box">'
                   f'<g transform="translate({gx},0)">{body}</g></g>')
    return "".join(out)


def pacman():
    top = MID - len(PAC_OPEN) * PX // 2
    o = sprite(PAC_OPEN, PAC_X, top, {"Y": Y})
    cl = sprite(PAC_CLOSED, PAC_X, top, {"Y": Y})
    return (f'<g class="chomp1">{o}</g>'
            f'<g class="chomp2" style="opacity:0">{cl}</g>')


def build():
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f"<style>{CSS}</style>"
        f'<rect width="{W}" height="{H}" rx="6" fill="{BG}"/>'
        f"{pellets()}"
        f'<rect x="0" y="0" width="{PAC_X + 30}" height="{H}" fill="{BG}"/>'  # eaten side / mask
        f"{ghosts()}{pacman()}"
        "</svg>"
    )


def main():
    os.makedirs("assets", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
