/* ============================================================
   J&A Freight Systems — main.js
   Shared JavaScript for all 8 pages of the static site.
   No external dependencies — pure vanilla JS.

   Sections:
     1. DOMContentLoaded  — nav, reveal, stats, FAQ, forms, parallax
     2. Interactive Components — Image Accordion, Scroll 3D, Hover Slideshow
     3. Chicago Service Reach Map (MapLibre GL JS, loaded on demand)
   ============================================================ */

const REDUCE_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

document.addEventListener('DOMContentLoaded', () => {

  /* ── Mobile nav ────────────────────────────────────────────
     Toggles the hamburger open/close on small screens.
     The .nav-toggle button is in the <header> of every page. */
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('nav.main');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
    });
  }

  /* ── Active nav link ───────────────────────────────────────
     Highlights the current page's link in the nav bar. */
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav.main a').forEach(a => {
    if (a.getAttribute('href') === page) {
      a.classList.add('active');
      a.setAttribute('aria-current', 'page');
    }
  });

  /* ── Scroll reveal ─────────────────────────────────────────
     Any element with class="reveal" fades/slides in when it
     enters the viewport. CSS handles the actual animation;
     this adds the "in" class to trigger it. */
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  /* ── Count-up stats ────────────────────────────────────────
     Elements with data-count="40" animate from 0 to that number
     when they scroll into view. Add data-suffix="+" for labels. */
  const cio = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target, target = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
      if (REDUCE_MOTION) {
        el.textContent = target.toFixed(dec) + (el.dataset.suffix || '');
        cio.unobserve(el);
        return;
      }
      const dur = 1200, t0 = performance.now();
      const tick = now => {
        const p = Math.min((now - t0) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * eased).toFixed(dec) + (el.dataset.suffix || '');
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      cio.unobserve(el);
    });
  }, { threshold: .5 });
  document.querySelectorAll('[data-count]').forEach(el => cio.observe(el));

  /* ── FAQ accordion ─────────────────────────────────────────
     Clicking a .faq-q button opens its parent .faq-item
     and closes any other open item (one-at-a-time behavior). */
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      item.parentElement.querySelectorAll('.faq-item.open').forEach(o => { if (o !== item) o.classList.remove('open'); });
      item.classList.toggle('open');
    });
  });

  /* ── Forms — local preview confirmation ────────────────────
     Forms with data-demo="true" show a success message on submit
     without sending any data (for local development preview).
     On Netlify, data-netlify="true" takes over and the real
     submission is sent to the Netlify Forms backend. */
  document.querySelectorAll('form[data-demo]').forEach(form => {
    form.addEventListener('submit', ev => {
      ev.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      const ok = form.querySelector('.form-success');
      if (ok) { ok.classList.add('show'); ok.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
      form.querySelectorAll('input,select,textarea').forEach(f => f.value = '');
    });
  });

  /* ── Parallax photo bands ──────────────────────────────────
     .photo-band sections have a .pb-bg background image that
     drifts at a slower rate than the page scroll for depth. */
  const bands = document.querySelectorAll('.photo-band .pb-bg');
  if (bands.length) {
    const onScroll = () => {
      bands.forEach(bg => {
        const rect = bg.closest('.photo-band').getBoundingClientRect();
        const pct = (rect.top / window.innerHeight);
        bg.style.transform = `translateY(${pct * 40}px)`;
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Stagger delays for grid children ──────────────────────
     Containers with class="stagger" animate their .reveal
     children in sequence for a cascade effect. The gap defaults
     to 80ms; override per-container with data-stagger="60". */
  document.querySelectorAll('.stagger').forEach(container => {
    const step = parseInt(container.dataset.stagger || '80', 10);
    container.querySelectorAll('.reveal').forEach((el, i) => {
      el.style.transitionDelay = (i * step) + 'ms';
    });
  });

  /* ── Team grid stagger (about.html) ────────────────────────
     Members scale/fade in 80ms apart; the second .team row
     starts 200ms after the first row's cascade. */
  document.querySelectorAll('.team').forEach((team, ti) => {
    team.querySelectorAll('.member.reveal').forEach((m, i) => {
      m.style.transitionDelay = (ti * 200 + i * 80) + 'ms';
    });
  });

  /* ── Position cards cascade (positions.html) ───────────────
     Cards drop in 80ms apart, cycling every 6 so cards deep in
     the list never wait more than ~0.5s once visible. */
  document.querySelectorAll('.pos.reveal').forEach((p, i) => {
    p.style.transitionDelay = ((i % 6) * 80) + 'ms';
  });

  /* ── Position filters (positions.html) ─────────────────────
     Filter chips on the Open Positions page show/hide job cards
     by department. The count badge updates to match. */
  const chips = document.querySelectorAll('.chip[data-filter]');
  const posts = document.querySelectorAll('.pos[data-dept]');
  chips.forEach(chip => chip.addEventListener('click', () => {
    chips.forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    const f = chip.dataset.filter;
    posts.forEach(p => p.style.display = (f === 'all' || p.dataset.dept === f) ? '' : 'none');
    const count = document.getElementById('pos-count');
    if (count) {
      const visible = [...posts].filter(p => p.style.display !== 'none').length;
      count.textContent = visible;
    }
  }));
});

/* ============================================================
   2. Interactive Components
   ============================================================ */

/* ── Video Modal ───────────────────────────────────────────────
   Any element with data-vid-trigger opens a fullscreen modal
   containing a <video>. Escape key and backdrop click close it. */
(function () {
  const modal = document.querySelector('.vid-modal');
  if (!modal) return;
  const video = modal.querySelector('video');

  document.querySelectorAll('[data-vid-trigger]').forEach(el => {
    el.addEventListener('click', () => {
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
      if (video && video.src) video.play().catch(() => {});
    });
  });

  const closeModal = () => {
    modal.classList.remove('open');
    document.body.style.overflow = '';
    if (video) { video.pause(); video.currentTime = 0; }
  };

  const closeBtn = modal.querySelector('.vid-modal-close');
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
})();

/* ── Image Accordion ───────────────────────────────────────────
   Panels inside .img-accordion expand on hover via CSS flex
   (flex:1 → flex:4). The "active" class is toggled here;
   the transition lives in CSS (styles.css, .ia-panel). */
(function () {
  document.querySelectorAll('.img-accordion').forEach(acc => {
    const panels = acc.querySelectorAll('.ia-panel');
    panels.forEach(panel => {
      panel.addEventListener('mouseenter', () => {
        panels.forEach(p => p.classList.remove('active'));
        panel.classList.add('active');
      });
    });
    /* Reset to first panel when the mouse leaves the accordion */
    acc.addEventListener('mouseleave', () => {
      panels.forEach(p => p.classList.remove('active'));
      if (panels[0]) panels[0].classList.add('active');
    });
    if (panels[0]) panels[0].classList.add('active');
  });
})();

/* ── Scroll 3D Tilt ────────────────────────────────────────────
   .scroll-3d-card starts tilted (rotateX 22deg, scale 0.94)
   and flattens to 0deg / scale 1 as the user scrolls it into view.
   Uses getBoundingClientRect on every scroll tick (passive listener). */
(function () {
  const cards = document.querySelectorAll('.scroll-3d-card');
  if (!cards.length) return;

  const update = () => {
    cards.forEach(card => {
      const outer = card.closest('.scroll-3d-outer');
      if (!outer) return;
      const rect = outer.getBoundingClientRect();
      const vh = window.innerHeight;
      /* progress: 0 = card at bottom of viewport, 1 = card fully revealed */
      const progress = Math.max(0, Math.min(1, 1 - (rect.top - vh * 0.25) / (vh * 0.65)));
      const angle = 22 * (1 - progress);
      const scale = 0.94 + 0.06 * progress;
      card.style.transform = `rotateX(${angle}deg) scale(${scale})`;
    });
  };

  window.addEventListener('scroll', update, { passive: true });
  update();
})();

/* ── Hover Slideshow ───────────────────────────────────────────
   .hover-slider has a list column (.hs-item) and an image column.
   All videos use autoplay so the browser starts them regardless of
   clip-path visibility. The clip-path transition (CSS) reveals
   whichever video is active. currentTime is reset on reveal so
   each hover starts the clip from the beginning. */
(function () {
  document.querySelectorAll('.hover-slider').forEach(slider => {
    const items = slider.querySelectorAll('.hs-item');
    const imgs = slider.querySelectorAll('.hs-img');

    const activate = idx => {
      items.forEach(i => i.classList.remove('active'));
      imgs.forEach(el => el.classList.remove('active'));
      if (items[idx]) items[idx].classList.add('active');
      if (imgs[idx]) {
        imgs[idx].classList.add('active');
        /* Restart the clip from the top each time it's revealed */
        if (imgs[idx].tagName === 'VIDEO') {
          imgs[idx].currentTime = 0;
          imgs[idx].play().catch(() => {});
        }
      }
    };

    items.forEach((item, i) => {
      item.addEventListener('mouseenter', () => activate(i));
      item.addEventListener('click', () => activate(i));
    });

    activate(0);
  });
})();

/* ── Hero video fade-in ────────────────────────────────────────
   Videos in .hero-img-wrap start at opacity:0 (CSS) to prevent the
   first decoded frame appearing as a static image before playback.
   The .playing class fades them in once the browser actually plays. */
document.querySelectorAll('.hero-img-wrap video').forEach(video => {
  video.addEventListener('playing', () => video.classList.add('playing'), { once: true });
});

/* ── Background hero video playback rate ───────────────────────
   Defaults to 0.6x for a slow cinematic drift; set data-playback-rate="1"
   on the <video> element to play at normal speed. */
document.querySelectorAll('.hero-bg-vid video').forEach(video => {
  const rate = parseFloat(video.dataset.playbackRate ?? 0.6);
  const setRate = () => { video.playbackRate = rate; };
  setRate();
  video.addEventListener('play', setRate);
});

/* ============================================================
   3. Motion System (v5)
   Hero entrance sequence, word reveals, accordion entrance,
   sticky-nav scroll state, page-to-page fade transitions.
   Everything here no-ops under prefers-reduced-motion.
   ============================================================ */

/* Wrap every word of an element in <span class="w"> while
   preserving nested elements (e.g. <span class="gold-text">). */
function splitWords(el) {
  const wrap = node => {
    [...node.childNodes].forEach(child => {
      if (child.nodeType === 3) {
        const frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
          const s = document.createElement('span');
          s.className = 'w';
          s.textContent = part;
          frag.appendChild(s);
        });
        node.replaceChild(frag, child);
      } else if (child.nodeType === 1) {
        wrap(child);
      }
    });
  };
  wrap(el);
  return el.querySelectorAll('.w');
}

/* ── Hero entrance sequence ────────────────────────────────────
   On page load: headline reveals word by word (80ms apart),
   then lead → CTAs (scale 95→100%) → badges → MBE row.
   Total sequence completes in under 2s. */
(function () {
  if (REDUCE_MOTION) return;
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const col = hero.querySelector('.hero-grid > div:first-child') || hero.querySelector(':scope > .wrap');
  if (!col) return;

  const h1 = col.querySelector('h1');
  let wordCount = 0;
  if (h1) {
    h1.classList.add('wsplit');
    const words = splitWords(h1);
    words.forEach((w, i) => { w.style.transitionDelay = (i * 80) + 'ms'; });
    wordCount = words.length;
  }

  const base = Math.min(wordCount * 80, 700);
  const steps = [
    [col.querySelector('.eyebrow'), 0, false],
    [col.querySelector('p.lead'), base + 150, false],
    [col.querySelector('.hero-actions'), base + 350, true],
    [col.querySelector('.hero-badges'), base + 550, false],
    [col.querySelector('.hero-mbe'), base + 700, false],
  ];
  steps.forEach(([el, delay, scale]) => {
    if (!el) return;
    el.classList.add('hseq');
    if (scale) el.classList.add('hseq-scale');
    el.style.transitionDelay = delay + 'ms';
  });

  requestAnimationFrame(() => requestAnimationFrame(() => {
    if (h1) h1.classList.add('in');
    steps.forEach(([el]) => { if (el) el.classList.add('in'); });
  }));
})();

/* ── Scroll-triggered word reveal ──────────────────────────────
   Headings marked class="word-reveal" (e.g. technology.html
   "The Stack" h2) reveal word by word when scrolled into view. */
(function () {
  if (REDUCE_MOTION) return;
  document.querySelectorAll('.word-reveal').forEach(el => {
    el.classList.add('wsplit');
    splitWords(el).forEach((w, i) => { w.style.transitionDelay = (i * 80) + 'ms'; });
    const o = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { el.classList.add('in'); o.unobserve(el); }
    }), { threshold: .4 });
    o.observe(el);
  });
})();

