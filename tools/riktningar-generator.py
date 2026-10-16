import sys, os
which=sys.argv[1]; out=sys.argv[2]; local=len(sys.argv)>3
G=os.path.expanduser('~/Assistant/projekt/groove-lounge/grafik')
SC='/private/tmp/claude-501/-Users-richardskalsky-Assistant/ce89e0b9-4a80-455c-bff6-a1cc82451ff4/scratchpad/simone'
B={'skratt':('/_blob/812de7fc2706b2b800a75335a5bcd6f3',f'file://{SC}/simone-skratt-700.jpg'),
   'leende':('/_blob/d4f795b60f9ea06cf13f6b761afb2ec2',f'file://{SC}/simone-leende-700.jpg')}
def img(k): return B[k][1] if local else B[k][0]
SHOWS=[('The Crossing','Delegation · Loose Ends · Imagination · Omar','004','/_blob/bce39c3f16173e9fd31735598a1cb52f','the-crossing','British Soul, 1977–1993','How a sound crossed the Atlantic, found a home in London and came back changed.'),
 ('Every City Has Its Soul','Gwen McCrae · Bloodstone · Ann Peebles · Ray Parker Jr. &amp; Raydio','003','/_blob/d7f9771a4209176c74780186bbc83648','every-city-has-its-soul','Miami, Memphis, Detroit &amp; More','Every city had a sound you could hear through the walls. Tonight we go door to door.'),
 ('Raised on the Gospel','Marvin Gaye · The Staple Singers · Loleatta Holloway · Deniece Williams','002','/_blob/dae1cfdd23d7475a8f518486a3200c93','raised-on-the-gospel','Soul Voices From the Church, 1971–1984','Before the charts there was a choir. These are the voices that never really left it.'),
 ('On My Own Now','Teddy Pendergrass · Eddie Kendricks · Frankie Beverly · Bobby Womack','001','/_blob/33a64e7e5623c2fdf80ce8705142ab45','on-my-own-now','Soul Voices Going Solo, 1971–1984','What happens to a voice when it finally has to stand alone?')]
V9='#07201a'; V8='#0b2a21'; V7='#155240'; GOLD='#c9a24a'; IV='#f3ecdc'; PAR='#c6bfa6'; G7='#8c6b22'
BOD="font-family:'Bodoni Moda',Didot,Georgia,serif;font-weight:600;font-variation-settings:'opsz' 28"
JOST="font-family:Jost,Futura,sans-serif"
WM=f"{JOST};font-weight:500;letter-spacing:0.4em;text-transform:uppercase"
SIG="font-family:'Pinyon Script',cursive"
def cover(s,px,shadow=True):
    k=px/600
    if local:
        inner=f'<div style="width:600px;height:600px;position:relative;background:radial-gradient(60% 60% at 50% 40%,{V7},{V8} 75%);"><div style="position:absolute;inset:22px;border:1.5px solid {GOLD}"></div><img src="file://{G}/showbilder/{s[4]}.jpg" style="position:absolute;left:34px;top:78px;width:532px;height:240px;object-fit:cover"><div style="position:absolute;top:340px;left:40px;right:40px;text-align:center;{BOD};font-size:52px;color:{IV}">{s[0]}</div></div>'
    else:
        inner=f'<dc-import name="BCover" symbol="showbild" title="{s[0]}" artists="{s[1]}" number="{s[2]}" bild="{s[3]}" hint-size="600px,600px"></dc-import>'
    sh='box-shadow:0 24px 50px rgba(0,0,0,0.45);' if shadow else ''
    return f'<div style="width:{px}px;height:{px}px;overflow:hidden;flex:none;{sh}"><div style="width:600px;height:600px;transform:scale({k:.4f});transform-origin:0 0">{inner}</div></div>'
