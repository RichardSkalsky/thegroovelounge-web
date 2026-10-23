#!/usr/bin/env python3
"""Bygger thegroovelounge.com som statiska sidor från content/ till out/.

    python3 build.py            # skarp version: bara godkända lappar (content/letters/)
    python3 build.py --demo     # med exempelshower (content/demo-shows/) och exempellappar (content/letters-demo/)

Bara standardbiblioteket. Designen följer riktning A (Velvet) i Claude Design,
canvasen "The Groove Lounge – riktningar", och designsystemet "The Groove Lounge".
"""
import argparse, datetime as dt, html, json, pathlib, re, shutil, urllib.parse
from email.utils import format_datetime

ROOT = pathlib.Path(__file__).resolve().parent
e = html.escape


def kern(h):
    """Bodoni Moda saknar kerning för W före gemen (Wa, We, Wo). Täpps till med .kw i site.css."""
    return re.sub(r"W(?=[a-zà-ÿ])", '<span class="kw">W</span>', h)


def md(s):
    """*kursiv* -> guldkursiv, resten escapas."""
    return kern(re.sub(r"\*(.+?)\*", r"<i>\1</i>", e(s or "")))


def is_out(show, now):
    """En show syns först när publish_at (UTC, t.ex. 2026-10-30T17:00:00Z) har passerat."""
    at = show.get("publish_at")
    return not at or dt.datetime.fromisoformat(at.replace("Z", "+00:00")) <= now


def load(demo=False):
    site = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
    dirs = ["content/shows"] + (["content/demo-shows"] if demo else [])     # exemplen bara i förhandsvisningen
    shows = [json.loads(p.read_text(encoding="utf-8")) for d in dirs for p in (ROOT / d).glob("*.json")]
    now = dt.datetime.now(dt.timezone.utc)
    shows = [s for s in shows if is_out(s, now)]
    shows.sort(key=lambda s: s["number"], reverse=True)
    return site, shows


def letters_for(show, demo):
    for d in (["letters"] + (["letters-demo"] if demo else [])):
        p = ROOT / "content" / d / f"{show['number']}.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return []


def nice_date(s):
    d = dt.date.fromisoformat(s)
    return f"{d.day} {d.strftime('%B %Y')}"


