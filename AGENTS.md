# AGENTS.md — AI assistant onboarding (single source of truth)

> Read this first. It is written so any AI assistant (Claude Code, Codex,
> Cursor, Copilot, Aider, Windsurf, ...) on any machine can continue work with
> **no chat history**. `CLAUDE.md`, `.cursorrules` and
> `.github/copilot-instructions.md` are pointers to this file plus the
> command cheat-sheet.

---

## 0. Two repos, one rule

| Repo | Visibility | Holds |
|---|---|---|
| `Portfolio` (this repo) | **PUBLIC** (GitHub Pages) | Anonymised site, resume source, scripts |
| `personal-vault` | **PRIVATE** | Facts ledger with real client names, phone numbers, ID scans, career strategy, job-search tracker, interview story bank |

Expected layout after cloning on a new laptop:

```bash
mkdir -p ~/Documents/Projects && cd ~/Documents/Projects
git clone git@github.com:Maurya2811/Portfolio.git
git clone git@github.com:Maurya2811/personal-vault.git   # private
```

If `../personal-vault/` exists, **read `../personal-vault/AGENTS.md` too** before
writing content: it holds the unredacted facts ledger
(`facts/facts-ledger.md`), which is the source of truth for every number.

**Rule:** anything confidential (client names, internal service names, contract
values, phone numbers, salary, job-search plans) goes in the vault, never here.
`scripts/check.py` enforces this using `../personal-vault/facts/blocklist.txt`.

---

## 1. Purpose and audience

Personal portfolio of **Rahul Maurya**, a backend software engineer, live at
**https://maurya2811.github.io/Portfolio**. Goal: land a **high-paying backend /
platform / forward-deployed software engineering role** (Australia first, India
as fallback). Readers are recruiters (10-second scan) and hiring managers or
interviewers (deep read of the case studies). Every claim must survive an
interviewer asking "how did you measure that?".

---

## 2. Owner profile (public-safe)

| Field | Value |
|---|---|
| Name | Rahul Maurya |
| Positioning headline | Software Engineer · Backend & Distributed Systems |
| Current | Software Engineer (Forward Deployed), **Addverb Australia**, Melbourne, Jan 2026 – Present. Two customer engagements: retail DC platform (main) and a metro rail project (UAT / defect triage) |
| Previous | Software Development Engineer, **Addverb Technologies**, Noida, Apr 2024 – Dec 2025 |
| Internships | Software Engineering Intern, **NEC Corporation India**, Oct 2023 – Jan 2024; Summer Intern (Web Development), **Celebal Technologies**, remote, May – Jun 2023 (hotel room-booking app, MERN) |
| Education | B.Tech CSE, Raj Kumar Goel Institute of Technology (AKTU), 2020–2024, CGPA 8.89 |
| Base | Melbourne, Australia |
| Email | maurya2811@gmail.com |
| Phone | **Not on the website.** Only in resume PDFs, injected from the vault |
| LinkedIn | https://www.linkedin.com/in/rahul-maurya-277069227 |
| GitHub | https://github.com/Maurya2811 |
| LeetCode | https://leetcode.com/Rahul_2811/ |
| Target roles | Backend SWE, Platform / Distributed Systems Engineer, Forward Deployed Engineer, SDE-2 |

Skills, with honesty tiers (do not promote a tier without asking Rahul):
- **Production:** Java 17, Spring Boot, Spring Data JPA, REST, RabbitMQ, MongoDB, MySQL, SQL Server, Docker, Kubernetes, Helm, Jenkins, Git, Grafana, Python scripting, Angular (operator screens), nginx, incident RCA / runbooks, PLC and host-system interface contracts
- **Used in projects:** Kafka, Redis, Jaeger, concurrency, LLM APIs / RAG / tool calling, React / Node.js (student projects), AI-assisted development (Claude Code)
- **Working knowledge:** AWS (EC2, EKS, S3, RDS, IAM), gRPC, GraphQL, OAuth2/JWT, Terraform, LangChain
- **In progress:** AWS Certified Solutions Architect – Associate (NOT certified yet; never write "certified")

