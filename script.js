/* ============================================================
   IA-ONE — Script v2
   ============================================================ */

/* ================================================================
   LOADER
   ================================================================ */
const loader = document.getElementById('loader');
const loaderFill = document.getElementById('loaderFill');
let loadPct = 0;

const loadInterval = setInterval(() => {
  loadPct += Math.random() * 18;
  if (loadPct >= 100) { loadPct = 100; clearInterval(loadInterval); finishLoad(); }
  loaderFill.style.width = loadPct + '%';
}, 80);

function finishLoad() {
  setTimeout(() => {
    loader.classList.add('hidden');
    document.body.style.overflow = '';
    initAnimations();
  }, 300);
}

document.body.style.overflow = 'hidden';

/* ================================================================
   CURSOR
   ================================================================ */
const cursor = document.getElementById('cursor');
const follower = document.getElementById('cursorFollower');
const cursorLabel = document.getElementById('cursorLabel');
let mx = 0, my = 0, fx = 0, fy = 0;

if (window.matchMedia('(hover:hover)').matches) {
  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cursor.style.left = mx + 'px'; cursor.style.top = my + 'px';
  });
  (function animCursor() {
    fx += (mx - fx) * 0.1; fy += (my - fy) * 0.1;
    follower.style.left = fx + 'px'; follower.style.top = fy + 'px';
    requestAnimationFrame(animCursor);
  })();

  document.querySelectorAll('a, button, .ep-row, .guest-card, .platform-card, .value-card').forEach(el => {
    el.addEventListener('mouseenter', () => {
      follower.classList.add('hovering');
      const label = el.dataset.cursor || '';
      cursorLabel.textContent = label;
    });
    el.addEventListener('mouseleave', () => {
      follower.classList.remove('hovering');
      cursorLabel.textContent = '';
    });
  });
}

/* ================================================================
   NAV
   ================================================================ */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

const burger = document.getElementById('navBurger');
const mobileMenu = document.getElementById('mobileMenu');
let menuOpen = false;

burger.addEventListener('click', () => {
  menuOpen = !menuOpen;
  mobileMenu.classList.toggle('open', menuOpen);
  const spans = burger.querySelectorAll('span');
  spans[0].style.transform = menuOpen ? 'translateY(6.5px) rotate(45deg)' : '';
  spans[1].style.transform = menuOpen ? 'translateY(-6.5px) rotate(-45deg)' : '';
});
document.querySelectorAll('.mobile-link').forEach(l => l.addEventListener('click', () => {
  menuOpen = false; mobileMenu.classList.remove('open');
  burger.querySelectorAll('span').forEach(s => s.style.transform = '');
}));

/* ================================================================
   HERO CANVAS (particle field)
   ================================================================ */
function initCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * W;
      this.y = Math.random() * H;
      this.vx = (Math.random() - 0.5) * 0.3;
      this.vy = (Math.random() - 0.5) * 0.3;
      this.r = Math.random() * 1.5 + 0.5;
      this.alpha = Math.random() * 0.5 + 0.1;
      this.color = Math.random() > 0.7 ? '200,255,0' : '255,255,255';
    }
    update() {
      this.x += this.vx; this.y += this.vy;
      if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color},${this.alpha})`;
      ctx.fill();
    }
  }

  for (let i = 0; i < 80; i++) particles.push(new Particle());

  function drawLines() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 100) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(200,255,0,${0.06 * (1 - d / 100)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => { p.update(); p.draw(); });
    drawLines();
    requestAnimationFrame(animate);
  }
  animate();
}

/* ================================================================
   WAVEFORM (mini hero canvas)
   ================================================================ */
function drawMiniWave() {
  const canvas = document.getElementById('miniWave');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const bars = 52;
  const heights = Array.from({length: bars}, () => 4 + Math.random() * 28);

  function draw(progress = 0.3) {
    ctx.clearRect(0, 0, W, H);
    const bw = W / bars;
    for (let i = 0; i < bars; i++) {
      const h = heights[i];
      const x = i * bw + bw * 0.2;
      const w = bw * 0.55;
      const isActive = i / bars <= progress;
      ctx.fillStyle = isActive ? 'rgba(200,255,0,0.9)' : 'rgba(255,255,255,0.15)';
      ctx.beginPath();
      ctx.roundRect(x, (H - h) / 2, w, h, 2);
      ctx.fill();
    }
  }
  draw(0.3);
  return { draw, heights };
}

/* ================================================================
   AUDIO PLAYER STATE
   ================================================================ */
const EPISODES = [
  { num: 12, title: "L'IA va-t-elle tuer le motion design ?", guest: "Marie Fontaine", duration: 52 * 60 },
  { num: 11, title: "Motion design & branding : identité qui bouge", guest: "Thomas Mayer", duration: 44 * 60 },
  { num: 10, title: "Freelance en motion : survivre en 2026", guest: "Sarah Dumas", duration: 38 * 60 },
  { num: 9,  title: "After Effects ou pas : quel logiciel ?", guest: "Antoine Leblanc", duration: 61 * 60 },
  { num: 8,  title: "Les coulisses d'un studio parisien", guest: "Romain Chevalier", duration: 47 * 60 },
  { num: 7,  title: "Design génératif : le code comme pinceau", guest: "Julie Bernard", duration: 55 * 60 },
  { num: 6,  title: "Pitcher un projet motion à un client", guest: "Nina Petit", duration: 49 * 60 },
  { num: 5,  title: "Son & motion : le rôle du sound design", guest: "Kevin Vidal", duration: 42 * 60 },
];

let currentEp = 0;
let isPlaying = false;
let progress = 0;
let playInterval = null;
let speeds = [1, 1.25, 1.5, 2];
let speedIdx = 0;

const player = document.getElementById('player');
const pPlay = document.getElementById('pPlay');
const pPlayIcon = document.getElementById('pPlayIcon');
const pPauseIcon = document.getElementById('pPauseIcon');
const pCurrent = document.getElementById('pCurrent');
const playerFill = document.getElementById('playerFill');
const playerBar = document.getElementById('playerBar');
const playerTitle = document.getElementById('playerTitle');
const playerEp = document.getElementById('playerEp');
const pClose = document.getElementById('pClose');
const speedBtn = document.getElementById('speedBtn');
const volRange = document.getElementById('volRange');
const vinylEl = document.getElementById('vinyl');
const vinylArm = document.getElementById('vinylArm');

let miniWaveCtrl = null;
const epProgress = document.getElementById('epProgress');

function loadEpisode(idx) {
  currentEp = idx;
  progress = 0;
  const ep = EPISODES[idx];
  playerTitle.textContent = ep.title;
  playerEp.textContent = `IA—ONE · Épisode ${ep.num}`;
  document.querySelector('.player-thumb').textContent = ep.num;
  playerFill.style.width = '0%';
  pCurrent.textContent = '0:00';
}

function openPlayer(epIdx = 0) {
  loadEpisode(epIdx);
  player.classList.add('visible');
}

function togglePlay() {
  isPlaying = !isPlaying;
  pPlayIcon.style.display = isPlaying ? 'none' : 'block';
  pPauseIcon.style.display = isPlaying ? 'block' : 'none';

  // Sync hero mini play
  const mpi = document.getElementById('miniPlayIcon');
  const mpa = document.getElementById('miniPauseIcon');
  if (mpi) mpi.style.display = isPlaying ? 'none' : 'block';
  if (mpa) mpa.style.display = isPlaying ? 'block' : 'none';

  if (vinylEl) {
    vinylEl.style.animationPlayState = isPlaying ? 'running' : 'paused';
    if (vinylArm) vinylArm.classList.toggle('playing', isPlaying);
  }

  if (isPlaying) {
    playInterval = setInterval(() => {
      const ep = EPISODES[currentEp];
      progress = Math.min(progress + 1, ep.duration);
      const pct = (progress / ep.duration) * 100;
      playerFill.style.width = pct + '%';
      if (epProgress) epProgress.style.width = pct + '%';
      const m = Math.floor(progress / 60), s = progress % 60;
      pCurrent.textContent = `${m}:${s.toString().padStart(2,'0')}`;
      if (miniWaveCtrl) miniWaveCtrl.draw(pct / 100);
    }, 1000 / speeds[speedIdx]);
  } else {
    clearInterval(playInterval);
  }
}

if (pPlay) pPlay.addEventListener('click', togglePlay);

document.getElementById('pPrev')?.addEventListener('click', () => {
  if (currentEp < EPISODES.length - 1) {
    loadEpisode(currentEp + 1);
    if (isPlaying) { clearInterval(playInterval); isPlaying = false; togglePlay(); }
  }
});
document.getElementById('pNext')?.addEventListener('click', () => {
  if (currentEp > 0) {
    loadEpisode(currentEp - 1);
    if (isPlaying) { clearInterval(playInterval); isPlaying = false; togglePlay(); }
  }
});

if (speedBtn) {
  speedBtn.addEventListener('click', () => {
    speedIdx = (speedIdx + 1) % speeds.length;
    speedBtn.textContent = speeds[speedIdx] + '×';
    if (isPlaying) { clearInterval(playInterval); isPlaying = false; togglePlay(); }
  });
}

if (pClose) {
  pClose.addEventListener('click', () => {
    player.classList.remove('visible');
    if (isPlaying) togglePlay();
  });
}

if (playerBar) {
  playerBar.addEventListener('click', e => {
    const r = playerBar.getBoundingClientRect();
    const pct = (e.clientX - r.left) / r.width;
    progress = Math.floor(pct * EPISODES[currentEp].duration);
    playerFill.style.width = (pct * 100) + '%';
    if (epProgress) epProgress.style.width = (pct * 100) + '%';
  });
}

if (volRange) volRange.addEventListener('input', () => {});

// All play triggers
document.querySelectorAll('[id^="featuredPlayBtn"], #featuredPlay, #miniPlay, #heroPlayBtn').forEach(btn => {
  btn?.addEventListener('click', () => {
    openPlayer(0);
    if (!isPlaying) togglePlay();
  });
});

document.querySelectorAll('.ep-row-play').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const epNum = parseInt(btn.dataset.ep);
    const idx = EPISODES.findIndex(e => e.num === epNum);
    openPlayer(idx >= 0 ? idx : 0);
    if (!isPlaying) togglePlay();
  });
});

document.querySelectorAll('.ep-row').forEach(row => {
  row.addEventListener('click', () => {
    const epNum = parseInt(row.dataset.ep || 12);
    const idx = EPISODES.findIndex(e => e.num === epNum);
    openPlayer(idx >= 0 ? idx : 0);
    if (!isPlaying) togglePlay();
  });
});

document.querySelectorAll('.gc-play').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const card = btn.closest('.guest-card');
    const epNum = parseInt(card?.dataset.ep || 12);
    const idx = EPISODES.findIndex(e => e.num === epNum);
    openPlayer(idx >= 0 ? idx : 0);
    if (!isPlaying) togglePlay();
  });
});

/* ================================================================
   COUNTER ANIMATION
   ================================================================ */
function animCounter(el, target, suffix = '') {
  const start = performance.now();
  const dur = 2200;
  function tick(now) {
    const t = Math.min((now - start) / dur, 1);
    const ease = 1 - Math.pow(1 - t, 4);
    const val = Math.round(target * ease);
    const display = val >= 1000 ? (val / 1000).toFixed(1) + 'k' : val;
    el.textContent = display;
    if (t < 1) requestAnimationFrame(tick);
    else el.textContent = target >= 1000 ? (target / 1000).toFixed(1) + 'k' : target;
  }
  requestAnimationFrame(tick);
}

/* ================================================================
   INTERSECTION OBSERVER
   ================================================================ */
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

const counterObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      animCounter(e.target, parseInt(e.target.dataset.target));
      counterObs.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-num[data-target]').forEach(el => counterObs.observe(el));

/* ================================================================
   EPISODE FILTERS
   ================================================================ */
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('.ep-row').forEach(row => {
      const tags = row.dataset.tags || '';
      row.classList.toggle('hidden', filter !== 'all' && !tags.includes(filter));
    });
  });
});

/* ================================================================
   LOAD MORE
   ================================================================ */
document.getElementById('loadMore')?.addEventListener('click', function() {
  document.querySelectorAll('.ep-row.hidden').forEach(r => r.classList.remove('hidden'));
  this.parentElement.style.display = 'none';
});

/* ================================================================
   NEWSLETTER
   ================================================================ */
document.getElementById('nlForm')?.addEventListener('submit', e => {
  e.preventDefault();
  const btn = e.target.querySelector('.nl-btn');
  const input = e.target.querySelector('.nl-input');
  btn.textContent = '✓ Abonné !';
  btn.style.background = '#22c55e';
  btn.style.boxShadow = '0 0 20px rgba(34,197,94,0.3)';
  input.value = '';
  setTimeout(() => {
    btn.textContent = 'S\'abonner gratuitement';
    btn.style.background = '';
    btn.style.boxShadow = '';
  }, 4000);
});

/* ================================================================
   SMOOTH SCROLL
   ================================================================ */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

/* ================================================================
   PARALLAX ORBS
   ================================================================ */
document.addEventListener('mousemove', e => {
  const x = (e.clientX / window.innerWidth - 0.5) * 30;
  const y = (e.clientY / window.innerHeight - 0.5) * 30;
  document.querySelector('.hero-orb-1')?.style.setProperty('transform', `translate(${x * 0.4}px, ${y * 0.4}px)`);
  document.querySelector('.hero-orb-2')?.style.setProperty('transform', `translate(${-x * 0.25}px, ${-y * 0.25}px)`);
  document.querySelector('.hero-orb-3')?.style.setProperty('transform', `translate(${x * 0.6}px, ${y * 0.6}px)`);
}, { passive: true });

/* ================================================================
   INIT ALL
   ================================================================ */
function initAnimations() {
  initCanvas();
  miniWaveCtrl = drawMiniWave();
}

// Fallback if loader finishes very fast
if (document.readyState === 'complete') initAnimations();
else window.addEventListener('load', () => {
  if (loadPct < 100) return;
  initAnimations();
});
