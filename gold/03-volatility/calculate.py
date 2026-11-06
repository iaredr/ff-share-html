"""Reproduce page figures. stdlib two-pass + independent one-pass check."""
import json, math, statistics
from pathlib import Path
ROOT=Path(__file__).parent
D=json.loads((ROOT/'data.json').read_text())
assert [d['year'] for d in D]==list(range(1972,2026))
def sd2(v):
 n=len(v);return math.sqrt((sum(x*x for x in v)-sum(v)**2/n)/(n-1))
def metrics(rows):
 g=[x['gold_return_pct'] for x in rows];s=[x['sp500_total_return_pct'] for x in rows]
 for v in [g,s]:assert abs(statistics.stdev(v)-sd2(v))<1e-10
 return {'n':len(rows),'gold_sd':statistics.stdev(g),'sp_sd':statistics.stdev(s),'gold_mean':statistics.mean(g),'sp_mean':statistics.mean(s),'gold_negative':sum(x<0 for x in g),'sp_negative':sum(x<0 for x in s),'gold_below_minus20':sum(x<-20 for x in g),'sp_below_minus20':sum(x<-20 for x in s),'correlation':statistics.correlation(g,s),'both_negative':[x['year'] for x in rows if x['gold_return_pct']<0 and x['sp500_total_return_pct']<0]}
M={str(y):metrics([x for x in D if x['year']>=y]) for y in [1972,1980,2000]}
g=[x['gold_return_pct'] for x in D];m=statistics.mean(g)
M['1979_squared_deviation_share']=(126.55-m)**2/sum((x-m)**2 for x in g)
M['gold_loss_years']=[x for x in D if x['gold_return_pct']<-20]
M['eras']=[{'start':a,'end':b,**metrics([x for x in D if a<=x['year']<=b])} for a,b in [(1972,1979),(1980,1989),(1990,1999),(2000,2009),(2010,2019),(2020,2025)]]
M['rolling10']=[{'end':D[i+9]['year'],**metrics(D[i:i+10])} for i in range(len(D)-9)]
M['rebound_gold_1981']=(-(-32.6)/(100-32.6))*100
assert abs(M['rebound_gold_1981']-(100/67.4-1)*100)<1e-10
(ROOT/'calculated.json').write_text(json.dumps(M,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in M.items() if k not in ['rolling10','eras','gold_loss_years']},ensure_ascii=False,indent=2))
