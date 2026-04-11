// ================================================================
// Global Workforce Gap Analyzer - Frontend Script
// ================================================================

let currentCity = '';
let allJobsCache = {};     // category -> jobs array
let allCompanies = [];
let allStartups = [];
let allOfficers = [];
let currentTab = 'high_demand';

// ── TAG CONFIG ────────────────────────────────────────────────
const TAG_CONFIG = {
  Fire:    { cls: 'badge-fire',  label: '🔥 High Demand' },
  Money:   { cls: 'badge-money', label: '💰 High Pay' },
  Star:    { cls: 'badge-star',  label: '⭐ Best Job' },
  Warning: { cls: 'badge-warn',  label: '⚠️ Risky' },
  Alarm:   { cls: 'badge-alarm', label: '🚨 Emergency' },
  New:     { cls: 'badge-new',   label: '🆕 New' },
};

// ── TAB SWITCHING ─────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentTab = btn.dataset.tab;
    showPanel(currentTab);
  });
});

function showPanel(tab) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const panel = document.getElementById('panel-' + tab);
  if (panel) panel.classList.add('active');

  const searchBar = document.getElementById('searchBar');
  const jobTabs = ['high_demand','high_pay','best','risky','emergency','new'];
  searchBar.style.display = jobTabs.includes(tab) ? 'flex' : 'none';
  updateResultsCount();
}

// ── CITY LOADING ──────────────────────────────────────────────
function loadCity() {
  const city = document.getElementById('citySelect').value;
  if (!city) { alert('Please select a city first'); return; }
  quickLoad(city);
}

function quickLoad(city) {
  currentCity = city;
  document.getElementById('citySelect').value = city;

  document.getElementById('welcomeState').classList.add('hidden');
  document.getElementById('globalLoading').classList.remove('hidden');
  document.getElementById('emptyState').classList.add('hidden');

  const categories = ['high_demand','high_pay','best','risky','emergency','new'];
  Promise.all([
    ...categories.map(cat =>
      fetch(`/api/jobs/${encodeURIComponent(city)}?category=${cat}`)
        .then(r => r.json()).then(d => ({ cat, jobs: d.jobs || [] }))
    ),
    fetch(`/api/companies/${encodeURIComponent(city)}`).then(r => r.json()),
    fetch(`/api/startups/${encodeURIComponent(city)}`).then(r => r.json()),
    fetch(`/api/officers/${encodeURIComponent(city)}`).then(r => r.json()),
  ]).then(results => {
    document.getElementById('globalLoading').classList.add('hidden');

    categories.forEach((cat, i) => {
      allJobsCache[cat] = results[i].jobs;
      renderJobCards(cat, results[i].jobs);
    });

    allCompanies = results[6].companies || [];
    allStartups  = results[7].startups  || [];
    allOfficers  = results[8].officers  || [];

    renderCompanies(allCompanies);
    renderStartups(allStartups);
    renderOfficers(allOfficers);

    showPanel(currentTab);
    updateResultsCount();
  }).catch(err => {
    document.getElementById('globalLoading').classList.add('hidden');
    alert('Error loading data: ' + err.message);
  });
}

// ── SEARCH FILTER ─────────────────────────────────────────────
function filterCards() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  const container = document.getElementById('cards-' + currentTab);
  if (!container) return;

  const cards = container.querySelectorAll('.job-card');
  let visible = 0;
  cards.forEach(card => {
    const text = card.textContent.toLowerCase();
    const show = !q || text.includes(q);
    card.style.display = show ? '' : 'none';
    if (show) visible++;
  });

  const empty = document.getElementById('emptyState');
  if (visible === 0 && cards.length > 0) {
    empty.classList.remove('hidden');
  } else {
    empty.classList.add('hidden');
  }
  updateResultsCount(visible);
}

function updateResultsCount(count) {
  const el = document.getElementById('resultsCount');
  if (!el) return;
  const jobTabs = ['high_demand','high_pay','best','risky','emergency','new'];
  if (!jobTabs.includes(currentTab)) { el.textContent = ''; return; }
  const jobs = allJobsCache[currentTab] || [];
  const shown = count !== undefined ? count : jobs.length;
  el.textContent = shown + ' job' + (shown !== 1 ? 's' : '') + ' shown';
}

// ── JOB CARD RENDERER ─────────────────────────────────────────
function renderJobCards(category, jobs) {
  const container = document.getElementById('cards-' + category);
  if (!container) return;
  container.innerHTML = '';

  if (!jobs || jobs.length === 0) {
    container.innerHTML = '<p style="color:var(--text-muted);padding:1rem;">No jobs in this category for the selected city.</p>';
    return;
  }

  jobs.forEach(job => {
    container.appendChild(createJobCard(job));
  });
}

