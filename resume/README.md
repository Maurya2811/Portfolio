# Resume (generated)

Do not edit files in this folder by hand. They are generated from `data/resume.json`:

```bash
python3 scripts/build_resume.py           # resume/index.html + Rahul_Maurya.pdf (AU) + Rahul_Maurya_India.pdf
python3 scripts/build_resume.py --no-pdf  # web page only
```

Phone numbers and work rights come from `../personal-vault/facts/contact.json` (private) and are
only written into the PDFs, never into the HTML. Without the vault the PDFs are built without a phone line.
