/* ============================================================
   QUIET FORCE STUDIO — Motion System
   Crafted interactions: line reveals, scroll-clip, magnetic,
   velocity marquee, parallax. Vanilla, 60fps, restrained.
   ============================================================ */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
  const hover = matchMedia('(hover:hover)').matches;

  /* ---------- LOADER ---------- */
  const loader = document.getElementById('loader');
  const fill = document.getElementById('loaderFill');
  let p = 0;
  document.body.style.overflow = 'hidden';
  const tick = setInterval(() => {
    p += Math.random() * 15 + 4;
    if (p >= 100) { p = 100; clearInterval(tick); setTimeout(reveal, 380); }
    if (fill) fill.style.width = p + '%';
  }, 95);

  function reveal() {
    loader.classList.add('out');
    document.body.style.overflow = '';
    // fire hero line masks
    document.querySelectorAll('.hero .line-mask').forEach((m, i) => {
      setTimeout(() => m.classList.add('in'), 60 + i * 110);
    });
    document.querySelector('.hero-badge')?.style.setProperty('animation-delay', '0s');
    startParticles();
  }

  /* ---------- CURSOR ---------- */
  const cur = document.getElementById('cursor');
  const ring = document.getElementById('cursorRing');
  if (hover && cur && ring) {
    let mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
    addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; cur.style.left = mx + 'px'; cur.style.top = my + 'px'; });
    (function l() { rx += (mx - rx) * .15; ry += (my - ry) * .15; ring.style.left = rx + 'px'; ring.style.top = ry + 'px'; requestAnimationFrame(l); })();
    document.querySelectorAll('a,button,.feature,.pack,.plan,.g-item,.booking-line,.faq-q').forEach(el => {
      el.addEventListener('mouseenter', () => ring.classList.add('on'));
      el.addEventListener('mouseleave', () => ring.classList.remove('on'));
    });
  }

  /* ---------- NAV ---------- */
  const nav = document.getElementById('nav');
  addEventListener('scroll', () => nav.classList.toggle('stuck', scrollY > 50), { passive: true });

  const burger = document.getElementById('burger');
  const mob = document.getElementById('mobMenu');
  let open = false;
  burger?.addEventListener('click', () => {
    open = !open; mob.classList.toggle('open', open);
    const s = burger.querySelectorAll('span');
    s[0].style.transform = open ? 'translateY(7px) rotate(45deg)' : '';
    s[1].style.transform = open ? 'translateY(-7px) rotate(-45deg)' : '';
  });
  document.querySelectorAll('.mob-link').forEach(a => a.addEventListener('click', () => {
    open = false; mob.classList.remove('open');
    burger.querySelectorAll('span').forEach(x => x.style.transform = '');
  }));

  /* ---------- REVEAL + LINE MASKS (scroll) ---------- */
  const io = new IntersectionObserver((es) => {
    es.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      el.classList.add('in');
      // auto-stagger sibling reveals sharing a parent grid
      io.unobserve(el);
    });
  }, { threshold: .14, rootMargin: '0px 0px -8% 0px' });

  document.querySelectorAll('.reveal, .g-item').forEach(el => io.observe(el));

  // line masks outside the hero (e.g. hero-p already fired by loader; observe section titles if wrapped later)
  const maskIO = new IntersectionObserver((es) => {
    es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); maskIO.unobserve(e.target); } });
  }, { threshold: .3 });
  document.querySelectorAll('.line-mask').forEach(m => { if (!m.closest('.hero')) maskIO.observe(m); });

  /* ---------- MAGNETIC BUTTONS ---------- */
  if (hover) {
    document.querySelectorAll('[data-magnetic]').forEach(btn => {
      const strength = 0.4;
      btn.addEventListener('mousemove', e => {
        const r = btn.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * strength;
        const y = (e.clientY - r.top - r.height / 2) * strength;
        btn.style.transform = `translate(${x}px,${y}px)`;
      });
      btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
    });
  }

  /* ---------- FAQ ---------- */
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-q'), a = item.querySelector('.faq-a');
    q.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(o => { o.classList.remove('open'); o.querySelector('.faq-a').style.maxHeight = null; });
      if (!isOpen) { item.classList.add('open'); a.style.maxHeight = a.scrollHeight + 'px'; }
    });
  });

  /* ---------- SMOOTH ANCHOR ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  }));

  /* ---------- SCROLL-DRIVEN: parallax + marquee velocity ---------- */
  const marqueeTrack = document.querySelector('.marquee-track');
  if (marqueeTrack && !reduce) {
    marqueeTrack.style.animation = 'none';
    const w = () => marqueeTrack.scrollWidth / 2;
    let lastY = scrollY, vel = 0, shift = 0;
    (function frame() {
      const y = scrollY;
      vel += ((y - lastY) - vel) * .2; lastY = y;
      shift += 0.4 + Math.min(Math.abs(vel) * 0.25, 14);
      marqueeTrack.style.transform = `translateX(${-(shift % w())}px)`;
      requestAnimationFrame(frame);
    })();
  }

  /* ---------- HERO PARTICLES (depth field) ---------- */
  function startParticles() {
    if (reduce) return;
    const hero = document.getElementById('hero');
    const media = hero?.querySelector('.hero-media');
    if (!media) return;
    const c = document.createElement('canvas');
    c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none;opacity:.55';
    media.appendChild(c);
    const ctx = c.getContext('2d');
    let W, H, ps = [];
    const resize = () => { W = c.width = hero.offsetWidth; H = c.height = hero.offsetHeight; };
    resize(); addEventListener('resize', resize);
    for (let i = 0; i < 64; i++) ps.push({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - .5) * .22, vy: (Math.random() - .5) * .22,
      r: Math.random() * 1.5 + .4,
      col: Math.random() > .6 ? '255,107,53' : '255,255,255',
      a: Math.random() * .4 + .08
    });
    (function draw() {
      ctx.clearRect(0, 0, W, H);
      for (const p of ps) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283);
        ctx.fillStyle = `rgba(${p.col},${p.a})`; ctx.fill();
      }
      for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) {
        const dx = ps[i].x - ps[j].x, dy = ps[i].y - ps[j].y, d = Math.hypot(dx, dy);
        if (d < 120) { ctx.beginPath(); ctx.moveTo(ps[i].x, ps[i].y); ctx.lineTo(ps[j].x, ps[j].y); ctx.strokeStyle = `rgba(255,107,53,${.045 * (1 - d / 120)})`; ctx.lineWidth = .5; ctx.stroke(); }
      }
      requestAnimationFrame(draw);
    })();
  }
})();