function createJobCard(job, showScores) {
  const card = document.createElement('div');
  card.className = 'job-card';

  // Badges
  const badgesHtml = (job.tags || []).map(tag => {
    const cfg = TAG_CONFIG[tag] || { cls: 'badge-default', label: tag };
    return `<span class="badge ${cfg.cls}">${cfg.label}</span>`;
  }).join('');

  // Skills
  const skillsHtml = (job.skills || []).map(s =>
    `<span class="skill-pill">${s}</span>`
  ).join('');

  // Score badge color
  const score = job.score || 0;
  const scoreClass = score >= 80 ? 'score-high' : score >= 55 ? 'score-mid' : 'score-low';

  // Growth bar
  const growth = job.growth || 0;
  const growthPct = (growth / 10 * 100).toFixed(0);

  // Posted
  const posted = job.posted_days_ago
    ? (job.posted_days_ago === 1 ? 'Today' : job.posted_days_ago + 'd ago')
    : '';

  let scoreSection = '';
  if (showScores) {
    scoreSection = `
    <div class="score-bars">
      <div class="score-row">
        <span class="s-label">Skill Match</span>
        <div class="s-bar"><div class="s-fill skill" style="width:${job.skill_match||0}%"></div></div>
        <span class="s-pct">${job.skill_match||0}%</span>
      </div>
      <div class="score-row">
        <span class="s-label">Experience</span>
        <div class="s-bar"><div class="s-fill exp" style="width:${job.experience_match||0}%"></div></div>
        <span class="s-pct">${job.experience_match||0}%</span>
      </div>
      <div class="score-row">
        <span class="s-label">Overall</span>
        <div class="s-bar"><div class="s-fill overall" style="width:${job.overall_score||0}%"></div></div>
        <span class="s-pct">${job.overall_score||0}%</span>
      </div>
    </div>`;
  }

  card.innerHTML = `
    <div class="job-card-header">
      <div class="job-role">${job.role}</div>
      <div class="job-company">${job.company || ''}</div>
      <div class="job-badges">${badgesHtml}</div>
    </div>
    <div class="job-card-body">
      <div class="job-stat">
        <span class="stat-label">💼 Openings</span>
        <span class="stat-value">${job.openings}</span>
      </div>
      <div class="job-stat">
        <span class="stat-label">💰 Salary</span>
        <span class="stat-value salary">${job.salary}</span>
      </div>
      <div class="job-stat">
        <span class="stat-label">🎯 Experience</span>
        <span class="stat-value">${job.experience || 'N/A'}</span>
      </div>
      <div class="job-stat">
        <span class="stat-label">🕐 Posted</span>
        <span class="stat-value">${posted}</span>
      </div>
      <div class="skills-row">${skillsHtml}</div>
    </div>
    ${scoreSection}
    <div class="job-card-footer">
      <div class="growth-bar-wrap">
        <div class="growth-label">Growth Potential: ${growth}/10</div>
        <div class="growth-bar"><div class="growth-fill" style="width:${growthPct}%"></div></div>
      </div>
      <div class="score-badge ${scoreClass}">${score}</div>
    </div>`;

  return card;
}

// ── COMPANY RENDERER ──────────────────────────────────────────
function renderCompanies(companies) {
  const container = document.getElementById('cards-companies');
  container.innerHTML = '';
  if (!companies || companies.length === 0) {
    container.innerHTML = '<p style="color:var(--text-muted);padding:1rem;">No company data available.</p>';
    return;
  }
  companies.forEach(co => {
    const skillsHtml = (co.skills || []).map(s => `<span class="skill-pill">${s}</span>`).join('');
    const growthKey = (co.growth || 'Medium').toLowerCase().replace(' ','_');
    const growthClass = 'growth-' + growthKey;
    const card = document.createElement('div');
    card.className = 'company-card';
    card.innerHTML = `
      <div class="company-name-row">
        <span class="company-name">🏢 ${co.name}</span>
        <span class="company-rating">⭐ ${co.rating}</span>
      </div>
      <div class="company-openings">💼 ${co.openings} Open Positions</div>
      <div class="company-salary">💰 ${co.salary}</div>
      <div class="skills-row">${skillsHtml}</div>
      <div class="company-benefits">🎁 ${co.benefits}</div>
      <div><span class="growth-tag ${growthClass}">📈 ${co.growth} Growth</span></div>`;
    container.appendChild(card);
  });
}

