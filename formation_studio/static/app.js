"use strict";

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const mdHtml = (text) => {
  if (window.marked && window.DOMPurify) return DOMPurify.sanitize(marked.parse(text || ""));
  return `<p style="white-space:pre-wrap">${esc(text)}</p>`;
};
const list = (items) => `<ul>${(items || []).map((i) => `<li>${esc(i)}</li>`).join("")}</ul>`;
const fmtMin = (m) => (m >= 60 ? `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, "0")}` : `${m} min`);

let course = null;
let currentLessonId = null;

async function api(path, options = {}) {
  const res = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!res.ok) {
    let detail = res.statusText;
    try { const body = await res.json(); detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail); } catch (_) {}
    throw new Error(detail);
  }
  return res.status === 204 ? null : res.json();
}

function show(view) {
  $$(".view").forEach((v) => (v.hidden = v.id !== `view-${view}`));
  window.scrollTo(0, 0);
}

// ---------------------------------------------------------------- liste
async function refreshList() {
  const courses = await api("/api/courses");
  $("#course-list").innerHTML = courses.length
    ? courses.map((c) => `<li data-id="${c.id}" class="${course && course.id === c.id ? "active" : ""}">${esc(c.title)}
        <small>${c.modules} modules · ${c.lessons} leçons · ${esc(c.status)}</small></li>`).join("")
    : `<li class="muted">Aucune formation pour l'instant.</li>`;
}
$("#course-list").addEventListener("click", (e) => {
  const li = e.target.closest("li[data-id]");
  if (li) openCourse(li.dataset.id);
});
$("#new-course").addEventListener("click", () => { course = null; refreshList(); show("brief"); });

// ---------------------------------------------------------------- brief
$("#brief-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const mode = e.submitter?.value || "full";
  const data = Object.fromEntries(new FormData(form));
  $$('input[type="checkbox"]', form).forEach((cb) => (data[cb.name] = cb.checked));
  ["duration_hours", "modules_count", "lessons_per_module"].forEach((k) => (data[k] = Number(data[k])));
  const buttons = $$("button", form);
  buttons.forEach((b) => (b.disabled = true));
  try {
    if (mode === "outline") {
      show("job");
      setJob({ step: "Conception du programme…", percent: 5, log: [] });
      const c = await api("/api/outline", { method: "POST", body: JSON.stringify(data) });
      await refreshList();
      openCourse(c.id);
    } else {
      const { job_id } = await api("/api/courses", { method: "POST", body: JSON.stringify(data) });
      await followJob(job_id);
    }
  } catch (err) {
    show("job");
    $("#job-error").textContent = `Erreur : ${err.message}`;
  } finally {
    buttons.forEach((b) => (b.disabled = false));
  }
});

// ---------------------------------------------------------------- tâches
function setJob(job) {
  $("#job-step").textContent = job.step || "";
  $("#job-bar").style.width = `${job.percent || 0}%`;
  $("#job-pct").textContent = `${job.percent || 0} %`;
  $("#job-log").innerHTML = (job.log || []).slice().reverse().map((l) => `<li>${esc(l)}</li>`).join("");
  $("#job-error").textContent = job.error ? `Erreur : ${job.error}` : "";
}

async function followJob(jobId) {
  show("job");
  setJob({ step: "Démarrage…", percent: 0 });
  for (;;) {
    const job = await api(`/api/jobs/${jobId}`);
    setJob(job);
    if (job.course_id) refreshList();
    if (job.status !== "en_cours") {
      if (job.course_id) await openCourse(job.course_id);
      if (job.status === "échec") alert(`Génération incomplète : ${job.error}`);
      return;
    }
    await new Promise((r) => setTimeout(r, 2000));
  }
}

// ---------------------------------------------------------------- formation
async function openCourse(id) {
  course = await api(`/api/courses/${id}`);
  currentLessonId = null;
  refreshList();
  renderCourse();
  show("course");
}

