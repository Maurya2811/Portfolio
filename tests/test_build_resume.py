"""Tests for scripts/build_resume.py. Run: python3 -m unittest discover -s tests"""
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_resume.py"
spec = importlib.util.spec_from_file_location("build_resume", SCRIPT)
br = importlib.util.module_from_spec(spec)
spec.loader.exec_module(br)

DATA = {
    "name": "Test Person",
    "headline": "Software Engineer",
    "email": "t@example.com",
    "links": [{"label": "GitHub", "url": "https://github.com/x"}],
    "variants": {
        "au": {"location": "Melbourne, Australia", "phone": "au", "summary": "AU summary"},
        "india": {"location": "Open to relocation to India", "phone": "india", "summary": "IN summary"},
    },
    "skills": [{"group": "Languages", "items": "Java, SQL"}],
    "experience": [
        {"company": "Co A", "title": "Engineer", "location": "City", "dates": "2026",
         "bullets": ["Raised throughput **800 → 1,200** totes/hr when x < y"]},
        {"company": "Co B", "title": "Intern", "location": "City", "dates": "2023", "bullets": ["b"]},
    ],
    "projects": [{"name": "P", "context": "ctx", "dates": "2025", "bullets": ["pb"]}],
    "education": [{"degree": "B.Tech", "school": "S", "dates": "2020 - 2024", "detail": "CGPA 9"}],
    "learning": ["Course"],
}
CONTACT = {"phones": {"au": "+61 400 000 001", "india": "+91 90000 00002"}, "workRights": "Full work rights"}


