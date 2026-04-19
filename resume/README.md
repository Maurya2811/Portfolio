# Resume

The portfolio's Resume CTA points to `resume/Rahul_Maurya.pdf`.

## To publish your PDF
Drop the final PDF here as **`Rahul_Maurya.pdf`** and commit it:

```bash
cp /path/to/your/resume.pdf "resume/Rahul_Maurya.pdf"
git add resume/Rahul_Maurya.pdf
git commit -m "chore(resume): publish PDF"
git push
```

## Quick generation options

### Option A — Print the HTML resume page (zero tooling)
1. Open `resume/index.html` in Chrome.
2. Ctrl/Cmd + P → **Save as PDF** → `Rahul_Maurya.pdf` → move into `resume/`.

### Option B — Headless Chromium (one command)
```bash
chromium --headless --disable-gpu --no-sandbox \
  --print-to-pdf="resume/Rahul_Maurya.pdf" \
  --print-to-pdf-no-header \
  "file://$(pwd)/resume/index.html"
```

### Option C — wkhtmltopdf
```bash
wkhtmltopdf --enable-local-file-access resume/index.html resume/Rahul_Maurya.pdf
```

Until the PDF exists, the CTA gracefully falls back to viewing `resume/index.html`
via the site nav (and users can Print → Save as PDF themselves).
