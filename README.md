# Shrikrishna Bhat K — Personal Academic Website (Quarto)

This is a [Quarto](https://quarto.org) website for Shrikrishna Bhat K's personal academic profile, showcasing publications, software, teaching, and research interests.

## Prerequisites

1. **Install Quarto** — Download from [https://quarto.org/docs/get-started/](https://quarto.org/docs/get-started/)
2. **Python 3** — Required for the bib-to-markdown pre-render script (`_scripts/generate_pages.py`)
3. (Optional) **R** — If you want bibliography rendering via `citeproc`

## Quick Start

```bash
# Navigate to the repository root directory
cd kskbhat.github.io

# Preview the website locally (with live reload)
quarto preview

# Build the website (production output goes directly to docs/)
quarto render
```

---

## How Automation Works

The website content for **Publications**, **Software**, **Conferences**, **Experience**, **Education**, and **Research** pages is **automatically generated** from `reference.bib` — the single source of truth used also by the LaTeX CV.

```text
reference.bib  →  _scripts/generate_pages.py  →  _includes/*.md  →  .qmd pages ({{< include >}})
```

- A **pre-render hook** in `_quarto.yml` runs `python _scripts/generate_pages.py` before every build.
- The script parses bib entries by `keywords` and generates markdown partials into `_includes/`.
- **Keywords used:**
  - `pub` — Publications (journal articles, preprints)
  - `software` — R packages
  - `present` — Papers presented at conferences
  - `poster` — Poster presentations
  - `part` — Workshops/conferences attended (participation)
  - `education` — Education history (degrees)
  - `experience` — Professional experience (work history)
- **Author Bolding**: The generation script recursively parses publication authors and automatically bolds all variations of your name (`Shrikrishna Bhat Kapu` and `Shrikrishna Bhat K`).
- To add a new entry, simply add a bib entry with the appropriate keyword to `reference.bib`, then re-render.
- Education/experience entries use `institution`, `description` (with `||` as bullet-point separator), and `date` (`YYYY-MM/YYYY-MM` or `YYYY-MM-DD/YYYY-MM-DD`) fields.

---

## Project Structure

```text
kskbhat.github.io/
├── _quarto.yml              # Quarto project configuration (includes pre-render hook)
├── _scripts/
│   └── generate_pages.py    # Bib-to-markdown generator (runs automatically)
├── _includes/               # Auto-generated markdown partials (do not edit)
│   ├── publications_content.md
│   ├── software_content.md
│   ├── conferences_content.md
│   ├── education_content.md
│   ├── experience_content.md
│   ├── research_counts.md
│   └── pub_conference_list.md
├── CVShrikrishnaBhat/       # LaTeX CV folder (contains CV reference.bib and certificates)
│   ├── CVShrikrishnaBhat.pdf
│   └── reference.bib
├── docs/                    # Rendered production build (deployed on GitHub Pages)
├── styles.css               # Custom global CSS (timeline styles, spacing rules)
├── custom.scss              # Custom light theme rules (Litera overrides)
├── custom-dark.scss         # Custom dark theme rules (Darkly overrides)
├── reference.bib            # BibTeX bibliography (single source of truth for the site)
├── index.qmd                # Home / About page
├── research.qmd             # Research interests & PhD details (awarded March 2026)
├── publications.qmd         # Publications & preprints (auto-generated content)
├── software.qmd             # R packages (auto-generated content)
├── experience.qmd           # Professional experience (auto-generated content)
├── conferences.qmd          # Workshops & conferences (auto-generated content)
├── cv.qmd                   # Curriculum Vitae with embedded PDF viewer
├── teaching.qmd             # Hidden course overview page (with Bookdown & tutorials download)
├── notes.qmd                # Writing - notes page
├── blog.qmd                 # Writing - blog listings page
├── 404.qmd                  # Custom 404 page
├── pp.png                   # Profile picture
├── .gitignore               # Ignores generated cache files and temporary folders
├── kskbhat.github.io.Rproj  # RStudio project file
└── README.md                # This file
```

---

## Deployment

The website is configured to render its production build directly into the **`docs/`** directory. 

* **GitHub Pages Hosting**: The website is served via GitHub Pages pointed to the **`/docs`** directory on the **`master`** branch of the `kskbhat/kskbhat.github.io` repository.
* Pushing updates to GitHub immediately deploys the site live at [https://kskbhat.github.io](https://kskbhat.github.io).

---

## Theme & Styling

- **Light theme**: `litera` + `custom.scss`
- **Dark theme**: `darkly` + `custom-dark.scss`
- Custom SCSS and CSS configuration is applied for responsive layouts, timeline styling (Education & Experience), publications tags, PDF embedding, and mobile layout fixes (avoiding button overlaps on wrapped flex layouts).
