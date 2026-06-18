/* ============================================================
   IA-ONE — Script
   ============================================================ */

/* ---- CURSOR ---- */
const cursor = document.getElementById('cursor');
const follower = document.getElementById('cursorFollower');
let mx = 0, my = 0, fx = 0, fy = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cursor.style.left = mx + 'px';
  cursor.style.top = my + 'px';
});

function animFollower() {
  fx += (mx - fx) * 0.12;
  fy += (my - fy) * 0.12;
  follower.style.left = fx + 'px';
  follower.style.top = fy + 'px';
  requestAnimationFrame(animFollower);
}
animFollower();

document.querySelectorAll('a, button, .ep-card, .platform-card, .guest-card, .value-card').forEach(el => {
  el.addEventListener('mouseenter', () => follower.classList.add('hovered'));
  el.addEventListener('mouseleave', () => follower.classList.remove('hovered'));
});

/* ---- NAV ---- */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 50);
}, { passive: true });

/* ---- MOBILE MENU ---- */
const burger = document.getElementById('navBurger');
const mobileMenu = document.getElementById('mobileMenu');
let menuOpen = false;

burger.addEventListener('click', () => {
  menuOpen = !menuOpen;
  mobileMenu.classList.toggle('open', menuOpen);
  burger.querySelectorAll('span')[0].style.transform = menuOpen ? 'translateY(7.5px) rotate(45deg)' : '';
  burger.querySelectorAll('span')[1].style.transform = menuOpen ? 'translateY(-7.5px) rotate(-45deg)' : '';
});

mobileMenu.querySelectorAll('.mobile-link').forEach(link => {
  link.addEventListener('click', () => {
    menuOpen = false;
    mobileMenu.classList.remove('open');
    burger.querySelectorAll('span').forEach(s => s.style.transform = '');
  });
});

/* ---- WAVEFORM GENERATION ---- */
const waveBars = document.getElementById('waveBars');
if (waveBars) {
  const numBars = 60;
  for (let i = 0; i < numBars; i++) {
    const h = 8 + Math.random() * 56;
    const x = (i / numBars) * 400;
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', (80 - h) / 2);
    rect.setAttribute('width', '4');
    rect.setAttribute('height', h);
    rect.setAttribute('rx', '2');
    rect.setAttribute('fill', i < numBars * 0.3 ? 'var(--accent)' : 'rgba(255,255,255,0.12)');
    rect.style.transition = `fill 0.1s`;
    waveBars.appendChild(rect);
  }
}

/* ---- VINYL ROTATION ---- */
const vinyl = document.getElementById('vinyl');
let isPlaying = false;

/* ---- AUDIO PLAYER ---- */
const audioPlayer = document.getElementById('audioPlayer');
const mainPlay = document.getElementById('mainPlay');
const playIcon = document.getElementById('playIcon');
const pauseIcon = document.getElementById('pauseIcon');
const progressFill = document.getElementById('progressFill');
const progressBar = document.getElementById('progressBar');
const timeCurrent = document.getElementById('timeCurrent');
const playerClose = document.getElementById('playerClose');
const volumeSlider = document.getElementById('volumeSlider');

let progress = 0;
let progressInterval = null;
const TOTAL_SECONDS = 52 * 60;

function openPlayer() {
  audioPlayer.classList.add('visible');
}

function togglePlay() {
  isPlaying = !isPlaying;
  playIcon.style.display = isPlaying ? 'none' : 'block';
  pauseIcon.style.display = isPlaying ? 'block' : 'none';

  if (vinyl) {
    vinyl.style.animationPlayState = isPlaying ? 'running' : 'paused';
  }

  if (isPlaying) {
    progressInterval = setInterval(() => {
      progress = Math.min(progress + 1, TOTAL_SECONDS);
      const pct = (progress / TOTAL_SECONDS) * 100;
      progressFill.style.width = pct + '%';
      const mins = Math.floor(progress / 60);
      const secs = progress % 60;
      timeCurrent.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;

      // animate waveform
      if (waveBars) {
        const bars = waveBars.querySelectorAll('rect');
        const activeCount = Math.floor((progress / TOTAL_SECONDS) * bars.length);
        bars.forEach((bar, i) => {
          bar.setAttribute('fill', i <= activeCount ? 'var(--accent)' : 'rgba(255,255,255,0.12)');
          if (isPlaying && Math.abs(i - activeCount) < 3) {
            const jitter = 0.8 + Math.random() * 0.4;
            const h = parseFloat(bar.getAttribute('height'));
            bar.setAttribute('height', Math.max(4, h * jitter));
            bar.setAttribute('y', (80 - parseFloat(bar.getAttribute('height'))) / 2);
          }
        });
      }
    }, 1000);
  } else {
    clearInterval(progressInterval);
    if (vinyl) vinyl.style.animationPlayState = 'paused';
  }
}

