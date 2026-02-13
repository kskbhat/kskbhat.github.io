#!/usr/bin/env python3
"""
generate_pages.py — Parse reference.bib and generate markdown content for Quarto website.

Reads the shared reference.bib file (same one used by the LaTeX CV) and generates
markdown partial files that are included in .qmd pages via Quarto's {{< include >}} shortcode.

This mirrors how the LaTeX CV uses \\printbibliography[keyword=...] to filter entries.
Keywords used:
    pub      → Publications (journal articles, preprints)
    software → R packages
    present  → Papers presented at conferences
    poster   → Poster presentations
    part     → Workshops/conferences attended (participation)

Usage:
    python _scripts/generate_pages.py

Runs automatically via Quarto's pre-render hook (see _quarto.yml).
"""

import re
import os
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
BIB_FILE = PROJECT_DIR / "reference.bib"
INCLUDES_DIR = PROJECT_DIR / "_includes"

# Author name to bold in outputs
BOLD_NAME = "Shrikrishna Bhat Kapu"

# ---------------------------------------------------------------------------
# BibTeX Parser (self-contained, no external dependencies)
# ---------------------------------------------------------------------------

def parse_bib(bib_path: Path) -> list[dict]:
    """Parse a .bib file into a list of entry dicts.

    Each dict has special keys ``_type`` (entry type) and ``_key`` (citation key),
    plus all fields found in the entry (lowercased field names).
    """
    with open(bib_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    entries: list[dict] = []

    # Match @type{key,
    for match in re.finditer(r"@(\w+)\{\s*([^,\s]+)\s*,", content):
        entry_type = match.group(1).lower()
        entry_key = match.group(2).strip()

        # Walk forward from just after the comma to find the matching closing brace
        start = match.end()
        depth = 1
        pos = start
        while pos < len(content) and depth > 0:
            ch = content[pos]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            pos += 1

        entry_body = content[start : pos - 1]
        fields = _parse_fields(entry_body)
        fields["_type"] = entry_type
        fields["_key"] = entry_key
        entries.append(fields)

    return entries


def _parse_fields(body: str) -> dict:
    """Extract field = {value} pairs from a bib entry body."""
    fields: dict = {}
    i = 0
    length = len(body)

    while i < length:
        # Skip whitespace, commas, newlines
        while i < length and body[i] in " \t\n\r,":
            i += 1
        if i >= length:
            break

        # Skip comment lines starting with %
        if body[i] == "%":
            while i < length and body[i] != "\n":
                i += 1
            continue

        # Expect: fieldname = ...
        m = re.match(r"(\w+)\s*=\s*", body[i:])
        if not m:
            i += 1
            continue

        field_name = m.group(1).lower()
        i += m.end()
        if i >= length:
            break

        # Parse value (braced, quoted, or bare)
        if body[i] == "{":
            depth = 1
            start = i + 1
            i += 1
            while i < length and depth > 0:
                if body[i] == "{":
                    depth += 1
                elif body[i] == "}":
                    depth -= 1
                i += 1
            value = body[start : i - 1]
        elif body[i] == '"':
            start = i + 1
            i += 1
            while i < length and body[i] != '"':
                i += 1
            value = body[start:i]
            i += 1
        else:
            start = i
            while i < length and body[i] not in ",}\n":
                i += 1
            value = body[start:i].strip()

        fields[field_name] = value.strip()

    return fields


# ---------------------------------------------------------------------------
# LaTeX → plain-text / Markdown helpers
# ---------------------------------------------------------------------------

def clean_latex(text: str) -> str:
    """Convert common LaTeX markup to Markdown / plain text."""
    if not text:
        return text
    # \textbf{...} → **...**
    text = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", text)
    # \textit{...} / \emph{...} → *...*
    text = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"*\1*", text)
    # \textsuperscript{...} → <sup>...</sup>
    text = re.sub(r"\\textsuperscript\{([^}]*)\}", r"<sup>\1</sup>", text)
    # Strip grouping braces {FooBar} → FooBar (not nested)
    text = re.sub(r"\{([^{}]*)\}", r"\1", text)
    # ~ → non-breaking space (just use regular space in markdown)
    text = text.replace("~", " ")
    # -- → en-dash
    text = text.replace("--", "–")
    # Remove stray LaTeX commands we don't handle
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Date formatting
# ---------------------------------------------------------------------------