function missingCount() {
  let n = 0;
  course.modules.forEach((m) => {
    m.lessons.forEach((l) => { if (!l.content) n++; });
    if (course.brief.include_quizzes && !m.quiz) n++;
  });
  if (course.brief.include_final_exam && !course.final_exam) n++;
  if (course.brief.include_capstone && !course.capstone) n++;
  if (!course.extras) n++;
  return n;
}

function renderCourse() {
  const minutes = course.modules.reduce((s, m) => s + m.lessons.reduce((t, l) => t + l.plan.duration_minutes, 0), 0);
  const lessons = course.modules.reduce((s, m) => s + m.lessons.length, 0);
  $("#c-title").textContent = course.title;
  $("#c-subtitle").textContent = course.subtitle;
  $("#c-stats").innerHTML = [
    `${course.modules.length} modules`, `${lessons} leçons`, fmtMin(minutes), course.brief.level, course.brief.language, course.status,
  ].map((s) => `<span>${esc(s)}</span>`).join("");
  $$(".export a").forEach((a) => (a.href = `/api/courses/${course.id}/export/${a.dataset.fmt}`));

  const missing = missingCount();
  $("#c-banner").innerHTML = missing
    ? `<div class="banner"><span>${missing} élément(s) restent à rédiger${course.error ? " — " + esc(course.error) : ""}. Validez / ajustez le programme puis lancez la rédaction.</span>
       <button class="primary" id="resume">Rédiger tout le contenu manquant</button></div>`
    : "";
  $("#resume")?.addEventListener("click", async () => {
    const { job_id } = await api(`/api/courses/${course.id}/generate`, { method: "POST" });
    followJob(job_id);
  });

  renderProgramme();
  renderLessons();
  renderEvaluations();
  renderProject();
  renderExtras();
}

$$(".tabs button").forEach((b) =>
  b.addEventListener("click", () => {
    $$(".tabs button").forEach((x) => x.classList.toggle("active", x === b));
    $$(".tab").forEach((t) => (t.hidden = t.id !== `tab-${b.dataset.tab}`));
  })
);

$("#delete-course").addEventListener("click", async () => {
  if (!confirm(`Supprimer définitivement « ${course.title} » ?`)) return;
  await api(`/api/courses/${course.id}`, { method: "DELETE" });
  course = null;
  await refreshList();
  show("brief");
});

// ---- Programme (éditable)
function renderProgramme() {
  const c = course;
  $("#tab-programme").innerHTML = `
    <div class="card prose" style="margin-bottom:16px">
      <p>${esc(c.description)}</p>
      <p><b>Public :</b> ${esc(c.target_audience)}</p>
      <div class="grid">
        <div><h3>Prérequis</h3>${list(c.prerequisites)}</div>
        <div><h3>Compétences</h3>${list(c.skills)}</div>
      </div>
      <h3>Ce que l'apprenant saura faire</h3>${list(c.learning_outcomes)}
      <h3>Approche pédagogique</h3><p>${esc(c.pedagogical_approach)}</p>
    </div>
    <form id="outline-form">
      ${c.modules.map((m, i) => `
        <div class="card module-card">
          <label>Module ${i + 1}<input class="title" data-m="${i}" data-f="title" value="${esc(m.title)}"></label>
          <label>Résumé<textarea rows="2" data-m="${i}" data-f="summary">${esc(m.summary)}</textarea></label>
          ${m.lessons.map((l, j) => `
            <div class="lesson-row">
              <input data-m="${i}" data-l="${j}" data-f="title" value="${esc(l.plan.title)}" aria-label="Titre de la leçon ${i + 1}.${j + 1}">
              <input data-m="${i}" data-l="${j}" data-f="duration_minutes" type="number" min="1" value="${l.plan.duration_minutes}" aria-label="Durée en minutes">
            </div>`).join("")}
        </div>`).join("")}
      <div class="actions"><button type="submit" class="primary">Enregistrer les modifications du programme</button></div>
    </form>`;
  $("#outline-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    $$("[data-m]", e.target).forEach((input) => {
      const m = course.modules[+input.dataset.m];
      const value = input.type === "number" ? Number(input.value) : input.value;
      if (input.dataset.l !== undefined) m.lessons[+input.dataset.l].plan[input.dataset.f] = value;
      else m[input.dataset.f] = value;
    });
    course = await api(`/api/courses/${course.id}`, { method: "PUT", body: JSON.stringify(course) });
    renderCourse();
    refreshList();
  });
}

