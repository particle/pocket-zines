"""Render and check a pocket-zine print sheet (.dc.html, 1056x816, 8 panels).

usage:
  python3 zine.py check  sheet.dc.html            fit + widows + default-print folds, and a preview png
  python3 zine.py pdf    sheet.dc.html out.pdf    print pdf with the cut line visible
  python3 zine.py cover  sheet.dc.html out.png    2x cover image, 524x812, for the website
  python3 zine.py pages  sheet.dc.html out.png    all 8 pages upright in reading order, for looking at

needs: playwright (python) with chromium, pillow. fonts are bundled next to this script.
"""
import json, pathlib, re, sys, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / 'fonts'
PAGE_OF_PANEL = ['5', '4', '3', '2', '6', '7', '8 (back)', 'cover']


def sheet_html(src, guides):
    html = pathlib.Path(src).read_text()
    body = re.search(r'<x-dc>(.*)</x-dc>', html, re.S).group(1)
    body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S)
    props = json.loads(re.search(r"data-props='([^']*)'", html).group(1).replace('&amp;', '&'))
    accent = props['accent']['default']
    vals = {'accent': accent, 'accentSoft': accent + '33',
            'guide': '#c4c4c4' if guides else 'transparent',
            'cut': '#6b6b6b' if guides else 'transparent',
            'cutSoft': '#a8a8a8' if guides else 'transparent'}
    body = re.sub(r'\{\{\s*(\w+)\s*\}\}', lambda m: vals.get(m.group(1), '#888'), body)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: 'Gochi Hand'; src: url('{(FONTS / 'gochi-hand.woff2').as_uri()}'); }}
@font-face {{ font-family: 'Patrick Hand'; src: url('{(FONTS / 'patrick-hand.woff2').as_uri()}'); }}
@page {{ size: 11in 8.5in; margin: 0 }}
body {{ margin: 0 }}
</style></head><body>{body}</body></html>"""


def open_sheet(browser, src, guides=False, scale=1):
    tmp = pathlib.Path(tempfile.mkdtemp()) / 'sheet.html'
    tmp.write_text(sheet_html(src, guides))
    pg = browser.new_page(viewport={'width': 1056, 'height': 816}, device_scale_factor=scale)
    pg.goto(tmp.as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(300)
    return pg


OVERFLOW_JS = """() => [...document.querySelectorAll('body > div > div')].slice(0, 8)
  .map((d, i) => ({i, over: d.scrollHeight - d.clientHeight})).filter(x => x.over > 0)"""

WIDOW_JS = r"""() => {
  const panels = [...document.querySelectorAll('body > div > div')].slice(0, 8);
  panels.forEach(p => p.style.transform = 'none');
  const out = [];
  panels.forEach((panel, pi) => {
    panel.querySelectorAll('p, h1, h2, div').forEach(el => {
      if (el.closest('svg')) return;
      if ([...el.children].some(c => c.tagName === 'DIV' || c.tagName === 'P')) return;
      const groups = [[]];
      const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
      while (w.nextNode()) {
        const n = w.currentNode;
        if (n.nodeType === 1) { if (n.tagName === 'BR') groups.push([]); continue; }
        for (let i = 0; i < n.length; i++) {
          const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 1);
          const b = r.getBoundingClientRect();
          if (!b.width && n.data[i] !== ' ') continue;
          groups[groups.length - 1].push({ch: n.data[i], top: Math.round(b.top / 4)});
        }
      }
      groups.forEach(g => {
        const tops = [...new Set(g.map(c => c.top))];
        if (tops.length < 2) return;
        const last = g.filter(c => c.top === Math.max(...tops)).map(c => c.ch).join('').trim();
        if (last && !last.includes(' ')) out.push({panel: pi, word: last});
      });
    });
  });
  return out;
}"""


def fold_hits(img):
    """Simulate a default 'fit to printable area' print on US letter (0.25in unprintable
    border, centered) and count dark pixels landing on fold lines."""
    ppi = 96
    W, H = round(11 * ppi), round(8.5 * ppi)
    s = min((11 - 0.5) * ppi / img.width, (8.5 - 0.5) * ppi / img.height)
    sw, sh = round(img.width * s), round(img.height * s)
    page = Image.new('L', (W, H), 255)
    page.paste(img.convert('L').resize((sw, sh)), ((W - sw) // 2, (H - sh) // 2))
    dark = lambda x, y: page.getpixel((x, y)) < 140
    hits = 0
    for x in (W // 4, W // 2, 3 * W // 4):
        hits += sum(1 for y in range(H) if abs(y - H // 2) >= 4 and any(dark(x + d, y) for d in (-1, 0, 1)))
    hits += sum(1 for x in range(W) if not (W // 4 <= x <= 3 * W // 4) and any(dark(x, H // 2 + d) for d in (-1, 0, 1)))
    return s, hits


def main():
    cmd, src = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else None
    with sync_playwright() as p:
        b = p.chromium.launch()
        if cmd == 'check':
            pg = open_sheet(b, src)
            over = pg.evaluate(OVERFLOW_JS)
            png = str(pathlib.Path(src).with_suffix('').with_suffix('.preview.png'))
            pg.screenshot(path=png)
            widows = pg.evaluate(WIDOW_JS)
            scale, hits = fold_hits(Image.open(png))
            ok = not over and not widows and hits == 0
            print('fit:    ', 'ok' if not over else ', '.join(f"page {PAGE_OF_PANEL[o['i']]} over by {o['over']}px" for o in over))
            print('widows: ', 'none' if not widows else ', '.join(f"page {PAGE_OF_PANEL[w['panel']]}: '{w['word']}'" for w in widows))
            print('folds:  ', f'ok (default print scales to {scale:.0%})' if hits == 0 else f'{hits} px of ink on fold lines')
            print('preview:', png)
            print('PASS' if ok else 'FIX THE ABOVE')
        elif cmd == 'pdf':
            pg = open_sheet(b, src, guides=True)
            pg.pdf(path=out, width='11in', height='8.5in', print_background=True,
                   margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
            print('wrote', out)
        elif cmd in ('cover', 'pages'):
            pg = open_sheet(b, src, scale=2)
            tmp = pathlib.Path(tempfile.mkdtemp()) / 'full.png'
            pg.screenshot(path=str(tmp))
            im = Image.open(tmp)
            panel = lambda i: (lambda c: c.rotate(180) if i < 4 else c)(
                im.crop(((i % 4) * 528, (i // 4) * 816, (i % 4) * 528 + 528, (i // 4) * 816 + 816)))
            if cmd == 'cover':
                panel(7).crop((2, 2, 526, 814)).save(out, optimize=True)
            else:
                order = [7, 3, 2, 1, 0, 4, 5, 6]  # cover, 2..7, back
                sheet = Image.new('RGB', (4 * 540, 2 * 828), '#dddddd')
                for k, i in enumerate(order):
                    sheet.paste(panel(i), ((k % 4) * 540 + 6, (k // 4) * 828 + 6))
                sheet.save(out)
            print('wrote', out)
        b.close()


if __name__ == '__main__':
    main()
