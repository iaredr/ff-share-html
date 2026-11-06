from pathlib import Path
import json,re
P=Path(__file__).parent
sample=Path('/workspace/scratch/86ce8fa7a9d3/upload/gold-45-years.html').read_text()
fonts='\n'.join(re.findall(r'@font-face\{[^\n]+',sample))
data=(P/'data.json').read_text()
html=(P/'template.html').read_text().replace('__FONTS__',fonts).replace('__DATA__',data)
(P/'index.html').write_text(html)
print('HTML bytes:',len(html.encode()))
