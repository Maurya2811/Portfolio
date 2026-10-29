# Acceptance criteria: `scripts/check.py` (portfolio publish gate)

## AC-1 Blocked terms
Trigger: `python3 scripts/check.py` runs while a publishable text file (`.html`, `.md`, `.json`, `.js`, `.css`, `.xml`, `.txt`) contains a term from the blocklist (whole word, case-insensitive).
Observable: exit code 1 and a line `BLOCKED <path>:<line>: <term>` for each hit.
Rejects: a repo where `projects/x.html` contains "Acme" while `Acme` is in the blocklist exits 0.

## AC-2 Built-in leak patterns
Trigger: a publishable file contains an IPv4 address, a `/home/<user>/` path, a `jdbc:` URL or a `password=` assignment.
Observable: exit code 1 with `LEAK <path>:<line>: <pattern-name>`.
Rejects: `10.1.2.3` in `index.html` passing the check.

## AC-3 Broken internal links
Trigger: an `href` or `src` in an `.html` file points to a relative path that does not exist in the repo (anchors, `mailto:`, `tel:`, `http(s):` and `//` are skipped; `dir/` resolves to `dir/index.html`).
Observable: exit code 1 with `LINK <path>: <target>`.
Rejects: `<a href="projects/missing.html">` passing the check.

## AC-4 Invalid JSON
Trigger: any `data/*.json` fails to parse.
Observable: exit code 1 with `JSON <path>: <error>`.
Rejects: a truncated `data/site.json` passing.

## AC-5 Clean repo passes, private list is optional
Trigger: the check runs on a repo with none of the above problems; the blocklist is read from `--blocklist`, else `$PORTFOLIO_BLOCKLIST`, else `../personal-vault/facts/blocklist.txt`.
Observable: exit code 0 and `OK`. If no blocklist file is found, a `WARN no blocklist` line is printed and the built-in checks still run.
Rejects: a missing blocklist causing a crash or a silent exit 0 with no warning.

# Acceptance criteria: `scripts/build_resume.py` (single-source resume)

## AC-6 Web page never carries a phone number
Trigger: `build_resume.py` renders the web resume from `data/resume.json` with a private contact file that has phone numbers.
Observable: the output `resume/index.html` contains the owner name, every experience entry, and none of the phone numbers.
Rejects: a web page that shows any phone digits.

## AC-7 Print variants carry the right phone and location line
Trigger: the print HTML is rendered for variant `au` and for variant `india`.
Observable: `au` contains the AU phone and the AU location line and not the India phone; `india` contains the India phone and its own location line and not the AU phone. Work rights appear only on `au`, only when set.
Rejects: the India PDF showing the AU number, or an empty work-rights label being rendered.

## AC-8 Missing private contact degrades safely
Trigger: the private contact file is absent.
Observable: rendering still succeeds, prints `WARN no private contact`, and no phone line is rendered.
Rejects: a crash, or a literal placeholder such as "None" appearing in output.

## AC-9 Bold markup and escaping
Trigger: a bullet contains `**800 → 1,200**` and a `<` character.
Observable: output contains `<strong>800 → 1,200</strong>` and `&lt;`.
Rejects: raw `**` or unescaped `<` in output.

## AC-10 Experience years never go stale
Trigger: a summary in `data/resume.json` contains `{years}` and the file has `"careerStart": "YYYY-MM"`.
Observable: `{years}` renders as whole or half years since `careerStart`, rounded down, with a `+` (Apr 2024 → Oct 2026 renders `2.5+`; → Apr 2027 renders `3+`).
Rejects: a literal `{years}` in output, or rounding up (e.g. `3+` in Mar 2027).