def player(dark=True,w='100%'):
    bg='#101614' if dark else '#ffffff'; fg='#e9e9e9' if dark else '#222'; bar='#3a4a44' if dark else '#d9d9d9'
    bars=''.join(f'<div style="width:3px;height:{6+((i*37)%26)}px;background:{GOLD if i<34 else bar};border-radius:1px"></div>' for i in range(90))
    return f'''<div style="width:{w};box-sizing:border-box;background:{bg};border-radius:6px;padding:14px 16px;display:flex;align-items:center;gap:14px;font-family:-apple-system,Helvetica,Arial,sans-serif">
<div style="width:44px;height:44px;border-radius:50%;background:{GOLD};display:flex;align-items:center;justify-content:center;flex:none"><div style="width:0;height:0;border-left:14px solid {V8};border-top:9px solid transparent;border-bottom:9px solid transparent;margin-left:4px"></div></div>
<div style="display:flex;flex-direction:column;gap:6px;flex:1;min-width:0"><div style="font-size:12px;color:{fg};opacity:.8">The Groove Lounge · Mixcloud</div><div style="display:flex;align-items:center;gap:2px;height:32px;overflow:hidden">{bars}</div></div>
<div style="font-size:12px;color:{fg};opacity:.6;flex:none">58:12</div></div>'''
def btn(t,solid=True,color=GOLD,ink=V8): 
    return f'<div style="display:inline-flex;align-items:center;height:48px;padding:0 26px;{JOST};font-size:14px;font-weight:500;letter-spacing:0.18em;text-transform:uppercase;{"background:"+color+";color:"+ink if solid else "border:1px solid "+color+";color:"+color}">{t}</div>'
def label(t,c=GOLD,size=13): return f'<div style="{WM};font-size:{size}px;color:{c}">{t}</div>'
def puck(px):
    return f'<div style="width:{px}px;height:{px}px;border-radius:50%;flex:none;background:conic-gradient(from 30deg,#7a5c1c,#f1dfa6 10%,#a8822f 22%,#6b4f16 38%,#c9a24a 52%,#f4e3b0 60%,#9c7a2c 72%,#6b4f16 86%,#7a5c1c);box-shadow:inset 0 0 0 1px rgba(255,240,200,.35),0 4px 10px rgba(0,0,0,.35);position:relative"><div style="position:absolute;left:50%;top:50%;width:{px*0.11:.0f}px;height:{px*0.11:.0f}px;transform:translate(-50%,-50%);border-radius:50%;background:{V8}"></div></div>'
def nav(fg,accent,bg='transparent',border='rgba(201,162,74,0.25)'):
    links=''.join(f'<div>{x}</div>' for x in ('Shows','About Simone','Newsletter'))
    return f'''<div style="height:84px;display:flex;align-items:center;justify-content:space-between;padding:0 72px;background:{bg};border-bottom:1px solid {border}">
<div style="display:flex;align-items:center;gap:14px">{puck(30)}<div style="{WM};font-size:15px;color:{accent}">The Groove Lounge</div></div>
<div style="display:flex;gap:40px;{JOST};font-size:15px;letter-spacing:0.08em;color:{fg}">{links}</div>
{btn("Listen on Mixcloud",False,accent)}</div>'''
def footer(bg,fg,accent):
    return f'''<div style="background:{bg};padding:56px 72px 48px;display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid rgba(201,162,74,0.25)">
<div style="display:flex;flex-direction:column;gap:14px">{label("The Groove Lounge",accent,14)}<div style="{BOD};font-size:30px;color:{fg}">Every record has a <i style="color:{accent}">story.</i></div><div style="{JOST};font-size:14px;color:{PAR}">Peckham, South London · simone@thegroovelounge.com</div></div>
<div style="display:flex;flex-direction:column;gap:12px;align-items:flex-end;{JOST};font-size:14px;letter-spacing:0.1em;color:{PAR}"><div style="display:flex;gap:26px;color:{fg}">Mixcloud · Instagram · Threads · TikTok · X</div><div>Privacy policy · RSS</div></div></div>'''
def newsletter(bg,fg,accent,ink,sub=PAR):
    return f'''<div style="background:{bg};padding:96px 72px;display:flex;flex-direction:column;align-items:center;gap:18px;text-align:center">
{label("The weekly letter",accent)}
<div style="{BOD};font-size:52px;color:{fg};line-height:1.1">One letter, <i style="color:{accent}">when a new show is out.</i></div>
<div style="{JOST};font-size:18px;color:{sub};max-width:560px;line-height:1.6">A few lines from Simone about the records, and a link to listen. No noise, unsubscribe any time.</div>
<div style="display:flex;gap:0;margin-top:12px"><div style="width:380px;height:52px;border:1px solid {accent};border-right:0;display:flex;align-items:center;padding:0 18px;{JOST};font-size:16px;color:{sub};box-sizing:border-box">Your email address</div>{btn("Subscribe",True,accent,ink)}</div></div>'''
QUOTE=("Not the most beautiful.","The most important.","On Sam Cooke, A Change Is Gonna Come")
def archive_grid(fg,accent,sub,n=4,px=290):
    cells=''.join(f'<div style="display:flex;flex-direction:column;gap:14px">{cover(s,px,False)}<div style="display:flex;flex-direction:column;gap:6px"><div style="{label_css(accent)}">No. {s[2]}</div><div style="{BOD};font-size:24px;color:{fg}">{s[0]}</div><div style="{JOST};font-size:14px;color:{sub}">{s[5]}</div></div></div>' for s in SHOWS[:n])
    return f'<div style="display:grid;grid-template-columns:repeat({n},{px}px);gap:32px;justify-content:space-between">{cells}</div>'
