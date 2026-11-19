"""Rebuild the one "pocket zines" Design canvas from sources/ and index.html.

usage: python3 build_canvas.py OUT_DIR
writes OUT_DIR/project/<name>.dc.html for every zine on the site (shelf order;
the first is Main.dc.html, the canvas's entry) and OUT_DIR/project/canvas.json:
one row per shelf, titled with the shelf name. publish OUT_DIR/project/* to the
canvas with publish_files (mode patch), and remove any project/*.dc.html the
canvas has that this run didn't write.
"""
import json, re, shutil, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
out = pathlib.Path(sys.argv[1]) / 'project'
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

html = (ROOT / 'index.html').read_text()
shelves = []
for sec in re.findall(r'<section class="shelf".*?</section>', html, re.S):
    title = re.search(r'<h2[^>]*>(.*?)</h2>', sec).group(1)
    zines = []
    for art in re.findall(r'<article class="zine">.*?</article>', sec, re.S):
        name = re.search(r'href="pdfs/([^"]+)\.pdf"', art).group(1)
        series = re.search(r'<p class="series">(.*?)</p>', art).group(1)
        h3 = re.search(r'<h3>(.*?)</h3>', art).group(1)
        zines.append((name, series.split('·')[-1].strip(), h3))
    shelves.append((title, zines))

W, H, GAP, ROW = 1056, 816, 80, 816 + 120 + 300
boards, order, notes = {}, [], {}
first = True
for r, (title, zines) in enumerate(shelves):
    y = r * ROW
    notes[f'shelf{r}'] = {'x': 0, 'y': y - 260, 'text': title, 'kind': 'title1',
                          'maxW': len(zines) * (W + GAP) - GAP}
    for i, (name, no, h3) in enumerate(zines):
        fname = 'Main.dc.html' if first else f'{name}.dc.html'
        first = False
        shutil.copy(ROOT / 'sources' / f'{name}.dc.html', out / fname)
        boards[fname] = {'x': i * (W + GAP), 'y': y, 'w': W, 'h': H,
                         'title': f'{no} · {h3} (print sheet)'}
        order.append(fname)

notes['fold'] = {'x': -460, 'y': 0, 'w': 340, 'fill': 'orange', 'size': 'm', 'text':
    "rebuilt from the pocket-zines repo (sources/) every time a zine ships. edit the sources, "
    "or tell claude about any hand edits here so they get copied back first.\n\n"
    "how to print & fold\n\n1. print on US letter at normal settings.\n"
    "2. fold into 8 rectangles and crease hard. unfold.\n"
    "3. fold in half left-to-right. from the fold, cut along the dashed line (one panel wide).\n"
    "4. unfold, fold in half lengthwise, push the ends together so the slit opens into a plus, "
    "then flatten into a book with the cover on the front."}

canvas = {'v': 3,
          'createdOnFiles': {'v': 1, 'at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
          'title': 'pocket zines', 'launch': {'view': 'canvas'}, 'pages': [],
          'boards': boards, 'order': order, 'notes': notes, 'designSystems': []}
(out / 'canvas.json').write_text(json.dumps(canvas))
print(f'wrote {len(order)} artboards in {len(shelves)} shelves to {out}')
