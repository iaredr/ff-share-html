"""Reproduce jewelry-spread results, no network or third-party dependencies."""
from decimal import Decimal, getcontext
from pathlib import Path
import json
getcontext().prec=30
ROOT=Path(__file__).resolve().parent
raw=json.loads((ROOT/'data.json').read_text())
P=Decimal(str(raw['retail_quote'])); R=Decimal(str(raw['buyback_reference'])); G=Decimal(str(raw['sge_weighted_average']))
def row(weight=10,fee=0,discount=0,change=0,other=0):
    w=Decimal(str(weight)); f=Decimal(str(fee)); d=Decimal(str(discount)); c=Decimal(str(change)); o=Decimal(str(other))
    cost=(P+f-d)*w
    proceeds=R*(1+c/100)*w-o
    gap=cost-proceeds
    loss=gap/cost*100
    recover=(cost+o)/(R*w)*100-100
    return {'weight_g':float(w),'craft_fee_cny_g':float(f),'discount_cny_g':float(d),'buyback_change_pct':float(c),'cost_cny':float(cost),'proceeds_cny':float(proceeds),'gap_cny':float(gap),'loss_pct':float(loss),'break_even_buyback_rise_pct':float(recover)}
baseline=row()
# Independent method: integer cents + retention fraction identity.
buy_cents=int(P*100); sell_cents=int(R*100)
loss_alt=100*(buy_cents-sell_cents)/buy_cents
rise_alt=100*(1/(1-loss_alt/100)-1)
assert abs(loss_alt-baseline['loss_pct'])<1e-12
assert abs(rise_alt-baseline['break_even_buyback_rise_pct'])<1e-12
assert abs((buy_cents-sell_cents)*10/100-baseline['gap_cny'])<1e-12
out={'baseline':baseline,'price_comparison':{'retail':float(P),'sge_weighted_average':float(G),'buyback':float(R),'retail_minus_sge':float(P-G),'sge_minus_buyback':float(G-R),'warning':'Differences are observable quotations, not verified company costs, profit or fees. Intraday times differ.'},'per_100_spent':{'recovered_cny':float(R/P*100),'gap_cny':float((P-R)/P*100)},'weights':[row(weight=x) for x in raw['scenario_inputs']['weights_g']],'fees':[row(fee=x) for x in raw['scenario_inputs']['craft_fees_cny_g']],'discounts':[row(discount=x) for x in raw['scenario_inputs']['retail_discounts_cny_g']],'buyback_changes':[row(change=x) for x in raw['scenario_inputs']['buyback_price_change_pct']],'cross_check':{'integer_cent_loss_pct':loss_alt,'retention_inverse_rise_pct':rise_alt,'passed':True},'scope':'Dated quote arithmetic only; scenarios are explicit assumptions, not offers or forecasts.'}
(ROOT/'calculated.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'baseline':baseline,'cross_check':out['cross_check']},ensure_ascii=False,indent=2))
