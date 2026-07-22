"""Generate a compact animated 'farm field' languages bar into dist/."""
import json
import os
import urllib.request

from pixel import BG, FG, ACCENT, CROP_CSS, crop

USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "SanoberRehman")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join("dist", "languages-field.svg")

# Validated categorical order for the dark surface: green, blue, gold, purple, rust.
PALETTE = ["#6FA344", "#4E93C9", "#B08428", "#8E5FA8", "#A9603A"]
OTHER = "#6b7075"
MAX_SEGMENTS = 5

W, H = 800, 128
BAR_X, BAR_W, BAR_Y, BAR_H = 10, 780, 66, 26
CROP_BASE = 64


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
        segments.append(
            f'<rect x="{x:.1f}" y="{BAR_Y}" width="{seg_w:.1f}" height="{BAR_H}" fill="{color}"/>'
        )
        if seg_w >= 90:
            segments.append(
                f'<text x="{x + 8:.1f}" y="{BAR_Y + 17}" fill="{BG}" font-size="12" '
                f'font-weight="700">{lang} {frac * 100:.1f}%</text>'
            )
        if seg_w >= 26 and lang != "Other":
            n = max(1, int(seg_w // 64))
            for k in range(n):
                cx = x + (k + 0.5) * seg_w / n - 7
                crops.append(crop(cx, CROP_BASE, color, delay_s=crop_i * 1.1))
                crop_i += 1
        legend.append(
            f'<rect x="{legend_x}" y="{H - 21}" width="9" height="9" fill="{color}"/>'
            f'<text x="{legend_x + 14}" y="{H - 12}" fill="{FG}" font-size="11">{lang} {frac * 100:.1f}%</text>'
        )
        legend_x += 14 + 8 + int(6.7 * (len(lang) + 7))
        x += w

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Courier New, monospace">'
        f"<style>{CROP_CSS}</style>"
        f'<rect width="{W}" height="{H}" fill="{BG}"/>'
        f'<text x="{BAR_X}" y="20" fill="{ACCENT}" font-size="14" font-weight="700">Languages</text>'
        + "".join(segments) + "".join(crops) + "".join(legend) + "</svg>"
    )


def main():
    os.makedirs("dist", exist_ok=True)
    svg = build_svg(collect_languages())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
