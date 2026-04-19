# AGENTS.md — AI Assistant Onboarding

> **Read this first.** Everything an AI coding assistant (Cascade / Windsurf, Cursor,
> Aider, Codex, Claude Code, etc.) needs to be productive in this repo and on
> behalf of the repo owner lives here. Keep it updated when context drifts.

---

## 1. Repo purpose

Personal portfolio for **Rahul Maurya**, a backend-focused Software Engineer.
Static single-page site + per-project deep-dive pages, deployed via **GitHub Pages**
at **https://maurya2811.github.io/Portfolio**. No build step, no frameworks — plain
HTML + CSS + tiny vanilla JS. The site is the primary surface recruiters /
hiring managers see, so visual polish and factual accuracy matter.

---

## 2. Owner profile (source of truth)

| Field | Value |
|---|---|
| Name | Rahul Maurya |
| Current role | Software Engineer, **Addverb Australia** (Melbourne) — Jan 2026 → Present |
| Previous role | Software Development Engineer, **Addverb Technologies** (Noida, India) — Apr 2024 → Dec 2025 |
| Internship | **NEC Corporation India** — Oct 2023 → Jan 2024 |
| Education | B.Tech CSE, **Raj Kumar Goel Institute of Technology (AKTU)**, 2020–2024, CGPA **8.67** |
| Base | Melbourne, Australia |
| Email | maurya2811@gmail.com |
| Phone | +91-7905496720 |
| LinkedIn | https://www.linkedin.com/in/rahul-maurya-277069227 |
| GitHub | https://github.com/Maurya2811 |
| LeetCode | https://leetcode.com/Rahul_2811/ |
| GfG | https://auth.geeksforgeeks.org/user/maurya2811 |
| Focus | Backend, Distributed Systems, Warehouse Automation (WCS / WMS / ASRS) |

### Core tech stack (verified, do not embellish)
- **Languages:** Java (Core/J2SE), SQL, Python
- **Frameworks:** Spring Boot, Spring JPA, REST APIs, Microservices, Multithreading, Event-Driven Design
- **Messaging / Cache:** RabbitMQ, Apache Kafka, Redis
- **Databases:** MySQL, MSSQL, MongoDB
- **DevOps:** Docker, Kubernetes, Helm, Jenkins, Git, CI/CD
- **Observability:** Grafana, Jaeger, distributed logging
- **Concepts:** System Design, Distributed Systems, Data Pipelining, LLM/AI Agents, Scalability, Performance Tuning

### Signature career metrics (use these verbatim in any generated content)
- 2+ years experience
- API latency **800ms → 600ms** (−25%)
- **10K+ events/min** processed, zero data loss
- **12+ microservices** in production
- **99.8% uptime**
- Unlocked **1.2M AUD** client revenue at Addverb Australia (SLA remediation)
- GTP picking throughput **800 → 1,200 totes/hr (+50%)**
- LLM inventory agent: **95%+ auto-resolution**, **−40%** support tickets
- Grafana dashboard migration automated: **8 hrs → 20 min (−95%)**, 50+ dashboards, 3 environments
- MRF UAT accelerated **6+ wks → 3 wks (+200%)**, ~₹15L saved
- Lenskart tote routing: **−15%** travel, **−200 ms** latency, **+12%** throughput
- UPS Movu telemetry: **99.9%** capture, **−70%** downtime diagnosis

---

## 3. Project portfolio (ordered recent → old)

Each entry has a detail page under `projects/<slug>.html` with HLD + LLD Mermaid diagrams.

### 3.1 Maersk · Adidas — Warehouse Automation Platform (2025)
- **Role:** SDE at Addverb Technologies, building the WES/WCS platform for the
  Maersk-operated Adidas distribution centre.
- **Services owned / contributed to** (all Spring Boot, all in
  `/home/rahulmaurya/ASRS_Project/adidas_services`):
  `adidas-wes`, `adidas-auction`, `adidas-decanting`, `adidas-packing`,
  `adidas-returns`, `adidas-robotic-arm`, `adidas-quadron`, `adidas-veloce`,
  `adidas-sso`, `box-it`, `multipro`, `outbound`, `adidas-frontend`.
- **Deployment:** Helm charts in `/home/rahulmaurya/ASRS_Project/project-adv-adidas`
  (aligned to the `project-adv-ups` pattern for CI/CD reuse).
