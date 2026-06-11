# J&A Freight Systems — Website

Static HTML site (no build step, no framework). 8 pages, shared CSS/JS, brand assets included.

## Structure
```
index.html        Home
shippers.html     For Shippers (services + lane-check form + TMS portal)
carriers.html     For Carriers (benefits + setup form + portal)
technology.html   Technology / MercuryGate TMS
about.html        About (story, timeline, stats, team, compliance)
careers.html      Join J&A (benefits + general application)
positions.html    17 open positions w/ department filters
contact.html      Contact (info cards + form + HQ map graphic)
css/styles.css    Full brand system
js/main.js        Nav, scroll reveal, count-up stats, FAQ, filters, forms
assets/           Logos (originals + transparent versions)
build.py          Optional: regenerates all pages from one template (edit nav/footer once)
```

## Deploy — GitHub Pages
1. Push this folder to a repo (e.g. `JA-Freight-Web`).
2. Settings → Pages → Deploy from branch → `main` / root.
3. Done. All paths are relative, so subpath hosting (`username.github.io/JA-Freight-Web/`) works with no basePath config.

## Deploy — Vercel
`vercel --prod` from this folder, or import the repo in the Vercel dashboard. Framework preset: **Other** (static).

## Wiring the forms
Forms currently show a client-side confirmation (`data-demo` attribute). To make them live:
- Easiest: [Formspree](https://formspree.io) — set `action="https://formspree.io/f/XXXX" method="POST"` and remove `data-demo`.
- Or point them at any backend / GoHighLevel webhook.

## Notes
- Phone, email, address, MC#/DOT# are placeholders — swap in real values before launch.
- Team names mirror the original mock; replace avatars with photos by swapping the `.avatar` div for an `<img>`.
- Editing the shared header/footer: change it once in `build.py` and run `python3 build.py`, or edit each HTML file directly.
