# paghosh.github.io

Source for Pallab Ghosh's academic website, https://paghosh.github.io. Built with Jekyll and served by GitHub Pages (native Jekyll build, no Actions workflow). Every push to `main` rebuilds the site within a couple of minutes; if it does not, check Settings, then Pages, in the repository.

## How to update the site

All content lives in plain text files under `_data/`. You never need to touch HTML.

| To do this | Edit this file |
|---|---|
| Add or change a paper | `_data/publications.yml` |
| Post a news item | `_data/news.yml` (add a block at the top) |
| Add a course or change a description | `_data/teaching.yml` |
| Add a student or a placement | `_data/students.yml` |
| Update talks, awards, service, refereeing | `_data/cv.yml` |
| Update the reading list | `_data/books.yml` |
| Change name, email, phone, profile IDs, citation counts | `_config.yml` |
| Rebuild the CV PDF | run `python3 scripts/build_cv.py` (needs pdflatex and pyyaml); it regenerates `assets/cv/CV_Pallab_Ghosh.pdf` from the data files, then update `cv_pdf_date` in `_config.yml` |
| Replace the headshot | overwrite `assets/img/headshot.jpg` (square, at least 500 by 500 pixels) |
| Rewrite the bio | `index.html`, the three paragraphs inside `<div class="bio">` |

### Adding a published paper

1. Copy the PDF to `assets/papers/<id>.pdf`, where `<id>` is a short slug such as `ghosh2027wages`.
2. Add a block to `_data/publications.yml` following the existing entries. Required fields: `id`, `title`, `authors` (published order), `journal`, `year`, `area` (`labor`, `econometrics`, or `health`), `status: published`. Optional: `volume`, `issue`, `pages`, `doi`, `pdf`, `abstract`, `bibtex`, `featured`, `citations`, `note`.
3. Add a news line in `_data/news.yml`.
4. Commit and push:

```bash
git add -A
git commit -m "Add paper: short title"
git push
```

### Moving a paper from under review to published

Change `status: under_review` to `status: published`, add `journal`, `year`, `doi`, `pdf`, `abstract`, and `bibtex`.

### Status values

`published`, `forthcoming`, `rr` (revise and resubmit), `reject_resubmit`, `under_review`, `working`, `in_progress`. Unpublished papers deliberately carry no journal name, and the site shows only "with coauthor names" for them rather than an author order.

## Local preview (optional)

The site builds on GitHub, so a local build is never required. On a machine with Ruby 3.x:

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000.

## Structure

- `_config.yml` site settings, profile IDs, citation metrics, navigation
- `_layouts/default.html` page frame
- `_includes/` head, navigation, footer, profile icons, and the paper card used on every research list
- `assets/css/main.css` the theme (light and dark)
- `assets/js/main.js` theme toggle, mobile menu, abstract and BibTeX panels, research filters, book filters
- `index.html`, `research.html`, `cv.html`, `teaching.html`, `students.html`, `ma-econometrics.md`, `news.html`, `books.html`, `contact.html`, `404.html`
- `news/feed.xml` and `feed.xml` RSS feed generated from `_data/news.yml`
- `scripts/build_cv.py` regenerates the CV PDF from the data files
- `cv_source/CV_Pallab_Ghosh.tex` the generated LaTeX source of the CV PDF (do not edit by hand)
