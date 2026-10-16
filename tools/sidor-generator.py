import sys
PAGE=sys.argv[1]; outp=sys.argv[2]; loc=len(sys.argv)>3
src=open('gen.py').read()
sys.argv=['gen.py','A','x']+(['1'] if loc else [])
exec(src[:src.index("pages={")])
def field(lbl,ph,h=52,w='100%'):
    return f'<div style="display:flex;flex-direction:column;gap:8px;width:{w}"><div style="{JOST};font-size:12px;letter-spacing:0.18em;text-transform:uppercase;color:{PAR}">{lbl}</div><div style="height:{h}px;border:1px solid rgba(201,162,74,0.5);display:flex;align-items:flex-start;padding:15px 16px;box-sizing:border-box;{JOST};font-size:15px;color:rgba(198,191,166,0.6)">{ph}</div></div>'
def stars(n=0,size=26,lit=GOLD,dim='rgba(201,162,74,0.35)'):
    return '<div style="display:flex;gap:6px">'+''.join(f'<div style="font-size:{size}px;line-height:1;color:{lit if i<n else dim}">★</div>' for i in range(5))+'</div>'
TRACKS=[('Delegation','Oh Honey','1977'),('Loose Ends','Hangin’ on a String','1985'),('Imagination','Body Talk','1981'),('Omar','There’s Nothing Like This','1990'),('Soul II Soul','Keep On Movin’','1989'),('Junior','Mama Used to Say','1982')]
LETTERS=[('“I played Hangin’ on a String at my wedding in 1986. Hearing you tell where it came from made me cry in the kitchen.”','Maureen, Croydon'),('“Never knew Delegation were from Birmingham. Thirty years of dancing to them and I never knew.”','Tunde, Manchester')]
def show_page():
    hero=f'''<div style="padding:72px 72px 80px;display:flex;gap:72px;align-items:flex-start;background:{BGV}">
{cover(L,500)}
<div style="display:flex;flex-direction:column;gap:20px;flex:1;min-width:0">
<div style="{JOST};font-size:13px;letter-spacing:0.18em;text-transform:uppercase;color:{PAR}">Shows / No. {L[2]}</div>
{label("Show No. "+L[2]+" · 16 October 2026")}
<div style="{BOD};font-size:72px;line-height:1.02;color:{IV}">The <i style="color:{GOLD}">Crossing</i></div>
<div style="{JOST};font-size:15px;letter-spacing:0.18em;text-transform:uppercase;color:{PAR}">{L[5]} · 58 min</div>
{player()}
<div style="display:flex;align-items:center;gap:18px;padding:14px 0;border-top:1px solid rgba(201,162,74,0.25);border-bottom:1px solid rgba(201,162,74,0.25)"><div style="{JOST};font-size:13px;letter-spacing:0.18em;text-transform:uppercase;color:{IV}">Rate this show</div>{stars(0,28)}<div style="{JOST};font-size:14px;color:{PAR}">Your rating goes straight to Simone.</div></div>
<div style="{JOST};font-size:18px;line-height:1.75;color:{PAR};max-width:640px">How a sound crossed the Atlantic, found a home in London and came back changed. From Philadelphia and Detroit to the clubs of Soho and the bedrooms of Brixton, where a new kind of British soul was pressed in small runs and played until the grooves gave out.</div>
<div style="display:flex;gap:16px">{btn("Open on Mixcloud")}{btn("Share",False)}</div></div></div>'''
    rows=''.join(f'<div style="display:grid;grid-template-columns:40px 1fr 1fr 70px;gap:20px;padding:16px 0;border-bottom:1px solid rgba(201,162,74,0.18);{JOST};font-size:17px;color:{IV}"><div style="color:{GOLD};font-size:13px;letter-spacing:.2em">{i+1:02d}</div><div>{a}</div><div style="{BOD};font-weight:400;font-style:italic;font-size:19px">{t}</div><div style="color:{PAR};text-align:right">{y}</div></div>' for i,(a,t,y) in enumerate(TRACKS))
    tl=f'''<div style="background:{V8};padding:88px 72px;display:grid;grid-template-columns:1.1fr 0.9fr;gap:80px">
<div style="display:flex;flex-direction:column;gap:22px">{label("Tracklist")}<div style="border-top:1px solid rgba(201,162,74,0.35)">{rows}</div><div style="{JOST};font-size:14px;color:{PAR}">Full tracklist on Mixcloud.</div></div>
<div style="display:flex;flex-direction:column;gap:22px">{label("From the show")}
<div style="{BOD};font-size:40px;line-height:1.25;color:{IV}">“A record can be pressed in Birmingham and still sound like <i style="color:{GOLD}">it was born in Philadelphia.</i>”</div>
<div style="{SIG};font-size:48px;color:{GOLD};transform:rotate(-3deg);transform-origin:left">Simone</div></div></div>'''
    dialog=f'''<div style="background:{V9};padding:96px 72px;display:grid;grid-template-columns:0.95fr 1.05fr;gap:80px">
<div style="display:flex;flex-direction:column;gap:22px">{label("Simone asks")}
<div style="{BOD};font-size:50px;line-height:1.12;color:{IV}">Which record carried <i style="color:{GOLD}">you</i> across a border?</div>
<div style="{JOST};font-size:18px;line-height:1.7;color:{PAR}">Every show ends with a question. Leave a note: a memory, a record we should play, or something I got wrong. I read every one. Some I share here, and some end up in a future show.</div>
<div style="display:flex;flex-direction:column;gap:22px;margin-top:18px">{label("Letters chosen by Simone")}
{''.join(f'<div style="border-left:2px solid {GOLD};padding:4px 0 4px 22px;display:flex;flex-direction:column;gap:8px"><div style="{BOD};font-weight:400;font-style:italic;font-size:22px;line-height:1.45;color:{IV}">{q}</div><div style="{JOST};font-size:13px;letter-spacing:0.18em;text-transform:uppercase;color:{PAR}">{w}</div></div>' for q,w in LETTERS)}</div></div>
<div style="background:{V8};border:1px solid rgba(201,162,74,0.35);padding:44px;display:flex;flex-direction:column;gap:20px">
<div style="{BOD};font-size:36px;color:{IV}">Leave a note <i style="color:{GOLD}">for Simone</i></div>
<div style="display:flex;flex-direction:column;gap:8px"><div style="{JOST};font-size:12px;letter-spacing:0.18em;text-transform:uppercase;color:{PAR}">How was the show?</div>{stars(4,34)}</div>
<div style="display:flex;gap:16px">{field("First name","Maureen")}{field("Where are you listening from?","Croydon")}</div>
{field("Your note","The record, the memory, the question…",170)}
{field("Email (optional, only if you want a reply)","you@example.com")}
<div style="display:flex;gap:12px;align-items:flex-start;{JOST};font-size:14px;line-height:1.5;color:{PAR}"><div style="width:18px;height:18px;border:1px solid {GOLD};flex:none;margin-top:2px"></div>Simone may quote my note and first name on this page or in a show.</div>
<div style="display:flex;justify-content:space-between;align-items:center">{btn("Send your note")}<div style="{JOST};font-size:13px;color:{PAR}">No account needed.</div></div></div></div>'''
    mix=f'''<div style="background:{BGV};padding:56px 72px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(201,162,74,0.25)">
<div style="display:flex;flex-direction:column;gap:8px"><div style="{BOD};font-size:30px;color:{IV}">On Mixcloud? <i style="color:{GOLD}">Say it there too.</i></div><div style="{JOST};font-size:16px;color:{PAR}">Comments and reposts on Mixcloud help the show reach new listeners.</div></div>
{btn("Comment on Mixcloud",False)}</div>'''
    nxt=f'''<div style="background:{V8};padding:64px 72px;display:flex;justify-content:space-between;align-items:center">
<div style="display:flex;gap:22px;align-items:center">{cover(SHOWS[1],110,False)}<div style="display:flex;flex-direction:column;gap:6px">{label("← Previous · No. 003")}<div style="{BOD};font-size:26px;color:{IV}">{SHOWS[1][0]}</div></div></div>
<div style="{JOST};font-size:15px;letter-spacing:0.18em;text-transform:uppercase;color:{GOLD}">All shows</div></div>'''
    body=f'<div style="width:1440px;background:{V8}">{nav(IV,GOLD,V8)}{hero}{tl}{dialog}{mix}{nxt}{newsletter(V9,IV,GOLD,V8)}{footer(V8,IV,GOLD)}</div>'
    m=f'''<div style="width:390px;background:{V8}"><div style="height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;border-bottom:1px solid rgba(201,162,74,0.25)"><div style="display:flex;align-items:center;gap:10px">{puck(24)}<div style="{WM};font-size:11px;color:{GOLD}">The Groove Lounge</div></div><div style="width:22px;display:flex;flex-direction:column;gap:5px"><div style="height:1.5px;background:{IV}"></div><div style="height:1.5px;background:{IV}"></div><div style="height:1.5px;background:{IV}"></div></div></div>
<div style="padding:24px 20px;display:flex;flex-direction:column;gap:16px">{cover(L,350)}{label("Show No. 004 · 16 Oct",GOLD,11)}<div style="{BOD};font-size:40px;color:{IV}">The <i style="color:{GOLD}">Crossing</i></div>{player()}<div style="display:flex;align-items:center;gap:12px"><div style="{JOST};font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:{IV}">Rate</div>{stars(0,24)}</div><div style="{JOST};font-size:15px;line-height:1.65;color:{PAR}">How a sound crossed the Atlantic, found a home in London and came back changed.</div></div>
<div style="background:{V9};padding:32px 20px;display:flex;flex-direction:column;gap:16px">{label("Simone asks",GOLD,11)}<div style="{BOD};font-size:30px;line-height:1.15;color:{IV}">Which record carried <i style="color:{GOLD}">you</i> across a border?</div>{field("Your note","The record, the memory…",120)}{field("First name","Maureen")}{btn("Send your note")}</div></div>'''
    return body,m,"Showsida","En sida per show. Spelaren, låtlistan och ett citat ur showen. Sedan dialogen: Betyg (1–5 stjärnor) direkt under spelaren och i formuläret, Simones fråga, ett formulär utan inloggning och brev som Simone väljer ut och Richard godkänner. Till sist en uppmaning att kommentera på Mixcloud, där det ger synlighet. Låtlistan och breven är exempel.",3700
