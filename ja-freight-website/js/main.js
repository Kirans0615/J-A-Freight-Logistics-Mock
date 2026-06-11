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
