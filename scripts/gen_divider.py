"""Generate an animated pixel divider into assets/ (run locally, commit output).

A butterfly flutters across a soft firefly-lit line — used between README sections.
"""
import os

OUT = os.path.join("assets", "divider.svg")
W, H = 640, 34
MID = 20

CSS = """
.fly-x{animation:flyx 9s linear infinite}
@keyframes flyx{0%{transform:translateX(-30px)}100%{transform:translateX(660px)}}
.hop{animation:hop 1.4s ease-in-out infinite}
@keyframes hop{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.w1{animation:wf .18s steps(1) infinite}
.w2{animation:wf2 .18s steps(1) infinite}
@keyframes wf{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes wf2{0%,49%{opacity:0}50%,100%{opacity:1}}
.fl{animation:fl 5s ease-in-out infinite}
@keyframes fl{0%,100%{opacity:.15;transform:translateY(0)}30%{opacity:1}50%{opacity:.5;transform:translateY(-4px)}70%{opacity:.9}}
"""

PX = 3
WING_OPEN = [".p.b.p.", "pbbbbbp", ".pbbbp.", "..pbp.."]
WING_CLOSED = ["..b.b..", ".pbbbp.", ".pbbbp.", "..pbp.."]
COL = {"b": "#c98adf", "p": "#f0b6ff"}


def sprite(rows, x, y):
    out = []
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch != ".":
                out.append(f'<rect x="{x + c * PX}" y="{y + r * PX}" width="{PX}" height="{PX}" fill="{COL[ch]}"/>')
    return "".join(out)


def butterfly():
    body_o = sprite(WING_OPEN, 0, 0)
    body_c = sprite(WING_CLOSED, 0, 0)
    return (f'<g class="fly-x"><g class="hop"><g transform="translate(0,{MID - 6})">'
            f'<g class="w1">{body_o}</g><g class="w2">{body_c}</g>'
            f"</g></g></g>")


def line():
    parts = [f'<defs><linearGradient id="ln" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="#2a3a1e" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="#5a7a3a" stop-opacity="0.7"/>'
             f'<stop offset="1" stop-color="#2a3a1e" stop-opacity="0"/></linearGradient></defs>'
             f'<rect x="0" y="{MID + 6}" width="{W}" height="2" fill="url(#ln)"/>']
    for i, (x, d) in enumerate([(120, 0.0), (300, 1.7), (430, 3.2), (540, 4.4)]):
        parts.append(f'<rect class="fl" x="{x}" y="{MID + 2}" width="3" height="3" fill="#A6D583" '
                     f'style="animation-delay:{-d:.2f}s"/>')
    return "".join(parts)


def build():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f"<style>{CSS}</style>{line()}{butterfly()}</svg>")


def main():
    os.makedirs("assets", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
