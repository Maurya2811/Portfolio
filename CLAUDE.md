# CLAUDE.md

Full context (owner profile, canonical metrics, confidentiality policy, session
protocol) is in **[`AGENTS.md`](./AGENTS.md)**. Read it before changing content.
If `../personal-vault/` exists, also read `../personal-vault/AGENTS.md` (private
facts ledger with the real numbers and their sources).

## What this is
Public, static portfolio for Rahul Maurya (backend software engineer), served by
GitHub Pages from `main` at https://maurya2811.github.io/Portfolio. The goal is
landing a high-paying backend / platform / forward-deployed engineering role.

## Commands
```bash
python3 -m http.server 8000               # preview
python3 scripts/build_resume.py           # data/resume.json -> resume/index.html + 2 PDFs
python3 -m unittest discover -s tests     # tests
python3 scripts/check.py                  # publish gate, must print OK before any push
```
Python 3 stdlib only. Chrome or Chromium is needed for PDFs.

## Module map
- `index.html`: home page. `projects/`: anonymised case studies. `notes/`: write-ups.
- `data/resume.json` is the source of all resume outputs. `resume/*` is generated, so never hand-edit it.
- `data/site.json` + `js/site.js`: contact-link hydration (HTML keeps a fallback).
- `css/styles.css`: tokens + components. `js/theme.js`: dark default, Mermaid theming.
- `scripts/check.py`: blocks confidential terms (list in the vault), IPs, paths and broken links.

## Hard rules
1. **Public repo.** No client or vendor names, internal codenames, paths, hosts,
   contract figures, phone numbers or personal documents. See AGENTS.md section 4.
2. Never invent experience or metrics. Use AGENTS.md section 3 wording verbatim.
3. Never `git commit` / `git push` unless Rahul explicitly asks in that request.
4. No frameworks, npm or bundlers. No emojis. Colours only via CSS variables.
5. Test-first for script changes (`.wave/ac.md` → failing test → code).
6. At session end, follow AGENTS.md section 8 (update ledger, TODO, change log; run the check).
