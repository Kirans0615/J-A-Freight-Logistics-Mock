/* J&A Freight Systems — shared interactions */
document.addEventListener('DOMContentLoaded', () => {

  /* Mobile nav */
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('nav.main');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
    });
  }

  /* Active nav link */
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav.main a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });

  /* Scroll reveal */
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  /* Count-up stats */
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

  /* FAQ accordion */
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      item.parentElement.querySelectorAll('.faq-item.open').forEach(o => { if (o !== item) o.classList.remove('open'); });
      item.classList.toggle('open');
    });
  });

  /* Forms — client-side confirmation (wire to Formspree/backend for production) */
  document.querySelectorAll('form[data-demo]').forEach(form => {
    form.addEventListener('submit', ev => {
      ev.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      const ok = form.querySelector('.form-success');
      if (ok) { ok.classList.add('show'); ok.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
      form.querySelectorAll('input,select,textarea').forEach(f => f.value = '');
    });
  });

  /* Parallax photo bands */
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

  /* Stagger delays for grid children */
  document.querySelectorAll('.stagger').forEach(container => {
    container.querySelectorAll('.reveal').forEach((el, i) => {
      el.style.transitionDelay = (i * 80) + 'ms';
    });
  });

  /* Position filters */
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