- **Stack:** Java 17, Spring Boot, Spring JPA, RabbitMQ, MongoDB, MySQL/MSSQL, Docker, Kubernetes, Helm, Jenkins, Grafana, Jaeger, Nexus.
- **HLD/LLD:** See `projects/maersk-adidas.html`.

### 3.2 UPS Healthcare — Movu Robotic Shuttle Integration (2024)
- Integrated 50+ Movu robotic shuttles + lifts into the existing ASRS control plane.
- Built MongoDB telemetry pipeline (99.9% capture) + Grafana health dashboard (−70% downtime diagnosis).
- Helm repo: `/home/rahulmaurya/ASRS_Project/project-adv-ups`.
- **Detail page:** `projects/ups-movu.html`.

### 3.3 Lenskart (Bhiwadi) — Tote Movement Optimization (2024)
- Java graph/pathfinding service (Dijkstra + K-shortest) for tote routing
  from ASRS to GTP floor. Congestion-weighted edges updated from live telemetry.
- **Detail page:** `projects/lenskart-tote.html`.

### 3.4 MRF Ankenpally — 5-Deep 9-Level ASRS (2024)
- Dense 5-deep × 9-level Automated Storage & Retrieval System, third-party
  hardware integration (cranes, shuttles, conveyors).
- Helm repo: `/home/rahulmaurya/ASRS_Project/project-adv-mrf`.
- **Detail page:** `projects/mrf-asrs.html`.

### 3.5 Also shipped (not yet detailed)
- **Reliance VF-Manual WMS** — 70+ UAT defects resolved, 14 leadership demos, formal PM appreciation.
- **LLM Inventory Agent** — auto-resolves 95%+ operator queries.
- **Grafana Dashboard Migration Automation** (Python) — 8 hr → 20 min.
- **RFP Management System** — B.Tech capstone, full-stack procurement platform with RBAC (3+ personas) and 15+ configurable reports.

### 3.6 Where real source lives
`/home/rahulmaurya/ASRS_Project/` (outside this repo). Sub-dirs of interest:
- `adidas_services/` — all Adidas microservice source trees.
- `project-adv-adidas/`, `project-adv-ups/`, `project-adv-mrf/`, `project-ril-sultanpur/`, `project-adv-dhlgermany/`, `project-adv-almarai/`, `project-adv-hindalco/`, `project-adv-gpc/`, `project-adv-wpl/` — Helm deployment repos per client.
- `wes/`, `quadron/`, `multipro/`, `movemachine/`, `box-it/`, `n-lane-conveyor/`, `packing/`, `rapido-service/`, `utility-service/`, `asrs-simulator/` — shared platform services.

---

## 4. Repository architecture

### 4.1 File map
```
Portfolio/
├── index.html                # Home (Hero / About / Skills / Experience / Projects / Contact)
├── 404.html                  # Branded 404 for GitHub Pages
├── robots.txt                # Allow all + sitemap pointer
├── sitemap.xml               # All canonical URLs
├── README.md                 # Human-facing repo readme
├── AGENTS.md                 # ← this file (AI onboarding)
├── CLAUDE.md                 # one-line pointer to AGENTS.md
├── favicon.ico
├── css/
│   └── styles.css            # Full design system + theme tokens
├── js/
│   └── theme.js              # Theme controller (dark default) + Mermaid re-render
├── projects/
│   ├── index.html            # Projects listing
│   ├── maersk-adidas.html    # Deep-dive + HLD + LLD (Mermaid)
│   ├── ups-movu.html
│   ├── lenskart-tote.html
│   └── mrf-asrs.html
├── resume/
│   ├── index.html            # Printable HTML resume
│   ├── Rahul_Maurya.pdf      # Auto-generated from index.html (headless Chrome)
│   └── README.md             # PDF regeneration instructions
└── images/                   # (optional, mostly empty after redesign)
```

### 4.2 Design system / theme

- **Default theme is DARK.** Light mode is a user opt-in via the toggle.
- Tokens live in `css/styles.css` under `:root` (light palette) and
  `[data-theme="dark"]` (dark override). The default is applied by an inline
  `<head>` script on every HTML page; JS then honours localStorage.
