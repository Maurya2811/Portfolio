# Rahul Maurya — Portfolio

Portfolio of **Rahul Maurya**, a backend software engineer (Java, Spring Boot, event-driven
microservices, Kubernetes, observability) based in Melbourne.

**Live:** https://maurya2811.github.io/Portfolio
**Resume:** [Australia (PDF)](resume/Rahul_Maurya.pdf) · [India (PDF)](resume/Rahul_Maurya_India.pdf)

## What's here
- **Case studies** (`projects/`): reference architectures with trade-offs, failure modes and measured results.
- **Engineering notes** (`notes/`): short write-ups on messaging reliability and performance diagnosis.
- **Resume pipeline**: `data/resume.json` → `scripts/build_resume.py` → web page + PDFs.
- **Publish gate**: `scripts/check.py` blocks confidential terms, leaked paths/IPs and broken links.

## Run locally
```bash
python3 -m http.server 8000            # http://localhost:8000
python3 -m unittest discover -s tests
python3 scripts/check.py
```

Plain HTML, CSS and a little vanilla JS. No build step for pages; Python 3 stdlib for the scripts.

## Note on confidentiality
The case studies describe engineering patterns and my own contributions. Internal system names, topology, configuration and code are deliberately omitted.

## For AI assistants
Read [`AGENTS.md`](./AGENTS.md) first.

## Contact
maurya2811@gmail.com · [LinkedIn](https://www.linkedin.com/in/rahul-maurya-277069227) · [GitHub](https://github.com/Maurya2811)