def label_css(c,size=12): return f"{WM};font-size:{size}px;color:{c}"
L=SHOWS[0]
BGV=f"radial-gradient(80% 60% at 50% 0%,{V7},{V8} 70%)"
# ---------------- A · Velvet ----------------
def A():
    hero=f'''<div style="padding:88px 72px 96px;display:flex;gap:72px;align-items:center;background:{BGV}">
{cover(L,540)}
<div style="display:flex;flex-direction:column;gap:22px;flex:1;min-width:0">
{label("New show · No. "+L[2])}
<div style="{BOD};font-size:76px;line-height:1.02;color:{IV}">The <i style="color:{GOLD}">Crossing</i></div>
<div style="{JOST};font-size:15px;letter-spacing:0.18em;text-transform:uppercase;color:{PAR}">{L[5]}</div>
<div style="{BOD};font-weight:400;font-style:italic;font-size:26px;line-height:1.45;color:{IV};max-width:560px">“{L[6]}”</div>
{player()}
<div style="display:flex;gap:16px">{btn("Listen on Mixcloud")}{btn("All shows",False)}</div></div></div>'''
    quote=f'''<div style="background:{V9};padding:110px 72px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:18px">
<div style="{BOD};font-size:120px;line-height:.6;color:{GOLD}">“</div>
<div style="{BOD};font-size:58px;line-height:1.15;color:{IV}">{QUOTE[0]} <i style="color:{GOLD}">{QUOTE[1]}</i></div>
<div style="{SIG};font-size:56px;color:{GOLD};transform:rotate(-3deg)">Simone</div>
<div style="{JOST};font-size:13px;letter-spacing:0.2em;text-transform:uppercase;color:{PAR}">{QUOTE[2]}</div></div>'''
    arch=f'''<div style="background:{V8};padding:96px 72px;display:flex;flex-direction:column;gap:44px">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div style="display:flex;flex-direction:column;gap:12px">{label("The archive")}<div style="{BOD};font-size:52px;color:{IV}">All <i style="color:{GOLD}">shows</i></div></div>{btn("See all shows",False)}</div>
{archive_grid(IV,GOLD,PAR)}</div>'''
    about=f'''<div style="background:{BGV};padding:96px 72px;display:flex;gap:80px;align-items:center">
<div style="position:relative;width:520px;height:600px;flex:none"><div style="position:absolute;inset:0;background:url({img('skratt')}) 50% 40%/cover"></div><div style="position:absolute;inset:-14px;border:1.5px solid {GOLD}"></div></div>
<div style="display:flex;flex-direction:column;gap:22px;max-width:600px">{label("Your host")}
<div style="{BOD};font-size:60px;line-height:1.05;color:{IV}">Hello, I’m <i style="color:{GOLD}">Simone.</i></div>
<div style="{JOST};font-size:19px;line-height:1.7;color:{PAR}">A South London broadcaster, digger and soul obsessive with two decades in record shops and late-night listening rooms. I grew up in Brixton with a mother who played Marvin Gaye on Sundays and explained every record like it was a story worth carrying.</div>
<div>{btn("Read her story",False)}</div></div></div>'''
    return f'<div style="width:1440px;background:{V8}">{nav(IV,GOLD,V8)}{hero}{quote}{arch}{about}{newsletter(V9,IV,GOLD,V8)}{footer(V8,IV,GOLD)}</div>'