class BuildResumeTests(unittest.TestCase):
    def test_web_has_no_phone(self):
        html = br.render_web(DATA)
        self.assertIn("Test Person", html)
        self.assertIn("Co A", html)
        self.assertIn("Co B", html)
        for p in CONTACT["phones"].values():
            self.assertNotIn(p, html)
            self.assertNotIn(p.replace(" ", ""), html)

    def test_au_variant(self):
        html = br.render_print(DATA, "au", CONTACT)
        self.assertIn("+61 400 000 001", html)
        self.assertNotIn("+91 90000 00002", html)
        self.assertIn("Melbourne, Australia", html)
        self.assertIn("Full work rights", html)

    def test_india_variant(self):
        html = br.render_print(DATA, "india", CONTACT)
        self.assertIn("+91 90000 00002", html)
        self.assertNotIn("+61 400 000 001", html)
        self.assertIn("Open to relocation to India", html)
        self.assertNotIn("Full work rights", html)

    def test_empty_work_rights_not_rendered(self):
        html = br.render_print(DATA, "au", {"phones": CONTACT["phones"], "workRights": ""})
        self.assertNotIn("Work rights", html)

    def test_missing_contact(self):
        with tempfile.TemporaryDirectory() as d:
            buf = io.StringIO()
            with redirect_stdout(buf):
                contact = br.load_contact(Path(d) / "missing.json")
            self.assertIn("WARN no private contact", buf.getvalue())
            html = br.render_print(DATA, "au", contact)
        self.assertNotIn("None", html)
        self.assertNotIn("+61", html)

    def test_bold_and_escaping(self):
        html = br.render_web(DATA)
        self.assertIn("<strong>800 → 1,200</strong>", html)
        self.assertIn("x &lt; y", html)
        self.assertNotIn("**", html)

    def test_years_since(self):
        import datetime as dt
        self.assertEqual(br.years_since("2024-04", dt.date(2026, 10, 29)), "2.5+")
        self.assertEqual(br.years_since("2024-04", dt.date(2027, 3, 31)), "2.5+")
        self.assertEqual(br.years_since("2024-04", dt.date(2027, 4, 1)), "3+")

    def test_years_placeholder_rendered(self):
        data = json.loads(json.dumps(DATA))
        data["careerStart"] = "2024-04"
        data["variants"]["au"]["summary"] = "Engineer with {years} years"
        html = br.render_web(data)
        self.assertNotIn("{years}", html)
        self.assertRegex(html, r"Engineer with \d+(\.5)?\+ years")

    def test_variant_only_filters(self):
        data = json.loads(json.dumps(DATA))
        data["projects"].append({"name": "AUONLY", "context": "c", "dates": "d", "bullets": ["x"], "only": ["au"]})
        data["experience"][0]["bullets"].append({"text": "Bullet for india", "only": ["india"]})
        au = br.render_print(data, "au", CONTACT)
        india = br.render_print(data, "india", CONTACT)
        self.assertIn("AUONLY", au)
        self.assertNotIn("AUONLY", india)
        self.assertIn("Bullet for india", india)
        self.assertNotIn("Bullet for india", au)
        self.assertNotIn("{'text'", india)
        self.assertIn("AUONLY", br.render_web(data))

    def test_experience_entry_only(self):
        data = json.loads(json.dumps(DATA))
        data["experience"].append({"company": "Intern Co", "title": "Intern", "location": "Remote",
                                   "dates": "2023", "bullets": ["x"], "only": ["au"]})
        self.assertIn("Intern Co", br.render_print(data, "au", CONTACT))
        self.assertNotIn("Intern Co", br.render_print(data, "india", CONTACT))

    def test_project_header_single_line(self):
        html = br.render_print(DATA, "au", CONTACT)
        self.assertRegex(html, r'<div class="proj-head"><h3>P <span class="ctx">· ctx</span></h3><span class="date">2025</span></div>')
        self.assertNotIn("<span></span>", html)

    def test_apply_names(self):
        html = br.render_print(DATA, "au", CONTACT)
        named = br.apply_names(html, {"ctx": "Acme Corp", "Co A": "Real Co"})
        self.assertIn("Acme Corp", named)
        self.assertIn("Real Co", named)
        self.assertNotIn("· ctx<", named)

    def test_named_map_missing_warns(self):
        with tempfile.TemporaryDirectory() as d:
            buf = io.StringIO()
            with redirect_stdout(buf):
                names = br.load_names(Path(d) / "missing.json")
        self.assertIsNone(names)
        self.assertIn("WARN no client-names map", buf.getvalue())

    def test_public_names_flag(self):
        names = {"ctx": "Acme"}
        self.assertIsNone(br.public_names(DATA, names))
        data = dict(DATA, namesInPublicPdfs=True)
        self.assertEqual(br.public_names(data, names), names)
        self.assertIsNone(br.public_names(data, None))
        self.assertNotIn("Acme", br.render_web(data))

    def test_empty_learning_section_hidden(self):
        data = json.loads(json.dumps(DATA))
        data["learning"] = [{"text": "Cert", "only": ["au"]}]
        self.assertNotIn("Certifications", br.render_print(data, "india", CONTACT))
        self.assertIn("Certifications", br.render_print(data, "au", CONTACT))

    def test_compact_variant(self):
        data = json.loads(json.dumps(DATA))
        data["variants"]["india"]["compact"] = True
        self.assertIn('<body class="compact">', br.render_print(data, "india", CONTACT))
        self.assertNotIn('class="compact"', br.render_print(data, "au", CONTACT))
        self.assertNotIn('class="compact"', br.render_web(data))

    def test_print_is_ats_safe(self):
        html = br.render_print(DATA, "au", CONTACT)
        self.assertIn("github.com/x", html)
        self.assertIn(" | ", html)
        self.assertNotIn("→", html)
        self.assertNotIn("−", html)
        self.assertIn("800 to 1,200", html)
        self.assertIn("<h2>Projects</h2>", html)
        self.assertIn("→", br.render_web(DATA))

    def test_repo_data_is_valid(self):
        data = json.loads((SCRIPT.parent.parent / "data" / "resume.json").read_text())
        html = br.render_web(data)
        self.assertIn(data["name"], html)


if __name__ == "__main__":
    unittest.main()
