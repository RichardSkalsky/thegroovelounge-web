#!/usr/bin/env python3
"""Renderar bilder till sociala medier för en ny show (The Groove Lounge) med headless Chrome.

Användning:
    python3 tools/social.py content/shows/001-long-way-from-home.json --cover omslag-2048.jpg --out-dir ut/
    -> ut/<slug>-instagram-post.jpg   (1080 × 1350, 4:5)
       ut/<slug>-instagram-story.jpg  (1080 × 1920, 9:16)

Utan --cover renderas omslaget först med cover.py i 2048 px. Layouten är mallarna "1 · Ny show (inlägg 4:5)"
och "3 · Ny show (story 9:16)" i designsystemet (grafik/riktningar/Instagram.dc.html). Ändra där först.
I storyn är de översta 250 px och de nedersta 340 px tomma, eftersom Instagram lägger sina knappar där.
Platsen under "Listen on Mixcloud." är till länk-stickern, som läggs till i appen.
"""
import argparse, html, json, pathlib, subprocess, sys, tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cover import CHROME, render as render_cover  # noqa: E402

FONTS = ("https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..800;"
         "1,6..96,400..700&family=Jost:wght@400;500;600&display=swap")
BG = "radial-gradient(70% 60% at 50% 38%, #155240, #0b2a21 78%)"
LABEL = ("position:absolute;left:0;right:0;text-align:center;font-family:Jost,Futura,sans-serif;font-weight:500;"
         "letter-spacing:.4em;text-transform:uppercase;color:#c9a24a")
HEAD = ("position:absolute;left:0;right:0;text-align:center;font-family:'Bodoni Moda',Didot,serif;font-weight:600;"
        "font-variation-settings:'opsz' 28;color:#f3ecdc")


def page(w, h, inner):
    return f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">
<style>html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;background:#0b2a21}}
.c{{position:relative;width:{w}px;height:{h}px;background:{BG};overflow:hidden}}
.cv{{position:absolute;left:0;right:0;display:flex;justify-content:center}}
.cv img{{display:block;box-shadow:0 18px 40px rgba(0,0,0,.45)}}
.g{{font-style:italic;color:#c9a24a}}</style></head><body><div class="c">{inner}</div></body></html>"""


def post_html(show, cover_uri):
    nr = html.escape(show["number"])
    return page(1080, 1350, f"""
<div style="position:absolute;inset:36px;border:1.5px solid #c9a24a"></div>
<div style="position:absolute;inset:48px;border:.75px solid rgba(201,162,74,.55)"></div>
<div style="{LABEL};top:96px;font-size:24px">New show · No. {nr}</div>
<div class="cv" style="top:160px"><img src="{cover_uri}" width="820" height="820" alt=""></div>
<div style="{HEAD};top:1040px;font-size:56px">Out now on <span class="g">Mixcloud.</span></div>
<div style="position:absolute;top:1130px;left:0;right:0;text-align:center;font-family:Jost,Futura,sans-serif;color:#c6bfa6;font-size:22px;letter-spacing:.18em;text-transform:uppercase">Link in bio · Every record has a story</div>""")


def story_html(show, cover_uri):
    nr = html.escape(show["number"])
    return page(1080, 1920, f"""
<div style="{LABEL};top:300px;font-size:28px">New show · No. {nr}</div>
<div class="cv" style="top:380px"><img src="{cover_uri}" width="900" height="900" alt=""></div>
<div style="{HEAD};top:1340px;font-size:64px">Listen on <span class="g">Mixcloud.</span></div>""")


def shoot(markup, w, h, out):
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "page.html"
        p.write_text(markup, encoding="utf-8")
        png = pathlib.Path(td) / "page.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        "--force-device-scale-factor=1", f"--window-size={w},{h}", "--virtual-time-budget=6000",
                        f"--screenshot={png}", p.as_uri()], check=True, capture_output=True)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", str(png), "--out", str(out)],
                       check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("show")
    ap.add_argument("--cover", help="färdigt omslag (helst 2048 px); annars renderas det med cover.py")
    ap.add_argument("--out-dir", default="social")
    a = ap.parse_args()
    show = json.loads(pathlib.Path(a.show).read_text(encoding="utf-8"))
    out_dir = pathlib.Path(a.out_dir)
    with tempfile.TemporaryDirectory() as td:
        cover = pathlib.Path(a.cover) if a.cover else pathlib.Path(td) / "cover.jpg"
        if not a.cover:
            render_cover(show, 2048, cover)
        uri = cover.resolve().as_uri()
        for kind, w, h, fn in (("instagram-post", 1080, 1350, post_html), ("instagram-story", 1080, 1920, story_html)):
            out = out_dir / f"{show['slug']}-{kind}.jpg"
            shoot(fn(show, uri), w, h, out)
            print(out)


if __name__ == "__main__":
    main()