# ---------------- B · Liner notes (ivory) ----------------
INK='#0b2a21'; PAP='#f3ecdc'; PAP2='#eadbb2'; GD='#8c6b22'; MUT='#3f5a4f'
def B_():
    hero=f'''<div style="background:{PAP};padding:110px 72px 70px;display:flex;flex-direction:column;align-items:center;gap:26px;text-align:center">
{label("Soul · Funk · Disco · R&amp;B · 1970–2005",GD)}
<div style="{BOD};font-size:128px;line-height:.98;color:{INK};letter-spacing:-0.01em">Every record<br>has a <i style="color:{GD}">story.</i></div>
<div style="{SIG};font-size:60px;color:{GD};transform:rotate(-3deg)">with Simone</div>
<div style="{JOST};font-size:18px;color:{MUT};max-width:620px;line-height:1.65">A new show every week on Mixcloud: the B-sides, the quiet storms and the voices that deserved more light.</div></div>'''
    latest=f'''<div style="background:{PAP};padding:30px 72px 110px"><div style="border-top:1px solid {INK};border-bottom:1px solid {INK};padding:56px 0;display:flex;gap:64px;align-items:center">
{cover(L,460)}
<div style="display:flex;flex-direction:column;gap:20px;flex:1;min-width:0">
<div style="display:flex;justify-content:space-between">{label("Latest · No. "+L[2],GD)}{label("This week",MUT)}</div>
<div style="{BOD};font-size:68px;line-height:1.02;color:{INK}">The <i style="color:{GD}">Crossing</i></div>
<div style="{JOST};font-size:15px;letter-spacing:0.18em;text-transform:uppercase;color:{MUT}">{L[1]}</div>
<div style="column-count:2;column-gap:36px;{JOST};font-size:17px;line-height:1.7;color:{INK}"><span style="{BOD};font-size:54px;float:left;line-height:.85;margin:6px 8px 0 0;color:{GD}">H</span>ow a sound crossed the Atlantic, found a home in London and came back changed. Simone follows the records from Philadelphia and Detroit to the clubs of Soho and the bedrooms of Brixton, where a new kind of British soul was being pressed in small runs and played until the grooves gave out.</div>
{player(False)}</div></div></div>'''
    rows=''.join(f'''<div style="display:grid;grid-template-columns:110px 96px 1fr 360px 140px;align-items:center;gap:28px;padding:22px 0;border-bottom:1px solid rgba(11,42,33,0.25)">
<div style="{WM};font-size:13px;color:{GD}">No. {s[2]}</div>{cover(s,96,False)}
<div style="{BOD};font-size:32px;color:{INK}">{s[0]}</div><div style="{JOST};font-size:15px;color:{MUT}">{s[5]}</div><div style="{JOST};font-size:13px;letter-spacing:0.18em;text-transform:uppercase;color:{INK};text-align:right">Listen →</div></div>''' for s in SHOWS)
    cat=f'''<div style="background:{PAP};padding:0 72px 110px;display:flex;flex-direction:column;gap:28px">
<div style="display:flex;justify-content:space-between;align-items:flex-end">{f'<div style="{BOD};font-size:56px;color:{INK}">The <i style="color:{GD}">catalogue</i></div>'}{label("All shows →",GD)}</div>
<div style="border-top:1px solid {INK}">{rows}</div></div>'''
    about=f'''<div style="background:{V8};padding:110px 72px;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center">
<div style="display:flex;flex-direction:column;gap:24px">{label("About")}
<div style="{BOD};font-size:64px;line-height:1.05;color:{IV}">Two shelves.<br><i style="color:{GOLD}">One education.</i></div>
<div style="{JOST};font-size:19px;line-height:1.7;color:{PAR}">My mother’s records and my father’s, side by side in a flat in Brixton. Four summers in Savannah, pirate radio in a Peckham tower block, northern soul in Wigan. Everything I play comes from somewhere.</div>
<div style="{SIG};font-size:52px;color:{GOLD};transform:rotate(-3deg);transform-origin:left">Simone</div></div>
<div style="height:620px;background:url({img('leende')}) 50% 40%/cover;filter:saturate(.9)"></div></div>'''
    return f'<div style="width:1440px;background:{PAP}">{nav(INK,GD,PAP,"rgba(11,42,33,0.2)")}{hero}{latest}{cat}{about}{newsletter(PAP2,INK,GD,PAP,MUT)}{footer(V8,IV,GOLD)}</div>'
