/* ============================================================
   QUIET FORCE STUDIO — Script
   ============================================================ */

/* LOADER */
const loader = document.getElementById('loader');
const loaderFill = document.getElementById('loaderFill');
let lp = 0;
document.body.style.overflow = 'hidden';
const li = setInterval(() => {
  lp += Math.random() * 16;
  if (lp >= 100) { lp = 100; clearInterval(li); setTimeout(endLoad, 350); }
  if (loaderFill) loaderFill.style.width = lp + '%';
}, 90);
function endLoad() {
  loader.classList.add('out');
  document.body.style.overflow = '';
  initParticles();
  initWave();
}

/* CURSOR */
const cur = document.getElementById('cursor');
const ring = document.getElementById('cursorRing');
let mx = 0, my = 0, rx = 0, ry = 0;
if (window.matchMedia('(hover:hover)').matches) {
  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cur.style.left = mx + 'px'; cur.style.top = my + 'px';
  });
  (function loop() {
    rx += (mx - rx) * 0.13; ry += (my - ry) * 0.13;
    ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
    requestAnimationFrame(loop);
  })();
  document.querySelectorAll('a,button,.feature,.pack,.plan,.g-item,.booking-line').forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('on'));
    el.addEventListener('mouseleave', () => ring.classList.remove('on'));
  });
}

/* NAV */
const nav = document.getElementById('nav');
addEventListener('scroll', () => nav.classList.toggle('stuck', scrollY > 50), { passive: true });

const burger = document.getElementById('burger');
const mob = document.getElementById('mobMenu');
let open = false;
burger.addEventListener('click', () => {
  open = !open;
  mob.classList.toggle('open', open);
  const s = burger.querySelectorAll('span');
  s[0].style.transform = open ? 'translateY(7px) rotate(45deg)' : '';
  s[1].style.transform = open ? 'translateY(-7px) rotate(-45deg)' : '';
});
document.querySelectorAll('.mob-link').forEach(l => l.addEventListener('click', () => {
  open = false; mob.classList.remove('open');
  burger.querySelectorAll('span').forEach(x => x.style.transform = '');
}));

/* FAQ ACCORDION */
document.querySelectorAll('.faq-item').forEach(item => {
  const q = item.querySelector('.faq-q');
  const a = item.querySelector('.faq-a');
  q.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(o => {
      o.classList.remove('open');
      o.querySelector('.faq-a').style.maxHeight = null;
    });
    if (!isOpen) {
      item.classList.add('open');
      a.style.maxHeight = a.scrollHeight + 'px';
    }
  });
});

/* REVEAL */
const io = new IntersectionObserver(es => {
  es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

/* SMOOTH SCROLL */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

/* HERO ORB PARALLAX */
addEventListener('mousemove', e => {
  const x = (e.clientX / innerWidth - 0.5) * 30;
  const y = (e.clientY / innerHeight - 0.5) * 30;
  const o1 = document.querySelector('.o1'), o2 = document.querySelector('.o2');
  if (o1) o1.style.transform = `translate(${x * 0.4}px,${y * 0.4}px)`;
  if (o2) o2.style.transform = `translate(${-x * 0.3}px,${-y * 0.3}px)`;
}, { passive: true });

/* PARTICLE FIELD (subtle, behind hero veil is fine — drawn on a fixed canvas appended) */
function initParticles() {
  const hero = document.getElementById('hero');
  if (!hero) return;
  const c = document.createElement('canvas');
  c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none;opacity:.5';
  hero.querySelector('.hero-media').appendChild(c);
  const ctx = c.getContext('2d');
  let W, H, ps = [];
  function resize() { W = c.width = hero.offsetWidth; H = c.height = hero.offsetHeight; }
  resize(); addEventListener('resize', resize);
  for (let i = 0; i < 60; i++) ps.push({
    x: Math.random() * W, y: Math.random() * H,
    vx: (Math.random() - .5) * .25, vy: (Math.random() - .5) * .25,
    r: Math.random() * 1.6 + .4,
    c: Math.random() > .6 ? '255,107,53' : '255,255,255',
    a: Math.random() * .4 + .1
  });
  (function draw() {
    ctx.clearRect(0, 0, W, H);
    ps.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 7);
      ctx.fillStyle = `rgba(${p.c},${p.a})`; ctx.fill();
    });
    for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) {
      const dx = ps[i].x - ps[j].x, dy = ps[i].y - ps[j].y, d = Math.hypot(dx, dy);
      if (d < 120) {
        ctx.beginPath(); ctx.moveTo(ps[i].x, ps[i].y); ctx.lineTo(ps[j].x, ps[j].y);
        ctx.strokeStyle = `rgba(255,107,53,${.05 * (1 - d / 120)})`; ctx.lineWidth = .5; ctx.stroke();
      }
    }
    requestAnimationFrame(draw);
  })();
}

/* placeholder hook (no mini wave element in this design) */
function initWave() {}
