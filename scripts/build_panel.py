"""Draw one project panel per repo (light and dark SVG) from live GitHub data.

Run by .github/workflows/panel.yml every day; keeps the last good numbers when the API is unreachable.
Add a project by adding an entry to PROJECTS and an <a><picture> block to README.md.
"""
import base64
import datetime as dt
import html
import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CACHE = ASSETS / "panel-data.json"

PROJECTS = [
    dict(slug="postglow", repo="BTCUP99/postglow", title="Postglow · 账号复盘", art="icon", image="postglow-icon.png",
         badge=("New", "#5b6cff", 70, 690), accent="#5b6cff",
         tag="一个轻量的 Mac 小工具，在本地复盘你的 X 帖子",
         en="Which posts got read, which hour and form work, where followers came from.",
         tech="Tauri 2 · Rust · plain JS · macOS universal · MIT",
         chips=[("🔑 No login", 100), ("💻 Local only", 108), ("⏱️ Hourly", 92), ("🧲 Follower sources", 150),
                ("🪶 Lightweight", 116)]),
    dict(slug="jax", repo="BTCUP99/jax-stopwatch", title="jax-stopwatch", art="watch", image="jax-face.jpg",
         badge=("Active", "#22c55e", 92, 612), accent="#ff9a4d",
         tag="按住说话，Mac 帮你办 —— 手腕上的 Codex / Agent 语音入口",
         en="Push-to-talk from an M5Stack StopWatch to Codex & webhook agents, through your Mac.",
         tech="ESP32-S3 firmware · Python bridge · MLX Whisper · MIT",
         chips=[("🎙️ Push-to-talk", 124), ("🔒 Local Whisper", 132), ("📶 Wi-Fi anywhere", 138), ("🔔 X alerts", 92),
                ("🎨 Avatars", 88)]),
]


def api(path):
    request = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        request.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def collect(repo, data):
    try:
        info = api(f"repos/{repo}")
        data.update(stars=info["stargazers_count"], forks=info["forks_count"], issues=info["open_issues_count"],
                    pushed=info["pushed_at"][:10])
    except Exception as error:  # keep the last good values
        print(repo, "repo:", error)
    try:
        data["release"] = api(f"repos/{repo}/releases/latest")["tag_name"]
    except Exception as error:
        print(repo, "release:", error)
    try:
        runs = api(f"repos/{repo}/actions/runs?branch=main&status=completed&per_page=1")["workflow_runs"]
        if runs:
            data["ci"] = runs[0]["conclusion"]
    except Exception as error:
        print(repo, "ci:", error)
    return data


THEMES = {
    "dark": dict(bg1="#0b0f17", bg2="#141a28", card="#ffffff08", line="#ffffff1c", fg="#f3f5f9", sub="#aeb6c6",
                 muted="#727c90", bezel="#2d323c", glow=".5"),
    "light": dict(bg1="#f8f9fc", bg2="#eef1f7", card="#ffffffd9", line="#d9dee8", fg="#141a24", sub="#4a5568",
                  muted="#8a94a6", bezel="#c9ced8", glow=".25"),
}


def art(p, t):
    path = ASSETS / p["image"]
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    src = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
    if p["art"] == "watch":
        return (f'<circle cx="170" cy="200" r="132" fill="{t["bezel"]}"/><circle cx="170" cy="200" r="122" fill="#0b0c0f"/>'
                f'<circle cx="170" cy="200" r="112" fill="#000"/>'
                f'<image clip-path="url(#screen)" x="58" y="88" width="224" height="224" href="{src}" xlink:href="{src}"/>')
    # App icon: the PNG already carries the macOS squircle; add a soft shadow under it.
    return (f'<rect x="66" y="104" width="208" height="208" rx="46" fill="#000" opacity=".18" filter="url(#blur)"/>'
            f'<image x="50" y="80" width="240" height="240" href="{src}" xlink:href="{src}"/>')


