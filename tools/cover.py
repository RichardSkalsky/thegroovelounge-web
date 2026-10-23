#!/usr/bin/env python3
"""Renderar showomslag (The Groove Lounge, mall B1 Klassisk) till JPG med headless Chrome.

Användning:
    python3 tools/cover.py content/shows/004-the-crossing.json            # -> static/covers/the-crossing.jpg (1200 px)
    python3 tools/cover.py content/shows/004-the-crossing.json --size 2048 --out /tmp/x.jpg

Mallen är en exakt kopia av komponenten BCover i Claude Design (canvasen
"The Groove Lounge – riktningar") och AlbumCover i designsystemet. Ändra där först.
"""
import argparse, html, json, os, pathlib, re, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def kern(h):
    """Bodoni Moda saknar kerning för W före gemen utan uppstapel (Wa, We, Wo, men inte Wh, Wi). Samma rättning som kern() i build.py."""
    return re.sub(r"W(?=[acegmnopqrsuvwxyzåäöéèêëóòôüú])", '<span class="kw">W</span>', h)


def artist_line(artists):
    """Raden bryts bara efter en punkt: hårda mellanslag inne i namnen och före varje ·."""
    return html.escape("\u00a0· ".join(a.replace(" ", "\u00a0") for a in artists))


def title_size(title):
    n = len(title)
    return 72 if n <= 10 else 60 if n <= 14 else 52 if n <= 18 else 46 if n <= 24 else 40 if n <= 32 else 34


def cover_html(show, image_uri):
    words = show["title"].split()
    last = words.pop() if len(words) > 1 else ""
    e = html.escape
    mask = ("linear-gradient(to right, transparent 0, #000 20%, #000 80%, transparent 100%), "
            "linear-gradient(to bottom, transparent 0, #000 20%, #000 80%, transparent 100%)")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..800;1,6..96,400..700&family=Jost:wght@400;500;600&family=Pinyon+Script&display=swap">
<style>
html,body{{margin:0;background:#0b2a21}}body{{padding:20px}}
.c{{width:600px;height:600px;position:relative;overflow:hidden;font-family:Jost,Futura,sans-serif;background:radial-gradient(60% 60% at 50% 40%,#155240,#0b2a21 75%)}}
.fo{{position:absolute;inset:22px;border:1.5px solid #c9a24a}}
.fi{{position:absolute;inset:30px;border:.75px solid rgba(201,162,74,.6)}}
.wm{{position:absolute;top:56px;left:0;right:0;text-align:center;font-size:15px;font-weight:500;letter-spacing:.4em;text-transform:uppercase;color:#c9a24a}}
.img{{position:absolute;left:34px;top:78px;width:532px;height:240px;object-fit:cover;-webkit-mask-image:{mask};-webkit-mask-composite:source-in;mask-image:{mask};mask-composite:intersect}}
.tb{{position:absolute;top:330px;bottom:100px;left:48px;right:48px;display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center}}
.t{{font-family:'Bodoni Moda',Didot,Georgia,serif;font-size:{title_size(show["title"])}px;font-weight:600;font-variation-settings:'opsz' 28;line-height:1.02;letter-spacing:-.01em;text-wrap:balance;color:#f3ecdc}}
.t i{{color:#c9a24a}}
.kw{{letter-spacing:-.1em}}
.a{{max-width:440px;font-size:13px;font-weight:500;letter-spacing:.18em;line-height:1.7;text-transform:uppercase;text-wrap:balance;color:#c6bfa6}}
.s{{position:absolute;bottom:44px;left:0;right:0;text-align:center;font-family:'Pinyon Script',cursive;font-size:40px;line-height:1;color:#c9a24a;transform:rotate(-3deg)}}
.n{{position:absolute;bottom:50px;right:48px;font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:#c6bfa6}}
</style></head><body><div class="c">
<div class="fo"></div><div class="fi"></div><div class="wm">The Groove Lounge</div>
<img class="img" src="{image_uri}" alt="">
<div class="tb"><div class="t">{kern(e(" ".join(words)))} <i>{kern(e(last))}</i></div><div class="a">{artist_line(show["artists"])}</div></div>
<div class="s">with Simone</div><div class="n">No. {e(show["number"])}</div>
</div></body></html>"""


def render(show, size, out):
    img = (ROOT.parent.parent / "grafik" / "showbilder" / f"{show['slug']}.jpg").resolve()
    if show.get("showbild"):
        img = (ROOT / show["showbild"]).resolve()
    with tempfile.TemporaryDirectory() as td:
        page = pathlib.Path(td) / "cover.html"
        page.write_text(cover_html(show, img.as_uri()), encoding="utf-8")
        png = pathlib.Path(td) / "cover.png"
        scale = size / 600
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        f"--force-device-scale-factor={scale}", "--window-size=640,640", "--virtual-time-budget=6000",
                        f"--screenshot={png}", page.as_uri()], check=True, capture_output=True)
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["sips", "-c", str(size), str(size), str(png), "--out", str(png)], check=True, capture_output=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90", str(png), "--out", str(out)],
                       check=True, capture_output=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("show", nargs="+")
    ap.add_argument("--size", type=int, default=1200)
    ap.add_argument("--out")
    a = ap.parse_args()
    for p in a.show:
        show = json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
        out = pathlib.Path(a.out) if a.out else ROOT / "static" / "covers" / f"{show['slug']}.jpg"
        render(show, a.size, out)
        print(out)
