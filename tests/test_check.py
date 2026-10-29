"""Tests for scripts/check.py. Run: python3 -m unittest discover -s tests"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECK = Path(__file__).resolve().parent.parent / "scripts" / "check.py"


def run_check(root, blocklist=None):
    args = [sys.executable, str(CHECK), "--root", str(root)]
    if blocklist is not None:
        args += ["--blocklist", str(blocklist)]
    env = dict(os.environ)
    env.pop("PORTFOLIO_BLOCKLIST", None)
    return subprocess.run(args, capture_output=True, text=True, env=env)


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "site"
        (self.root / "projects").mkdir(parents=True)
        (self.root / "data").mkdir()
        (self.root / "index.html").write_text(
            '<a href="projects/">p</a><a href="#top">t</a>'
            '<a href="mailto:a@b.c">m</a><a href="https://x.y">x</a>'
        )
        (self.root / "projects" / "index.html").write_text('<a href="../index.html">h</a>')
        (self.root / "data" / "site.json").write_text('{"a": 1}')
        self.blocklist = Path(self.tmp.name) / "blocklist.txt"
        self.blocklist.write_text("# comment\nacme\nfoo corp\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_repo_passes(self):
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("OK", r.stdout)

    def test_blocked_term_fails(self):
        (self.root / "projects" / "x.html").write_text("line1\nBuilt for ACME warehouse\n")
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 1)
        self.assertIn("BLOCKED projects/x.html:2: acme", r.stdout)

    def test_blocked_term_is_whole_word(self):
        (self.root / "projects" / "x.html").write_text("acmeology is fine")
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_multiword_term(self):
        (self.root / "README.md").write_text("worked at Foo  Corp")
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 1)
        self.assertIn("BLOCKED README.md:1: foo corp", r.stdout)

    def test_ip_address_leak(self):
        (self.root / "index.html").write_text("db at 10.1.2.3")
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 1)
        self.assertIn("LEAK index.html:1: ipv4", r.stdout)

    def test_home_path_jdbc_password_leaks(self):
        (self.root / "a.md").write_text("/home/someone/src\njdbc:sqlserver://h\npassword=hunter2\n")
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 1)
        self.assertIn("LEAK a.md:1: home-path", r.stdout)
        self.assertIn("LEAK a.md:2: jdbc", r.stdout)
        self.assertIn("LEAK a.md:3: password", r.stdout)

    def test_broken_link_fails(self):
        (self.root / "index.html").write_text('<a href="projects/missing.html">x</a>')
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 1)
        self.assertIn("LINK index.html: projects/missing.html", r.stdout)

    def test_data_bind_href_is_not_a_link(self):
        (self.root / "index.html").write_text('<a href="projects/" data-bind-href="owner.github">x</a>')
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_invalid_json_fails(self):
        (self.root / "data" / "site.json").write_text('{"a": ')
        r = run_check(self.root, self.blocklist)
        self.assertEqual(r.returncode, 1)
        self.assertIn("JSON data/site.json", r.stdout)

    def test_missing_blocklist_warns_but_runs(self):
        r = run_check(self.root, Path(self.tmp.name) / "nope.txt")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("WARN no blocklist", r.stdout)
        (self.root / "index.html").write_text("10.0.0.1")
        r = run_check(self.root, Path(self.tmp.name) / "nope.txt")
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