- **Do not hardcode colours** in new HTML — use CSS variables:
  `--bg`, `--bg-elev`, `--bg-soft`, `--border`, `--text`, `--muted`,
  `--accent`, `--accent-2`, `--chip`, `--diagram-bg`, `--nav-bg`,
  `--hero-glow-1`, `--hero-glow-2`, `--shadow`, `--shadow-hover`.
- **Accent colours:** light `#0ea371` emerald, dark `#7cf5c2` mint. Secondary: light `#2563eb`, dark `#78a6ff`.
- **Fonts:** Inter (UI) + JetBrains Mono (code/eyebrows/meta). Loaded from Google Fonts.

### 4.3 Theme controller (`js/theme.js`)

- Single file, loaded with `<script defer>` on every HTML page.
- Reads `localStorage['rm-theme']`, falls back to **`'dark'`**.
- Injects the toggle button into `header.nav` automatically.
- On every page that contains `<pre class="mermaid">`, it re-renders Mermaid
  diagrams with matching `themeVariables` on toggle (cached source via
  `dataset.mermaidSrc`). **Do not add per-page Mermaid `initialize()` calls** —
  theme.js owns that. Per-page pages still need the Mermaid CDN `<script>`.
- The no-flash inline snippet in each `<head>`:
  ```html
  <script>try{var t=localStorage.getItem('rm-theme');document.documentElement.setAttribute('data-theme',t==='light'?'light':'dark');}catch(e){}</script>
  ```

### 4.4 Adding a new project detail page

1. Copy `projects/mrf-asrs.html` as `projects/<slug>.html`.
2. Update: `<title>`, meta description, breadcrumb, header, meta-grid.
3. Fill `Problem`, `My Contribution`, `Tech Stack`, `HLD`, `LLD`, `Impact`,
   `Key Learnings` sections. Use Mermaid `flowchart`/`sequenceDiagram` inside
   `<pre class="mermaid">` — nothing else is needed.
4. Add a card to `projects/index.html` and (if featured) `index.html#projects`.
5. Add the URL to `sitemap.xml`.

### 4.5 Resume PDF

- Source is `resume/index.html`. PDF at `resume/Rahul_Maurya.pdf` is **generated**, not hand-edited.
- Regenerate (one-liner):
  ```bash
  google-chrome --headless --disable-gpu --no-sandbox \
    --print-to-pdf="resume/Rahul_Maurya.pdf" \
    --print-to-pdf-no-header \
    --virtual-time-budget=2000 \
    "file://$(pwd)/resume/index.html"
  ```
- Print CSS in `resume/index.html` forces light palette for the PDF regardless
  of the active theme — do not remove it.

### 4.6 Local dev
```bash
python3 -m http.server 8000 -d "/path/to/Portfolio"
# open http://localhost:8000
```

### 4.7 Content hydration (data/site.json)

The portfolio has a **Phase-1 client-side hydration layer** so volatile content
(contact info, resume URL, metrics) can be edited in one JSON file without
touching HTML.

- **Source of truth:** `data/site.json` (validated JSON, no comments).
- **Hydrator:** `js/site.js`, loaded with `defer` on pages that opt in.
- **Binding:**
  - `data-bind="owner.phone"` on an element → its `textContent` is replaced
    with `data.owner.phone` (only if the path resolves).
  - `data-bind-href="owner.phoneTel"` on an `<a>` → its `href` is replaced.
  - `data-bind-attr-<attr>="path"` → any attribute (generic escape hatch).
- **Fallback guarantee:** the HTML ships with the authoritative text/href
  inline. If `data/site.json` fails to fetch or JS is disabled, the site
  renders identically to pre-hydration. **Never remove the HTML fallback
  content** when adding a `data-bind`.
- **Currently hydrated fields** (index.html):
  - Hero links: github, linkedin, leetcode, email, phone (+ resume button).
  - Contact section: email, phone, linkedin, github.
- **To edit content:** change `data/site.json`, commit, push — GitHub Pages
  serves the new JSON, browsers re-render on next load.

When binding new fields:
1. Add the value to `data/site.json` (keep existing keys stable).
2. Add `data-bind` / `data-bind-href` attributes to the matching HTML nodes.
3. Keep the inline HTML fallback current — it's what no-JS visitors and
   crawlers see.