/* ── Image accordion entrance ──────────────────────────────────
   Panels scale 0.85 → 1.0, 100ms apart, on first scroll into
   view. .acc-done then strips the stagger delays so the
   existing hover-expand stays instant. */
(function () {
  document.querySelectorAll('.img-accordion').forEach(acc => {
    const o = new IntersectionObserver(entries => entries.forEach(e => {
      if (!e.isIntersecting) return;
      acc.classList.add('acc-in');
      setTimeout(() => acc.classList.add('acc-done'), 1100);
      o.unobserve(acc);
    }), { threshold: .25 });
    o.observe(acc);
  });
})();

/* ── Sticky nav scroll state ───────────────────────────────────
   After 80px of scroll the header deepens to solid navy with a
   drop shadow (300ms transition in CSS). */
(function () {
  const header = document.querySelector('header.site');
  if (!header) return;
  const update = () => header.classList.toggle('scrolled', window.scrollY > 80);
  window.addEventListener('scroll', update, { passive: true });
  update();
})();

/* ── Page-to-page fade transition ──────────────────────────────
   Internal .html links fade the page out for 200ms before
   navigating; CSS animates the next page in. Modifier-key
   clicks, anchors, and external links pass through untouched. */
(function () {
  if (REDUCE_MOTION) return;
  document.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href || href.includes('#') || a.target === '_blank') return;
    if (/^(https?:|mailto:|tel:)/i.test(href)) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault();
    document.body.classList.add('page-leaving');
    setTimeout(() => { location.href = href; }, 200);
  });
  /* bfcache restore (back button) must never show a faded page */
  window.addEventListener('pageshow', () => document.body.classList.remove('page-leaving'));
})();

