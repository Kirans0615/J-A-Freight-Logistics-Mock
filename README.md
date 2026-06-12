# J&A Freight Systems — Marketing Website

Corporate marketing website for J&A Freight Systems, a Chicago-based freight logistics company. Built as a pure static HTML/CSS/JS site — no framework, no build step required.

---

## What This Project Is

| Detail | Value |
|--------|-------|
| Type | Static multi-page website (8 pages) |
| Stack | HTML5, CSS3, Vanilla JavaScript |
| Fonts | Barlow Condensed (headings) + Barlow (body) via Google Fonts |
| Map | MapLibre GL JS 4.7.1 (service-reach map on the Home page) |
| Forms | Netlify Forms (submissions collected in Netlify dashboard) |
| Deployment | GitHub Pages (primary) or Netlify (alternative) |

---

## How To Run Locally

No build tools needed. Open any page directly in a browser:

```bash
# Option 1 — open index.html directly
open ja-freight-website/index.html

# Option 2 — serve with Python (avoids CORS issues with local video files)
cd ja-freight-website
python3 -m http.server 8080
# then visit http://localhost:8080
```

> **Tip:** Use the Python server if hero background videos don't play — some browsers block `file://` video requests.

---

## Folder Organization

```
ja-freight-repo/              ← Repo root (this is what gets deployed)
├── index.html                ← Home page
├── about.html                ← About Us
├── shippers.html             ← For Shippers
├── carriers.html             ← For Carriers
├── technology.html           ← Technology platform
├── careers.html              ← Join J&A (job listings + application form)
├── positions.html            ← Open positions detail
├── contact.html              ← Contact Us
├── css/
│   └── styles.css            ← All styles (single stylesheet)
├── js/
│   └── main.js               ← All JavaScript (single script file)
├── assets/                   ← Images, SVGs, and videos
│   ├── *.png / *.jpg         ← Logos, headshots, illustrations
│   ├── *.svg                 ← Vector assets (e.g. LogoFooterYellow.svg)
│   └── *.mp4                 ← Background / hero videos
├── .github/
│   └── workflows/
│       └── deploy.yml        ← GitHub Actions auto-deploy to GitHub Pages
├── .gitignore
├── netlify.toml              ← Netlify deployment config
└── README.md                 ← This file
```

---

## How To Edit Content

### Change text on a page
Open the relevant `.html` file in any text editor. Content lives directly in the HTML — look for headings (`<h1>`, `<h2>`), paragraphs (`<p>`), and list items (`<li>`).

### Change the navigation or footer
Navigation and footer are **duplicated** across all 8 pages (no server-side includes). To update a nav link or footer text, edit each `.html` file. Search for the text you want to change across all files at once:

```bash
grep -rn "text to find" ja-freight-website/
```

### Change colors or fonts
All design tokens are in `css/styles.css` at the top of the file under `:root { }`. Key values:

| Token | Value | Used for |
|-------|-------|----------|
| `--navy` | `#14365C` | Primary navy |
| `--navy-deep` | `#0B2138` | Dark navy backgrounds |
| `--gold` | `#FFC20D` | Brand gold / CTAs |
| `--gold-dk` | `#E2A900` | Gold hover state |

### Swap a background video
Replace the `.mp4` file in `assets/` with the new file using the **same filename**, or update the `<source src="...">` path inside the `<video>` tag in the relevant HTML file.

---

## How To Deploy

### GitHub Pages (primary — auto-deploys on push)

The site deploys automatically via GitHub Actions whenever you push to `main`. No manual steps needed after initial setup.

**First-time setup:**
1. Push the repo to GitHub
2. Go to **Settings → Pages → Source** and select **GitHub Actions**
3. Push any commit to `main` — the workflow runs and publishes the site

Live URL: `https://<your-github-username>.github.io/<repo-name>/`

### Netlify (alternative)

1. Log in to [netlify.com](https://netlify.com) and click **Add new site → Import an existing project**
2. Connect your GitHub repo
3. Netlify reads `netlify.toml` automatically — no settings to change
4. Click **Deploy site**

Netlify also collects form submissions (see **Form Submissions** below).

---

## How To Add A New Page

1. Copy an existing page (e.g. `about.html`) and rename it (e.g. `new-page.html`)
2. Update the `<title>` tag and the `<h1>` heading
3. Edit the content sections
4. Add a link to the new page in the `<nav>` block of **all 8 existing pages** (search for `<nav` to find them quickly)
5. The new page automatically inherits all styles from `css/styles.css` and scripts from `js/main.js`

---

## Form Submissions

All forms use **Netlify Forms** — no backend server required. Submissions appear in the Netlify dashboard under **Forms → Submissions**.

| Form | Page | Netlify form name |
|------|------|-------------------|
| Contact Us | `contact.html` | `contact` |
| Job Application | `careers.html` | `job-application` |
| Newsletter signup | Footer on all pages | `newsletter-signup` |

> **Note:** Forms only work when the site is hosted on Netlify. When running locally, form submits will 404 — this is expected.

To receive email notifications for form submissions: Netlify dashboard → **Forms → [form name] → Form notifications → Add notification → Email**.

---

## Brand Assets

| Asset | File | Usage |
|-------|------|-------|
| Icon mark | `assets/Group-1321315098.png` | Navbar logo |
| Wordmark (yellow) | `assets/LogoFooterYellow.svg` | Footer |
| 40th anniversary | `assets/logo-40years.png` | Carriers page |
| MBE certification | `assets/mbe-certification-copy-1.png` | About page |

Brand colors: Navy `#0B2138` · Gold `#FFC20D`

---

## Local Development Notes

- **Videos** (`assets/*.mp4`) are large files (~10 MB each). They are tracked in git but excluded from the build artifact size limit on GitHub Pages (100 MB max per repo is the soft limit).
- **No npm / Node.js** is required. The site has zero dependencies that need installing.
- **MapLibre GL JS** is loaded from CDN (see `<head>` in `index.html`). An internet connection is required to render the service-reach map.