def page(site, title, body, desc=None, current=None, image=None, path="/"):
    desc = desc or site["description"]
    url = site["base_url"] + path
    img = site["base_url"] + (image or "/static/img/simone-leende.jpg")
    menu = "".join(f'<a href="{h}"{" aria-current=page" if current == k else ""}>{t}</a>'
                   for k, h, t in (("shows", "/shows/", "Shows"), ("about", "/about/", "About me"), ("letter", "/#letter", "Newsletter")))
    socials = " · ".join(f'<a href="{e(u)}" rel="me">{e(n)}</a>' if u else e(n) for n, u in site["socials"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="tgl-api" content="{e(site.get('api_base', ''))}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{e(img)}">
<meta property="og:url" content="{e(url)}">
<meta name="theme-color" content="#0b2a21">
<link rel="canonical" href="{e(url)}">
<link rel="alternate" type="application/rss+xml" title="The Groove Lounge" href="/feed.xml">
<link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/static/fonts/BodoniModa-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/static/fonts/fonts.css">
<link rel="stylesheet" href="/static/site.css">
</head>
<body>
<header class="nav"><div class="wrap">
<a class="brand" href="/"><span class="puck" aria-hidden="true"></span>The Groove Lounge</a>
<nav class="menu" aria-label="Main">{menu}</nav>
<a class="btn" href="https://www.mixcloud.com/{e(site['mixcloud_user'])}/">Listen on Mixcloud</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<main>
{body}
</main>
<footer class="site"><div class="wrap">
<div style="display:flex;flex-direction:column;gap:14px"><div class="label">The Groove Lounge</div>
<div class="display" style="font-size:30px">Every record has a <i>story.</i></div>
<div class="muted" style="font-size:14px">Peckham, South London · <a href="mailto:{e(site['email'])}">{e(site['email'])}</a></div></div>
<div class="links"><div>{socials}</div><div><a href="/privacy/">Privacy policy</a> · <a href="/feed.xml">RSS</a></div></div>
</div></footer>
<script src="/static/site.js" defer></script>
</body>
</html>
"""


def player(site, show):
    if show.get("mixcloud_key"):
        feed = urllib.parse.quote(f"/{site['mixcloud_user']}/{show['mixcloud_key']}/", safe="")
        return (f'<div class="player"><iframe title="Play {e(show["title"])} on Mixcloud" loading="lazy" allow="autoplay" '
                f'src="https://player-widget.mixcloud.com/widget/iframe/?hide_cover=1&amp;feed={feed}"></iframe></div>')
    return f'<div class="player soon">Coming to Mixcloud on {nice_date(show["date"])}.</div>'


def stars(show_number, label):
    btns = "".join(f'<button type="button" aria-label="{i} star{"s" if i > 1 else ""}">★</button>' for i in range(1, 6))
    return f'<div class="stars" role="group" aria-label="{e(label)}" data-show="{e(show_number)}">{btns}</div>'


def cover_img(show, eager=False):
    return (f'<img class="cover" src="/static/covers/{e(show["slug"])}.jpg" width="1200" height="1200" '
            f'alt="Cover of The Groove Lounge No. {e(show["number"])}: {e(show["title"])}"{"" if eager else " loading=lazy"}>')


def card(show):
    return f"""<a class="card" href="/shows/{e(show['slug'])}/" data-tags="{e(' '.join(show.get('tags', [])))}">
{cover_img(show)}
<div class="row"><span class="label" style="font-size:12px">No. {e(show['number'])}</span><span class="muted" style="font-size:13px">{dt.date.fromisoformat(show['date']).strftime('%b %Y')}</span></div>
<h3>{kern(e(show['title']))}</h3><div class="muted" style="font-size:14px">{e(show['subtitle'])}</div></a>"""


def signup(site):
    action = site.get("newsletter_action") or ""
    return f"""<section class="section deep" id="letter"><div class="wrap letter-signup">
<div class="label">The weekly letter</div>
<h2 class="display" style="font-size:clamp(34px,4.5vw,52px)">One letter, <i>when a new show is out.</i></h2>
<p class="muted" style="max-width:560px;margin:0;font-size:18px">A few lines from me about the records, and a link to listen. No noise, unsubscribe any time.</p>
<form class="signup"{f' action="{e(action)}" method="post"' if action else ''}>
<label class="hp">Leave empty <input name="website" tabindex="-1" autocomplete="off"></label>
<input type="email" name="email" required placeholder="Your email address" aria-label="Your email address">
<button class="btn solid" type="submit">Subscribe</button></form>
<div class="status" role="status"></div></div></section>"""


def engraved_puck(size="min(420px,70vw)"):
    """Den graverade guldpucken (designsystemet, komponenten Puck): THE GROOVE LOUNGE upptill, sloganen nertill."""
    C = 150
    def arc(r, top):
        return f"M {C-r},{C} a {r},{r} 0 {'1,1' if top else '0,0'} {2*r},0"
    def tp(pid, path, text, fs, ls):
        return (f'<path id="{pid}" d="{path}" fill="none"/>'
                f'<text font-family="Jost, Futura, sans-serif" font-size="{fs}" font-weight="600" letter-spacing="{ls}">'
                f'<textPath href="#{pid}" startOffset="50%" text-anchor="middle">{text}</textPath></text>')
    inner = tp("pk-top", arc(118, True), "THE GROOVE LOUNGE", 15, 5.5) + tp("pk-bot", arc(130, False), "EVERY RECORD HAS A STORY", 10, 3.6)
    g = f'<defs><g id="pk-txt">{inner}</g></defs>'
    layers = ('<use href="#pk-txt" fill="rgba(255,244,210,.55)" transform="translate(0,.8)"/>'
              '<use href="#pk-txt" fill="rgba(36,24,4,.75)" transform="translate(0,-.56)"/>'
              '<use href="#pk-txt" fill="#7a5c1c"/>')
    return (f'<div role="img" aria-label="The Groove Lounge gold puck, engraved: Every record has a story" style="position:relative;width:{size};aspect-ratio:1;border-radius:50%;'
            'background:conic-gradient(from 30deg,#7a5c1c,#f1dfa6 10%,#a8822f 22%,#6b4f16 38%,#c9a24a 52%,#f4e3b0 60%,#9c7a2c 72%,#6b4f16 86%,#7a5c1c);'
            'box-shadow:inset 0 0 0 2px rgba(255,240,200,.35),inset 0 0 0 12px rgba(0,0,0,.12),0 24px 50px rgba(0,0,0,.45)">'
            f'<svg viewBox="0 0 300 300" style="position:absolute;inset:0;width:100%;height:100%" aria-hidden="true">{g}{layers}'
            '<circle cx="150" cy="150" r="16" fill="#0b2a21"/></svg></div>')


def home_prelaunch(site):
    q = site["home_quote"]
    body = f"""<section class="section glow"><div class="wrap hero">
<div style="display:flex;justify-content:center">{engraved_puck()}</div>
<div class="meta">
<div class="label">The Groove Lounge · with Simone</div>
<h1 class="display">Every record has a <i>story.</i></h1>
<p class="lead" style="margin:0">My first show is on its way. Soul, funk, disco and R&amp;B, and the stories behind the records, every week on Mixcloud.</p>
<p class="muted" style="margin:0;font-size:18px">Leave your email below and I’ll write to you the day it’s out.</p>
<div class="btns"><a class="btn solid" href="#letter">Tell me when it’s out</a><a class="btn" href="/about/">Read my story</a></div>
</div></div></section>
<section class="section deep"><div class="wrap quote">
<div class="mark" aria-hidden="true">“</div>
<blockquote class="display">{md(q['text'])}</blockquote>
<div class="sig" style="font-size:56px">Simone</div>
<div class="caps" style="font-size:13px">{e(q['source'])}</div></div></section>
<section class="section glow"><div class="wrap split">
<div class="framed"><img src="/static/img/simone-skratt.jpg" alt="Simone laughing in front of her record shelves" loading="lazy"></div>
<div class="prose"><div class="label">Your host</div>
<h2 class="display" style="font-size:clamp(40px,5vw,60px)">Hello, I’m <i>Simone.</i></h2>
<p>A South London broadcaster, digger and soul obsessive with two decades in record shops and late-night listening rooms. I grew up in Brixton with a mother who played Marvin Gaye on Sundays and explained every record like it was a story worth carrying.</p>
<div><a class="btn" href="/about/">Read my story</a></div></div></div></section>
{signup(site)}"""
    return page(site, "The Groove Lounge · Every record has a story", body, path="/")


def archive_empty(site):
    body = """<section class="glow"><div class="center-page"><span class="puck" aria-hidden="true"></span><div class="label">The archive</div>
<h1 class="display" style="font-size:clamp(44px,6vw,64px)">The first show is <i>on its way.</i></h1>
<p class="muted" style="margin:0;font-size:18px;max-width:560px">Every show will live here, newest first. Until then, leave your email and I’ll tell you when it’s out.</p>
<a class="btn solid" href="/#letter">Tell me when it’s out</a></div></section>"""
    return page(site, "All shows · The Groove Lounge", body, current="shows", path="/shows/")


def home(site, shows):
    s = shows[0]
    # Startsidans citat: Simones val från den senaste showen (home_quote), annars showens citat, annars standard.
    hq = s.get("home_quote") or ({"text": s["quote"], "context": ""} if s.get("quote") else None)
    if hq:
        q = {"text": hq["text"], "source": hq.get("context", ""), "href": f"/shows/{s['slug']}/"}
    else:
        q = dict(site["home_quote"], href="")
    grid = "".join(card(x) for x in shows[:4])
    body = f"""<section class="section glow"><div class="wrap hero">
{cover_img(s, True)}
<div class="meta">
<div class="label">New show · No. {e(s['number'])}</div>
<h1 class="display">{md(title_md(s['title']))}</h1>
<div class="caps">{e(s['subtitle'])}</div>
<p class="lead" style="margin:0">“{e(s['teaser'])}”</p>
{player(site, s)}
<div class="btns"><a class="btn solid" href="/shows/{e(s['slug'])}/">Listen &amp; leave a note</a><a class="btn" href="/shows/">All shows</a></div>
</div></div></section>
<section class="section deep"><div class="wrap quote">
<div class="mark" aria-hidden="true">“</div>
<blockquote class="display">{md(q['text'])}</blockquote>
<div class="sig" style="font-size:56px">Simone</div>
<div class="caps" style="font-size:13px">{f'<a href="{e(q["href"])}">{e(q["source"])}</a>' if q.get("href") else e(q["source"])}</div></div></section>
<section class="section"><div class="wrap" style="display:flex;flex-direction:column;gap:44px">
<div class="head-row"><div style="display:flex;flex-direction:column;gap:12px"><div class="label">The archive</div><h2 class="display" style="font-size:clamp(36px,4.5vw,52px)">All <i>shows</i></h2></div><a class="btn" href="/shows/">See all shows</a></div>
<div class="grid">{grid}</div></div></section>
<section class="section glow"><div class="wrap split">
<div class="framed"><img src="/static/img/simone-skratt.jpg" alt="Simone laughing in front of her record shelves" loading="lazy"></div>
<div class="prose"><div class="label">Your host</div>
<h2 class="display" style="font-size:clamp(40px,5vw,60px)">Hello, I’m <i>Simone.</i></h2>
<p>A South London broadcaster, digger and soul obsessive with two decades in record shops and late-night listening rooms. I grew up in Brixton with a mother who played Marvin Gaye on Sundays and explained every record like it was a story worth carrying.</p>
<div><a class="btn" href="/about/">Read my story</a></div></div></div></section>
{signup(site)}"""
    return page(site, "The Groove Lounge · Every record has a story", body, path="/")


def title_md(t):
    w = t.split()
    return t if len(w) < 2 else " ".join(w[:-1]) + f" *{w[-1]}*"


def show_page(site, shows, i, demo):
    s = shows[i]
    prev = shows[i + 1] if i + 1 < len(shows) else None
    nxt = shows[i - 1] if i > 0 else None
    def fmt(sec):
        sec = int(sec or 0)
        return f"{sec // 60}:{sec % 60:02d}"

    def row(x):
        # Nytt format: {"type": "track"|"chapter", "start": sek, "artist", "title", "year"}; gammalt: [artist, titel, år]
        if isinstance(x, dict):
            st = f'<span class=y data-start="{int(x.get("start") or 0)}">{fmt(x.get("start"))}</span>' if x.get("start") is not None else '<span class=y></span>'
            if x.get("type") == "chapter":
                return f'<li class="chapter"><span class="gold">Simone</span><i>{e(x.get("title", ""))}</i>{st}</li>'
            return f'<li><span>{e(x.get("artist", ""))}</span><i>{e(x.get("title", ""))}</i>{st}</li>'
        a, t, y = (list(x) + ["", "", ""])[:3]
        return f"<li><span>{e(a)}</span><i>{e(t)}</i><span class=y>{e(y)}</span></li>"
    tl = "".join(row(x) for x in s.get("tracklist", []))
    tracks = f"""<div style="display:flex;flex-direction:column;gap:22px"><div class="label">Tracklist</div><ol class="tracks">{tl}</ol>
<div class="muted" style="font-size:14px">Full tracklist on Mixcloud.</div></div>""" if tl else ""
    quote = f"""<div style="display:flex;flex-direction:column;gap:22px"><div class="label">From the show</div>
<div class="display" style="font-size:clamp(30px,3.4vw,40px);line-height:1.25">“{md(s['quote'])}”</div>
<div class="sig" style="font-size:48px;align-self:flex-start">Simone</div></div>""" if s.get("quote") else ""
    mid = f'<section class="section"><div class="wrap two">{tracks}{quote}</div></section>' if (tracks or quote) else ""
    ls = letters_for(s, demo)
    letters = ("<div style='display:flex;flex-direction:column;gap:22px;margin-top:18px'><div class=label>Letters I’ve chosen</div><div class=letters>"
               + "".join(f'<figure class="letter" style="margin:0"><p>“{e(l["text"])}”</p><figcaption class="caps" style="font-size:13px">{e(l["name"])}, {e(l["town"])}</figcaption></figure>' for l in ls)
               + "</div></div>") if ls else ("<div style='display:flex;flex-direction:column;gap:14px;margin-top:18px'><div class=label>Letters I’ve chosen</div>"
               "<div class=letter><p>No letters yet. <span class=gold>Be the first.</span></p><span class='caps' style='font-size:13px'>Write to me below, and I may share yours here.</span></div></div>")
    # Showens fråga är valfri (pausad 2026-10-22). Utan fråga: en allmän uppmaning att skriva.
    if s.get("question"):
        ask_label, ask_title = "This week I’m asking", s["question"]
        ask_text = "Every show ends with a question. Leave me a note: a memory, a record I should play, or something I got wrong. I read every one. Some I share here, and some end up in a future show."
        placeholder = "The record, the memory, the question…"
    else:
        ask_label, ask_title = "Your turn", "Which record should I play *next?*"
        ask_text = "Tell me what you thought of the show, ask for a record, or share a memory it brought back. I read every note. Some I share here, and some find their way into a future show."
        placeholder = "The record, the memory, your thoughts…"
    pn = ""
    if prev:
        pn += f'<a class="prevnext" href="/shows/{e(prev["slug"])}/"><img src="/static/covers/{e(prev["slug"])}.jpg" alt="" loading="lazy"><div><div class="label" style="font-size:12px">← Previous · No. {e(prev["number"])}</div><div class="display" style="font-size:26px">{e(prev["title"])}</div></div></a>'
    if nxt:
        pn += f'<a class="prevnext" href="/shows/{e(nxt["slug"])}/"><div style="text-align:right"><div class="label" style="font-size:12px">Next · No. {e(nxt["number"])} →</div><div class="display" style="font-size:26px">{e(nxt["title"])}</div></div><img src="/static/covers/{e(nxt["slug"])}.jpg" alt="" loading="lazy"></a>'
    mixcloud = f"https://www.mixcloud.com/{site['mixcloud_user']}/{s['mixcloud_key']}/" if s.get("mixcloud_key") else f"https://www.mixcloud.com/{site['mixcloud_user']}/"
    body = f"""<section class="section glow"><div class="wrap hero" style="align-items:flex-start">
{cover_img(s, True)}
<div class="meta">
<div class="crumbs"><a href="/shows/">Shows</a> / No. {e(s['number'])}</div>
<div class="label">Show No. {e(s['number'])} · {nice_date(s['date'])}</div>
<h1 class="display">{md(title_md(s['title']))}</h1>
<div class="caps">{e(s['subtitle'])}{' · ' + e(s['duration']) if s.get('duration') else ''}</div>
{player(site, s)}
<div class="rate"><span class="caps" style="color:var(--ivory);font-size:13px">Rate this show</span>{stars(s['number'], 'Rate this show')}<span class="thanks muted">Your rating comes straight to me.</span></div>
<p class="muted" style="margin:0;font-size:18px;line-height:1.75;max-width:640px">{e(s['teaser'])} {e(s.get('description', ''))}</p>
<div class="btns"><a class="btn solid" href="{e(mixcloud)}">Open on Mixcloud</a><a class="btn" href="#note">Leave me a note</a></div>
</div></div></section>
{mid}
<section style="border-top:1px solid var(--hairline)"><div class="wrap band" style="padding-block:40px;border-top:0">{pn}<a class="caps" href="/shows/" style="color:var(--gold-500)">All shows</a></div></section>
<section class="section deep" id="note"><div class="wrap two">
<div class="prose"><div class="label">{ask_label}</div>
<h2 class="display" style="font-size:clamp(36px,4vw,50px)">{md(ask_title)}</h2>
<p>{ask_text}</p>
{letters}</div>
<form class="panel note" data-show="{e(s['number'])}" novalidate>
<h3>Leave me <i class="gold">a note</i></h3>
<div class="field"><span>How was the show?</span>{stars(s['number'], 'Your rating')}</div>
<div class="pair"><label class="field"><span>First name</span><input name="name" autocomplete="given-name" maxlength="60"></label>
<label class="field"><span>Where are you listening from?</span><input name="town" maxlength="80"></label></div>
<label class="field"><span>Your note</span><textarea name="text" required maxlength="3000" placeholder="{placeholder}"></textarea></label>
<label class="field"><span>Email (optional, only if you want a reply)</span><input type="email" name="email" autocomplete="email" maxlength="200"></label>
<label class="hp">Leave empty <input name="website" tabindex="-1" autocomplete="off"></label>
<label class="check"><input type="checkbox" name="consent"> You may quote my note and first name on this page or in a show.</label>
<div class="btns" style="justify-content:space-between;align-items:center"><button class="btn solid" type="submit">Send your note</button><span class="muted" style="font-size:13px">No account needed. <a href="/privacy/" style="text-decoration:underline">Privacy</a></span></div>
<div class="status" role="status"></div>
</form></div></section>
<section class="glow"><div class="wrap band" style="padding-block:56px">
<div><div class="display" style="font-size:30px">On Mixcloud? <i>Say it there too.</i></div><div class="muted" style="font-size:16px">Comments and reposts on Mixcloud help the show find new listeners. I read those too.</div></div>
<a class="btn" href="{e(mixcloud)}">Comment on Mixcloud</a></div></section>
{signup(site)}"""
    return page(site, f"{s['title']} · The Groove Lounge No. {s['number']}", body, desc=s["teaser"], current="shows",
                image=f"/static/covers/{s['slug']}.jpg", path=f"/shows/{s['slug']}/")


def archive(site, shows):
    tags = []
    for s in shows:
        for t in s.get("tags", []):
            if t not in tags:
                tags.append(t)
    names = {"uk": "UK", "rnb": "R&B", "70s": "70s", "80s": "80s", "90s": "90s"}
    chips = '<button type="button" data-tag="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-tag="{e(t)}" aria-pressed="false">{e(names.get(t, t.title()))}</button>' for t in tags)
    body = f"""<section class="glow" style="padding-block:80px 56px"><div class="wrap" style="display:flex;flex-direction:column;gap:18px">
<div class="label">The archive</div><h1 class="display" style="font-size:clamp(48px,6vw,72px)">All <i>shows</i></h1>
<p class="muted" style="margin:0;max-width:640px;font-size:18px">Every show since No. 001, newest first. A new one every week.</p>
<div class="chips" style="margin-top:12px">{chips}</div></div></section>
<section style="padding-block:40px 96px"><div class="wrap"><div class="grid">{''.join(card(s) for s in shows)}</div></div></section>"""
    return page(site, "All shows · The Groove Lounge", body, current="shows", path="/shows/")


def about(site):
    chapters = [("1981", "Brixton", "My mother played Marvin Gaye on Sundays and explained every record like it was a story worth carrying. My father left his collection behind. His shelves sat next to hers."),
                ("Four summers", "Savannah, Georgia", "Church on Sundays, then Stax and Muscle Shoals on 45s in Auntie Paulette’s garage. I never stopped listening the same way."),
                ("Pirate radio", "Peckham", "I started by making tea at a pirate station in a Peckham tower block and ended up with Sunday midnight to three. Four listeners, maybe. Worth it."),
                ("Northern soul", "Manchester", "Northern soul nights up north changed how I hear a record. Some songs only make sense at four in the morning.")]
    ch = "".join(f'<div><span class="label" style="font-size:12px">{e(a)}</span><h3>{e(b)}</h3><p>{e(c)}</p></div>' for a, b, c in chapters)
    body = f"""<section class="section glow"><div class="wrap split">
<div class="framed"><img src="/static/img/simone-leende.jpg" alt="Simone smiling in front of her record shelves"></div>
<div class="prose"><div class="label">About me</div>
<h1 class="display" style="font-size:clamp(48px,6vw,76px)">Two shelves.<br><i>One education.</i></h1>
<p>I’m Simone, a South London broadcaster, digger and soul obsessive with two decades in record shops and late-night listening rooms.</p>
<p>I grew up in Brixton with a mother who played Marvin Gaye on Sundays and explained every record like it was a story worth carrying. My father left his collection behind — his shelves sat next to hers. Two collections, two lives, one education.</p>
<p>Four summers from fourteen were spent at my Auntie Paulette’s in Savannah, Georgia — church on Sundays, then Stax and Muscle Shoals on 45s in her garage after. I never stopped listening the same way.</p>
<p>I cut my teeth on pirate radio and late-night sets across London and Manchester, learning the music from every angle without losing the reason I started.</p>
<div class="sig" style="font-size:56px;align-self:flex-start">Simone</div></div></div></section>
<section class="section"><div class="wrap" style="display:flex;flex-direction:column;gap:44px"><div class="label">Where it comes from</div><div class="chapters">{ch}</div></div></section>
<section class="section deep"><div class="wrap quote"><div class="label">The show</div>
<p class="display" style="font-size:clamp(30px,4vw,54px);line-height:1.15;max-width:1000px;margin:0">A home for soul, funk, disco and R&amp;B from when the music was made to last, where the story behind a track matters <i>as much as the groove itself.</i></p>
<div class="btns" style="justify-content:center"><a class="btn solid" href="https://www.mixcloud.com/{e(site['mixcloud_user'])}/">Listen on Mixcloud</a><a class="btn" href="mailto:{e(site['email'])}">Write to me</a></div></div></section>
<section class="section glow"><div class="wrap split" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)">
<div class="prose"><div class="label">Write to me</div><h2 class="display" style="font-size:clamp(36px,4vw,48px)">Requests, stories, a record <i>I should play?</i></h2>
<p>I read every one. <a href="mailto:{e(site['email'])}" class="gold">{e(site['email'])}</a></p></div>
<img src="/static/img/simone-skratt.jpg" alt="" loading="lazy" style="width:100%;aspect-ratio:16/10;object-fit:cover;object-position:50% 35%;border:1.5px solid var(--gold-500)"></div></section>"""
    return page(site, "About Simone · The Groove Lounge", body, current="about", path="/about/")


def thanks(site):
    body = f"""<section class="glow"><div class="center-page"><span class="puck" aria-hidden="true"></span><div class="label">The weekly letter</div>
<h1 class="display" style="font-size:clamp(48px,6vw,72px)">You’re <i>in.</i></h1>
<p class="muted" style="max-width:620px;margin:0;font-size:20px;line-height:1.7">Thank you. Check your inbox and confirm your address, and my next letter will find you when the new show is out.</p>
<div class="sig" style="font-size:60px">Simone</div><a class="btn" href="/">Listen to my latest show</a></div></section>"""
    return page(site, "You’re in · The Groove Lounge", body, path="/newsletter/thanks/")


def privacy(site):
    em = e(site["email"])
    secs = [
        ("Who we are", f"<p>The Groove Lounge is a music radio show about soul, funk, disco and R&amp;B, published on Mixcloud. It is a private, non-commercial project. Richard Skalsky is responsible for your data. Contact: <a href=\"mailto:richard@thegroovelounge.com\">richard@thegroovelounge.com</a>.</p>"),
        ("This website", "<ul><li>We do not use cookies, analytics, advertising or tracking of any kind.</li><li>The website is hosted on GitHub Pages. GitHub may log technical information such as IP addresses for security and operation. See the <a href=\"https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement\">GitHub Privacy Statement</a>.</li><li>All fonts are served from this website. No requests are made to Google or other font services.</li><li>Shows are played through Mixcloud’s player. When you play a show, Mixcloud’s own <a href=\"https://www.mixcloud.com/privacy/\">privacy policy</a> applies.</li></ul>"),
        ("Ratings and notes", "<p>When you rate a show or leave a note for Simone, we store your rating, your note, the first name and town you give us, and your email address only if you add it. The data is stored with our provider Scaleway in Paris, France, within the EU. We use it to read your note, to reply if you asked us to, and to remember feedback for future shows. We quote your note and first name on the website or in a show only if you ticked the box. Notes are deleted after two years, or earlier if you ask.</p>"),
        ("The weekly letter", "<p>If you sign up, we use your email address only to send the letter when a new show is out. You confirm your address before anything is sent, and every letter has a one-click unsubscribe link.</p>"),
        ("When you write to us", f"<p>If you email <a href=\"mailto:{em}\">{em}</a>, we use your email address and message only to read and reply to you, and to remember song requests or feedback for future shows. We never sell or share your information with anyone.</p>"),
        ("Google user data", "<p>The Groove Lounge uses an application that connects to Google Drive. It is used only with the show’s own Google account, to store and retrieve audio files, show material and backups.</p><ul><li>The application does not access, collect or store data from any other Google user.</li><li>Data from Google Drive is used only to produce and archive The Groove Lounge. It is not shared with third parties, not used for advertising and not used to train AI models.</li><li>The use of information received from Google APIs adheres to the <a href=\"https://developers.google.com/terms/api-services-user-data-policy\">Google API Services User Data Policy</a>, including the Limited Use requirements.</li></ul>"),
        ("Your rights", f"<p>Under the EU General Data Protection Regulation (GDPR) you can ask to see, correct or delete the personal data we hold about you. Write to <a href=\"mailto:richard@thegroovelounge.com\">richard@thegroovelounge.com</a> and we will respond within 30 days. You may also contact the Swedish Authority for Privacy Protection (IMY).</p>"),
        ("Changes", "<p>If this policy changes, the new version will be published on this page with a new date.</p>")]
    body = f"""<section class="section"><div class="wrap doc">
<div style="display:flex;flex-direction:column;gap:16px"><div class="label">Privacy</div><h1 class="display" style="font-size:clamp(44px,5vw,60px)">Your data, <i>kept small.</i></h1><div class="muted" style="font-size:14px">Last updated: {dt.date.today().day} {dt.date.today().strftime('%B %Y')}</div></div>
<div>{''.join(f'<section><h2>{h}</h2>{t}</section>' for h, t in secs)}</div></div></section>"""
    return page(site, "Privacy policy · The Groove Lounge", body, path="/privacy/")


def notfound(site):
    body = """<section class="glow"><div class="center-page"><span class="puck" aria-hidden="true"></span>
<h1 class="display" style="font-size:clamp(44px,6vw,64px)">This groove <i>skipped.</i></h1>
<p class="muted" style="margin:0;font-size:18px">The page you were looking for isn’t here.</p><a class="btn" href="/">Back to the lounge</a></div></section>"""
    return page(site, "Not found · The Groove Lounge", body, path="/404.html")


def feed(site, shows):
    items = ""
    for s in shows:
        d = dt.datetime.fromisoformat(s["date"] + "T18:00:00+00:00")
        url = f"{site['base_url']}/shows/{s['slug']}/"
        items += f"""<item><title>{e(s['title'])} · No. {e(s['number'])}</title><link>{url}</link><guid>{url}</guid>
<pubDate>{format_datetime(d)}</pubDate><description>{e(s['teaser'])} {e(s.get('description', ''))}</description>
<enclosure url="{site['base_url']}/static/covers/{e(s['slug'])}.jpg" type="image/jpeg" length="0"/></item>\n"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>The Groove Lounge</title><link>{site['base_url']}/</link>
<description>{e(site['description'])}</description><language>en-gb</language>
{items}</channel></rss>
"""


def favicon():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#c9a24a"/><circle cx="32" cy="32" r="3.5" fill="#0b2a21"/></svg>"""


def build(demo, out):
    site, shows = load(demo)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT / "static", out / "static")
    w = lambda rel, text: ((out / rel).parent.mkdir(parents=True, exist_ok=True), (out / rel).write_text(text, encoding="utf-8"))
    w("static/img/favicon.svg", favicon())
    w("index.html", home(site, shows) if shows else home_prelaunch(site))
    w("shows/index.html", archive(site, shows) if shows else archive_empty(site))
    for i, s in enumerate(shows):
        w(f"shows/{s['slug']}/index.html", show_page(site, shows, i, demo))
    w("about/index.html", about(site))
    w("newsletter/thanks/index.html", thanks(site))
    w("privacy/index.html", privacy(site))
    w("privacy.html", privacy(site))      # adressen som står i Google-appens samtyckesskärm
    w("404.html", notfound(site))
    w("feed.xml", feed(site, shows))
    w("CNAME", site["domain"] + "\n")
    w(".nojekyll", "")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "out"))
    a = ap.parse_args()
    print(build(a.demo, pathlib.Path(a.out)))