/* ============================================================
   4. Homepage Get a Quote form
   ============================================================ */
(function () {
  const card = document.getElementById('quote-card');
  if (!card) return;
  const form = document.getElementById('quote-form');
  const success = card.querySelector('.quote-success');
  const col = card.closest('.reveal');

  /* Submit → success state (demo: no data sent locally; on Netlify
     the data-netlify attribute captures real submissions). */
  form.addEventListener('submit', ev => {
    ev.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    if (REDUCE_MOTION) {
      form.style.display = 'none';
      success.hidden = false;
      success.classList.add('show');
      return;
    }
    form.classList.add('q-out');
    setTimeout(() => {
      form.style.display = 'none';
      success.hidden = false;
      success.classList.add('show');
    }, 300);
  });

  /* "Submit another request" → reset and replay the field cascade */
  card.querySelector('.qs-reset').addEventListener('click', () => {
    form.reset();
    success.classList.remove('show');
    success.hidden = true;
    form.classList.remove('q-out');
    form.style.display = '';
    if (!REDUCE_MOTION && col) {
      col.classList.remove('in');
      void col.offsetWidth; /* force reflow so the cascade replays */
      col.classList.add('in');
    }
  });

  /* Map awareness: when origin + destination are filled, draw the
     lane on the map (known cities) or pulse the Chicago HQ ping. */
  const CITY_LOOKUP = {
    'chicago': [-87.6298, 41.8781], 'milwaukee': [-87.9065, 43.0389],
    'indianapolis': [-86.1581, 39.7684], 'st louis': [-90.1994, 38.6270],
    'st. louis': [-90.1994, 38.6270], 'detroit': [-83.0458, 42.3314],
    'columbus': [-82.9988, 39.9612], 'minneapolis': [-93.2650, 44.9778],
    'kansas city': [-94.5786, 39.0997], 'memphis': [-90.0490, 35.1495],
    'nashville': [-86.7816, 36.1627], 'cleveland': [-81.6944, 41.4993],
    'new york': [-74.0060, 40.7128], 'los angeles': [-118.2437, 34.0522],
    'dallas': [-96.7970, 32.7767], 'houston': [-95.3698, 29.7604],
    'atlanta': [-84.3880, 33.7490], 'denver': [-104.9903, 39.7392],
    'seattle': [-122.3321, 47.6062], 'phoenix': [-112.0740, 33.4484],
    'miami': [-80.1918, 25.7617], 'boston': [-71.0589, 42.3601],
    'philadelphia': [-75.1652, 39.9526], 'charlotte': [-80.8431, 35.2271],
    'pittsburgh': [-79.9959, 40.4406], 'baltimore': [-76.6122, 39.2904],
    'washington': [-77.0369, 38.9072], 'tampa': [-82.4572, 27.9506],
    'orlando': [-81.3792, 28.5383], 'jacksonville': [-81.6557, 30.3322],
    'cincinnati': [-84.5120, 39.1031], 'louisville': [-85.7585, 38.2527],
    'new orleans': [-90.0715, 29.9511], 'oklahoma city': [-97.5164, 35.4676],
    'omaha': [-95.9345, 41.2565], 'des moines': [-93.6250, 41.5868],
    'salt lake city': [-111.8910, 40.7608], 'las vegas': [-115.1398, 36.1699],
    'portland': [-122.6765, 45.5231], 'san francisco': [-122.4194, 37.7749],
    'san diego': [-117.1611, 32.7157], 'sacramento': [-121.4944, 38.5816],
    'austin': [-97.7431, 30.2672], 'san antonio': [-98.4936, 29.4241],
    'el paso': [-106.4850, 31.7619], 'albuquerque': [-106.6504, 35.0844],
    'buffalo': [-78.8784, 42.8864], 'richmond': [-77.4360, 37.5407],
    'raleigh': [-78.6382, 35.7796], 'birmingham': [-86.8025, 33.5207],
    'little rock': [-92.2896, 34.7465], 'boise': [-116.2023, 43.6150],
    'fargo': [-96.7898, 46.8772], 'tucson': [-110.9747, 32.2226],
  };

  function geocode(text) {
    const t = text.toLowerCase().trim();
    if (t.length < 3) return null;
    for (const key in CITY_LOOKUP) {
      if (t.startsWith(key) || t.includes(key)) return CITY_LOOKUP[key];
    }
    return null;
  }

  let pingMarker = null;
  let routeAnim = null;

  function clearMapResponse(map) {
    if (pingMarker) { pingMarker.remove(); pingMarker = null; }
    if (routeAnim) { cancelAnimationFrame(routeAnim); routeAnim = null; }
    if (map.getLayer('quote-route')) map.removeLayer('quote-route');
    if (map.getSource('quote-route')) map.removeSource('quote-route');
  }

  function updateMapResponse() {
    const map = window.__jaMap;
    if (!map || !window.__jaMapReady) return;
    const o = document.getElementById('q-origin').value;
    const d = document.getElementById('q-dest').value;
    clearMapResponse(map);
    if (o.trim().length < 3 || d.trim().length < 3) return;

    const oc = geocode(o), dc = geocode(d);
    if (oc && dc) {
      /* Animated lane: route line draws itself origin → destination */
      const data = {
        type: 'Feature', properties: {},
        geometry: { type: 'LineString', coordinates: [oc, oc] }
      };
      map.addSource('quote-route', { type: 'geojson', data });
      map.addLayer({
        id: 'quote-route', type: 'line', source: 'quote-route',
        layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: { 'line-color': '#FFC20D', 'line-width': 3, 'line-opacity': 0.9 }
      });
      const start = performance.now();
      const draw = now => {
        const t = REDUCE_MOTION ? 1 : Math.min((now - start) / 1000, 1);
        const e = 1 - Math.pow(1 - t, 3);
        data.geometry.coordinates = [oc, [oc[0] + (dc[0] - oc[0]) * e, oc[1] + (dc[1] - oc[1]) * e]];
        map.getSource('quote-route').setData(data);
        if (t < 1) routeAnim = requestAnimationFrame(draw);
      };
      routeAnim = requestAnimationFrame(draw);
      const el = document.createElement('div');
      el.className = 'ja-ping';
      pingMarker = new maplibregl.Marker({ element: el, anchor: 'center' }).setLngLat(dc).addTo(map);
      map.fitBounds([oc, dc], { padding: 80, duration: REDUCE_MOTION ? 0 : 900, maxZoom: 6 });
    } else {
      /* Unknown lane: pulse the Chicago HQ so map + form feel connected */
      const el = document.createElement('div');
      el.className = 'ja-ping';
      pingMarker = new maplibregl.Marker({ element: el, anchor: 'center' })
        .setLngLat([-87.6298, 41.8781]).addTo(map);
    }
  }

  let debounce;
  ['q-origin', 'q-dest'].forEach(id => {
    document.getElementById(id).addEventListener('input', () => {
      clearTimeout(debounce);
      debounce = setTimeout(updateMapResponse, 450);
    });
  });
})();

