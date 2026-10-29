#!/usr/bin/env python3
"""Build the resume from data/resume.json.

    python3 scripts/build_resume.py            # web page + both PDFs
    python3 scripts/build_resume.py --no-pdf   # web page only
    python3 scripts/build_resume.py --named    # + private PDFs with real client
                                               #   names, into ../personal-vault/resumes/

Outputs:
  resume/index.html          public web resume (never contains a phone number)
  resume/<variant pdf>       one PDF per variant (au, india), with the phone
                             number and work rights from the private contact
                             file (../personal-vault/facts/contact.json or
                             $PORTFOLIO_CONTACT). Print HTML is rendered in a
                             temp dir so the phone never lands in the repo.
"""
import argparse
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOLD = re.compile(r"\*\*(.+?)\*\*")


def md(text):
    """Escape, then turn **x** into <strong>x</strong>."""
    return BOLD.sub(r"<strong>\1</strong>", html.escape(text, quote=False))


def esc(text):
    return html.escape(text or "")


def years_since(start, today=None):
    """'2024-04' -> '2.5+': whole or half years elapsed, rounded down."""
    today = today or datetime.date.today()
    y, m = (int(x) for x in start.split("-"))
    months = (today.year - y) * 12 + today.month - m
    halves = max(months, 0) // 6
    return f"{halves // 2}+" if halves % 2 == 0 else f"{halves // 2}.5+"


def load_contact(path):
    if path and Path(path).is_file():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    print(f"WARN no private contact at {path}; PDFs will have no phone number")
    return {"phones": {}, "workRights": ""}


def default_contact_path():
    env = os.environ.get("PORTFOLIO_CONTACT")
    return Path(env) if env else ROOT.parent / "personal-vault" / "facts" / "contact.json"


def shown(item, variant):
    return not isinstance(item, dict) or variant in item.get("only", [variant])


def bullets(items, variant):
    return "".join(
        f"<li>{md(b['text'] if isinstance(b, dict) else b)}</li>" for b in items if shown(b, variant)
    )


def body(data, variant, contact=None, plain=False):
    """Resume body shared by the web page and the print variants.

    plain=True is the ATS-safe print form: visible URLs and | separators.
    """
    v = data["variants"][variant]
    contact = contact or {}
    bits = [esc(v["location"])]
    phone = (contact.get("phones") or {}).get(v.get("phone"))
    if phone:
        bits.append(esc(phone))
    bits.append(f'<a href="mailto:{esc(data["email"])}">{esc(data["email"])}</a>')
    for l in data["links"]:
        text = re.sub(r"^https?://(www\.)?", "", l["url"]).rstrip("/") if plain else l["label"]
        bits.append(f'<a href="{esc(l["url"])}">{esc(text)}</a>')
    sep = " | " if plain else " · "
    out = [
        f'<h1>{esc(data["name"])}</h1>',
        f'<p class="headline">{esc(data["headline"])}</p>',
        f'<p class="contact-line">{sep.join(bits)}</p>',
    ]
    rights = contact.get("workRights") if variant == "au" else ""
    if rights:
        out.append(f'<p class="contact-line"><strong>Work rights:</strong> {esc(rights)}</p>')

    summary = v["summary"]
    if data.get("careerStart"):
        summary = summary.replace("{years}", years_since(data["careerStart"]))
    out.append(f'<h2>Summary</h2><p>{md(summary)}</p>')

    out.append("<h2>Experience</h2>")
    for job in data["experience"]:
        if not shown(job, variant):
            continue
        out.append(
            '<div class="entry">'
            f'<h3>{esc(job["title"])} · {esc(job["company"])}</h3>'
            f'<p class="role-meta"><span>{esc(job["location"])}</span><span>{esc(job["dates"])}</span></p>'
            "<ul>" + bullets(job["bullets"], variant) + "</ul></div>"
        )

    out.append("<h2>Projects</h2>")
    for p in data["projects"]:
        if not shown(p, variant):
            continue
        name = esc(p["name"])
        if p.get("link"):
            name = f'<a href="{esc(p["link"])}">{name}</a>'
        out.append(
            '<div class="entry">'
            f'<div class="proj-head"><h3>{name} <span class="ctx">· {esc(p["context"])}</span></h3>'
            f'<span class="date">{esc(p["dates"])}</span></div>'
            "<ul>" + bullets(p["bullets"], variant) + "</ul></div>"
        )

    out.append('<h2>Technical Skills</h2><ul class="skills">')
    out += [f'<li><strong>{esc(s["group"])}:</strong> {esc(s["items"])}</li>'
            for s in data["skills"] if shown(s, variant)]
    out.append("</ul>")

    out.append("<h2>Education</h2>")
    for e in data["education"]:
        out.append(
            f'<h3>{esc(e["degree"])}</h3>'
            f'<p class="role-meta"><span>{esc(e["school"])} · {esc(e["detail"])}</span><span>{esc(e["dates"])}</span></p>'
        )

    learning = bullets(data["learning"], variant)
    if learning:
        out.append(f"<h2>Certifications &amp; Learning</h2><ul>{learning}</ul>")
    return "\n".join(out)