# ---------------- C · The room (photo-led) ----------------
def C():
    hero=f'''<div style="position:relative;height:780px;background:{V8};overflow:hidden">
<div style="position:absolute;right:0;top:0;width:860px;height:780px;background:url({img('skratt')}) 45% 35%/cover;-webkit-mask-image:linear-gradient(to right,transparent 0,#000 38%);mask-image:linear-gradient(to right,transparent 0,#000 38%)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(to top,{V8} 0,transparent 30%)"></div>
<div style="position:absolute;left:72px;top:170px;width:640px;display:flex;flex-direction:column;gap:24px">
{label("The Groove Lounge · with Simone")}
<div style="{BOD};font-size:96px;line-height:1;color:{IV}">Every record<br>has a <i style="color:{GOLD}">story.</i></div>
<div style="{JOST};font-size:20px;line-height:1.65;color:{PAR};max-width:520px">Soul, funk, disco and R&amp;B from when the music was made to last, and the stories behind it. A new show every week.</div>
<div style="display:flex;gap:16px;margin-top:8px">{btn("Play the latest show")}{btn("About Simone",False)}</div></div></div>'''
    latest=f'''<div style="background:{V8};padding:30px 72px 100px"><div style="background:{V9};border:1px solid rgba(201,162,74,0.3);padding:44px;display:flex;gap:56px;align-items:center">
{cover(L,380)}
<div style="display:flex;flex-direction:column;gap:18px;flex:1;min-width:0">{label("New this week · No. "+L[2])}
<div style="{BOD};font-size:60px;line-height:1.02;color:{IV}">The <i style="color:{GOLD}">Crossing</i></div>
<div style="{BOD};font-weight:400;font-style:italic;font-size:24px;line-height:1.45;color:{IV}">“{L[6]}”</div>
{player()}</div></div></div>'''
    row=''.join(f'<div style="display:flex;flex-direction:column;gap:12px">{cover(s,300,False)}<div style="{label_css(GOLD)}">No. {s[2]}</div><div style="{BOD};font-size:24px;color:{IV}">{s[0]}</div></div>' for s in SHOWS)
    arch=f'''<div style="background:{V8};padding:0 72px 100px;display:flex;flex-direction:column;gap:36px">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div style="{BOD};font-size:48px;color:{IV}">Earlier <i style="color:{GOLD}">shows</i></div>{label("All shows →")}</div>
<div style="display:flex;gap:32px">{row}</div></div>'''
    quotes=''.join(f'<div style="display:flex;flex-direction:column;gap:14px;padding:36px;border:1px solid rgba(201,162,74,0.3)"><div style="{BOD};font-size:30px;line-height:1.3;color:{IV}">“{q}”</div><div style="{JOST};font-size:13px;letter-spacing:0.18em;text-transform:uppercase;color:{PAR}">{w}</div></div>' for q,w in (("Not the most beautiful. The most important.","On Sam Cooke"),("Four listeners, maybe. Worth it.","On pirate radio, Peckham"),("Not the dancefloor, not the church. Somewhere in between.","On the quiet room")))
    qsec=f'''<div style="background:{V9};padding:100px 72px;display:flex;flex-direction:column;gap:36px">{label("In her words")}<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:28px">{quotes}</div></div>'''
    return f'<div style="width:1440px;background:{V8}">{nav(IV,GOLD,V8)}{hero}{latest}{arch}{qsec}{newsletter(V8,IV,GOLD,V8)}{footer(V9,IV,GOLD)}</div>'