MONTHS = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


def format_date(date_str: str) -> str:
    """Format an ISO-style bib date to a human-readable string.

    Handles single dates (``2024-02-05``) and ranges (``2024-02-06/2024-02-08``).
    """
    if not date_str:
        return ""

    # Date range
    if "/" in date_str:
        start, end = date_str.split("/")
        sp = start.split("-")
        ep = end.split("-")
        if len(sp) == 3 and len(ep) == 3:
            sm = MONTHS.get(sp[1], sp[1])
            em = MONTHS.get(ep[1], ep[1])
            if sp[1] == ep[1]:  # same month
                return f"{int(sp[2])}–{int(ep[2])} {sm} {sp[0]}"
            return f"{int(sp[2])} {sm} – {int(ep[2])} {em} {sp[0]}"

    parts = date_str.split("-")
    if len(parts) == 3:
        return f"{int(parts[2])} {MONTHS.get(parts[1], parts[1])} {parts[0]}"
    if len(parts) == 2:
        return f"{MONTHS.get(parts[1], parts[1])} {parts[0]}"
    return date_str


def get_year(entry: dict) -> str:
    """Extract the year string from an entry."""
    if "year" in entry:
        return entry["year"]
    if "date" in entry:
        return entry["date"].split("-")[0].split("/")[0]
    return ""


# ---------------------------------------------------------------------------
# Filtering & sorting
# ---------------------------------------------------------------------------

def filter_by_keyword(entries: list[dict], keyword: str) -> list[dict]:
    """Return entries whose ``keywords`` field contains *keyword*."""
    result = []
    for e in entries:
        kw_list = [k.strip() for k in e.get("keywords", "").split(",")]
        if keyword in kw_list:
            result.append(e)
    return result


def sort_by_year_desc(entries: list[dict]) -> list[dict]:
    """Sort entries by year, newest first."""
    return sorted(entries, key=lambda e: get_year(e), reverse=True)


def bold_author(author_str: str) -> str:
    """Bold the target author name in an author string."""
    return author_str.replace(BOLD_NAME, f"**{BOLD_NAME}**")


# Bib 'file' fields are relative to the CVShrikrishnaBhat folder
CV_DIR = PROJECT_DIR / "CVShrikrishnaBhat"


def file_exists(rel_path: str) -> bool:
    """Check whether a file exists relative to the CV directory."""
    if not rel_path:
        return False
    return (CV_DIR / rel_path).is_file()


def resolve_file_path(rel_path: str) -> str:
    """Return the project-relative path for a bib 'file' field value."""
    return f"CVShrikrishnaBhat/{rel_path}"


# ---------------------------------------------------------------------------
# Content generators — Publications
# ---------------------------------------------------------------------------

PUB_PAGES_DIR = PROJECT_DIR / "publications"


def _get_pub_type_label(entry: dict) -> str:
    """Return a human-readable type label for a publication entry."""
    if entry["_type"] == "article":
        return "JOURNAL ARTICLES"
    return "PREPRINTS"


def generate_publications(entries: list[dict]) -> str:
    """Generate markdown for the Publications page.

    Produces compact numbered reference entries (like a CV bibliography)
    where each title links to its own detail page.
    """
    pubs = sort_by_year_desc(filter_by_keyword(entries, "pub"))

    articles = [e for e in pubs if e["_type"] == "article"]
    preprints = [e for e in pubs if e["_type"] != "article"]

    lines: list[str] = []

    if articles:
        lines.append("## Journal Articles\n")
        for i, e in enumerate(articles, 1):
            lines.append(_fmt_publication_bullet(e, i))
        lines.append("")

    if preprints:
        lines.append("## Preprints\n")
        for i, e in enumerate(preprints, 1):
            lines.append(_fmt_publication_bullet(e, i))
        lines.append("")

    return "\n".join(lines)


def generate_publication_pages(entries: list[dict]) -> None:
    """Generate individual .qmd detail pages for each publication.

    Creates ``publications/<bib_key>/index.qmd`` for every entry tagged with
    the ``pub`` keyword.  Each page shows the full bibliographic metadata in
    a card layout (like Rob Hyndman's site), plus abstract and download links.
    Pages are regenerated on every pre-render run, so adding a new bib entry
    with ``keywords = {pub}`` is all that's needed.
    """
    pubs = filter_by_keyword(entries, "pub")
    PUB_PAGES_DIR.mkdir(exist_ok=True)

    for entry in pubs:
        bib_key = entry["_key"]
        page_dir = PUB_PAGES_DIR / bib_key
        page_dir.mkdir(exist_ok=True)

        qmd_content = _build_detail_page(entry)
        (page_dir / "index.qmd").write_text(qmd_content, encoding="utf-8")

    print(f"[generate_pages]   → Generated {len(pubs)} publication detail pages")