Next phases (not yet implemented):
- **Phase 2:** Jinja2 + GitHub Actions build step that pre-renders all HTML
  from `data/site.json` + `templates/*.html` so the deployed HTML is fully
  populated without JS. Better SEO; same edit workflow.
- **Phase 3:** Per-project content in `content/projects/*.md` (YAML front-matter)
  rendered by the Phase-2 build step.

### 4.8 Deploy
GitHub Pages on `main` branch, root folder. Push to `origin/main` and the site
goes live at `https://maurya2811.github.io/Portfolio`.

---

## 5. Editorial rules for AI assistants

1. **Never fabricate experience, companies, metrics, or technologies.** If
   something isn't in §2 / §3 of this file or in the resume, ask Rahul before
   writing it.
2. **Use the signature metrics verbatim** (§2) — they are marketing-consistent
   across resume, portfolio, LinkedIn.
3. **Preserve the factual framing of each project** — Problem → Contribution →
   Tech Stack → HLD → LLD → Impact → Learnings.
4. **No emojis** anywhere (site copy, commit messages, docs) unless Rahul asks.
5. **No build step** — keep the site runnable as a static folder. No npm,
   bundlers, TypeScript, or frameworks without explicit approval.
6. **Accessibility:** keep `aria-label`s on icon-only buttons, keep semantic
   HTML (`<main>`, `<header>`, `<section>`, `<article>`), keep colour contrast
   AA in both themes.
7. **SEO:** update `sitemap.xml` and meta tags whenever you add a page.
8. **Diagrams:** prefer Mermaid inside `<pre class="mermaid">`; avoid inline
   SVG unless Mermaid can't express it.
9. **Commits / PRs:** conventional commit style (`feat:`, `fix:`, `chore:`,
   `docs:`), imperative mood, no emojis.

---

## 6. Known TODOs / open improvements

- [ ] Expand `projects/` with a **Reliance VF-Manual WMS** deep-dive page.
- [ ] Add an **LLM Inventory Agent** deep-dive (architecture + prompt flow).
- [ ] Add an **Observability / Event Store** design write-up (the cross-service
      irregular-event pattern used at Addverb Australia).
- [ ] Pin 3 public GitHub repos that mirror resume projects (scrubbed / demo).
- [ ] Add a short tech blog (Medium / Dev.to) on message-broker observability.
- [ ] AWS Certified Developer Associate — add once cleared.
- [ ] Replace Google Drive resume references everywhere with `resume/Rahul_Maurya.pdf` (done for portfolio, remaining on LinkedIn / other profiles).
- [ ] Capture p99 latency / QPS / data volume numbers per service.

---

## 7. How to keep this file fresh

**Rule (mandatory):** at the end of every working session with Rahul, update
this file so no context is lost between machines / sessions / LLMs.

Concretely, before wrapping up a session, check and update:

1. **§2 owner profile** — new role, new contact, new metric.
2. **§3 project portfolio** — new project shipped, new impact numbers, new
   detail page URL.
3. **§4 architecture** — new file added, new convention adopted, new build
   tooling, new design-system token.
4. **§6 TODOs** — close items that were shipped this session; add any new
   TODOs surfaced during the work.
5. **`_lastUpdated` in `data/site.json`** if content changed.
6. **The footer date below** (`_Last major update_`).

If you (the AI) are about to finish responding and any of the above changed
during the session and isn't captured here yet, **fix it before signing off**.
Do not create parallel context files — one source of truth only.

If tool-specific context files are desired later (e.g. `.cursorrules`,
`.windsurf/rules/context.md`), make them one-line pointers to this file.
`CLAUDE.md` already follows that pattern.

---

## 8. Change log (append-only, concise)

- **2026-04-19** — Phase-1 content hydration landed: `data/site.json` +
  `js/site.js`. Contact fields on `index.html` now hydrate from JSON with HTML
  fallback. Phone number (+91 79054 96720) added to hero links and contact
  section. Dark mode is the default; light mode available via toggle.
- **2026-04-19** — Portfolio redesigned: nav, hero, about, skills, experience,
  projects, contact. 4 project deep-dive pages with Mermaid HLD/LLD. Printable
  resume page + auto-generated `resume/Rahul_Maurya.pdf`. `404.html`,
  `robots.txt`, `sitemap.xml` added.

---

_Last major update: 2026-04-19. Owner: Rahul Maurya._