/* ============================================================
   Chicago Service Reach Map (MapLibre GL JS)
   ============================================================ */
(function () {
  if (!document.getElementById('ja-map')) return;

  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css';
  document.head.appendChild(css);

  const js = document.createElement('script');
  js.src = 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js';
  js.onload = initJAMap;
  document.head.appendChild(js);
})();

function initJAMap() {
  const CHICAGO = [-87.6298, 41.8781];

  const map = new maplibregl.Map({
    container: 'ja-map',
    style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
    center: [-96, 38.5],
    zoom: 4.0,
    attributionControl: false,
    pitchWithRotate: false,
    dragRotate: false,
  });

  const serviceCities = [
    { name: 'Milwaukee, WI',    coords: [-87.9065, 43.0389] },
    { name: 'Indianapolis, IN', coords: [-86.1581, 39.7684] },
    { name: 'St. Louis, MO',    coords: [-90.1994, 38.6270] },
    { name: 'Detroit, MI',      coords: [-83.0458, 42.3314] },
    { name: 'Columbus, OH',     coords: [-82.9988, 39.9612] },
    { name: 'Minneapolis, MN',  coords: [-93.2650, 44.9778] },
    { name: 'Kansas City, MO',  coords: [-94.5786, 39.0997] },
    { name: 'Memphis, TN',      coords: [-90.0490, 35.1495] },
    { name: 'Nashville, TN',    coords: [-86.7816, 36.1627] },
    { name: 'Cleveland, OH',    coords: [-81.6944, 41.4993] },
    { name: 'New York, NY',     coords: [-74.0060, 40.7128] },
    { name: 'Los Angeles, CA',  coords: [-118.2437, 34.0522] },
    { name: 'Houston, TX',      coords: [-95.3698, 29.7604] },
  ];

  window.__jaMap = map;
  map.on('load', function () {
    window.__jaMapReady = true;
    /* Route lines */
    serviceCities.forEach(function (city, i) {
      map.addSource('route-' + i, {
        type: 'geojson',
        data: {
          type: 'Feature', properties: {},
          geometry: { type: 'LineString', coordinates: [CHICAGO, city.coords] }
        }
      });
      map.addLayer({
        id: 'route-' + i,
        type: 'line',
        source: 'route-' + i,
        layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: {
          'line-color': '#FFC20D',
          'line-width': 1.5,
          'line-opacity': 0.32,
          'line-dasharray': [4, 5]
        }
      });
    });

    /* City markers */
    serviceCities.forEach(function (city) {
      const el = document.createElement('div');
      el.className = 'ja-city-marker';
      el.innerHTML = '<span></span>';
      new maplibregl.Marker({ element: el, anchor: 'center' })
        .setLngLat(city.coords)
        .setPopup(
          new maplibregl.Popup({ offset: 14, closeButton: false, closeOnClick: true })
            .setHTML('<div class="ja-popup"><strong>' + city.name + '</strong><small>J&A Service Hub</small></div>')
        )
        .addTo(map);
    });

    /* Chicago HQ marker */
    const hub = document.createElement('div');
    hub.className = 'ja-hub-marker';
    hub.innerHTML = '<span>HQ</span>';
    new maplibregl.Marker({ element: hub, anchor: 'center' })
      .setLngLat(CHICAGO)
      .setPopup(
        new maplibregl.Popup({ offset: 26, closeButton: false, closeOnClick: true })
          .setHTML('<div class="ja-popup"><strong>Chicago, IL</strong><small>J&A Freight Systems HQ — Est. 1986</small></div>')
      )
      .addTo(map);
  });
}
