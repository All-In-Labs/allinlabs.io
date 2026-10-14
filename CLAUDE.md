# allinlabs.io

The All In Labs website: a static homepage, `index.html`, plus a notes page, served from the repo root (GitHub Pages, `CNAME`). There's no local build step, framework, external CSS or fonts; keep it that way. GitHub Pages does run Jekyll on push, and only `notes.html`, `feed.xml` and `sitemap.xml` use it. Everything else is copied through untouched.

## The page

- The design is artboard "E · One page, minimal copy" on the canvas https://claude.ai/artifact/WQG5XtReYNjyZgxPE4AzFc, in the spirit of danluu.com: Times on white, default browser link colours, text running the full window width (no max-width, as on danluu.com), short lists. Resist adding colour, webfonts, cards or a nav; new content goes in as another line or another short section.
- All styles are in the `<style>` block in the head. The only script animates the range figure (see below); the page must read fine without it.
- Preview the homepage with `python3 -m http.server` from the repo root.

## Notes

- `notes.html` (served at `/notes/`) lists every file in `_notes/` on one page, newest first. To add a note, create `_notes/YYYY-MM-DD.md` and write Markdown. The date heading and the `#YYYY-MM-DD` anchor come from the filename. Front matter (`---` lines) is optional: notes with it are Jekyll documents, notes without it are read in with `include_relative`, and both are listed.
- `_config.yml` declares the `notes` collection (`output: false`, so there are no per-note pages) and excludes repo-only files (`CLAUDE.md`, `README.md`, `vision.md`, `brand_assets/`) from the public site. Setting `exclude` replaces Jekyll's defaults, so keep the Ruby entries in it.
- `feed.xml` (served at `/feed.xml`) is an Atom feed of the same notes, one entry per note with the full text, linking to `/notes/#YYYY-MM-DD`. It repeats `notes.html`'s listing logic (the `jekyll-feed` plugin would miss notes, since collection documents get no date from their filename), so change the two together. Both pages and the homepage advertise it with `<link rel="alternate">`.
- `sitemap.xml` lists the two pages and dates `/notes/` by its newest note, found with the same listing logic again. The homepage has no `lastmod` because nothing records when it changed. `robots.txt` allows every crawler, AI ones included, and points at the sitemap. Both pages carry a `rel="canonical"` link.
- `notes.html` duplicates the homepage's styles in its own `<style>` block; keep the two in step.
- `python3 -m http.server` shows `notes.html` as a raw template. To preview it, run GitHub Pages' Jekyll (the `github-pages` gem, Jekyll 3.x). Under Ruby 3.2+ its old Liquid needs a shim defining `Object#tainted?` and `#taint`, loaded with `RUBYOPT=-r<shim>`. Without that, the build fails with "undefined method 'tainted?'". Build with `--safe` to match GitHub.

## The range figure

- The `<pre id="range">` holds the finished grid as plain text: suited hands above the diagonal, offsuit below, `·` for folds. It's the big blind's ICM Nash calling range against a small-blind shove on the bubble: four players left, three paid 50/30/20, everyone on 10 big blinds, no antes. The small blind's equilibrium is to shove any two cards; the big blind calls 66+, A7s+, A9o+, KTs+, KQo, KJo (13.4%). KJo is a coin-flip (+0.00007 of the prize pool) and is included.
- It was computed with `tools/pushfold/` (excluded from the site): `equities.py` builds win/tie tables for all 169×169 hand classes with eval7 (`python equities.py 60000 1500 eq.json`, about 2 minutes), `solve.py icm 10` solves the equilibrium with Malmuth-Harville ICM by fictitious play, and `precise.py` re-checks borderline hands with 20M samples. `solve.py cev 10` reproduces the published heads-up 10bb Nash numbers (58% shove, 37% call) as a sanity check. Run from that folder in a venv with `eval7` and `numpy`.
- The script reads its targets from that text, scrambles every cell with random hands and settles them top-left to bottom-right over about three seconds. With `prefers-reduced-motion` or no JS the text never changes. So to change the range, edit the text in the HTML; keep the layout (rank letter, three spaces, then each cell padded to four characters) or the parsing breaks.
- The grid is 55 characters wide; its font size scales with the viewport so it fits a 320px phone without scrolling.

## Assets

- The favicon is pocket aces (A♥ A♦) as 16×16 pixel art: `favicon.svg` (with a dark-mode style) and `favicon.ico` (16/32). The PNGs (`favicon-96x96`, `apple-touch-icon`, `web-app-manifest-*`) are that same grid scaled by whole numbers with nearest-neighbour on white, padded so the manifest icons also work as maskable. If the icon changes, re-render them the same way.
- `og-image.png` (1200×630) is the pocket-aces grid scaled 22× beside "All In Labs" in Times New Roman Bold, all on white and centred as a group; re-render it the same way if the icon changes. `logo.png` is from the old brand and is unused.
