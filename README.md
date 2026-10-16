# thegroovelounge.com – källkod

Statisk webbplats, riktning A (Velvet) från Claude Design. Bara Pythons standardbibliotek behövs.

- `python3 build.py --demo` bygger till `out/` med exempelbrev. Utan `--demo` blir det den skarpa versionen.
- `python3 -m http.server 8765 --directory out` startar en förhandsvisning på http://localhost:8765.
- `python3 tools/cover.py content/shows/*.json` renderar omslagen till `static/covers/` (1200 px). Lägg till `--size 2048` för Mixcloud.
- Innehåll: `content/site.json`, en show per fil i `content/shows/`, godkända brev i `content/letters/<nr>.json`.
- Arkitektur och API: `../arkitektur-och-api.md`. Lyssnardialog: `../lyssnardialog-krav.md`.
- `tools/riktningar-generator.py` och `tools/sidor-generator.py` genererade skisserna på canvasen.