[document.getElementById('featuredPlay'), document.getElementById('featuredPlayBtn')].forEach(btn => {
  if (btn) btn.addEventListener('click', () => {
    openPlayer();
    if (!isPlaying) togglePlay();
  });
});

if (mainPlay) mainPlay.addEventListener('click', togglePlay);

if (playerClose) {
  playerClose.addEventListener('click', () => {
    audioPlayer.classList.remove('visible');
    if (isPlaying) togglePlay();
  });
}

// Progress bar click
if (progressBar) {
  progressBar.addEventListener('click', e => {
    const rect = progressBar.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    progress = Math.floor(pct * TOTAL_SECONDS);
    progressFill.style.width = (pct * 100) + '%';
  });
}

// Episode cards play
document.querySelectorAll('.ep-play-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    openPlayer();
    if (!isPlaying) togglePlay();
  });
});

/* ---- COUNTER ANIMATION ---- */
function animateCounter(el, target, duration = 2000) {
  const start = performance.now();
  const startVal = 0;

  function update(time) {
    const elapsed = time - start;
    const t = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    const current = Math.round(startVal + (target - startVal) * ease);
    el.textContent = current >= 1000 ? (current / 1000).toFixed(1) + 'k' : current;
    if (t < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

/* ---- INTERSECTION OBSERVER ---- */
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      io.unobserve(entry.target);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

// Add reveal class to elements
const revealTargets = [
  '.featured-card',
  '.ep-card',
  '.value-card',
  '.guest-card',
  '.platform-card',
  '.newsletter-card',
  '.section-header',
  '.about-left',
  '.about-right',
];
revealTargets.forEach(selector => {
  document.querySelectorAll(selector).forEach((el, i) => {
    el.classList.add('reveal');
    if (i < 4) el.classList.add(`reveal-delay-${i + 1}`);
    io.observe(el);
  });
});

// Counter animation on hero stats
const statNums = document.querySelectorAll('.stat-num[data-target]');
const statObs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const target = parseInt(entry.target.dataset.target);
      animateCounter(entry.target, target);
      statObs.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });
statNums.forEach(el => statObs.observe(el));

/* ---- SMOOTH SCROLL ---- */
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

/* ---- NEWSLETTER ---- */
const form = document.getElementById('newsletterForm');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('.newsletter-btn');
    btn.textContent = '✓ Abonné !';
    btn.style.background = '#22c55e';
    btn.style.boxShadow = '0 0 20px rgba(34,197,94,0.3)';
    form.querySelector('input').value = '';
    setTimeout(() => {
      btn.textContent = "S'abonner";
      btn.style.background = '';
      btn.style.boxShadow = '';
    }, 3000);
  });
}

/* ---- PARALLAX ORBS ---- */
window.addEventListener('mousemove', e => {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;

  document.querySelector('.hero-orb-1')?.style.setProperty('transform', `translate(${x * 0.3}px, ${y * 0.3}px)`);
  document.querySelector('.hero-orb-2')?.style.setProperty('transform', `translate(${-x * 0.2}px, ${-y * 0.2}px)`);
  document.querySelector('.hero-orb-3')?.style.setProperty('transform', `translate(${x * 0.5}px, ${y * 0.5}px)`);
}, { passive: true });

/* ---- TITLE SPLIT ANIMATION ---- */
document.querySelectorAll('.title-line').forEach(line => {
  const text = line.textContent;
  line.innerHTML = '';
  text.split('').forEach((char, i) => {
    const span = document.createElement('span');
    span.textContent = char === ' ' ? ' ' : char;
    span.style.display = 'inline-block';
    span.style.opacity = '0';
    span.style.transform = 'translateY(20px)';
    span.style.transition = `opacity 0.5s ease ${0.3 + i * 0.02}s, transform 0.5s ease ${0.3 + i * 0.02}s`;
    line.appendChild(span);
  });
  setTimeout(() => {
    line.querySelectorAll('span').forEach(s => {
      s.style.opacity = '1';
      s.style.transform = 'translateY(0)';
    });
  }, 100);
});

/* ---- GUESTS TRACK DRAG SCROLL ---- */
const track = document.querySelector('.guests-track');
if (track) {
  let isDragging = false, startX = 0, scrollLeft = 0;
  track.addEventListener('mousedown', e => {
    isDragging = true; startX = e.pageX - track.offsetLeft;
    scrollLeft = track.scrollLeft; track.style.cursor = 'grabbing';
  });
  track.addEventListener('mouseleave', () => { isDragging = false; track.style.cursor = ''; });
  track.addEventListener('mouseup', () => { isDragging = false; track.style.cursor = ''; });
  track.addEventListener('mousemove', e => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - track.offsetLeft;
    track.scrollLeft = scrollLeft - (x - startX) * 1.5;
  });
}