def about_page():
    hero=f'''<div style="background:{BGV};padding:88px 72px;display:flex;gap:80px;align-items:center">
<div style="position:relative;width:560px;height:760px;flex:none"><div style="position:absolute;inset:0;background:url({img('leende')}) 50% 40%/cover"></div><div style="position:absolute;inset:-14px;border:1.5px solid {GOLD}"></div></div>
<div style="display:flex;flex-direction:column;gap:24px;max-width:620px">{label("About Simone")}
<div style="{BOD};font-size:76px;line-height:1.02;color:{IV}">Two shelves.<br><i style="color:{GOLD}">One education.</i></div>
<div style="{JOST};font-size:18px;line-height:1.75;color:{PAR}">I’m Simone, a South London broadcaster, digger and soul obsessive with two decades in record shops and late-night listening rooms.</div><div style="{JOST};font-size:18px;line-height:1.75;color:{PAR}">I grew up in Brixton with a mother who played Marvin Gaye on Sundays and explained every record like it was a story worth carrying. My father left his collection behind — his shelves sat next to hers. Two collections, two lives, one education.</div><div style="{JOST};font-size:18px;line-height:1.75;color:{PAR}">I cut my teeth on pirate radio and late-night sets across London and Manchester, learning the music from every angle without losing the reason I started.</div>
<div style="{SIG};font-size:56px;color:{GOLD};transform:rotate(-3deg);transform-origin:left">Simone</div></div></div>'''
    chapters=[('Brixton','1981','My mother played Marvin Gaye on Sundays and explained every record like it was a story worth carrying. My father left his collection behind. His shelves sat next to hers.'),
              ('Savannah, Georgia','Four summers','Church on Sundays, then Stax and Muscle Shoals on 45s in Auntie Paulette’s garage. I never stopped listening the same way.'),
              ('Peckham','Pirate radio','I started by making tea at Groove City FM and ended up with Sunday midnight to three. Four listeners, maybe. Worth it.'),
              ('Wigan','Northern soul','The all-nighters changed how I hear a record. Some songs only make sense at four in the morning.')]
    ch=''.join(f'<div style="display:flex;flex-direction:column;gap:14px;padding-top:26px;border-top:1px solid {GOLD}"><div style="{WM};font-size:12px;color:{GOLD}">{y}</div><div style="{BOD};font-size:34px;color:{IV}">{p}</div><div style="{JOST};font-size:16px;line-height:1.7;color:{PAR}">{t}</div></div>' for p,y,t in chapters)
    story=f'''<div style="background:{V8};padding:96px 72px;display:flex;flex-direction:column;gap:44px">{label("Where it comes from")}<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:40px">{ch}</div></div>'''
    show=f'''<div style="background:{V9};padding:110px 72px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:20px">{label("The show")}
<div style="{BOD};font-size:54px;line-height:1.15;color:{IV};max-width:1000px">A home for soul, funk, disco and R&amp;B from when the music was made to last, where the story behind a track matters <i style="color:{GOLD}">as much as the groove itself.</i></div>
<div style="display:flex;gap:16px;margin-top:10px">{btn("Listen on Mixcloud")}{btn("Write to Simone",False)}</div></div>'''
    contact=f'''<div style="background:{BGV};padding:88px 72px;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center">
<div style="display:flex;flex-direction:column;gap:18px">{label("Write to Simone")}<div style="{BOD};font-size:48px;line-height:1.1;color:{IV}">Requests, stories, a record <i style="color:{GOLD}">I should play?</i></div><div style="{JOST};font-size:18px;line-height:1.7;color:{PAR}">I read every one. simone@thegroovelounge.com</div></div>
<div style="height:380px;background:url({img('skratt')}) 50% 35%/cover;border:1.5px solid {GOLD}"></div></div>'''
    body=f'<div style="width:1440px;background:{V8}">{nav(IV,GOLD,V8)}{hero}{story}{show}{contact}{footer(V8,IV,GOLD)}</div>'
    m=f'''<div style="width:390px;background:{V8}"><div style="height:64px;display:flex;align-items:center;gap:10px;padding:0 20px;border-bottom:1px solid rgba(201,162,74,0.25)">{puck(24)}<div style="{WM};font-size:11px;color:{GOLD}">The Groove Lounge</div></div>
<div style="height:420px;background:url({img('leende')}) 50% 35%/cover"></div><div style="padding:28px 20px;display:flex;flex-direction:column;gap:16px">{label("About Simone",GOLD,11)}<div style="{BOD};font-size:40px;line-height:1.05;color:{IV}">Two shelves. <i style="color:{GOLD}">One education.</i></div><div style="{JOST};font-size:16px;line-height:1.7;color:{PAR}">My mother played Marvin Gaye on Sundays and explained every record like it was a story worth carrying.</div></div></div>'''
    return body,m,"Om Simone","Hennes historia i fyra kapitel ur profilen: Brixton, Savannah, Peckham och Wigan. Texterna bygger på hennes bio på Mixcloud och profilen. Sedan vad showen är och hur man skriver till henne.",3120

