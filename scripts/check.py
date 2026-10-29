#!/usr/bin/env python3
"""Publish gate for the portfolio. Run before every push:

    python3 scripts/check.py

Fails (exit 1) on:
  BLOCKED  a confidential term from the private blocklist (client names,
           internal codenames, phone numbers). The list lives outside this
           public repo: --blocklist, $PORTFOLIO_BLOCKLIST, or
           ../personal-vault/facts/blocklist.txt.
  LEAK     IPv4 addresses, /home/<user>/ paths, jdbc: URLs, password=.
  LINK     relative href/src that does not resolve inside the repo.
  JSON     data/*.json that does not parse.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

TEXT_EXT = {".html", ".md", ".json", ".js", ".css", ".xml", ".txt"}
SKIP_DIRS = {".git", ".wave", "tests", "node_modules"}
# scripts/ is skipped because this file names the leak patterns it hunts for.
SKIP_TOP = {"scripts"}

LEAK_PATTERNS = [
    ("ipv4", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("home-path", re.compile(r"/home/[A-Za-z0-9_.-]+/")),
    ("jdbc", re.compile(r"jdbc:", re.I)),
    ("password", re.compile(r"\b(?:password|passwd|pwd)\s*[=:]\s*\S", re.I)),
]
LINK_RE = re.compile(r"""(?<![\w-])(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
EXTERNAL = ("http:", "https:", "//", "mailto:", "tel:", "#", "data:", "javascript:")


def default_blocklist(root):
    env = os.environ.get("PORTFOLIO_BLOCKLIST")
    if env:
        return Path(env)
    return root.resolve().parent / "personal-vault" / "facts" / "blocklist.txt"


def load_blocklist(path):
    if not path or not path.is_file():
        return None
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            words = [re.escape(w) for w in line.split()]
            pattern = r"(?<![\w-])" + r"\s+".join(words) + r"(?![\w-])"
            terms.append((line.lower(), re.compile(pattern, re.I)))
    return terms


def publishable_files(root):
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if not path.is_file() or path.suffix.lower() not in TEXT_EXT:
            continue
        if any(part in SKIP_DIRS for part in rel.parts) or rel.parts[0] in SKIP_TOP:
            continue
        yield path, rel.as_posix()


def check_link(root, path, target):
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target or target.lower().startswith(EXTERNAL):
        return True
    if target.startswith("/"):
        # Absolute site paths are served under /Portfolio/ on GitHub Pages.
        target = re.sub(r"^/Portfolio/?", "", target)
        resolved = root / target
    else:
        resolved = path.parent / target
    if target.endswith("/") or resolved.is_dir():
        resolved = resolved / "index.html"
    return resolved.exists()


def run(root, blocklist_path):
    problems = []
    terms = load_blocklist(blocklist_path)
    if terms is None:
        print(f"WARN no blocklist at {blocklist_path}; confidential-term scan skipped")
        terms = []

    for path, rel in publishable_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            for name, rx in terms:
                if rx.search(line):
                    problems.append(f"BLOCKED {rel}:{n}: {name}")
            for name, rx in LEAK_PATTERNS:
                if rx.search(line):
                    problems.append(f"LEAK {rel}:{n}: {name}")
        if path.suffix == ".html":
            for target in LINK_RE.findall(text):
                if not check_link(root, path, target):
                    problems.append(f"LINK {rel}: {target}")

    for path in sorted((root / "data").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except ValueError as e:
            problems.append(f"JSON {path.relative_to(root).as_posix()}: {e}")

    for p in problems:
        print(p)
    if problems:
        print(f"FAIL {len(problems)} problem(s)")
        return 1
    print("OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path)
    ap.add_argument("--blocklist", type=Path)
    args = ap.parse_args()
    return run(args.root, args.blocklist or default_blocklist(args.root))


if __name__ == "__main__":
    sys.exit(main())
