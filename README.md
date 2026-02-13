# Shrikrishna Bhat K — Personal Academic Website (Quarto)

This is a [Quarto](https://quarto.org) website for Shrikrishna Bhat K's personal academic profile.

## Prerequisites

1. **Install Quarto** — Download from [https://quarto.org/docs/get-started/](https://quarto.org/docs/get-started/)
2. **Python 3** — Required for the bib-to-markdown pre-render script (`_scripts/generate_pages.py`)
3. (Optional) **R** — If you want bibliography rendering via `citeproc`

## Quick Start

```bash
# Navigate to this folder
cd "quarto website"

# Preview the website locally (with live reload)
quarto preview

# Build the website (output goes to _site/)
quarto render
```

## How Automation Works

The website content for **Publications**, **Software**, **Conferences**, and **Research** pages is **automatically generated** from `reference.bib` — the same file used by the LaTeX CV.

```text
reference.bib  →  _scripts/generate_pages.py  →  _includes/*.md  →  .qmd pages ({{< include >}})
```

- A **pre-render hook** in `_quarto.yml` runs `python _scripts/generate_pages.py` before every build.
- The script parses bib entries by `keywords` (`pub`, `software`, `present`, `poster`, `part`) and generates markdown partials into `_includes/`.
- To add a new entry, simply add a bib entry with the appropriate keyword (and optional `abstract` field) to `reference.bib`, then re-render.

## Project Structure

```text
quarto website/
├── _quarto.yml              # Quarto project configuration (includes pre-render hook)
├── _scripts/
│   └── generate_pages.py    # Bib-to-markdown generator (runs automatically)
├── _includes/               # Auto-generated markdown partials (do not edit)
│   ├── publications_content.md
│   ├── software_content.md
│   ├── conferences_content.md
│   ├── research_counts.md
│   └── pub_conference_list.md
├── CVShrikrishnaBhat/       # LaTeX CV folder (PDF referenced by cv.qmd)
│   └── CVShrikrishnaBhat.pdf
├── styles.css               # Custom CSS (cards, timeline, PDF viewer, colors)
├── reference.bib            # BibTeX bibliography (single source of truth)
├── index.qmd                # Home / About page
├── research.qmd             # Research interests & PhD details
├── publications.qmd         # Publications & preprints (auto-generated content)
├── software.qmd             # R packages (auto-generated content)
├── experience.qmd           # Professional experience
├── conferences.qmd          # Workshops & conferences (auto-generated content)
├── cv.qmd                   # Curriculum Vitae with embedded PDF viewer
├── 404.qmd                  # Custom 404 page
├── pp.png                   # Profile picture
├── .gitignore               # Ignores _site/, _includes/, .quarto/, etc.
├── quarto website.Rproj     # RStudio project file
└── README.md                # This file
```

## Deployment

The rendered `_site/` folder can be deployed to:

- **GitHub Pages** — Push `_site/` to a `gh-pages` branch, or use `quarto publish gh-pages`
- **Netlify** — Point build to `quarto render` with publish directory `_site`
- **Quarto Pub** — `quarto publish quarto-pub`

See [Quarto Publishing Guide](https://quarto.org/docs/publishing/) for details.

## Theme

- Light theme: **Cosmo** / Dark theme: **Darkly**
- Primary color: `#1E3A5F` (navy blue, matching original Mintlify site)
- Custom CSS for cards, timeline, accordions, PDF viewer, and contact table