---

## 3. Canonical metrics (public wording, use verbatim)

Reconciled 2026-10-29. Where older documents disagreed, the conservative value
won. Provenance for each number is in the vault ledger.

| Metric | Public wording |
|---|---|
| Experience | computed: `{years}` in `data/resume.json` renders years since `careerStart` (2024-04), e.g. "2.5+". Site copy says "since 2024" so it never goes stale |
| GTP throughput | 800 → 1,200 totes/hr (+50%) |
| SLA | closed the gap to the contracted throughput SLA; unblocked a seven-figure (AUD) contractual milestone. **Never publish the exact SLA rate or contract value** |
| Flow segregation | +30% client operational efficiency |
| Current platform size | 20+ microservices (maintained / evolved) |
| Decomposition | 12+ microservices (decomposed from monolith, previous role) |
| Latency | p95 800 ms → 600 ms (−25%) |
| Uptime | 99.6% |
| Events | 10,000+ events/min, zero data loss |
| LLM assistant | 75%+ queries auto-resolved, −40% support tickets |
| Grafana tool | 8 hrs → 20 min, 200+ dashboards, 3 environments |
| Incident response | −60% |
| Production incidents | led RCA for 20+ |
| Mentoring | mentored interns in the India team (no further detail confirmed) |
| Clients | 5+ enterprise clients |
| Shuttle telemetry | 99.6% capture, 50+ devices, −70% downtime diagnosis |
| Tote routing | −200 ms per decision, −15% path resolution, +12% pilot throughput |
| Deep-lane ASRS | 500+ daily transactions, interface testing 3 months → 3 weeks, UAT ~2x faster |
| Grocery WMS | 70+ critical UAT defects fixed, 14 leadership demos, note of appreciation |

Banned: percentage claims with wrong arithmetic (e.g. "+200%" for 6 → 3 weeks),
internal cost savings, "early adopter / drives innovation" style fluff.

---

## 4. Confidentiality and IP policy (mandatory for every edit)

The case studies exist so Rahul can discuss architecture in interviews **without
breaching employer or client confidentiality**.

Allowed in public:
- Employer names (Addverb Australia, Addverb Technologies, NEC) and job titles.
- Anonymised client descriptors only: "tier-1 global retail brand, 3PL-operated DC",
  "US healthcare logistics provider", "D2C retailer fulfilment centre",
  "tyre manufacturing plant", "large Indian grocery retailer".
- Generic, textbook-level patterns: event-driven choreography, idempotent consumers,
  DLQ + replay, outbox, adapters / anti-corruption layers, Dijkstra / Yen's K-shortest,
  scored slot selection (concept only), RAG + allowlisted tools.
- Generic service names: Order Orchestrator, Allocation Service, Slotting / Location
  Service, GTP Station Service, Robot Cell Adapter, Hardware Fleet Adapters,
  Host Integration, Identity Service.
- Rahul's own measured outcomes as listed in section 3.

Never in public:
- Client or hardware-vendor names, client site cities, internal product / service
  codenames, repository names, file paths, hostnames, IPs, queue / exchange / topic
  names, DB / table names, config values, credentials, screenshots of internal tools.
- Contract values, SLA figures, pricing, internal cost data.
- Proprietary algorithm details (weights, formulas, thresholds).
- Real code from employer repositories. Demo code must be written from scratch.
- Phone numbers, ID documents, salary or job-search strategy.

Every case study carries the disclaimer: *simplified and anonymised; no proprietary
code, configuration, topology or client data.*

---

## 5. Repository map