WEB_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<!-- GENERATED by scripts/build_resume.py from data/resume.json. Do not edit by hand. -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume — {name}</title>
    <meta name="description" content="{name} — {headline}. Java, Spring Boot, microservices, distributed systems.">
    <link rel="canonical" href="https://maurya2811.github.io/Portfolio/resume/">
    <meta property="og:image" content="https://maurya2811.github.io/Portfolio/images/og-card.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="../favicon.ico?v=3">
    <link rel="stylesheet" href="../css/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
    <script>try{{var t=localStorage.getItem('rm-theme');document.documentElement.setAttribute('data-theme',t==='light'?'light':'dark');}}catch(e){{}}</script>
    <style>
        .resume-doc {{ max-width: 820px; margin: 0 auto; padding: 48px 32px 80px; }}
        .resume-doc h1 {{ font-size: 34px; margin: 0; }}
        .resume-doc .headline {{ color: var(--accent); font-family: 'JetBrains Mono', monospace; font-size: 14px; margin: 4px 0 8px; }}
        .resume-doc .contact-line {{ color: var(--muted); font-size: 14px; margin: 0 0 6px; }}
        .resume-doc h2 {{ font-size: 13px; color: var(--accent); font-family: 'JetBrains Mono', monospace; letter-spacing: 1.5px; text-transform: uppercase; margin: 30px 0 10px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
        .resume-doc h3 {{ font-size: 16px; margin: 16px 0 2px; font-weight: 700; }}
        .resume-doc h3 .ctx {{ color: var(--muted); font-weight: 500; }}
        .resume-doc .proj-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; }}
        .resume-doc .proj-head .date {{ color: var(--muted); font-size: 13px; font-family: 'JetBrains Mono', monospace; white-space: nowrap; }}
        .resume-doc p {{ color: var(--muted); }}
        .resume-doc .role-meta {{ display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; font-size: 13px; margin: 0 0 6px; font-family: 'JetBrains Mono', monospace; }}
        .resume-doc ul {{ margin: 4px 0 10px; padding-left: 20px; color: var(--muted); font-size: 14.5px; }}
        .resume-doc ul li {{ margin-bottom: 5px; }}
        .resume-doc ul.skills {{ list-style: none; padding-left: 0; }}
        .resume-actions {{ display: flex; gap: 10px; margin: 18px 0 6px; flex-wrap: wrap; }}
        .resume-note {{ font-size: 13px; color: var(--muted); margin: 0 0 8px; }}
    </style>
</head>

<body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="nav">
        <a href="../" class="brand">RM<span>.</span></a>
        <nav aria-label="Primary">
            <a href="../#about">About</a>
            <a href="../#experience">Experience</a>
            <a href="../projects/">Case Studies</a>
            <a href="../notes/">Notes</a>
            <a href="../#contact">Contact</a>
        </nav>
        <a class="nav-cta" href="{pdf_au}" target="_blank" rel="noopener">Download PDF</a>
    </header>

    <main id="main" class="resume-doc">
        <div class="resume-actions">
            <a class="btn btn-primary" href="{pdf_au}" target="_blank" rel="noopener">PDF · Australia</a>
            <a class="btn" href="{pdf_in}" target="_blank" rel="noopener">PDF · India</a>
        </div>
        <p class="resume-note">Phone number is on the PDF.</p>
{body}
    </main>

    <footer class="footer"><p>© <span id="year">2026</span> {name}</p></footer>
    <script src="../js/theme.js" defer></script>
    <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""

