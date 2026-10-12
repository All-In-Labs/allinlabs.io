# allinlabs.io

The All In Labs website: a single static page, `index.html`, served from the repo root (GitHub Pages, `CNAME`). No build step, no framework, no external CSS or fonts. Keep it that way.

## The page

- The design is artboard "E · One page, minimal copy" on the canvas https://claude.ai/artifact/WQG5XtReYNjyZgxPE4AzFc, in the spirit of danluu.com: Times on white, default browser link colours, text running the full window width (no max-width, as on danluu.com), short lists. Resist adding colour, webfonts, cards or a nav; new content goes in as another line or another short section.
- All styles are in the `<style>` block in the head. The only script animates the range figure; the page must read fine without it.
- Preview with `python3 -m http.server` from the repo root.

## The range figure

- The `<pre id="range">` holds the finished grid as plain text: a button opening range at 100 big blinds, suited hands above the diagonal, offsuit below, `·` for folds. It was generated from the artboard's rules (`initRange` in `OnePage.dc.html`).
- The script reads its targets from that text, scrambles every cell with random hands and settles them top-left to bottom-right over about three seconds. With `prefers-reduced-motion` or no JS the text never changes. So to change the range, edit the text in the HTML; keep the layout (rank letter, three spaces, then each cell padded to four characters) or the parsing breaks.
- The grid is 55 characters wide; its font size scales with the viewport so it fits a 320px phone without scrolling.

## Assets

- The favicon is pocket aces (A♥ A♦) as 16×16 pixel art: `favicon.svg` (with a dark-mode style) and `favicon.ico` (16/32). The PNGs (`favicon-96x96`, `apple-touch-icon`, `web-app-manifest-*`) are that same grid scaled by whole numbers with nearest-neighbour on white, padded so the manifest icons also work as maskable. If the icon changes, re-render them the same way.
- `assets/logos/` holds the old chip mark and lockups; the page no longer uses them.
- `og-image.png` (1200×630) is the pocket-aces grid scaled 22× beside "All In Labs" in Times New Roman Bold, all on white and centred as a group; re-render it the same way if the icon changes. `logo.png` is from the old brand and is unused.
