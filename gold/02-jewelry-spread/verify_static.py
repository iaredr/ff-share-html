"""Static checks complement (not replace) viewport/browser verification."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,tempfile
ROOT=Path(__file__).resolve().parent
html=(ROOT/'index.html').read_text()
class Audit(HTMLParser):
 def __init__(self):
  super().__init__();self.in_main=False;self.skip=False;self.text=[];self.ids=[];self.anchors=[];self.resources=[];self.figures=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='main':self.in_main=True
  if t in ('style','script'):self.skip=True
  if a.get('id'):self.ids.append(a['id'])
  if a.get('href','').startswith('#'):self.anchors.append(a['href'][1:])
  if t in ('img','script','link','iframe') and re.match(r'https?://',a.get('src',a.get('href',''))):self.resources.append(a)
  if t=='figure' and 'evidence' in a.get('class',''):self.figures.append(a.get('data-chart'))
 def handle_endtag(self,t):
  if t=='main':self.in_main=False
  if t in ('style','script'):self.skip=False
 def handle_data(self,d):
  if self.in_main and not self.skip:self.text.append(d)
a=Audit();a.feed(html)
assert len(a.figures)>=10,a.figures
assert len(a.ids)==len(set(a.ids)),'duplicate id'
assert set(a.anchors)<=set(a.ids),'broken internal citation'
assert not a.resources,'external dependency'
assert not re.search(r'url\(["\']?https?://',html),'external CSS request'
script=re.search(r'<script>(.*?)</script>',html,re.S).group(1)
assert not re.search(r'\b(fetch|XMLHttpRequest|WebSocket)\s*\(',script),'network function'
assert len(re.findall('[\u4e00-\u9fff]',''.join(a.text)))>=3500
assert all(x in html for x in ['class="question"','class="finding"','class="meta"'])
for f in re.findall(r'<figure class="evidence".*?</figure>',html,re.S):
 assert all(f'class="{x}"' in f for x in ['question','finding','meta'])
 assert re.search(r'href="#s[0-9]+"',f),'missing figure source'
public=json.loads((ROOT/'sources.json').read_text())
assert {f"s{x['id']}" for x in public}==set(re.findall(r'<li id="(s[0-9]+)"',html))
raw=json.loads((ROOT/'data.json').read_text()); calc=json.loads((ROOT/'calculated.json').read_text())
for k,v in [('retail',raw['retail_quote']),('buyback',raw['buyback_reference']),('sge',raw['sge_weighted_average'])]:
 assert re.search(rf'{k}:{v}(?:,|}})',script),f'inline {k} mismatch'
assert calc['cross_check']['passed']
assert round(calc['baseline']['loss_pct'],1)==30.7
assert round(calc['baseline']['break_even_buyback_rise_pct'],1)==44.3
assert calc['baseline']['gap_cny']==3640
assert round(calc['price_comparison']['retail_minus_sge'],2)==340.44
assert round(calc['price_comparison']['sge_minus_buyback'],2)==23.56
with tempfile.NamedTemporaryFile('w',suffix='.js') as f:
 f.write(script);f.flush();subprocess.run(['node','--check',f.name],check=True,capture_output=True)
result={'static_checks':'passed','main_chinese_characters':len(re.findall('[\u4e00-\u9fff]',''.join(a.text))),'evidence_modules':len(a.figures),'citations':len(public),'external_resource_tags':len(a.resources),'js_syntax':'passed','numeric_cross_check':'passed','browser_check':'Requires parent-agent viewport, screenshot, offline and runtime verification; not asserted here.'}
(ROOT/'static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
