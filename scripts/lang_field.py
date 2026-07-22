"""Generate the animated 'farm field' languages card (Stardew wooden frame) into dist/."""
import json
import os
import urllib.request

from pixel import CARD, FG, GOLD, CROP_CSS, CROP_KINDS, crop, shade

USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "SanoberRehman")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join("dist", "languages-field.svg")

# Validated categorical order on the night-blue card surface.
PALETTE = ["#6DA232", "#4B8DD4", "#BD8A1F", "#A66FC4", "#C4703F"]
OTHER = "#77838f"
MAX_SEGMENTS = 5

W, H = 800, 172
FRAME = 8
BAR_X, BAR_W = 24, W - 48
BAR_Y, BAR_H = 90, 20
SOIL_H = 7
CROP_BASE = BAR_Y - 2

STAR_CSS = """
.star{animation:tw 4s infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:.9}}
"""


def api(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        req.add_header("Authorization", f"token {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect_languages():
    totals = {}
    page = 1
    while True:
        repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}")
        if not repos:
            break
        for repo in repos:
            if repo.get("fork"):
                continue
            for lang, size in api(repo["languages_url"]).items():
                totals[lang] = totals.get(lang, 0) + size
        page += 1
    return totals


def frame():
    """Stardew-style pixel wooden frame."""
    gold = "#D9A441"
    parts = [
        f'<rect width="{W}" height="{H}" fill="#2a1c0e"/>',
        f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" fill="#8B5A2B"/>',
        f'<rect x="5" y="5" width="{W - 10}" height="{H - 10}" fill="#5A3A1E"/>',
        f'<rect x="{FRAME}" y="{FRAME}" width="{W - 2 * FRAME}" height="{H - 2 * FRAME}" fill="{CARD}"/>',
    ]
    for cx, cy in ((2, 2), (W - 8, 2), (2, H - 8), (W - 8, H - 8)):
        parts.append(f'<rect x="{cx}" y="{cy}" width="6" height="6" fill="{gold}"/>')
    return "".join(parts)


def sky_stars():
    spots = [(120, 25), (300, 20), (470, 28), (620, 22), (740, 30), (390, 38)]
    return "".join(
        f'<rect class="star" x="{x}" y="{y}" width="3" height="3" fill="#f7e7a0" '
        f'style="animation-delay:{-i * 0.7:.2f}s"/>'
        for i, (x, y) in enumerate(spots)
    )


def soil():
    parts = [f'<rect x="{BAR_X}" y="{BAR_Y + BAR_H}" width="{BAR_W}" height="{SOIL_H}" fill="#4a3220"/>']
    for gx in range(BAR_X, BAR_X + BAR_W, 14):
        parts.append(f'<rect x="{gx + (gx // 14) % 7}" y="{BAR_Y + BAR_H + 2}" width="3" height="3" fill="#3a2718"/>')
    return "".join(parts)


def build_svg(totals):
    total = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    top = ranked[:MAX_SEGMENTS]
    rest = sum(size for _, size in ranked[MAX_SEGMENTS:])
    if rest:
        top.append(("Other", rest))

    segments, crops, legend = [], [], []
    x = float(BAR_X)
    legend_x = BAR_X
    crop_i = 0
    for i, (lang, size) in enumerate(top):
        frac = size / total
        w = frac * BAR_W
        color = OTHER if lang == "Other" else PALETTE[i % len(PALETTE)]
        seg_w = max(w - 2, 1)
        hi, lo = shade(color, 0.32), shade(color, -0.32)
        segments.append(
            f'<rect x="{x:.1f}" y="{BAR_Y}" width="{seg_w:.1f}" height="4" fill="{hi}"/>'
            f'<rect x="{x:.1f}" y="{BAR_Y + 4}" width="{seg_w:.1f}" height="{BAR_H - 8}" fill="{color}"/>'
            f'<rect x="{x:.1f}" y="{BAR_Y + BAR_H - 4}" width="{seg_w:.1f}" height="4" fill="{lo}"/>'
        )
        if seg_w >= 100:
            segments.append(
                f'<text x="{x + 9:.1f}" y="{BAR_Y + 14}" fill="{CARD}" font-size="12" '
                f'font-weight="700">{lang} {frac * 100:.1f}%</text>'
            )
        if seg_w >= 34 and lang != "Other":
            n = max(1, int(seg_w // 78))
            for k in range(n):
                cx = x + (k + 0.5) * seg_w / n - 13
                kind = CROP_KINDS[crop_i % len(CROP_KINDS)]
                crops.append(crop(cx, CROP_BASE, kind, delay_s=crop_i * 1.15, px=3))
                crop_i += 1
        legend.append(
            f'<rect x="{legend_x}" y="{H - 32}" width="9" height="7" fill="{color}"/>'
            f'<rect x="{legend_x}" y="{H - 25}" width="9" height="2" fill="{shade(color, -0.32)}"/>'
            f'<text x="{legend_x + 14}" y="{H - 24}" fill="{FG}" font-size="11">{lang} {frac * 100:.1f}%</text>'
        )
        legend_x += 14 + 8 + int(6.7 * (len(lang) + 7))
        x += w

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Courier New, monospace">'
        f"<style>{CROP_CSS}{STAR_CSS}</style>"
        + frame() + sky_stars()
        + f'<text x="{BAR_X}" y="32" fill="{GOLD}" font-size="15" font-weight="700">Languages</text>'
        + soil() + "".join(segments) + "".join(crops) + "".join(legend) + "</svg>"
    )


def main():
    os.makedirs("dist", exist_ok=True)
    svg = build_svg(collect_languages())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