// ---- Leçons
function renderLessons() {
  if (!currentLessonId) currentLessonId = course.modules[0]?.lessons[0]?.id;
  $("#lesson-tree").innerHTML = course.modules.map((m, i) => `
    <li class="mod">Module ${i + 1} — ${esc(m.title)}</li>
    ${m.lessons.map((l, j) => `<li class="les ${l.content ? "" : "missing"} ${l.id === currentLessonId ? "active" : ""}" data-id="${l.id}">${i + 1}.${j + 1} ${esc(l.plan.title)}</li>`).join("")}
  `).join("");
  $$("#lesson-tree .les").forEach((li) => li.addEventListener("click", () => { currentLessonId = li.dataset.id; renderLessons(); }));
  renderLesson();
}

function lessonMarkdown(l) {
  const c = l.content;
  const p = l.plan;
  let out = `# ${p.title}\n\n*${fmtMin(p.duration_minutes)} · ${p.format}*\n\n### Objectifs\n${p.objectives.map((o) => `- ${o}`).join("\n")}\n\n`;
  if (!c) return out + "> Contenu non encore rédigé.";
  out += `${c.introduction_markdown}\n\n`;
  c.sections.forEach((s) => (out += `## ${s.heading}\n\n${s.content_markdown}\n\n`));
  if (c.examples.length) out += `## Exemples\n\n` + c.examples.map((e) => `### ${e.title}\n\n${e.content_markdown}`).join("\n\n") + "\n\n";
  out += `## À retenir\n${c.key_takeaways.map((k) => `- ${k}`).join("\n")}\n\n`;
  if (c.common_mistakes.length) out += `## Erreurs fréquentes\n${c.common_mistakes.map((k) => `- ${k}`).join("\n")}\n\n`;
  if (c.exercises.length) out += `## Exercices\n\n` + c.exercises.map((e) =>
    `### ${e.title} (${e.difficulty}, ~${e.estimated_minutes} min)\n\n${e.instructions_markdown}\n\n<details><summary>Solution</summary>\n\n${e.solution_markdown}\n\n</details>`).join("\n\n") + "\n\n";
  if (c.resources.length) out += `## Pour aller plus loin\n${c.resources.map((r) => `- **${r.title}** (${r.type}) — ${r.description}`).join("\n")}\n\n`;
  if (c.video_script_markdown?.trim()) out += `## Script vidéo\n\n${c.video_script_markdown}\n\n`;
  if (c.slides?.length) out += `## Diapositives\n\n` + c.slides.map((s, i) => `### ${i + 1}. ${s.title}\n${s.bullets.map((b) => `- ${b}`).join("\n")}\n\n*Notes : ${s.speaker_notes}*`).join("\n\n");
  return out;
}

function renderLesson() {
  const view = $("#lesson-view");
  let lesson = null;
  course.modules.forEach((m) => m.lessons.forEach((l) => { if (l.id === currentLessonId) lesson = l; }));
  if (!lesson) { view.innerHTML = `<p class="muted">Sélectionnez une leçon.</p>`; return; }
  view.innerHTML = `
    <div class="toolbar">
      <input id="regen-instr" placeholder="Consignes (optionnel) : plus d'exemples, plus simple, ajouter un cas pratique…">
      <button id="regen" class="primary">${lesson.content ? "Régénérer la leçon" : "Rédiger la leçon"}</button>
    </div>${mdHtml(lessonMarkdown(lesson))}`;
  $("#regen").addEventListener("click", async (e) => {
    e.target.disabled = true;
    e.target.textContent = "Rédaction en cours…";
    try {
      course = await api(`/api/courses/${course.id}/lessons/${lesson.id}/regenerate`, {
        method: "POST", body: JSON.stringify({ instructions: $("#regen-instr").value }),
      });
      renderCourse();
    } catch (err) {
      alert(err.message);
      e.target.disabled = false;
    }
  });
}