PRINT_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{name} - Software Engineer Resume</title><meta name="author" content="{name}">
<style>
  @page {{ size: A4; margin: 12mm 13mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Helvetica Neue', Arial, 'Liberation Sans', sans-serif; color: #111; font-size: 10pt; line-height: 1.38; margin: 0; }}
  a {{ color: #0b4f9c; text-decoration: none; }}
  h1 {{ font-size: 20pt; margin: 0; letter-spacing: .2px; }}
  .headline {{ margin: 1px 0 3px; font-size: 10.5pt; font-weight: 600; color: #0a6b4a; }}
  .contact-line {{ margin: 0 0 2px; font-size: 9.2pt; color: #333; }}
  .contact-line a {{ white-space: nowrap; }}
  h2 {{ font-size: 10pt; text-transform: uppercase; letter-spacing: 1.2px; color: #0a6b4a; border-bottom: 1px solid #bbb; padding-bottom: 2px; margin: 11px 0 5px; }}
  h3 {{ font-size: 10.2pt; margin: 6px 0 0; }}
  h3 .ctx {{ font-weight: 400; color: #444; }}
  .proj-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-top: 6px; }}
  .proj-head h3 {{ margin: 0; }}
  .proj-head .date {{ font-size: 9pt; color: #444; white-space: nowrap; }}
  p {{ margin: 0 0 4px; }}
  .role-meta {{ display: flex; justify-content: space-between; font-size: 9pt; color: #444; margin: 0 0 2px; }}
  ul {{ margin: 1px 0 4px; padding-left: 15px; }}
  li {{ margin-bottom: 2px; }}
  ul.skills {{ list-style: none; padding-left: 0; }}
  h2, h3 {{ break-after: avoid; }}
  li, .entry {{ break-inside: avoid; }}
  .compact {{ font-size: 9.3pt; line-height: 1.3; }}
  .compact h2 {{ margin: 8px 0 4px; }}
  .compact h3 {{ margin: 4px 0 0; }}
  .compact li {{ margin-bottom: 1px; }}
</style></head>
<body{body_attr}>
{body}
</body></html>
"""


def render_web(data):
    pdf_au = data["variants"]["au"].get("pdf", "Rahul_Maurya.pdf")
    pdf_in = data["variants"]["india"].get("pdf", "Rahul_Maurya_India.pdf")
    content = "\n".join("        " + line for line in body(data, "au").splitlines())
    return WEB_TEMPLATE.format(name=esc(data["name"]), headline=esc(data["headline"]),
                               pdf_au=esc(pdf_au), pdf_in=esc(pdf_in), body=content)


def render_print(data, variant, contact):
    body_attr = ' class="compact"' if data["variants"][variant].get("compact") else ""
    text = body(data, variant, contact, plain=True)
    # Older ATS parsers mangle arrows and the Unicode minus sign.
    text = text.replace(" → ", " to ").replace("→", " to ").replace("−", "-")
    return PRINT_TEMPLATE.format(name=esc(data["name"]), body=text, body_attr=body_attr)


def load_names(path):
    """Private {anonymised phrase: real client name} map for named resumes."""
    if path and Path(path).is_file():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    print(f"WARN no client-names map at {path}; named resumes skipped")
    return None


def apply_names(html_text, names):
    for anon, real in names.items():
        if not anon.startswith("_"):
            html_text = html_text.replace(anon, real)
    return html_text


def public_names(data, names):
    """Names map to apply to the public PDFs, only when the owner opted in."""
    return names if names and data.get("namesInPublicPdfs") else None


def find_chrome():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(name):
            return name
    return None


def build_pdf(chrome, html_text, out_path):
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "resume.html"
        src.write_text(html_text, encoding="utf-8")
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
             "--print-to-pdf-no-header", f"--print-to-pdf={out_path}", src.as_uri()],
            check=True, capture_output=True,
        )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--contact", type=Path, default=None)
    ap.add_argument("--named", action="store_true",
                    help="also write private PDFs with real client names into ../personal-vault/resumes/")
    args = ap.parse_args()

    data = json.loads((ROOT / "data" / "resume.json").read_text(encoding="utf-8"))
    (ROOT / "resume" / "index.html").write_text(render_web(data), encoding="utf-8")
    print("wrote resume/index.html")
    if args.no_pdf:
        return 0

    chrome = find_chrome()
    if not chrome:
        print("WARN no Chrome/Chromium found; PDFs not rebuilt")
        return 0
    contact = load_contact(args.contact or default_contact_path())
    vault = ROOT.parent / "personal-vault"
    names = None
    if args.named or data.get("namesInPublicPdfs"):
        names = load_names(vault / "facts" / "client-names.json")
    pub = public_names(data, names)
    for variant, v in data["variants"].items():
        out = ROOT / "resume" / v["pdf"]
        html_text = render_print(data, variant, contact)
        build_pdf(chrome, apply_names(html_text, pub) if pub else html_text, out)
        print(f"wrote resume/{v['pdf']}" + (" (with client names)" if pub else ""))

    if args.named:
        if names:
            for variant, v in data["variants"].items():
                out = vault / "resumes" / v["pdf"].replace(".pdf", "_named.pdf")
                build_pdf(chrome, apply_names(render_print(data, variant, contact), names), out)
                print(f"wrote {out.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