def more_page():
    # archive desktop
    allshows=SHOWS*2
    cells=''.join(f'<div style="display:flex;flex-direction:column;gap:14px">{cover(s,290,False)}<div style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between"><div style="{label_css(GOLD)}">No. {s[2] if i<4 else "%03d"%(int(s[2])+4)}</div><div style="{JOST};font-size:13px;color:{PAR}">Oct 2026</div></div><div style="{BOD};font-size:24px;color:{IV}">{s[0]}</div><div style="{JOST};font-size:14px;color:{PAR}">{s[5]}</div></div></div>' for i,s in enumerate(allshows))
    chips=''.join(f'<div style="height:38px;display:inline-flex;align-items:center;padding:0 18px;border:1px solid {"#c9a24a" if j==0 else "rgba(201,162,74,0.35)"};{JOST};font-size:13px;letter-spacing:0.14em;text-transform:uppercase;color:{IV if j==0 else PAR}">{c}</div>' for j,c in enumerate(("All","Soul","Funk","Disco","R&amp;B","Northern soul","70s","80s","90s")))
    arch=f'''<div style="width:1440px;background:{V8}">{nav(IV,GOLD,V8)}<div style="background:{BGV};padding:80px 72px 56px;display:flex;flex-direction:column;gap:18px">{label("The archive")}<div style="{BOD};font-size:72px;color:{IV}">All <i style="color:{GOLD}">shows</i></div><div style="{JOST};font-size:18px;color:{PAR};max-width:640px;line-height:1.6">Every show since No. 001, newest first. A new one every week.</div><div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px">{chips}</div></div>
<div style="padding:40px 72px 96px;display:grid;grid-template-columns:repeat(4,290px);gap:56px 32px;justify-content:space-between">{cells}</div>{footer(V8,IV,GOLD)}</div>'''
    def small(inner,title):
        return f'<div style="display:flex;flex-direction:column;gap:12px"><div style="font-size:16px;font-weight:600;color:{IV}">{title}</div><div style="width:720px;height:560px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.5)"><div style="width:1440px;transform:scale(0.5);transform-origin:0 0">{inner}</div></div></div>'
    confirm=f'''<div style="width:1440px;height:1120px;background:{BGV};position:relative">{nav(IV,GOLD,V8)}<div style="position:absolute;top:84px;left:0;right:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;text-align:center">{puck(120)}{label("The weekly letter")}<div style="{BOD};font-size:72px;color:{IV}">You’re <i style="color:{GOLD}">in.</i></div><div style="{JOST};font-size:20px;line-height:1.7;color:{PAR};max-width:620px">Thank you. Check your inbox and confirm your address, and the next letter will find you when the new show is out.</div><div style="{SIG};font-size:60px;color:{GOLD};transform:rotate(-3deg)">Simone</div><div style="margin-top:10px">{btn("Listen to the latest show",False)}</div></div></div>'''
    paras=''.join(f'<div style="display:flex;flex-direction:column;gap:10px"><div style="{BOD};font-size:30px;color:{IV}">{h}</div><div style="{JOST};font-size:17px;line-height:1.75;color:{PAR}">{t}</div></div>' for h,t in (("Who we are","The Groove Lounge is run by Richard Skalsky. Contact: simone@thegroovelounge.com."),("What we collect","Your email address if you sign up for the weekly letter, and your first name, town, rating and note if you write to Simone. Nothing else."),("Why","To send the letter, to read and answer your notes, and, only if you ticked the box, to quote them."),("Your rights","Ask us to see, correct or delete your data at any time. Unsubscribe with one click.")))
    privacy=f'''<div style="width:1440px;height:1120px;background:{V8}">{nav(IV,GOLD,V8)}<div style="padding:80px 72px;display:grid;grid-template-columns:420px 1fr;gap:80px"><div style="display:flex;flex-direction:column;gap:16px">{label("Privacy")}<div style="{BOD};font-size:60px;line-height:1.05;color:{IV}">Your data, <i style="color:{GOLD}">kept small.</i></div><div style="{JOST};font-size:14px;color:{PAR}">Last updated October 2026</div></div><div style="display:flex;flex-direction:column;gap:34px;max-width:720px">{paras}</div></div></div>'''
    side=f'<div style="display:flex;flex-direction:column;gap:40px">{small(confirm,"Nyhetsbrev · bekräftelse")}{small(privacy,"Integritet")}</div>'
    mob=f'''<div style="width:390px;background:{V8}"><div style="height:64px;display:flex;align-items:center;gap:10px;padding:0 20px;border-bottom:1px solid rgba(201,162,74,0.25)">{puck(24)}<div style="{WM};font-size:11px;color:{GOLD}">The Groove Lounge</div></div><div style="padding:28px 20px;display:flex;flex-direction:column;gap:14px">{label("The archive",GOLD,11)}<div style="{BOD};font-size:44px;color:{IV}">All <i style="color:{GOLD}">shows</i></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">{"".join(f'<div style="display:flex;flex-direction:column;gap:8px">{cover(s,165,False)}<div style="{BOD};font-size:16px;color:{IV}">{s[0]}</div></div>' for s in SHOWS)}</div></div></div>'''
    body=f'<div style="display:flex;gap:42px;align-items:flex-start"><div style="box-shadow:0 30px 80px rgba(0,0,0,.5)">{arch}</div>{side}</div>'
    return body,mob,"Arkiv, nyhetsbrev och integritet","Arkivet med alla shower och filter för genre och decennium. Till höger, i halv storlek, bekräftelsen efter anmälan till nyhetsbrevet och integritetssidan. Längst till höger mobilversionen. Show 005–008 är upprepade platshållare.",1880
