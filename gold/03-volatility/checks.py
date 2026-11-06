from pathlib import Path
from html.parser import HTMLParser
import re,json,subprocess
P=Path(__file__).parent
s=(P/'index.html').read_text()
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[];self.resources=[];self.charts=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.append(a['id'])
  if t=='a' and a.get('href','').startswith('#'):self.refs.append(a['href'][1:])
  if t in ['script','img','iframe','link','video','audio','source']:
   self.resources.extend(v for k,v in a.items() if k in ['src','href','srcset'])
  if t=='figure' and 'evidence' in a.get('class',''):self.charts.append(a.get('data-chart'))
a=Audit();a.feed(s)
assert len(a.ids)==len(set(a.ids)),'duplicate ids'
assert set(a.refs)<=set(a.ids),'missing anchors'
assert len(a.charts)>=10 and len(a.charts)==len(set(a.charts))
assert not a.resources,a.resources
assert not re.search(r'url\(["\']?https?://',s)
assert not re.search(r'\bfetch\s*\(|XMLHttpRequest|WebSocket\(',s)
assert not any(x in s for x in ['TODO','待核实','稳赚','闭眼买','建议买入'])
main=s.split('<main>')[1].split('</main>')[0];chars=len(re.findall('[\u4e00-\u9fff]',re.sub('<[^>]+>','',main)))
assert chars>=3500,chars
script=re.search(r'<script>(.*?)</script>',s,re.S).group(1)
f=P/'check-syntax.js';f.write_text(script);subprocess.run(['node','--check',str(f)],check=True);f.unlink()
subprocess.run(['python',str(P/'calculate.py')],check=True,capture_output=True)
report={'status':'static_checks_passed','han_main':chars,'evidence_figures':len(a.charts),'source_anchors_resolve':True,'external_resource_tags':0,'external_css_urls':0,'network_api_calls':0,'js_syntax':'pass','data_recalculation':'pass','browser_responsive_and_screenshots':'pending root QA'}
(P/'static-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