def _build_detail_page(entry: dict) -> str:
    """Build the full .qmd content for a single publication detail page."""
    title = clean_latex(entry.get("title", "Untitled"))
    author = clean_latex(entry.get("author", ""))
    year = get_year(entry)
    journal = clean_latex(entry.get("journal", ""))
    volume = entry.get("volume", "")
    number = clean_latex(entry.get("number", ""))
    pages = clean_latex(entry.get("pages", ""))
    doi = entry.get("doi", "")
    note = clean_latex(entry.get("note", ""))
    abstract = clean_latex(entry.get("abstract", ""))
    eprint = entry.get("eprint", "")
    eprinttype = entry.get("eprinttype", "").lower()
    file_path = entry.get("file", "")
    date = entry.get("date", "")
    pub_type = _get_pub_type_label(entry)

    # Format a readable date string
    pub_date = format_date(date) if date else year

    # Publication details string (use HTML since it's inside a raw HTML card)
    pub_details_parts: list[str] = []
    if journal:
        pd = f"<em>{journal}</em>"
        if volume:
            pd += f", <strong>{volume}</strong>"
        if number:
            pd += f"({number})"
        if pages:
            pd += f", {pages}"
        pub_details_parts.append(pd)
    elif note:
        pub_details_parts.append(note)

    pub_details = ". ".join(pub_details_parts) if pub_details_parts else ""

    # Links HTML
    link_badges: list[str] = []
    if doi:
        link_badges.append(
            f'<a href="https://doi.org/{doi}" class="pub-link-badge pub-link-doi" '
            f'target="_blank" rel="noopener">DOI</a>'
        )
    if file_path and file_exists(file_path):
        resolved = resolve_file_path(file_path)
        link_badges.append(
            f'<a href="../../{resolved}" class="pub-link-badge pub-link-pdf" '
            f'target="_blank" rel="noopener">PDF</a>'
        )
    if eprint and eprinttype == "researchsquare":
        link_badges.append(
            f'<a href="https://www.researchsquare.com/article/{eprint}" '
            f'class="pub-link-badge pub-link-preprint" target="_blank" rel="noopener">ResearchSquare</a>'
        )
    if eprint and eprinttype == "arxiv":
        link_badges.append(
            f'<a href="https://arxiv.org/abs/{eprint}" '
            f'class="pub-link-badge pub-link-preprint" target="_blank" rel="noopener">arXiv</a>'
        )

    links_html = "\n".join(link_badges) if link_badges else ""

    # Build the page
    lines: list[str] = []
    # YAML front matter
    lines.append("---")
    # Escape quotes in title for YAML
    safe_title = title.replace('"', '\\"')
    lines.append(f'title: "{safe_title}"')
    lines.append("toc: false")
    lines.append("---")
    lines.append("")

    # Type badge
    lines.append(f'<span class="pub-type-badge">{pub_type}</span>')
    lines.append("")

    # Metadata card (no indentation — Pandoc treats 4-space indent as code block)
    lines.append('<div class="pub-meta-card">')

    # AUTHORS row
    lines.append('<div class="pub-meta-row">')
    lines.append('<div class="pub-meta-label">AUTHORS</div>')
    lines.append(f'<div class="pub-meta-value">{author}</div>')
    lines.append("</div>")

    # PUBLISHED row
    lines.append('<div class="pub-meta-row">')
    lines.append('<div class="pub-meta-label">PUBLISHED</div>')
    lines.append(f'<div class="pub-meta-value">{pub_date}</div>')
    lines.append("</div>")

    # PUBLICATION DETAILS row (if any)
    if pub_details:
        lines.append('<div class="pub-meta-row">')
        lines.append('<div class="pub-meta-label">PUBLICATION DETAILS</div>')
        lines.append(f'<div class="pub-meta-value">{pub_details}</div>')
        lines.append("</div>")

    # LINKS row (if any)
    if links_html:
        lines.append('<div class="pub-meta-row">')
        lines.append('<div class="pub-meta-label">LINKS</div>')
        lines.append(f'<div class="pub-meta-value">{links_html}</div>')
        lines.append("</div>")

    lines.append("</div>")
    lines.append("")

    # Abstract
    if abstract:
        lines.append(f"{abstract}")
        lines.append("")

    return "\n".join(lines)