f={'show':show_page,'about':about_page,'more':more_page}[PAGE]
body,m,title,desc,H=f()
W=2800 if PAGE=='more' else 2000
content=f'''<div style="width:{W}px;box-sizing:border-box;padding:56px 64px;background:#04140f;color:#f3ecdc;font-family:Jost,Futura,sans-serif;display:flex;flex-direction:column;gap:32px">
<div style="display:flex;flex-direction:column;gap:6px"><div style="font-size:15px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#c9a24a">Webbsidan A · {title}</div><div style="font-size:18px;color:#c6bfa6;max-width:1400px">{desc}</div></div>
<div style="display:flex;gap:42px;align-items:flex-start"><div style="box-shadow:0 30px 80px rgba(0,0,0,.5)">{body}</div><div style="box-shadow:0 30px 80px rgba(0,0,0,.5)">{m}</div></div></div>'''
pre='' if loc else '<script src="./support.js"></script>'
SCRIPT='' if loc else '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":%d,"height":%d}}\'>\nclass Component extends DCLogic {\n  renderVals() {\n    return {};\n  }\n}\n</script>' % (W,H)
html=f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<title>Webbsidan A · {title}</title>
{pre}
</head>
<body>
{'' if loc else '<x-dc>'}
{'' if loc else '<helmet>'}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..800;1,6..96,400..700&amp;family=Jost:wght@400;500;600&amp;family=Pinyon+Script&amp;display=swap">
<style>
body{{margin:0}}
</style>
{'' if loc else '</helmet>'}
<div style="width:{W}px;height:{H}px;overflow:hidden;background:#04140f">{content}</div>
{'' if loc else '</x-dc>'}
{SCRIPT}
</body>
</html>
'''
open(outp,'w',encoding='utf-8').write(html)
