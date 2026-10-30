---
name: pocket-zine-build
description: Use to draw, lay out, check, print or publish a pocket zine once its story is agreed (see pocket-zine-story). Covers the exact sheet format, drawing style, the render-and-check script, and updating the pocket-zines site.
---

# pocket zine: building, checking, publishing

start only after the 8-page beat sheet is agreed with jerry (pocket-zine-story). keep the agreed text exactly as written.

## where things live

- `sources/<name>.dc.html` holds every sheet's source. **start a new zine by copying an existing source** (`little-packet.dc.html` and `genie-in-the-light-switch.dc.html` are the cleanest) and replacing the content. every format value below is already right in them.
- `pdfs/<name>.pdf` holds the print files, `covers/<name>.png` the site covers, `index.html` is the site.
- the sheets also live as artboards on Design canvases, where jerry looks at and edits them. **one canvas per collection**, named for the collection, with its zines as artboards in shelf order (`Main.dc.html` is no. 1):
  - once upon a model: https://claude.ai/artifact/NrxC9fSXmhNd5rXfEKwGo7
  - true-ish tales of the internet: https://claude.ai/artifact/REBbM8d3pj7Cwn31jes3aL
  - tales of software gone sideways: https://claude.ai/artifact/3KJ47Vt1eqpFVxa5YvqQuE
  - field guides to the digital wild: https://claude.ai/artifact/9j2KkQhFbUszZCKqLmgnZH

  add a new zine as an artboard on its collection's canvas, so jerry can review it there. a new collection gets a new canvas with the same name as its shelf (add it to this list). `sources/` is the copy of record in git, so keep the two in sync.
  - the old mixed "devcon hopewell mini-zines" canvas (https://claude.ai/artifact/XUkVFWG5BA1689WQi6sr1x) still holds older copies plus two sheets not on any shelf yet (tiny habits, rapunzel). don't add new zines there.
- `.claude/skills/pocket-zine-build/scripts/zine.py` renders and checks a sheet. its fonts are bundled.

## the sheet format

- one sheet: 1056×816 px (11×8.5 in at 96 dpi) as a 4×2 css grid of 264×408 panels. the root style includes `text-wrap: pretty`.
- panel order in the file: the top row is pages **5, 4, 3, 2** from left to right, each with `transform: rotate(180deg)` (it prints upside down on purpose). the bottom row is pages **6, 7, 8 (back), cover**.
- panel padding (top right bottom left). the outer paper edges get 30px so a default print clears the printer margin and the folds land on the paper's own halves. fold-side edges get 24px.
  - top row: `22 30 30 24`, `22 24 30 24`, `22 24 30 24`, `22 24 30 30`
  - bottom row: `22 24 30 30`, `22 24 30 24`, `22 24 30 24`, cover `26 30 30 24`
- no panel borders. the only printed guide is the cut line: a dashed rule at y=407 from x=264 to x=792, with a tiny "cut along the dashes" label. both are driven by the `showGuides` tweak.
- type:
  - headings: `Gochi Hand` 28px, line-height 1, `text-wrap: balance`
  - body: `Patrick Hand` 15px, line-height about 1.22
  - punch lines: Gochi Hand about 20px
  - page numbers: `— N —`, 13px, `#555`, pushed down with `margin: auto 0 0`
  - cover title: Gochi Hand 52 to 56px, in caps
- drawings: `<svg style="flex-shrink: 0; max-width: 100%" width="224" height="~100" role="img" aria-label="…">`, about 224 wide and 80 to 110 tall.
- back-page callout box: 2px solid ink border, 6px radius, filled with `{{accentSoft}}` (the accent at 20%).
- the `data-props` script block declares `accent` (default = the zine's color) and `showGuides`.

## drawing style

- hand-inked look: every drawing's shapes sit inside `<g filter="url(#ink)">`, using the wobble filter defined once per sheet. stroke `#1b1b1b`, width about 3 (finer details 1.5 to 2.4), round caps and joins, white or accent-tint fills.
- one accent color per zine, used as fills at partial opacity (0.25 to 0.6). colors in use:

  | zine | accent |
  |---|---|
  | genie | gold `#f2a93b` |
  | golem | clay `#d98b5f` |
  | mirror | blue `#5aa9e6` |
  | library | purple `#b48ce0` |
  | frankenstein | green `#8fcf6a` |
  | packet | blue `#5aa9e6` |
  | tuesday ghost | tan `#c98c5a` |
  | wild bugs | gold `#f2a93b` |
  | wild errors | coral `#e4572e` |

  pick something distinct for a new zine, but a shared color within a collection is fine.
- **every drawing must read without its caption.** draw whole, recognizable things. a lone cat paw read as a three-eyed face; a whole cat on its back legs pawing the switch read instantly.
- **a recurring character looks the same on every page.** design it once and reuse it (a helper function is fine).
- **don't hide the subject.** the genie floats beside its switch on an angled smoke trail, because rising straight out of it covered the switch.
- keep drawings simple: the page is pocket-sized when printed.
- text inside drawings uses the same fonts, 11 to 17px, `stroke="none"`.

## render and check

```
pip install playwright pillow --break-system-packages   # if missing; chromium must be available
python3 .claude/skills/pocket-zine-build/scripts/zine.py check  sources/<name>.dc.html            # must print PASS
python3 .claude/skills/pocket-zine-build/scripts/zine.py pages  sources/<name>.dc.html pages.png   # all 8 pages upright, in reading order
python3 .claude/skills/pocket-zine-build/scripts/zine.py pdf    sources/<name>.dc.html pdfs/<name>.pdf
python3 .claude/skills/pocket-zine-build/scripts/zine.py cover  sources/<name>.dc.html covers/<name>.png
```

`check` tests three things:
- **fit:** no panel's content overflows its box. fix by trimming words or reducing a drawing's height, never by shrinking body type.
- **widows:** no paragraph or heading ends on a lone word. reword, or keep the last two words together with `<span style="white-space: nowrap">`.
- **folds:** simulates a default "fit to printable area" print on US letter (about 94%, centered) and confirms no ink lands on any fold line. US letter only; A4 is not supported yet.

then **look at `pages.png` yourself**: clipped text, collisions, drawings that don't read, anything off-model. a script pass is not a review.

## review, then publish

1. send jerry the pdf (and `pages.png`) for review. iterate. **publish nothing until he says the review is done.**
2. update the canvas artboard and `sources/`.
3. `pdf` and `cover` into `pdfs/` and `covers/`.
4. rebuild the all-in-one packet in `pdfs/` (every zine's pdf appended, in shelf order). rename the file and the "get all N" button text when the count changes.
5. in `index.html`, add a card to the right shelf, copying its neighbors' markup: cover image, series line (`<collection> · no. N`), title, a one-sentence blurb that sets up the story without spoiling it, and a download button. a new collection gets a new shelf section. update the zine count in the lede and meta description, and add the source to the footer's "after …" credits.
6. serve locally (`python3 -m http.server`) and check that every link and image returns 200 and there's no horizontal scroll at 390px wide.
7. commit and push to `main`. GitHub Pages redeploys on its own. confirm on the live site.
