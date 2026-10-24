// The Groove Lounge – webbplatsens skript: meny, arkivfilter, betyg och lappar till Simone.
(() => {
  const api = (document.querySelector('meta[name="tgl-api"]') || {}).content || "";

  // Meny på mobil
  const nav = document.querySelector(".nav");
  const burger = document.querySelector(".burger");
  if (burger) burger.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open);
  });

  // Arkivfilter
  const chips = document.querySelectorAll(".chips button");
  chips.forEach(chip => chip.addEventListener("click", () => {
    chips.forEach(c => c.setAttribute("aria-pressed", c === chip));
    const tag = chip.dataset.tag;
    document.querySelectorAll(".grid .card").forEach(card => {
      card.hidden = tag !== "all" && !card.dataset.tags.split(" ").includes(tag);
    });
  }));

  async function post(path, body) {
    if (!api) throw new Error("offline");
    const r = await fetch(api.replace(/\/$/, "") + path, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error(String(r.status));
    return r.json().catch(() => ({}));
  }

  // Stjärnor: gemensam logik för snabbetyget och betyget i lappen
  document.querySelectorAll(".stars").forEach(group => {
    const buttons = [...group.querySelectorAll("button")];
    const set = n => { group.dataset.value = n; buttons.forEach((b, i) => { b.classList.toggle("on", i < n); b.setAttribute("aria-pressed", i < n); }); };
    buttons.forEach((b, i) => b.addEventListener("click", async () => {
      set(i + 1);
      if (!group.closest(".rate")) return;               // betyget i lappen skickas med lappen
      const msg = group.closest(".rate").querySelector(".thanks");
      try {
        await post("/v1/ratings", { show: group.dataset.show, stars: i + 1 });
        msg.textContent = "Thank you. I’ll see it.";
      } catch (e) {
        msg.textContent = api ? "Sorry, that didn’t go through. Try again later." : "Ratings open when my first show is out.";
      }
    }));
  });

  // Lapp till Simone
  const form = document.querySelector("form.note");
  if (form) form.addEventListener("submit", async ev => {
    ev.preventDefault();
    const status = form.querySelector(".status");
    const d = new FormData(form);
    if (d.get("website")) return;                        // fälla för spam
    const stars = Number(form.querySelector(".stars").dataset.value || 0) || null;
    const body = {
      show: form.dataset.show, stars, name: d.get("name"), town: d.get("town"),
      text: d.get("text"), email: d.get("email") || null, consent: d.get("consent") === "on"
    };
    if (!body.text || !body.text.trim()) { status.textContent = "Write a few words first."; return; }
    form.querySelector("button[type=submit]").disabled = true;
    try {
      await post("/v1/notes", body);
      form.reset(); form.querySelector(".stars").dataset.value = 0;
      form.querySelectorAll(".stars button").forEach(b => b.classList.remove("on"));
      status.textContent = "Thank you. I read every note.";
    } catch (e) {
      status.textContent = api ? "Sorry, that didn’t go through. Please try again, or write to simone@thegroovelounge.com."
                               : "Notes open when my first show is out. Until then: simone@thegroovelounge.com";
    } finally { form.querySelector("button[type=submit]").disabled = false; }
  });

  // Nyhetsbrev utan tjänst ännu
  document.querySelectorAll("form.signup").forEach(f => {
    if (f.getAttribute("action")) return;
    f.addEventListener("submit", ev => {
      ev.preventDefault();
      const s = f.parentElement.querySelector(".status");
      if (s) s.textContent = "My letter starts with the first show. Check back soon.";
    });
  });

  // Besöksstatistik: Google Analytics laddas först när besökaren har sagt ja. Innan dess skickas inget till Google.
  const ga = (document.querySelector('meta[name="tgl-ga"]') || {}).content || "";
  const KEY = "tgl-consent";
  const choice = () => { try { return localStorage.getItem(KEY); } catch (e) { return null; } };
  const remember = v => { try { localStorage.setItem(KEY, v); } catch (e) {} };
  function loadGA() {
    if (window.gtag) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", ga, { allow_google_signals: false, allow_ad_personalization_signals: false, cookie_expires: 34128000 }); // 13 månader
    const s = document.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ga);
    document.head.appendChild(s);
  }
  function clearGA() {
    document.cookie.split(";").map(c => c.split("=")[0].trim()).filter(n => n.startsWith("_ga")).forEach(n => {
      for (const d of ["", "; domain=" + location.hostname, "; domain=." + location.hostname.replace(/^www\./, "")])
        document.cookie = n + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + d;
    });
  }
  function ask() {
    if (document.querySelector(".consent")) return;
    const box = document.createElement("div");
    box.className = "consent"; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", "Cookies");
    box.innerHTML = '<p>May I count your visit? I use Google Analytics to see which shows you like. It sets cookies only if you say yes. <a href="/privacy/#cookies">Read more</a></p>'
      + '<div class="btns"><button class="btn" data-v="denied">No thanks</button><button class="btn" data-v="granted">Yes please</button></div>';
    box.addEventListener("click", ev => {
      const v = ev.target.dataset.v;
      if (!v) return;
      const had = choice() === "granted";
      remember(v); box.remove();
      if (v === "granted") loadGA();
      else if (had) { clearGA(); location.reload(); }     // laddat skript försvinner först vid omladdning
    });
    document.body.appendChild(box);
    box.querySelector("button").focus({ preventScroll: true });
  }
  if (ga) {
    if (choice() === "granted") loadGA(); else { clearGA(); if (!choice()) ask(); }   // städar även cookies som GA skrev precis innan omladdningen
    document.querySelectorAll("[data-consent]").forEach(a => a.addEventListener("click", ev => { ev.preventDefault(); ask(); }));
  }
})();