# ---------------- mobile ----------------
def mob(kind):
    if kind=='B':
        bg=PAP; fg=INK; ac=GD; sub=MUT
    else:
        bg=V8; fg=IV; ac=GOLD; sub=PAR
    top=f'<div style="height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;border-bottom:1px solid rgba(201,162,74,0.25)"><div style="display:flex;align-items:center;gap:10px">{puck(24)}<div style="{WM};font-size:11px;color:{ac}">The Groove Lounge</div></div><div style="width:22px;display:flex;flex-direction:column;gap:5px"><div style="height:1.5px;background:{fg}"></div><div style="height:1.5px;background:{fg}"></div><div style="height:1.5px;background:{fg}"></div></div></div>'
    if kind=='C':
        hero=f'<div style="position:relative;height:520px;overflow:hidden"><div style="position:absolute;inset:0;background:url({img("skratt")}) 50% 30%/cover"></div><div style="position:absolute;inset:0;background:linear-gradient(to top,{V8} 25%,transparent 70%)"></div><div style="position:absolute;left:20px;right:20px;bottom:30px;display:flex;flex-direction:column;gap:14px"><div style="{BOD};font-size:46px;line-height:1.02;color:{IV}">Every record has a <i style="color:{GOLD}">story.</i></div><div style="{SIG};font-size:34px;color:{GOLD}">with Simone</div></div></div>'
    elif kind=='B':
        hero=f'<div style="padding:44px 20px 24px;text-align:center;display:flex;flex-direction:column;gap:14px;align-items:center"><div style="{BOD};font-size:52px;line-height:1;color:{INK}">Every record has a <i style="color:{GD}">story.</i></div><div style="{SIG};font-size:34px;color:{GD}">with Simone</div></div>'
    else:
        hero=''
    latest=f'''<div style="padding:28px 20px;display:flex;flex-direction:column;gap:16px">{label("New show · No. "+L[2],ac,11)}{cover(L,350)}
<div style="{BOD};font-size:40px;line-height:1.05;color:{fg}">The <i style="color:{ac}">Crossing</i></div><div style="{JOST};font-size:15px;line-height:1.6;color:{sub}">{L[6]}</div>{player(kind!='B')}</div>'''
    arch=''.join(f'<div style="display:flex;gap:14px;align-items:center;padding:12px 0;border-bottom:1px solid rgba(201,162,74,0.2)">{cover(s,72,False)}<div style="display:flex;flex-direction:column;gap:4px"><div style="{WM};font-size:10px;color:{ac}">No. {s[2]}</div><div style="{BOD};font-size:20px;color:{fg}">{s[0]}</div></div></div>' for s in SHOWS[1:])
    return f'<div style="width:390px;background:{bg}">{top}{hero}{latest}<div style="padding:8px 20px 40px">{arch}</div></div>'
pages={'A':(A,"A · Velvet","Helt i sammetsgrönt och guld, som omslagen. Senaste showen stort överst med spelaren, sedan ett citat, arkivet, Simone och nyhetsbrevet."),
       'B':(B_,"B · Liner Notes","Elfenbensvitt papper som baksidan av ett skivkonvolut: stor typografi, text i spalter och arkivet som en katalog. Grönt bara i Om-delen och sidfoten."),
       'C':(C,"C · The Room","Bildledd. Simone skrattar i stort format och tonas ut i grönt bakom sloganen. Sedan senaste showen som ett kort, arkivet och hennes egna ord.")}
f,title,desc=pages[which]
body=f()
H={'A':3760,'B':4020,'C':3460}[which]
content=f'''<div style="width:2000px;box-sizing:border-box;padding:56px 64px;background:#04140f;color:#f3ecdc;font-family:Jost,Futura,sans-serif;display:flex;flex-direction:column;gap:32px">
<div style="display:flex;flex-direction:column;gap:6px"><div style="font-size:15px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#c9a24a">Webbsidan · {title}</div><div style="font-size:18px;color:#c6bfa6;max-width:1400px">{desc} Till vänster dator (1440 px), till höger mobil (390 px).</div></div>
<div style="display:flex;gap:42px;align-items:flex-start"><div style="box-shadow:0 30px 80px rgba(0,0,0,.5)">{body}</div><div style="box-shadow:0 30px 80px rgba(0,0,0,.5)">{mob(which)}</div></div></div>'''
pre='' if local else '<script src="./support.js"></script>'
SCRIPT='' if local else '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":2000,"height":%d}}\'>\nclass Component extends DCLogic {\n  renderVals() {\n    return {};\n  }\n}\n</script>' % H
html=f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<title>Webbsidan · {title}</title>
{pre}
</head>
<body>
{'' if local else '<x-dc>'}
{'' if local else '<helmet>'}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..800;1,6..96,400..700&amp;family=Jost:wght@400;500;600&amp;family=Pinyon+Script&amp;display=swap">
<style>
body{{margin:0}}
</style>
{'' if local else '</helmet>'}
<div style="width:2000px;height:{H}px;overflow:hidden;background:#04140f">{content}</div>
{'' if local else '</x-dc>'}
{SCRIPT}
</body>
</html>
'''
open(out,'w',encoding='utf-8').write(html)