def _fmt_publication_bullet(entry: dict, index: int) -> str:
    """Format one publication as a compact numbered reference entry.

    The title is a clickable link to the publication's own detail page.
    Mirrors the numbered bibliography style used in the LaTeX CV.
    """
    title = clean_latex(entry.get("title", "Untitled"))
    author = bold_author(clean_latex(entry.get("author", "")))
    year = get_year(entry)
    journal = clean_latex(entry.get("journal", ""))
    volume = entry.get("volume", "")
    number = clean_latex(entry.get("number", ""))
    pages = clean_latex(entry.get("pages", ""))
    doi = entry.get("doi", "")
    note = clean_latex(entry.get("note", ""))
    eprint = entry.get("eprint", "")
    eprinttype = entry.get("eprinttype", "").lower()
    bib_key = entry["_key"]

    # Link to detail page
    detail_url = f"publications/{bib_key}/"

    # --- Build compact citation string ---
    cite_parts: list[str] = []
    cite_parts.append(f"{author} ({year}).")
    cite_parts.append(f'\u201c[{title}]({detail_url}).\u201d')

    if journal:
        jcite = f"*{journal}*"
        if volume:
            jcite += f", {volume}"
        if number:
            jcite += f"({number})"
        if pages:
            jcite += f", {pages}"
        jcite += "."
        cite_parts.append(jcite)
    elif note:
        cite_parts.append(f"*{note}.*")

    # DOI inline
    if doi:
        cite_parts.append(f"DOI: [{doi}](https://doi.org/{doi}).")

    # Eprint link inline
    if eprint and eprinttype == "researchsquare":
        cite_parts.append(
            f"ResearchSquare: [{eprint}](https://www.researchsquare.com/article/{eprint})."
        )

    citation = " ".join(cite_parts)

    # --- Build the numbered entry ---
    lines: list[str] = []
    lines.append(f"{index}. {citation}")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Content generators — Software
# ---------------------------------------------------------------------------

def generate_software(entries: list[dict]) -> str:
    """Generate markdown for the Software page."""
    software = sort_by_year_desc(filter_by_keyword(entries, "software"))
    lines: list[str] = []
    for e in software:
        lines.append(_fmt_software(e))
    return "\n".join(lines)


