# Business Taxes and M&A — course website

Static HTML version of the course site for *Business Taxes and Mergers & Acquisitions*
(Dr. Matthijs Breugem, Nyenrode Business University), converted from the original
Google Site at `sites.google.com/view/btandma`.

## Structure

| File | Page |
|---|---|
| `index.html` | Intro / landing page |
| `1-corporate-valuation.html` | Financial statements, cost of capital, business valuation (MENSAM & PINGGUO cases) |
| `2-business-taxes.html` | Business taxes in NL; global taxation, avoidance & ethics |
| `simulation.html` | Power Beverage simulation — rules & grading |
| `3-ma.html` | M&A motives, synergies, merger waves, Cournot appendix |
| `solutions.html` | Worked solutions to the taxation exercises |
| `assets/style.css` | Shared stylesheet (light + dark mode) |

No build step is required — the pages are plain HTML and can be edited directly.
(`build.py` and the `fragments/` used to generate them initially are *not* required to
maintain the site; edit the HTML files themselves.)

## Formulas

Formulas are written in LaTeX and rendered with [MathJax 3](https://www.mathjax.org/),
loaded from a CDN in each page's `<head>`. Inline math uses `$...$`, display math uses
`$$...$$` — the same notation as the course's papers and slides.

## Publishing on GitHub Pages

1. Put these files at the root of a repository (or in a `/docs` folder).
2. Repository **Settings → Pages** → Source: *Deploy from a branch* → select the branch
   and root (or `/docs`).
3. The site appears at `https://<user>.github.io/<repo>/`.

Note: a GitHub Pages site is public even if the repository is private.

## Known differences from the Google Site

- **Figures 5.1–5.6** (third-party charts: Our World in Data, Tax Foundation,
  Zucman/Saez) could not be exported automatically — Google serves them behind
  session-bound URLs. Their slots are marked with dashed placeholders linking to the
  original sources. To restore them: open the Google Site in a browser, right-click →
  *Save image as…*, save into `assets/images/` with the filename named in each
  placeholder, then replace the placeholder `<figure class="placeholder">…</figure>`
  block with `<img src="assets/images/<name>.png" alt="…">`.
- **Figures 3.4–3.6 and the WCR diagram** were recreated as inline SVG charts from the
  case data itself (values match the MENSAM tables; discounted curve uses r = 15%).
- Links to Google Docs / Sheets / Forms (cases, practice material, Huntar/Gauta forms)
  still point to the original Google-hosted documents and keep working as long as those
  documents remain shared.
- The search box of Google Sites has no equivalent here (browser Ctrl+F works per page).
