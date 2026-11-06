from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'data.json').read_text())
sources = json.loads((ROOT / 'sources.json').read_text())
items = []
for s in sources:
    name = escape(s['label'])
    if s['url']:
        name = '<a href="' + escape(s['url'], quote=True) + '">' + name + '</a>'
    extra = '；'.join('<a href="' + escape(url, quote=True) + '">' + escape(label) + '</a>' for label, url in s['links'])
    items.append(f'<li id="s{s["number"]}">{name}。{escape(s["note"])}' + (f' {extra}。' if extra else '') + '</li>')
text = (ROOT / 'template.html').read_text()
text = text.replace('__FONTS__', (ROOT / 'fonts.css').read_text())
text = text.replace('__DATA__', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
text = text.replace('__SOURCES__', '\n'.join(items))
assert '__DATA__' not in text and '__SOURCES__' not in text and '__FONTS__' not in text
(ROOT / 'index.html').write_text(text)
print(f'Built index.html: {len(text.encode())} bytes')