```
Portfolio/
├── index.html               Home: hero + metrics, about, experience, featured case studies, skills, notes, contact
├── projects/                Case studies (anonymised)
│   ├── index.html           listing
│   ├── retail-dc-platform.html     flagship (current role)
│   ├── event-observability.html    design deep-dive behind the flagship
│   ├── llm-inventory-agent.html
│   ├── shuttle-telemetry.html
│   ├── tote-routing.html
│   ├── deep-lane-asrs.html
│   └── grafana-migration.html
├── notes/                   Short engineering write-ups (index + 2 notes)
├── resume/
│   ├── index.html           GENERATED web resume (no phone)
│   ├── Rahul_Maurya.pdf     GENERATED, Australia variant (+61)
│   └── Rahul_Maurya_India.pdf  GENERATED, India variant (+91)
├── data/
│   ├── resume.json          SOURCE for all resume outputs
│   └── site.json            contact / link values hydrated by js/site.js
├── css/styles.css           design tokens + components (dark default)
├── js/theme.js              theme toggle + Mermaid theming
├── js/site.js               data-bind hydration (HTML fallback always present)
├── scripts/check.py         publish gate: blocklist, leaks, links, JSON
├── scripts/build_resume.py  resume.json -> web page + PDFs
├── tests/                   unittest suites for both scripts
├── .wave/ac.md              acceptance criteria for the scripts
├── images/og-card.png      social preview (source scripts/og-card.html)
├── 404.html, robots.txt, sitemap.xml, favicon.ico
└── AGENTS.md / CLAUDE.md / README.md
```

---

## 6. Commands

```bash
python3 -m http.server 8000                 # preview at http://localhost:8000
python3 scripts/build_resume.py             # rebuild resume page + both PDFs (needs Chrome/Chromium)
python3 scripts/build_resume.py --no-pdf    # web page only
python3 -m unittest discover -s tests       # tests
python3 scripts/check.py                    # publish gate; MUST print OK before any push
```

No `npm`, no bundler, no framework. Python 3 standard library only.

---

## 7. Conventions

- **Static site, no build step for pages.** Hand-written HTML. Only the resume is generated, and its output is committed.
- **Dark theme by default.** Colours come from CSS variables in `css/styles.css` (`--bg`, `--bg-elev`, `--bg-soft`, `--border`, `--text`, `--muted`, `--accent`, `--accent-2`, `--chip`, `--diagram-bg`). Never hardcode colours.
- Every page needs the no-flash theme snippet in `<head>`, the skip link, the shared nav (About, Experience, Case Studies, Notes, Contact, Resume CTA) and the footer.
- **Mermaid:** `<pre class="mermaid">` inside `.diagram`. Load `mermaid@10.9.1` with the SRI `integrity` attribute copied from an existing case study. `js/theme.js` owns `mermaid.initialize`; never call it per page.
- **Case-study structure:** Context → Problem → What I did → Reference architecture → Low-level flow → Trade-offs table → Failure modes → Impact → What I would do differently → Interview talking points → Tech. Copy `projects/retail-dc-platform.html`.
- **New page checklist:** add a card to `projects/index.html` (and the home page if featured), add to `sitemap.xml`, add to the page-nav chain, run `scripts/check.py`.
- **ATS rules for the resume:** single column, standard headings (Summary, Experience, Projects, Technical Skills, Education, Certifications & Learning), visible plain URLs, no icons/tables/images, ASCII in print. Tests in `tests/test_build_resume.py` enforce this.
- **Evergreen copy:** never hard-code durations ("2.5 years") or "currently learning" claims in HTML. Use dates ("since 2024") or the computed `{years}` in `data/resume.json`.
- **Social preview:** every page carries `og:image` → `images/og-card.png` (source: `scripts/og-card.html`; regenerate command inside it).
- **Writing style:** plain, direct, first person, active voice. No emojis. Avoid "leveraged", "seamless", "robust", "spearheaded", "synergy".
- **Accessibility:** semantic landmarks, `aria-label` on icon-only buttons, AA contrast in both themes, visible focus.
- **Commits:** conventional commits (`feat:`, `fix:`, `docs:`, `chore:`). **Never commit or push unless Rahul explicitly asks in that request.**
- Code changes follow test-first: add AC to `.wave/ac.md`, write a failing test, then implement.