// ---- Évaluations
function quizHtml(q) {
  if (!q) return `<p class="muted">Non généré.</p>`;
  return `<p>${esc(q.instructions)} <span class="tag">Seuil : ${q.passing_score_percent} %</span></p>` +
    q.questions.map((x, i) => `
      <div class="question">
        <b>${i + 1}. ${esc(x.question)}</b> <span class="tag">${esc(x.type)} · Bloom : ${esc(x.bloom_level)}</span>
        <ul>${x.options.map((o, j) => `<li class="${x.correct_indexes.includes(j) ? "ok" : ""}">${esc(o)}${x.correct_indexes.includes(j) ? " ✓" : ""}</li>`).join("")}</ul>
        <p class="muted">${esc(x.explanation)}</p>
      </div>`).join("");
}

function renderEvaluations() {
  const el = $("#tab-evaluations");
  el.innerHTML = course.modules.map((m, i) => `
    <details class="card" ${i === 0 ? "open" : ""}><summary><b>Quiz — Module ${i + 1} : ${esc(m.title)}</b></summary>
      <div class="toolbar" style="margin-top:12px"><button data-quiz="${m.id}">${m.quiz ? "Régénérer le quiz" : "Générer le quiz"}</button></div>
      ${quizHtml(m.quiz)}
    </details>`).join("") +
    (course.brief.include_final_exam ? `<details class="card"><summary><b>Examen final</b></summary>${quizHtml(course.final_exam)}</details>` : "");
  $$("[data-quiz]", el).forEach((b) => b.addEventListener("click", async () => {
    b.disabled = true;
    b.textContent = "Génération…";
    try {
      course = await api(`/api/courses/${course.id}/modules/${b.dataset.quiz}/quiz`, { method: "POST" });
      renderCourse();
    } catch (err) { alert(err.message); b.disabled = false; }
  }));
}

// ---- Projet final
function renderProject() {
  const cp = course.capstone;
  $("#tab-projet").innerHTML = !cp ? `<p class="muted">Projet final non généré.</p>` : `
    <div class="card">
      <h2>${esc(cp.title)}</h2><p class="muted">Durée estimée : ${cp.estimated_hours} h</p>
      ${mdHtml(cp.context_markdown)}
      <h3>Livrables</h3>${list(cp.deliverables)}
      <h3>Étapes</h3><ol>${cp.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>
      <h3>Grille d'évaluation</h3>
      <table><tr><th>Critère</th><th>Description</th><th>Points</th></tr>
      ${cp.rubric.map((r) => `<tr><td>${esc(r.criterion)}</td><td>${esc(r.description)}</td><td>${r.points}</td></tr>`).join("")}</table>
    </div>`;
}

// ---- Accompagnement
function renderExtras() {
  const x = course.extras;
  $("#tab-accompagnement").innerHTML = !x ? `<p class="muted">Éléments d'accompagnement non générés.</p>` : `
    <div class="card"><h2>Message de bienvenue</h2>${mdHtml(x.welcome_message_markdown)}
      <h2>Comment suivre la formation</h2>${mdHtml(x.how_to_follow_markdown)}</div><br>
    <div class="card"><h2>Page de vente</h2><p>${esc(x.marketing_pitch)}</p>${list(x.sales_page_bullets)}</div><br>
    <div class="card"><h2>Glossaire</h2><dl>${x.glossary.map((g) => `<dt><b>${esc(g.term)}</b></dt><dd>${esc(g.definition)}</dd>`).join("")}</dl></div><br>
    <div class="card"><h2>FAQ</h2>${x.faq.map((f) => `<details><summary>${esc(f.title)}</summary>${mdHtml(f.content_markdown)}</details>`).join("")}</div><br>
    <div class="card"><h2>Certification</h2>${list(x.certification_criteria)}<h2>Conclusion</h2>${mdHtml(x.conclusion_markdown)}</div>`;
}

refreshList().catch((err) => console.error(err));
