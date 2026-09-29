"""Validated data contracts for the twelve authored chart layouts."""
from copy import deepcopy
from math import ceil, floor, isfinite, log10

DEFAULTS = {
    'progress_ring': dict(categories=['完了','残り'], series=[dict(label='割合',values=[75,25])],unit='%',total=100),
    'semicircle_gauge': dict(categories=['表示値'],series=[dict(label='到達度',values=[65])],unit='%',domain=[0,100]),
    'pictogram': dict(categories=['該当','その他'],series=[dict(label='人数',values=[7,3])],unit='人',total=10),
    'horizontal_bar': dict(categories=['項目 A','項目 B','項目 C','項目 D'],series=[dict(label='件数',values=[80,65,45,30])],unit='件',domain=[0,100]),
    'vertical_bar': dict(categories=['項目 A','項目 B','項目 C','項目 D'],series=[dict(label='件数',values=[30,55,80,65])],unit='件',domain=[0,100]),
    'line': dict(categories=['第1期','第2期','第3期','第4期','第5期'],series=[dict(label='件数',values=[20,35,30,55,75])],unit='件',domain=[0,100]),
    'pie': dict(categories=['区分 A','区分 B','区分 C'],series=[dict(label='構成比',values=[50,30,20])],unit='%',total=100),
    'donut': dict(categories=['区分 A','区分 B','区分 C'],series=[dict(label='件数',values=[80,70,50])],unit='件',total=200),
    'grouped_bar': dict(categories=['項目 A','項目 B','項目 C'],series=[dict(label='前期',values=[35,50,40]),dict(label='当期',values=[50,65,55])],unit='件',domain=[0,80]),
    'stacked_percent_bar': dict(categories=['構成 A','構成 B','構成 C'],series=[dict(label='区分 1',values=[50,30,20]),dict(label='区分 2',values=[30,45,35]),dict(label='区分 3',values=[20,25,45])],unit='%'),
    'waterfall': dict(categories=['期初','増加要因','減少要因','追加要因','期末'],series=[dict(label='合計と増減',values=[100,40,-25,15,130])],unit='万円',domain=[0,160]),
    'slope': dict(categories=['前期','当期'],series=[dict(label='区分 A',values=[35,60]),dict(label='区分 B',values=[55,45]),dict(label='区分 C',values=[75,80])],unit='%',domain=[0,100]),
}


def _numeric(value, name):
    if isinstance(value,bool) or not isinstance(value,(int,float)):
        raise ValueError(f'{name} must be a finite number')
    if abs(value)>1e12:
        raise ValueError(f'{name} must be between -1e12 and 1e12; scale the unit first')
    if not isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    return value


def _text(value,name,maximum):
    if not isinstance(value,str) or not value.strip() or len(value)>maximum or any(ord(c)<32 for c in value):
        raise ValueError(f'{name} must be a nonempty string of at most {maximum} characters without control characters')
    return value


def _close(a,b):
    return a==b or abs(a-b)<=max(abs(a),abs(b))*1e-9


def _ceiling(value):
    if value<=0:return 1
    power=10**floor(log10(value))
    if power==0:return value*2
    scaled=value/power
    return next(f for f in (1,2,4,5,8,10) if f>=scaled-1e-12)*power


