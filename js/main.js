/* ============================================================
   J&A Freight Systems — main.js
   Shared JavaScript for all 8 pages of the static site.
   No external dependencies — pure vanilla JS.

   Sections:
     1. DOMContentLoaded  — nav, reveal, stats, FAQ, forms, parallax
     2. Interactive Components — Image Accordion, Scroll 3D, Hover Slideshow
     3. Chicago Service Reach Map (MapLibre GL JS, loaded on demand)
   ============================================================ */

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
    if (a.getAttribute('href') === page) a.classList.add('active');
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
      const dur = 1400, t0 = performance.now();
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
     children in sequence (80ms apart) for a cascade effect. */
  document.querySelectorAll('.stagger').forEach(container => {
    container.querySelectorAll('.reveal').forEach((el, i) => {
      el.style.transitionDelay = (i * 80) + 'ms';
    });
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
    center: [-89.8, 41.9],
    zoom: 5.8,
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
  ];

  map.on('load', function () {
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
