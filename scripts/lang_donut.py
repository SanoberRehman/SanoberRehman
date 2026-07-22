"""Generate a minimal languages donut SVG from the GitHub API into dist/."""
import json
import math
import os
import urllib.request

USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "SanoberRehman")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join("dist", "languages-donut.svg")

PALETTE = ["#8B5CF6", "#A78BFA", "#C4B5FD", "#9aa0a6", "#6b7075", "#3c4043"]
BG = "#0d1117"
FG = "#c9d1d9"
ACCENT = "#8B5CF6"
MAX_SEGMENTS = 5


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

    cx, cy, r, stroke = 105, 110, 62, 26
    circ = 2 * math.pi * r
    parts, legend = [], []
    offset = 0.0
    for i, (lang, size) in enumerate(top):
        frac = size / total
        color = PALETTE[i % len(PALETTE)]
        dash = max(frac * circ - 1.5, 0.1)
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" '
            f'stroke-width="{stroke}" stroke-dasharray="{dash:.2f} {circ:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        )
        y = 74 + i * 22
        legend.append(
            f'<rect x="215" y="{y - 9}" width="10" height="10" rx="2" fill="{color}"/>'
            f'<text x="233" y="{y}" fill="{FG}" font-size="13">{lang}</text>'
            f'<text x="385" y="{y}" fill="{FG}" font-size="13" text-anchor="end">{frac * 100:.1f}%</text>'
        )
        offset += frac * circ

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200" '
        f'font-family="Segoe UI, Ubuntu, sans-serif">'
        f'<rect width="400" height="200" rx="8" fill="{BG}"/>'
        f'<text x="215" y="42" fill="{ACCENT}" font-size="16" font-weight="600">Languages</text>'
        + "".join(parts) + "".join(legend) + "</svg>"
    )


def main():
    os.makedirs("dist", exist_ok=True)
    svg = build_svg(collect_languages())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