// ── STARTUP RENDERER ──────────────────────────────────────────
function renderStartups(startups) {
  const container = document.getElementById('cards-startups');
  container.innerHTML = '';
  if (!startups || startups.length === 0) {
    container.innerHTML = '<p style="color:var(--text-muted);padding:1rem;">No startup data available.</p>';
    return;
  }
  startups.forEach(st => {
    const rolesHtml = (st.roles || []).map(r => `<span class="role-pill">${r}</span>`).join('');
    const stars = '★'.repeat(Math.min(st.growth || 5, 10)) + '☆'.repeat(10 - Math.min(st.growth || 5, 10));
    const card = document.createElement('div');
    card.className = 'startup-card';
    card.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <span class="startup-name">🚀 ${st.name}</span>
        <span class="stage-badge">${st.stage}</span>
      </div>
      <div class="startup-desc">${st.description}</div>
      <div class="startup-salary">💰 ${st.salary}</div>
      <div class="startup-equity">📊 Equity: ${st.equity}</div>
      <div class="roles-row">${rolesHtml}</div>
      <div class="growth-stars" title="Growth: ${st.growth}/10">${stars}</div>`;
    container.appendChild(card);
  });
}

// ── OFFICER RENDERER ──────────────────────────────────────────
function renderOfficers(officers) {
  const container = document.getElementById('cards-officers');
  container.innerHTML = '';
  if (!officers || officers.length === 0) {
    container.innerHTML = '<p style="color:var(--text-muted);padding:1rem;">No officer data available.</p>';
    return;
  }
  officers.forEach(off => {
    const card = document.createElement('div');
    card.className = 'officer-card';
    card.innerHTML = `
      <div class="officer-name-row">
        <span class="officer-name">👔 ${off.name}</span>
        <span class="success-badge">${off.success_rate}% success</span>
      </div>
      <div class="officer-spec">🎯 ${off.specialization}</div>
      <div class="officer-info">📞 <a href="tel:${off.phone}">${off.phone}</a></div>
      <div class="officer-info">📧 <a href="mailto:${off.email}">${off.email}</a></div>
      <div class="officer-info">🏅 ${off.experience} yrs experience</div>
      <div class="placed-count">✅ Placed <strong>${off.placed.toLocaleString()}</strong> candidates</div>`;
    container.appendChild(card);
  });
}

// ── RESUME UPLOAD ─────────────────────────────────────────────
const uploadZone = document.getElementById('uploadZone');
const resumeFile = document.getElementById('resumeFile');

// Drag & drop
['dragenter','dragover'].forEach(e => {
  uploadZone.addEventListener(e, ev => { ev.preventDefault(); uploadZone.classList.add('dragover'); });
});
['dragleave','drop'].forEach(e => {
  uploadZone.addEventListener(e, ev => { ev.preventDefault(); uploadZone.classList.remove('dragover'); });
});
uploadZone.addEventListener('drop', ev => {
  const file = ev.dataTransfer.files[0];
  if (file) { resumeFile.files = ev.dataTransfer.files; showFileName(file.name); }
});

resumeFile.addEventListener('change', () => {
  if (resumeFile.files[0]) showFileName(resumeFile.files[0].name);
});

function showFileName(name) {
  document.getElementById('fileInfo').textContent = '📎 ' + name + ' selected';
}

function analyzeResume() {
  const file = resumeFile.files[0];
  const city = document.getElementById('resumeCity').value;

  if (!file) { alert('Please upload your resume first'); return; }
  if (!city) { alert('Please select a city'); return; }

  document.getElementById('resumeLoading').classList.remove('hidden');
  document.getElementById('resumeResults').classList.add('hidden');

  const formData = new FormData();
  formData.append('resume', file);
  formData.append('city', city);

  fetch('/api/upload-resume', { method: 'POST', body: formData })
    .then(r => r.json())
    .then(data => {
      document.getElementById('resumeLoading').classList.add('hidden');
      if (data.error) { alert('Error: ' + data.error); return; }
      displayResumeResults(data);
    })
    .catch(err => {
      document.getElementById('resumeLoading').classList.add('hidden');
      alert('Error: ' + err.message);
    });
}

function displayResumeResults(data) {
  const resultsDiv = document.getElementById('resumeResults');
  resultsDiv.classList.remove('hidden');

  // Skill summary
  const skillsHtml = (data.extracted_skills || []).map(s =>
    `<span class="ext-skill-pill">${s}</span>`
  ).join('') || '<span style="color:var(--text-muted)">No skills detected</span>';

  document.getElementById('skillSummary').innerHTML = `
    <h3>📋 Resume Analysis</h3>
    <div class="extracted-skills">${skillsHtml}</div>
    <p class="years-exp">⏳ Experience detected: <strong>${data.experience_years || 0} years</strong> &nbsp;|&nbsp;
      Jobs analyzed: <strong>${data.total_jobs_analyzed}</strong></p>`;

  // Recommendations
  const container = document.getElementById('resumeRecommendations');
  container.innerHTML = '';
  (data.recommendations || []).forEach((job, i) => {
    const card = createJobCard(job, true);
    // Add rank badge
    const rankEl = document.createElement('div');
    rankEl.style.cssText = 'position:absolute;top:10px;right:10px;background:var(--primary);color:#fff;' +
      'border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;' +
      'font-size:.8rem;font-weight:800;z-index:1;';
    rankEl.textContent = '#' + (i + 1);
    card.style.position = 'relative';
    card.appendChild(rankEl);
    container.appendChild(card);
  });
}

// ── INIT ──────────────────────────────────────────────────────
showPanel('high_demand');
document.getElementById('searchBar').style.display = 'flex';