def _fmt_software(entry: dict) -> str:
    """Format one software entry with cards for links."""
    title = clean_latex(entry.get("title", "Untitled"))
    author = bold_author(clean_latex(entry.get("author", "")))
    note = clean_latex(entry.get("note", ""))
    doi = entry.get("doi", "")
    url = entry.get("url", "")
    eprint = entry.get("eprint", "")
    eprinttype = entry.get("eprinttype", "").lower()
    abstract = clean_latex(entry.get("abstract", ""))

    # Split "PackageName: Subtitle" if applicable
    if ":" in title:
        pkg_name, pkg_desc = title.split(":", 1)
        pkg_name = pkg_name.strip()
        pkg_desc = pkg_desc.strip()
    else:
        pkg_name = title
        pkg_desc = ""

    # Derive GitHub user/repo from pkgdown URL (https://user.github.io/repo)
    github_repo = ""
    if url:
        import re as _re
        m = _re.match(r"https://([^.]+)\.github\.io/([^/]+)", url)
        if m:
            github_repo = f"{m.group(1)}/{m.group(2)}"

    lines: list[str] = []

    # Package header with optional logo
    if github_repo:
        logo_url = f"https://raw.githubusercontent.com/{github_repo}/main/man/figures/logo.png"
        lines.append(f'<div class="pkg-header">')
        lines.append(f'<img src="{logo_url}" alt="{pkg_name} logo" class="pkg-logo" onerror="this.style.display=\'none\'">')
        lines.append(f'<div class="pkg-header-text">')
        lines.append(f'<h2>{pkg_name}</h2>')
        if pkg_desc:
            lines.append(f"\n**{pkg_desc}**\n")
        lines.append(f'</div>')
        lines.append(f'</div>\n')
    else:
        lines.append(f"## {pkg_name}\n")
        if pkg_desc:
            lines.append(f"**{pkg_desc}**\n")

    # CRAN download badges
    if eprinttype == "cran" and eprint:
        lines.append('<div class="pkg-downloads">')
        lines.append(f'<strong>Downloads</strong><br>')
        lines.append(
            f'<a href="https://cran.r-project.org/package={eprint}">'
            f'<img src="https://cranlogs.r-pkg.org/badges/{eprint}" alt="monthly downloads"></a> '
            f'<a href="https://cran.r-project.org/package={eprint}">'
            f'<img src="https://cranlogs.r-pkg.org/badges/grand-total/{eprint}" alt="total downloads"></a>'
        )
        lines.append('</div>\n')

    # Link cards
    cards: list[str] = []
    if eprinttype == "cran" and eprint:
        cards.append(
            f"::: {{.card}}\n\n### [📦 CRAN](https://cran.r-project.org/package={eprint})\n\n"
            f"{note or 'Available on CRAN'}\n\n:::"
        )
    if eprinttype == "github" and eprint:
        cards.append(
            f"::: {{.card}}\n\n### [🐙 GitHub](https://github.com/{eprint})\n\n"
            f"Source code repository\n\n:::"
        )
    if url:
        cards.append(
            f"::: {{.card}}\n\n### [📖 Documentation]({url})\n\n"
            f"Package website & vignettes\n\n:::"
        )

    if cards:
        lines.append("::: {.card-grid-2}\n")
        lines.append("\n\n".join(cards))
        lines.append("\n:::\n")

    if doi:
        lines.append(f"**Authors:** {author}\\")
        lines.append(f"**DOI:** [{doi}](https://doi.org/{doi})\n")
    else:
        lines.append(f"**Authors:** {author}\n")

    # Description / abstract
    if abstract:
        lines.append(f"### Description\n\n{abstract}\n")

    # Installation snippet
    if eprinttype == "cran" and eprint:
        lines.append(f'### Installation\n\n```r\ninstall.packages("{eprint}")\n```\n')
    elif eprinttype == "github" and eprint:
        lines.append(
            f"### Installation\n\n```r\n"
            f"# Install from GitHub\n"
            f'# install.packages("devtools")\n'
            f'devtools::install_github("{eprint}")\n```\n'
        )

    lines.append("---\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Content generators — Conferences
# ---------------------------------------------------------------------------

def generate_conferences(entries: list[dict]) -> str:
    """Generate markdown for the Conferences page."""
    presentations = sort_by_year_desc(filter_by_keyword(entries, "present"))
    posters = sort_by_year_desc(filter_by_keyword(entries, "poster"))
    participated = sort_by_year_desc(filter_by_keyword(entries, "part"))

    lines: list[str] = []

    if presentations:
        lines.append("## Papers Presented\n")
        lines.append("::: {.timeline}\n")
        for e in presentations:
            lines.append(_fmt_conference(e))
        lines.append(":::\n\n---\n")

    if posters:
        lines.append("## Posters Presented\n")
        lines.append("::: {.timeline}\n")
        for e in posters:
            lines.append(_fmt_conference(e))
        lines.append(":::\n\n---\n")

    if participated:
        lines.append("## Workshops & Conferences Attended\n")
        lines.append("::: {.timeline}\n")
        for e in participated:
            lines.append(_fmt_conference(e))
        lines.append(":::\n")

    return "\n".join(lines)


def _fmt_conference(entry: dict) -> str:
    """Format one conference/workshop entry as a timeline item with date/place left, content right."""
    title = clean_latex(entry.get("title", ""))
    booktitle = clean_latex(entry.get("booktitle", ""))
    howpublished = clean_latex(entry.get("howpublished", ""))
    date = format_date(entry.get("date", ""))
    address = clean_latex(entry.get("address", ""))
    note = clean_latex(entry.get("note", ""))
    abstract = clean_latex(entry.get("abstract", ""))
    file_path = entry.get("file", "")

    lines: list[str] = []
    lines.append("::: {.timeline-item}")

    # Left column: date & place
    lines.append("::: {.timeline-left}")
    lines.append(f"[{date}]{{.tl-date}}\\")
    if address:
        lines.append(f"[{address}]{{.tl-place}}")
    lines.append(":::")

    # Center line
    lines.append("::: {.timeline-center}")
    lines.append(":::")

    # Right column: content
    lines.append("::: {.timeline-right}")
    lines.append(f"### {title}")

    # Conference full name
    if booktitle and booktitle != title:
        lines.append(f"*{booktitle}*")
    elif howpublished:
        lines.append(f"*{howpublished}*")

    # Note (e.g. "Virtual paper presentation", "Student Poster Competition")
    if note and note.lower() not in ("participation", "paper presented"):
        lines.append(f"\n*{note}*")

    if abstract:
        lines.append(f"\n{abstract}")

    if file_path and file_exists(file_path):
        resolved = resolve_file_path(file_path)
        lines.append(f"\n[📄 Certificate]({resolved}){{.tl-cert}}")

    lines.append(":::")

    lines.append("\n:::\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Content generators — Research output counts
# ---------------------------------------------------------------------------

def generate_research_counts(entries: list[dict]) -> str:
    """Generate a markdown table of research output counts."""
    pubs = filter_by_keyword(entries, "pub")
    n_articles = sum(1 for e in pubs if e["_type"] == "article")
    n_preprints = sum(1 for e in pubs if e["_type"] != "article")
    n_software = len(filter_by_keyword(entries, "software"))
    n_present = len(filter_by_keyword(entries, "present"))
    n_poster = len(filter_by_keyword(entries, "poster"))

    lines = [
        "| Type | Count |",
        "|---|---|",
        f"| Peer-reviewed journal articles | {n_articles} |",
        f"| Preprints | {n_preprints} |",
        f"| R packages (CRAN / GitHub) | {n_software} |",
        f"| Conference papers presented | {n_present} |",
        f"| Poster presentations | {n_poster} |",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Content generators — Publications list for the publications page sidebar
# ---------------------------------------------------------------------------

def generate_pub_conference_list(entries: list[dict]) -> str:
    """Short numbered list of conference papers for the publications page."""
    presentations = sort_by_year_desc(filter_by_keyword(entries, "present"))
    posters = sort_by_year_desc(filter_by_keyword(entries, "poster"))

    lines: list[str] = []

    if presentations:
        lines.append("## Conference Papers Presented\n")
        for i, e in enumerate(presentations, 1):
            title = clean_latex(e.get("title", ""))
            booktitle = clean_latex(e.get("booktitle", ""))
            address = clean_latex(e.get("address", ""))
            date = format_date(e.get("date", ""))
            note = clean_latex(e.get("note", ""))
            note_str = f" *({note})*" if note and note.lower() != "paper presented" else ""
            lines.append(
                f"{i}. **{title}**\\\n"
                f"   *{booktitle}*, {address}. {date}.{note_str}\n"
            )
        lines.append("")

    if posters:
        lines.append("## Poster Presentations\n")
        for i, e in enumerate(posters, 1):
            title = clean_latex(e.get("title", ""))
            booktitle = clean_latex(e.get("booktitle", ""))
            address = clean_latex(e.get("address", ""))
            date = format_date(e.get("date", ""))
            note = clean_latex(e.get("note", ""))
            note_str = f" *({note})*" if note else ""
            lines.append(
                f"{i}. **{title}**\\\n"
                f"   *{booktitle}*, {address}. {date}.{note_str}\n"
            )
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Entry point — parse bib, generate all content partials."""
    INCLUDES_DIR.mkdir(exist_ok=True)

    entries = parse_bib(BIB_FILE)
    print(f"[generate_pages] Parsed {len(entries)} entries from {BIB_FILE.name}")

    # Disable markdownlint for auto-generated include partials
    ML_DISABLE = "<!-- markdownlint-disable -->\n\n"

    content_map = {
        "publications_content.md": generate_publications(entries),
        "software_content.md": generate_software(entries),
        "conferences_content.md": generate_conferences(entries),
        "research_counts.md": generate_research_counts(entries),
        "pub_conference_list.md": generate_pub_conference_list(entries),
    }

    for filename, content in content_map.items():
        filepath = INCLUDES_DIR / filename
        filepath.write_text(ML_DISABLE + content, encoding="utf-8")
        print(f"[generate_pages]   → {filepath.relative_to(PROJECT_DIR)}")

    # Generate individual publication detail pages
    generate_publication_pages(entries)

    print("[generate_pages] Done!")


if __name__ == "__main__":
    main()