def normalize(chart_type, supplied=None):
    if chart_type not in DEFAULTS:raise ValueError(f'Unknown chart_type: {chart_type}')
    sample=supplied is None
    raw=deepcopy(DEFAULTS[chart_type] if sample else supplied)
    if not isinstance(raw,dict):raise ValueError('data must be an object')
    allowed={'categories','series','unit','total','domain'}
    if set(raw)-allowed:raise ValueError('Unknown data fields: '+', '.join(sorted(set(raw)-allowed)))
    for name in ('categories','series','unit'):
        if name not in raw:raise ValueError(f'data.{name} is required')
    default=DEFAULTS[chart_type];nc=len(default['categories']);ns=len(default['series'])
    if not isinstance(raw['categories'],list) or len(raw['categories'])!=nc:
        raise ValueError(f'{chart_type} requires exactly {nc} categories')
    raw['categories']=[_text(v,f'categories[{i}]',16) for i,v in enumerate(raw['categories'])]
    if not isinstance(raw['series'],list) or len(raw['series'])!=ns:
        raise ValueError(f'{chart_type} requires exactly {ns} series')
    for i,series in enumerate(raw['series']):
        if not isinstance(series,dict) or set(series)!={'label','values'}:raise ValueError(f'series[{i}] requires label and values')
        _text(series['label'],f'series[{i}].label',12)
        if not isinstance(series['values'],list) or len(series['values'])!=nc:raise ValueError(f'series[{i}] requires exactly {nc} values')
        for j,value in enumerate(series['values']):_numeric(value,f'series[{i}].values[{j}]')
    _text(raw['unit'],'unit',12)
    values=[v for s in raw['series'] for v in s['values']]
    if chart_type!='waterfall' and any(v<0 for v in values):raise ValueError('values must be nonnegative')
    total=raw.get('total')
    if total is not None:
        _numeric(total,'total')
        if total<=0:raise ValueError('total must be positive')
    parts={'progress_ring','pictogram','pie','donut'}
    if chart_type in parts:
        summed=sum(values)
        if summed<=0:raise ValueError('parts must have a positive sum')
        if total is not None and not _close(total,summed):raise ValueError('total must equal the sum of the parts')
        raw['total']=summed
        if raw['unit']=='%' and not _close(summed,100):raise ValueError('percentage parts must sum to 100')
    if chart_type in ('pie','donut') and any(v<=0 for v in values):raise ValueError('pie and donut segments must be positive')
    if chart_type=='pictogram':
        if raw['unit']!='人':raise ValueError('pictogram unit must be 人')
        if not _close(sum(values),10) or any(int(v)!=v for v in values):raise ValueError('pictogram requires integer parts adding to 10')
    if chart_type=='stacked_percent_bar':
        if raw['unit']!='%':raise ValueError('stacked_percent_bar unit must be %')
        if any(not _close(sum(s['values'][i] for s in raw['series']),100) for i in range(nc)):
            raise ValueError('each stacked category must sum to 100')
    high=max(values)
    if chart_type=='waterfall':
        running=[values[0]]
        for v in values[1:-1]:running.append(running[-1]+v)
        if values[0]<0 or values[-1]<0 or min(running)<0:raise ValueError('waterfall totals and running balances must be nonnegative')
        if not _close(running[-1],values[-1]):raise ValueError('waterfall start plus changes must equal the end')
        high=max(running+[values[-1]])
    domain=raw.get('domain')
    if domain is not None:
        if not isinstance(domain,list) or len(domain)!=2:raise ValueError('domain must be [0, upper]')
        for v in domain:_numeric(v,'domain')
        if domain[0]!=0 or domain[1]<=0 or domain[1]<high:raise ValueError('domain must start at 0 and end at or above every plotted value')
    if chart_type=='semicircle_gauge':
        upper=domain[1] if domain else total if total is not None else 100
        if high>upper:raise ValueError('gauge value must not exceed its upper limit')
        if total is not None and domain is not None and not _close(total,upper):raise ValueError('gauge total and domain upper must match')
        raw['domain']=[0,upper]
    elif chart_type in ('horizontal_bar','vertical_bar','line','grouped_bar','waterfall','slope'):
        raw['domain']=domain or [0,100 if raw['unit']=='%' else _ceiling(high)]
        if raw['unit']=='%' and high>100:raise ValueError('percentage values must not exceed 100')
    elif domain is not None:raise ValueError(f'{chart_type} does not accept domain')
    if total is not None and chart_type not in parts|{'semicircle_gauge'}:
        raise ValueError(f'{chart_type} does not accept total')
    raw['is_sample']=sample
    return raw


def input_contract(chart_type):
    if chart_type not in DEFAULTS:raise ValueError(f'Unknown chart_type: {chart_type}')
    a=DEFAULTS[chart_type]
    constraints=['表示値は最大6有効桁。丸める場合も3有効桁以上を保つ。E表記で収まらない値は単位か小数桁を調整。入力値はseriesに保持。','文字は大判24px、小判20px以上で収まる長さ。収まらないカテゴリ名・系列名・単位は短縮して入力。','有限な数値。絶対値は1兆以下。大きな値は単位を変更して入力。','categoriesは16文字以内、series.label・unitは12文字以内。']
    constraints.append('最初と最後は合計、中央の3値は増減。期初＋増減＝期末。残高は0以上。' if chart_type=='waterfall' else '値は0以上。')
    if chart_type in ('progress_ring','pie','donut','pictogram'):constraints.append('totalを指定する場合は各部分の合計と一致。単位が%の場合は合計100。')
    if chart_type in ('pie','donut'):constraints.append('3区分とも0より大きい値。')
    if chart_type=='pictogram':constraints.append('単位は人。2区分は整数で、合計10。')
    if chart_type=='stacked_percent_bar':constraints.append('単位は%。各カテゴリの3系列を足すと100。')
    if chart_type=='semicircle_gauge':constraints.append('上限はdomain[1]またはtotal。省略時は100。値は上限以下。')
    if chart_type in ('horizontal_bar','vertical_bar','line','grouped_bar','waterfall','slope'):constraints.append('domainは[0,上限]。省略時は値から計算。上限は全値・残高以上。')
    return dict(chart_type=chart_type,category_count=len(a['categories']),series_count=len(a['series']),values_per_series=len(a['categories']),required=['categories','series','unit'],constraints=constraints,example=deepcopy(a))