def panel(p, data, theme):
    t = THEMES[theme]
    ci = data.get("ci")
    ci_text, ci_color = {"success": ("passing", "#22c55e"), "failure": ("failing", "#ef4444")}.get(ci, ("—", t["muted"]))
    stats = [("STARS", str(data.get("stars", 0)), t["fg"]), ("FORKS", str(data.get("forks", 0)), t["fg"]),
             ("RELEASE", data.get("release") or "—", t["fg"]), ("CI", ci_text, ci_color)]
    tiles = ""
    for i, (label, value, color) in enumerate(stats):
        x = 360 + i * 152
        tiles += (f'<g transform="translate({x},196)"><rect width="140" height="76" rx="14" fill="{t["card"]}" stroke="{t["line"]}"/>'
                  f'<text x="16" y="28" class="label">{label}</text>'
                  f'<text x="16" y="58" class="value" fill="{color}">{html.escape(value)}</text></g>')
    chips, x = "", 360
    for text, w in p["chips"]:
        chips += (f'<g transform="translate({x},296)"><rect width="{w:.0f}" height="30" rx="15" fill="{t["card"]}" stroke="{t["line"]}"/>'
                  f'<text x="{w / 2:.0f}" y="20" text-anchor="middle" class="chip">{html.escape(text)}</text></g>')
        x += w + 8
    badge, color, bw, bx = p["badge"]  # bx: left edge, set by eye after the title
    updated = data.get("pushed") or dt.date.today().isoformat()
    title = html.escape(p["title"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1000" height="400" viewBox="0 0 1000 400" role="img" aria-label="{title} project panel">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{p["accent"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="glow2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#5b6cff" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="#5b6cff" stop-opacity="0"/></radialGradient>
<clipPath id="screen"><circle cx="170" cy="200" r="112"/></clipPath>
<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="12"/></filter>
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Helvetica,Arial,sans-serif}}
.title{{font-size:34px;font-weight:700;fill:{t["fg"]}}}
.tag{{font-size:17px;fill:{t["sub"]}}}
.en{{font-size:14px;fill:{t["muted"]}}}
.label{{font-size:11px;font-weight:600;letter-spacing:1.5px;fill:{t["muted"]}}}
.value{{font-size:24px;font-weight:700}}
.chip{{font-size:13px;fill:{t["sub"]}}}
.foot{{font-size:12px;fill:{t["muted"]}}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}} @keyframes pulse{{50%{{opacity:.35}}}}
.bob{{animation:bob 5s ease-in-out infinite}} @keyframes bob{{50%{{transform:translateY(-6px)}}}}
</style>
</defs>
<rect width="1000" height="400" rx="22" fill="url(#bg)" stroke="{t["line"]}"/>
<circle cx="170" cy="200" r="190" fill="url(#glow)"/><circle cx="900" cy="60" r="160" fill="url(#glow2)"/>
<g class="bob">{art(p, t)}</g>
<text x="360" y="78" class="title">{title}</text>
<g transform="translate({bx},52)"><rect width="{bw}" height="28" rx="14" fill="{color}1f" stroke="{color}66"/>
<circle cx="18" cy="14" r="5" fill="{color}" class="pulse"/><text x="30" y="19" font-size="13" font-weight="600" fill="{color}">{badge}</text></g>
<text x="360" y="118" class="tag">{html.escape(p["tag"])}</text>
<text x="360" y="146" class="en">{html.escape(p["en"])}</text>
<text x="360" y="176" class="en">{html.escape(p["tech"])}</text>
{tiles}
{chips}
<text x="360" y="366" class="foot">Updated {updated} · github.com/{p["repo"]}</text>
</svg>
'''


if __name__ == "__main__":
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if "stars" in cache:  # the old single-project format
        cache = {"BTCUP99/jax-stopwatch": cache}
    for p in PROJECTS:
        cache[p["repo"]] = collect(p["repo"], cache.get(p["repo"], {}))
        for theme in THEMES:
            (ASSETS / f"panel-{p['slug']}-{theme}.svg").write_text(panel(p, cache[p["repo"]], theme))
    CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(cache, ensure_ascii=False))
