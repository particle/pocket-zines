"""Build the unlisted reading room: a phone-friendly web view of every published zine.

usage:  python3 scripts/build-backroom.py

reads the shelves and cards in index.html (so only zines that are on the public site
show up, in the same order), pulls the 8 pages out of each sheet in sources/, and writes
backroom/index.html (the catalog) and backroom/<name>.html (one reader per zine).

nothing on the public site links here, and every page carries a noindex tag. the repo is
public, though, so this is unlisted, not private. stdlib only; rerun after shipping a zine.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROOM = 'backroom'
OUT = ROOT / ROOM
SITE = 'https://particle.github.io/pocket-zines'
READING_ORDER = [7, 3, 2, 1, 0, 4, 5, 6]  # file order is 5,4,3,2 / 6,7,8,cover
LABELS = ['cover', '2', '3', '4', '5', '6', '7', '8']


def shelves():
    page = (ROOT / 'index.html').read_text()
    out = []
    for sec in re.finditer(r'<section class="shelf"[^>]*>(.*?)</section>', page, re.S):
        s = sec.group(1)
        shelf = {'name': re.search(r'<h2[^>]*>(.*?)</h2>', s, re.S).group(1).strip(),
                 'note': (re.search(r'<p class="shelf-note">(.*?)</p>', s, re.S) or [None, ''])[1].strip(),
                 'zines': []}
        for a in re.finditer(r'<article class="zine">(.*?)</article>', s, re.S):
            a = a.group(1)
            pdf = re.search(r'href="pdfs/([^"]+)\.pdf"', a).group(1)
            shelf['zines'].append({
                'name': pdf,
                'cover': re.search(r'<img class="cover" src="([^"]+)"', a).group(1),
                'alt': re.search(r'alt="([^"]*)"', a).group(1),
                'series': re.search(r'<p class="series">(.*?)</p>', a, re.S).group(1).strip(),
                'title': re.search(r'<h3>(.*?)</h3>', a, re.S).group(1).strip(),
                'blurb': re.search(r'<p class="blurb">(.*?)</p>', a, re.S).group(1).strip(),
            })
        out.append(shelf)
    return out


def pages(name):
    """the sheet's ink filter, plus its 8 panels in reading order, upright, guides off."""
    src = (ROOT / 'sources' / f'{name}.dc.html').read_text()
    body = re.search(r'<x-dc>(.*)</x-dc>', src, re.S).group(1)
    body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S)
    accent = json.loads(re.search(r"data-props='([^']*)'", src).group(1).replace('&amp;', '&'))['accent']['default']
    vals = {'accent': accent, 'accentSoft': accent + '33', 'guide': 'transparent', 'cut': 'transparent', 'cutSoft': 'transparent'}
    body = re.sub(r'\{\{\s*(\w+)\s*\}\}', lambda m: vals.get(m.group(1), '#888'), body)
    defs = re.search(r'<svg aria-hidden="true" width="0" height="0".*?</svg>', body, re.S).group(0)
    # split the sheet's direct child divs by counting div depth
    panels, depth, start = [], 0, None
    for m in re.finditer(r'<(/?)div\b[^>]*>', body):
        if m.group(1):
            depth -= 1
            if depth == 1 and start is not None:
                panels.append(body[start:m.end()])
                start = None
        else:
            if depth == 1:
                start = m.start()
            depth += 1
    panels = panels[:8]
    assert len(panels) == 8, f'{name}: found {len(panels)} panels'
    upright = [re.sub(r'transform:\s*rotate\(180deg\);?\s*', '', p, count=1) for p in panels]
    return accent, defs, [upright[i] for i in READING_ORDER]


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gochi+Hand&family=Patrick+Hand&display=swap">
<style>
:root {{
  --bg: #f3f4f1; --ink: #1b1b1b; --muted: #565a55; --paper: #ffffff; --line: #1b1b1b; --focus: #2f6fb3;
  --display: 'Gochi Hand', 'Comic Neue', cursive; --body: 'Patrick Hand', 'Trebuchet MS', sans-serif;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #1e211f; --ink: #eceee9; --muted: #b3b8b1; --line: #eceee9; --focus: #8fbcf0; color-scheme: dark; }}
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--body); }}
a {{ color: inherit; }}
a:focus-visible, button:focus-visible {{ outline: 3px solid var(--focus); outline-offset: 3px; }}
{css}
</style>
</head>
"""

CATALOG_CSS = """
body { font-size: 19px; line-height: 1.4; padding: 32px max(16px, env(safe-area-inset-right)) 56px max(16px, env(safe-area-inset-left)); }
.wrap { max-width: 1120px; margin: 0 auto; display: flex; flex-direction: column; gap: 48px; }
header { display: flex; flex-direction: column; gap: 10px; max-width: 40rem; }
h1 { margin: 0; font-family: var(--display); font-weight: 400; font-size: clamp(48px, 9vw, 80px); line-height: .95; }
h2 { margin: 0; font-family: var(--display); font-weight: 400; font-size: 36px; line-height: 1; }
header p, .shelf-note { margin: 0; color: var(--muted); }
.shelf { display: flex; flex-direction: column; gap: 18px; }
.rack { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px 24px; }
.zine { display: flex; flex-direction: column; gap: 10px; min-width: 0; text-decoration: none; }
.zine img { display: block; width: 100%; height: auto; aspect-ratio: 262 / 406; background: var(--paper); border: 1.5px solid var(--line); box-shadow: 5px 6px 0 rgba(0,0,0,.12); transition: transform .15s; }
.zine:nth-child(odd) img { transform: rotate(-1.2deg); }
.zine:nth-child(even) img { transform: rotate(1deg); }
.zine:hover img { transform: rotate(0) translateY(-3px); }
.series { margin: 2px 0 0; font-size: 15px; color: var(--muted); }
.zine h3 { margin: 0; font-family: var(--display); font-weight: 400; font-size: 26px; line-height: 1.05; text-wrap: balance; }
.zine p.blurb { margin: 0; font-size: 17px; }
footer { color: var(--muted); font-size: 16px; border-top: 2px dashed var(--muted); padding-top: 16px; }
@media (max-width: 900px) { .rack { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 420px) { .rack { gap: 26px 16px; } .zine h3 { font-size: 22px; } .zine p.blurb { display: none; } }
@media (prefers-reduced-motion: reduce) { .zine img { transition: none; } }
"""

READER_CSS = """
html, body { height: 100%; overflow: hidden; overscroll-behavior: none; }
body { display: flex; flex-direction: column; height: 100dvh; }
.bar { flex: none; display: flex; align-items: center; gap: 12px; padding: max(10px, env(safe-area-inset-top)) max(14px, env(safe-area-inset-right)) 8px max(14px, env(safe-area-inset-left)); font-size: 17px; }
.bar a { text-decoration: none; white-space: nowrap; }
.bar .title { flex: 1; min-width: 0; text-align: center; font-family: var(--display); font-size: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar .pdf { color: var(--muted); }
.track { flex: 1; min-height: 0; display: flex; overflow-x: auto; overflow-y: hidden; scroll-snap-type: x mandatory; scrollbar-width: none; -webkit-tap-highlight-color: transparent; }
.track::-webkit-scrollbar { display: none; }
.slide { flex: 0 0 100%; scroll-snap-align: center; scroll-snap-stop: always; display: flex; align-items: center; justify-content: center; padding: 8px 16px; }
.paper { background: #fff; color: #1b1b1b; box-shadow: 0 1px 0 rgba(0,0,0,.08), 4px 5px 0 rgba(0,0,0,.12); border-radius: 2px; }
.paper > div { zoom: var(--z, 1); }
.end { width: calc(264px * var(--z, 1)); max-width: 100%; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center; }
.end h2 { margin: 0 0 6px; font-family: var(--display); font-weight: 400; font-size: 44px; line-height: 1; }
.end a { display: block; width: 100%; padding: 12px 16px; border: 2.5px solid var(--line); border-radius: 10px 14px 9px 13px; text-decoration: none; font-size: 18px; box-shadow: 3px 3px 0 var(--line); background: var(--bg); }
.end a small { display: block; color: var(--muted); font-size: 14px; }
.nav { flex: none; display: flex; align-items: center; justify-content: center; gap: 18px; padding: 6px 16px max(12px, env(safe-area-inset-bottom)); font-size: 17px; color: var(--muted); }
.nav button { font: inherit; font-size: 26px; line-height: 1; width: 44px; height: 44px; border: 0; border-radius: 50%; background: transparent; color: var(--ink); cursor: pointer; }
.nav button:disabled { opacity: .25; cursor: default; }
.count { min-width: 5.5em; text-align: center; }
@media (prefers-reduced-motion: reduce) { .track { scroll-behavior: auto; } }
"""


def catalog(data):
    shelves_html = []
    for s in data:
        cards = ''.join(f"""
      <a class="zine" href="{z['name']}.html">
        <img src="../{z['cover']}" alt="{z['alt']}" width="262" height="406" loading="lazy">
        <p class="series">{z['series']}</p>
        <h3>{z['title']}</h3>
        <p class="blurb">{z['blurb']}</p>
      </a>""" for z in s['zines'])
        shelves_html.append(f"""
  <section class="shelf">
    <h2>{s['name']}</h2>
    <p class="shelf-note">{s['note']}</p>
    <div class="rack">{cards}
    </div>
  </section>""")
    return HEAD.format(title='pocket zines · the back room', desc='read the pocket zines on your phone.',
                       image=f"{SITE}/{data[0]['zines'][0]['cover']}", css=CATALOG_CSS) + f"""<body>
<div class="wrap">
  <header>
    <h1>the back room</h1>
    <p>every pocket zine, made for reading on a screen. tap a cover to start, then swipe or tap to turn the page.</p>
  </header>
{''.join(shelves_html)}
  <footer>words and doodles by jerry gay · the paper versions are <a href="../">out front</a></footer>
</div>
</body>
</html>
"""


def reader(z, nxt):
    accent, defs, pgs = pages(z['name'])
    slides = ''.join(f"""
  <section class="slide" role="group" aria-roledescription="page" aria-label="{'cover' if i == 0 else f'page {i + 1} of 8'}"><div class="paper">{p}</div></section>"""
                     for i, p in enumerate(pgs))
    next_link = (f'<a href="{nxt["name"]}.html">next zine<small>{nxt["title"]}</small></a>' if nxt else '')
    end = f"""
  <section class="slide" role="group" aria-label="the end"><div class="end">
    <h2>the end.</h2>
    {next_link}
    <a href="./">back to the shelf<small>all the zines</small></a>
    <a href="../pdfs/{z['name']}.pdf" download>print your own<small>one sheet, one cut, a few folds</small></a>
  </div></section>"""
    t = html.unescape(re.sub('<[^>]+>', '', z['title']))
    return HEAD.format(title=f'{t} · pocket zines', desc=html.escape(html.unescape(z['blurb'])),
                       image=f"{SITE}/{z['cover']}", css=READER_CSS + f"\n.nav .count b {{ color: {accent}; }}") + f"""<body>
{defs}
<div class="bar">
  <a href="./" aria-label="back to the shelf">← shelf</a>
  <span class="title">{z['title']}</span>
  <a class="pdf" href="../pdfs/{z['name']}.pdf" download>pdf</a>
</div>
<main class="track" id="track" aria-label="{z['title']}" tabindex="-1">{slides}{end}
</main>
<nav class="nav" aria-label="pages">
  <button id="prev" aria-label="previous page">‹</button>
  <span class="count" id="count" aria-live="polite">cover</span>
  <button id="next" aria-label="next page">›</button>
</nav>
<script>
(() => {{
  const track = document.getElementById('track');
  const slides = [...track.children], last = slides.length - 1;
  const label = i => i === 0 ? 'cover' : i === last ? 'the end' : (i + 1) + ' / 8';
  const prev = document.getElementById('prev'), next = document.getElementById('next'), count = document.getElementById('count');
  let cur = 0;
  function fit() {{
    const w = track.clientWidth - 32, h = track.clientHeight - 16;
    document.documentElement.style.setProperty('--z', Math.min(w / 264, h / 408, 2.4).toFixed(4));
  }}
  function show(i) {{
    cur = i;
    count.textContent = label(i);
    prev.disabled = i === 0; next.disabled = i === last;
    history.replaceState(null, '', i ? '#p' + (i + 1) : location.pathname);
  }}
  function go(i, smooth = true) {{
    i = Math.max(0, Math.min(last, i));
    track.scrollTo({{ left: i * track.clientWidth, behavior: smooth ? 'smooth' : 'instant' }});
    show(i);
  }}
  let t;
  track.addEventListener('scroll', () => {{
    clearTimeout(t);
    t = setTimeout(() => {{ const i = Math.round(track.scrollLeft / track.clientWidth); if (i !== cur) show(i); }}, 60);
  }}, {{ passive: true }});
  track.addEventListener('click', e => {{
    if (e.target.closest('a') || getSelection().toString()) return;
    go(cur + (e.clientX < innerWidth / 3 ? -1 : 1));
  }});
  prev.onclick = () => go(cur - 1);
  next.onclick = () => go(cur + 1);
  addEventListener('keydown', e => {{
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{ e.preventDefault(); go(cur + 1); }}
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{ e.preventDefault(); go(cur - 1); }}
    else if (e.key === 'Home') go(0); else if (e.key === 'End') go(last);
  }});
  addEventListener('resize', () => {{ fit(); go(cur, false); }});
  fit();
  const m = location.hash.match(/^#p(\\d+)$/);
  go(m ? +m[1] - 1 : 0, false);
}})();
</script>
</body>
</html>
"""


def main():
    data = shelves()
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob('*.html'):
        old.unlink()
    (OUT / 'index.html').write_text(catalog(data))
    flat = [z for s in data for z in s['zines']]
    for i, z in enumerate(flat):
        (OUT / f"{z['name']}.html").write_text(reader(z, flat[i + 1] if i + 1 < len(flat) else None))
    print(f'wrote {ROOM}/index.html and {len(flat)} readers')


if __name__ == '__main__':
    main()