---

## 8. Session protocol for AI assistants

At the start: read this file, then `../personal-vault/AGENTS.md` if present.

At the end of any session that changed facts, files or plans:
1. Update section 3 here **and** the vault ledger if a metric changed.
2. Update section 5 if files were added or removed.
3. Update section 9 (TODO) and append to section 10 (change log).
4. Bump `_lastUpdated` in `data/site.json` / `data/resume.json` if content changed.
5. Run `python3 scripts/check.py` and the tests; both must pass.
6. Personal and job-search notes go to `../personal-vault/` (see its AGENTS.md).

---

## 9. Open TODO (ranked by hiring impact)

- [ ] Build public demo repo #1: event-driven warehouse simulator (Spring Boot, Kafka/RabbitMQ, outbox, idempotent consumers, DLQ, Grafana). Written from scratch, MIT licence, linked from the flagship case study.
- [ ] Build public demo repo #2: LLM ops assistant with an eval harness (allowlisted tools, golden-question set, accuracy and latency report).
- [ ] GitHub: paste bio + profile README from `personal-vault/job-search/profiles-copy.md`, archive the 2023 student repos, pin the demo repos + this portfolio.
- [ ] Ask 2-3 colleagues / client contacts for LinkedIn recommendations (social proof is the weakest area).
- [ ] Align the LinkedIn headline, About and Experience with `data/resume.json`.
- [ ] Clear AWS SAA-C03; then move it from "in preparation" to certified in `data/resume.json`.
- [ ] Optional: custom domain (e.g. rahulmaurya.dev). Add a `CNAME` file, then replace `https://maurya2811.github.io/Portfolio` everywhere (`grep -rl` + `sed`) and update `robots.txt` / `sitemap.xml`.
- [ ] Rebuild the resume PDF at least every 6 months (the years figure is computed at build time).
- [ ] Publish the two notes on dev.to / Medium with a canonical link back to the site.

---

## 10. Change log (append-only)

- **2026-10-30 (b)**: Title now "Software Engineer (Forward Deployed)". Added: 20+ production incidents, mentoring interns, metro-rail FDE engagement (client anonymised and added to the vault blocklist), Celebal internship (AU resume + site only). `only` filter now also applies to experience entries.
- **2026-10-30**: Recruiter pass. Outcome-led case-study titles; "What I bring" block; skills now include Angular, nginx, reliability/RCA, AI-assisted dev. Resume: jargon translated (fulfilment throughput), incident-RCA bullet, per-variant content (`only`), India variant is 1 page (`compact`), ATS-safe print (visible URLs, `|` separators, ASCII arrows/minus, standard `Projects` heading, non-wrapping URLs). LinkedIn/GitHub copy drafted in the vault (`job-search/profiles-copy.md`).
- **2026-10-29 (b)**: Facts confirmed by Rahul: CGPA 8.89, LLM assistant 75%+, Grafana 200+ dashboards. AU work rights (Subclass 482, nomination transfer) added to the AU PDF via the vault. Experience years computed at build time. Evergreen home copy, resume-first hero CTA, `og:image` social card on all pages.
- **2026-10-29**: Full redesign for job hunting. All client names and internal codenames removed; case studies rewritten as anonymised reference architectures with trade-offs, failure modes and talking points. Three new case studies (event observability, LLM assistant, Grafana tool) and a notes section were added. Resume is now single-source (`data/resume.json` → web + AU/India PDFs; phone only in PDFs, from the vault). Metrics reconciled across all old resumes. `scripts/check.py` publish gate and tests added. Personal files (ID scans, career report, old resumes) moved to the private `personal-vault`. Unused images deleted. Git history squashed to remove previously published confidential material.
- **2026-04-19**: Phase-1 hydration (`data/site.json` + `js/site.js`); dark default; first redesign with Mermaid deep-dives.

_Last major update: 2026-10-29._
