"""Quantitative chart examples with geometry calculated from explicit sample data."""
from math import cos, sin, radians
from chart_inputs import normalize, input_contract
import re
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER
from vector import path, rect, circle, line, poly, group, slot, asset

CATEGORY = '10-数値とグラフ'
POSITIVE = '#137D66'
NEGATIVE = '#B5473A'
SERIES_SECONDARY = '#526272'

# Original monoline figures. Coordinates are independent of any installed typeface.
_DIGITS = {
    '0': 'M6 1C1 1 0 5 0 11C0 17 1 21 6 21C11 21 12 17 12 11C12 5 11 1 6 1Z',
    '1': 'M2 5L7 1V21M2 21H12',
    '2': 'M0 5C1 0 10 0 12 5C14 11 2 13 0 21H12',
    '3': 'M0 3C5 0 12 0 12 6C12 10 9 11 5 11M5 11C10 11 13 13 12 18C11 22 4 22 0 19',
    '4': 'M9 21V1L0 15H13',
    '5': 'M12 1H1V10C6 7 12 9 12 15C12 21 6 23 0 19',
    '6': 'M11 2C3 -1 0 6 0 13C0 21 4 22 8 21C14 19 13 10 7 10C3 10 1 12 0 15',
    '7': 'M0 1H13L4 21',
    '8': 'M6 1C-2 1 -2 10 6 11C14 10 14 1 6 1M6 11C-2 11 -2 21 6 21C14 21 14 11 6 11',
    '9': 'M1 20C9 23 12 16 12 9C12 1 8 0 4 1C-2 3 -1 12 5 12C9 12 11 10 12 7',
    '-': 'M0 11H12',
    '+': 'M0 11H12M6 5V17',
    '/': 'M0 22L12 0',
    'E': 'M12 1H0V21H12M0 11H10',
}


def number(value, x, y, size=28, color=INK, align='center', max_width=160, halo=False):
    """Draw a numeric string at its top edge using original vector glyphs."""
    text = str(value)
    suffix = '%' if text.endswith('%') else ''
    numeric = text[:-1] if suffix else text
    if re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?', numeric):
        val = float(numeric)
        for precision in (6,5,4,3):
            formatted = format(val, f'.{precision}g').upper()
            formatted = re.sub(r'E([+-])0+', r'E\1', formatted).replace('E+', 'E')
            if numeric.startswith('+') and val >= 0:
                formatted = '+'+formatted
            text = formatted+suffix
            extent = sum(24 if c=='%' else 8 if c=='.' else 18 for c in text)-5
            if extent*size/22 <= max_width*1.12:
                break
        else:
            raise ValueError('Numeric label exceeds this chart layout; scale the unit or use fewer decimal places')
    advances = [24 if c == '%' else 8 if c == '.' else 18 for c in text]
    width = sum(advances) - 5
    scale = min(size / 22,max_width/max(width,1))
    origin = x - (width * scale / 2 if align == 'center' else width * scale if align == 'right' else 0)
    body = ''; position = 0
    for char, advance in zip(text, advances):
        if char == '%':
            glyph = circle(4,5,3,'none',color,1.8)+circle(16,17,3,'none',color,1.8)+line(2,21,18,1,color,1.8)
        elif char == '.':
            glyph = circle(2,20,1.6,color)
        else:
            glyph = path(_DIGITS[char],stroke=color,sw=1.8)
        body += group(glyph,position,0)
        position += advance
    if halo:
        outline=body.replace(f'stroke="{color}"',f'stroke="{WHITE}"').replace('stroke-width="1.8"','stroke-width="5"').replace(f'fill="{color}"',f'fill="{WHITE}"')
        body=outline+body
    return group(body,origin,y,scale)


def polar(cx, cy, radius, angle):
    angle = radians(angle)
    return cx + radius * cos(angle), cy + radius * sin(angle)


def annular_sector(cx,cy,outer,inner,start,end,fill):
    """Exact angular sector with flat radial ends and no angle-changing stroke caps."""
    if end-start <= 1e-10:return ''
    if end-start > 180:
        middle=(start+end)/2
        return (annular_sector(cx,cy,outer,inner,start,middle,fill)
                +annular_sector(cx,cy,outer,inner,middle,end,fill))
    ox1,oy1=polar(cx,cy,outer,start);ox2,oy2=polar(cx,cy,outer,end)
    ix1,iy1=polar(cx,cy,inner,start);ix2,iy2=polar(cx,cy,inner,end)
    large=int(end-start>180)
    return path(f'M{ox1:.6f} {oy1:.6f}A{outer} {outer} 0 {large} 1 {ox2:.6f} {oy2:.6f}L{ix2:.6f} {iy2:.6f}A{inner} {inner} 0 {large} 0 {ix1:.6f} {iy1:.6f}Z',fill)


def chart(name,title,description,keywords,body,labels,data,guidance,size=(1200,720)):
    a=asset(name,CATEGORY,title,description,keywords,body,labels,size)
    a['kind']='chart';a['data']={'is_sample':True,**data};a['guidance']=guidance
    a['key']='chart/'+data['chart_type'].replace('_','-')
    a['data']['number_format']={'maximum_significant_digits':6,'minimum_significant_digits':3,'large_or_small_values':'E notation','source_values':'series'}
    if not a['data']['is_sample']:
        a['id']=re.sub(r'_[^_]*作例$', '_入力データ',a['id'])
        titles={'horizontal_bar':'項目別の値を横棒で比べる','line':'期間ごとの値の変化を線で追う','grouped_bar':'項目ごとに二つの系列を比べる'}
        a['title']=titles.get(data['chart_type'],title)
        a['description']='入力した'+data['unit']+'の値を、'+a['title']+'ために描画する。'
        lines=[series['label']+'：'+'、'.join(f'{category} {value:g}{data["unit"]}' for category,value in zip(data['categories'],series['values']))+'。' for series in data['series']]
        if data['chart_type'] in ('progress_ring','semicircle_gauge'):
            lines.append(f'強調した範囲は全体の{data["percentage"]:g}%。')
        elif data['chart_type']=='waterfall':
            lines.append('破線は各段階の残高を次の棒へつなぐ。')
        elif data.get('domain'):
            lines.append(f'共通の尺度は0から{data["domain"][1]:g}{data["unit"]}。')
        elif data.get('total'):
            lines.append(f'各部分の合計は{data["total"]:g}{data["unit"]}。')
        a['guidance']={k:v.replace('件数','値') if isinstance(v,str) else v for k,v in guidance.items()}
        a['guidance'].update(reading=lines[:4],avoid=guidance['avoid'].replace('数値は作例。',''))
        if data['chart_type']=='semicircle_gauge':
            a['guidance']['message']='設定した上限に対する現在値の到達割合を示す。'
        if data['chart_type']=='slope':
            a['guidance'].update(use_case='複数の区分について二つの時点の値を比較する。',message='増減の方向と二時点の順位の違いを確認できる。')
        if data['chart_type']=='grouped_bar':
            a['guidance'].update(use_case='複数項目について二つの系列を同じ尺度で比較する。',message='項目間と系列間の差を同じ目盛りで読める。',avoid='各組で系列の左右位置や縦軸の尺度を入れ替えない。')
    for label in a['labels']:
        columns=max(4,int(label['width']/27))
        if len(label['text'])>columns and '\n' not in label['text']:
            label['text']='\n'.join(label['text'][i:i+columns] for i in range(0,len(label['text']),columns))
    if not a['data']['is_sample']:
        minimum=20 if a['width']<=600 else 24
        for label in a['labels']:
            lines=label['text'].split('\n')
            fitted=min(27,label['height']/(len(lines)*1.4),label['width']/max(map(len,lines))*.92)
            if fitted<minimum:
                raise ValueError(f'{data["chart_type"]}: shorten category, series or unit text {label["text"]!r}; this layout requires labels of at least {minimum}px')
    return a


def progress_ring(data=None):
    data=normalize('progress_ring',data)
    total=data['total'];value=data['series'][0]['values'][0]/total*100;remainder=100-value
    b=circle(300,270,159,'none',PALE,42)
    b+=annular_sector(300,270,180,138,-90,-90+360*value/100,BLUE)
    b+=number(f'{value:g}%',300,221,72,max_width=250)
    b+=rect(112,503,21,21,BLUE,3)+rect(334,503,21,21,PALE,3, MID,1.5)
    b+=number(f'{value:g}%',193,546,25)+number(f'{remainder:g}%',416,546,25)
    return chart('進捗共有_全体に対する完了率_75パーセント作例','全体に対する完了率','主色の弧が75%、残りの淡い弧が25%を表す進捗リングの作例。','進捗 達成率 完了率 リング パーセント 割合 円形 progress ring',b,[slot(181,322,238,57,data['categories'][0]),slot(146,487,130,54,data['categories'][0]),slot(369,487,130,54,data['categories'][1])],dict(is_sample=data['is_sample'],unit=data['unit'],categories=data['categories'],series=data['series'],chart_type='progress_ring',total=total,percentage=value,start_angle_degrees=-90,outer_radius=180,inner_radius=138),dict(use_case='目標に対する完了率を一つの値で示す。',message='全体のうち完了した範囲と残りを同時に示す。',reading=['主色の弧は完了75%、淡い弧は残り25%。','中央の数値は主色の弧の割合と一致する。'],avoid='数値は作例。割合を変更する場合は弧と数値を同時に更新する。'),size=(600,620))


def horizontal_bars(data=None):
    data=normalize('horizontal_bar',data)
    categories=data['categories'];values=data['series'][0]['values'];maximum=data['domain'][1];ticks=[maximum*i/4 for i in range(5)]
    x0=309;plot_width=734;bar_height=46
    b=''
    for tick in ticks:
        x=x0+plot_width*tick/maximum
        b+=line(x,149,x,558,INK if tick==0 else PALE,3 if tick==0 else 1.5)
        b+=number(tick,x,592,25,GRAY)
    labels=[slot(780,63,355,56,'単位：'+data['unit'])]
    for i,(label,value) in enumerate(zip(categories,values)):
        y=177+i*103
        b+=rect(x0,y,plot_width*value/maximum,bar_height,BLUE)
        b+=number(value,x0+plot_width*value/maximum+26,y+8,30,INK,'left',max_width=117)
        labels.append(slot(67,y-13,211,72,label))
    return chart('項目比較_件数の大小をそろえて比べる_横棒グラフ作例','項目別の件数を横棒で比べる','ゼロを共通の始点にして80・65・45・30件を比較する横棒グラフの作例。','横棒 棒グラフ 比較 ランキング 件数 カテゴリ horizontal bar',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=data['series'],chart_type='horizontal_bar',baseline=0,domain=data['domain'],ticks=ticks,plot=dict(x=x0,y=149,width=plot_width,height=409)),dict(use_case='同じ単位で集計した項目別の件数を比較する。',message='棒が長い項目ほど件数が多い。',reading=['すべての棒は同じゼロ位置から始まる。','棒の終点に実際の作例値を示す。','横軸は0件から100件までの共通目盛り。'],avoid='数値は作例。異なる単位や母数の項目を一つの比較に混ぜない。'))


def line_chart(data=None):
    data=normalize('line',data)
    categories=data['categories'];values=data['series'][0]['values'];maximum=data['domain'][1];ticks=[maximum*i/4 for i in range(5)]
    x0=205;y0=559;width=860;height=420
    b=''
    for tick in ticks:
        y=y0-height*tick/maximum
        b+=line(x0,y,x0+width,y,INK if tick==0 else PALE,3 if tick==0 else 1.5)
        b+=number(tick,165,y-12,24,GRAY,'right')
    points=[(x0+i*width/(len(values)-1),y0-height*v/maximum) for i,v in enumerate(values)]
    b+=path('M'+'L'.join(f'{x:.4f} {y:.4f}' for x,y in points),stroke=BLUE,sw=6)
    labels=[slot(65,24,350,57,'単位：'+data['unit'])]
    for i,((x,y),label,value) in enumerate(zip(points,categories,values)):
        value_x=x+35 if i==0 else x
        value_y=y-54 if i==0 else y-46
        b+=circle(x,y,8,WHITE,BLUE,4)+number(value,value_x,value_y,29,halo=True)
        labels.append(slot(x-85,588,170,64,label))
    return chart('推移確認_期間ごとの増減を見る_折れ線グラフ作例','期間ごとの増減を線で追う','等間隔の五つの期間を直線で結び、20・35・30・55・75件の推移を示す作例。','折れ線 推移 時系列 変化 件数 トレンド line time series',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=data['series'],chart_type='line',baseline=0,domain=data['domain'],ticks=ticks,interpolation='linear',plot=dict(x=x0,y=y0-height,width=width,height=height)),dict(use_case='同じ間隔で集計した期間別の件数の変化を示す。',message='各期間の増減と全体の推移を確認できる。',reading=['点は各期間の作例値、線は隣り合う点の接続。','第3期では前期より減り、その後は増加する。','縦軸は0件から100件までの共通目盛り。'],avoid='数値は作例。点の間の線を実測値とみなさず、不規則な期間間隔にはそのまま使わない。'))


def semicircle_gauge(data=None):
    data=normalize('semicircle_gauge',data)
    raw=data['series'][0]['values'][0];maximum=data['domain'][1];value=raw/maximum*100;cx=300;cy=385;outer=211;inner=165
    b=annular_sector(cx,cy,outer,inner,180,360,PALE)
    b+=annular_sector(cx,cy,outer,inner,180,180+180*value/100,BLUE)
    for tick in [0,25,50,75,100]:
        a=180+180*tick/100
        p=polar(cx,cy,221,a);q=polar(cx,cy,231,a)
        b+=line(*p,*q,INK,2.5)
    angle=180+180*value/100
    tip=polar(cx,cy,148,angle);left=polar(cx,cy,7,angle+90);right=polar(cx,cy,7,angle-90)
    b+=poly(f'{tip[0]},{tip[1]} {left[0]},{left[1]} {right[0]},{right[1]}',INK)+circle(cx,cy,13,INK)
    b+=number(0,79,407,24,GRAY)+number(maximum/2,300,117,24,GRAY,max_width=120)+number(maximum,521,407,24,GRAY,max_width=115)
    b+=number(f'{value:g}%',300,450,63,max_width=250)
    return chart('指標確認_上限に対する到達度_65パーセントゲージ作例','上限に対する到達度を示す','0から100の半円を等間隔の目盛りに分け、65%を示すゲージの作例。','ゲージ 到達度 達成率 指標 メーター 半円 gauge',b,[slot(83,40,434,63,'上限に対する到達度' if data['is_sample'] else data['categories'][0]),slot(75,533,450,54,'表示値は作例' if data['is_sample'] else f'{raw:g} / {maximum:g} {data["unit"]}')],dict(is_sample=data['is_sample'],unit=data['unit'],categories=data['categories'],series=data['series'],chart_type='semicircle_gauge',baseline=0,domain=data['domain'],ticks=[maximum*i/4 for i in range(5)],percentage=value,start_angle_degrees=180,sweep_angle_degrees=180,needle_angle_degrees=angle),dict(use_case='上限が明確な指標について現在の到達度を示す。',message='0から100の範囲で現在値がどこにあるかを示す。',reading=['左端は0、上端は50、右端は100。','主色の弧と針の位置はどちらも65%に対応する。'],avoid='数値は作例。主色は良否を表さず、上限を超える指標には使わない。'),size=(600,620))


def pictogram(data=None):
    data=normalize('pictogram',data)
    total=10;selected=int(data['series'][0]['values'][0])
    b=number(f'{selected*100//total}%',600,91,74,max_width=300)
    for i in range(total):
        x=128+i*99;y=266;fill=BLUE if i<selected else PALE
        outline='none' if i<selected else MID
        person=circle(24,15,14,fill,outline,2)
        person+=path('M14 39H34Q48 39 48 53V78H39V127H28V89H20V127H9V78H0V53Q0 39 14 39Z',fill,outline,2)
        b+=group(person,x,y)
    b+=number(f'{selected}/{total}',600,458,45)
    return chart('人数比較_全体に占める対象の割合_10人中7人作例',f'10人中{selected}人の割合を示す','同じ大きさの人物10体のうち7体を主色で塗り、70%を示すピクトグラムの作例。','ピクトグラム 人数 人物 割合 比率 回答 該当 70パーセント pictogram',b,[slot(309,20,582,62,'全体に占める対象の割合'),slot(324,526,552,68,'10人中7人が該当する作例' if data['is_sample'] else f'{data["categories"][0]}：{selected} / {total}')],dict(is_sample=data['is_sample'],unit=data['unit'],categories=data['categories'],series=data['series'],chart_type='pictogram',total=total,mark_count=total,value_per_mark=1,selected_marks=selected,percentage=selected/total*100),dict(use_case='同じ母集団の中で条件に該当する人数の割合を説明する。',message='全体と該当する人数の関係が一目で分かる。',reading=['人物1体が1人に対応し、全部で10人。','主色の7人が該当、淡い3人がその他。','7人を10人で割った割合が70%。'],avoid='数値は作例。実際の人数と異なる場合は1体が表す人数も含めて更新する。'))


def vertical_bars(data=None):
    data=normalize('vertical_bar',data)
    categories=data['categories'];values=data['series'][0]['values'];maximum=data['domain'][1];ticks=[maximum*i/4 for i in range(5)]
    baseline=566;top=146;height=420;centers=[332,556,780,1004]
    b=''
    for tick in ticks:
        y=baseline-height*tick/maximum
        b+=line(205,y,1090,y,INK if tick==0 else PALE,3 if tick==0 else 1.5)
        b+=number(tick,169,y-12,24,GRAY,'right')
    labels=[slot(65,63,350,57,'単位：'+data['unit'])]
    for x,value,label in zip(centers,values,categories):
        bar_height=height*value/maximum;bar_top=baseline-bar_height
        b+=rect(x-52,bar_top,104,bar_height,BLUE)+number(value,x,bar_top-44,30)
        labels.append(slot(x-91,593,182,65,label))
    return chart('項目比較_値の大きさを高さで比べる_縦棒グラフ作例','同じ基準で値の高さを比べる','共通のゼロ位置から30・55・80・65件の大きさを示す縦棒グラフの作例。','縦棒 棒グラフ 件数 比較 カテゴリ column vertical bar',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=data['series'],chart_type='vertical_bar',baseline=0,domain=data['domain'],ticks=ticks,plot=dict(x=205,y=top,width=885,height=height)),dict(use_case='順序を固定した項目について同じ単位の値を比較する。',message='棒が高い項目ほど値が大きい。',reading=['各棒の底は共通の0件。','縦軸は25件間隔、上端は100件。','棒の上に作例値を直接表示する。'],avoid='数値は作例。棒の底を切り詰めず、項目間で同じ単位を使う。'))


def pie_sector(cx,cy,radius,start,end,fill):
    if end-start>180:
        middle=(start+end)/2
        return pie_sector(cx,cy,radius,start,middle,fill)+pie_sector(cx,cy,radius,middle,end,fill)
    p=polar(cx,cy,radius,start);q=polar(cx,cy,radius,end)
    return path(f'M{cx} {cy}L{p[0]:.6f} {p[1]:.6f}A{radius} {radius} 0 {int(end-start>180)} 1 {q[0]:.6f} {q[1]:.6f}Z',fill)


def pie_chart(data=None):
    data=normalize('pie',data)
    values=data['series'][0]['values'];categories=data['categories'];colors=[BLUE,SERIES_SECONDARY,MID];total=sum(values)
    cx=360;cy=352;radius=216;start=-90;b='';labels=[]
    for i,(value,label,color) in enumerate(zip(values,categories,colors)):
        end=start+360*value/sum(values)
        b+=pie_sector(cx,cy,radius,start,end,color)
        tx,ty=polar(cx,cy,135,(start+end)/2)
        percentage=value/total*100
        if percentage>=12:b+=number(f'{percentage:g}%',tx,ty-16,33,INK if color==MID else WHITE,max_width=118)
        y=223+i*111
        b+=rect(729,y+20,24,24,color,3)+number(f'{percentage:g}%',1062,y+11,34,max_width=139)
        labels.append(slot(784,y,189,67,label,align='left'))
        start=end
    for angle in [-90]+[-90+360*sum(values[:i])/total for i in range(1,len(values))]:
        edge=polar(cx,cy,radius,angle);b+=line(cx,cy,*edge,WHITE,1.8)
    labels.append(slot(723,110,389,66,'全体に占める構成比'))
    return chart('構成比確認_全体を三つの区分に分ける_円グラフ作例','三つの区分で全体を表す','50%・30%・20%の角度を正確に割り当て、合計100%を示す円グラフの作例。','円グラフ 構成比 内訳 全体 部分 割合 pie chart',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=data['series'],chart_type='pie',total=total,percentages=[v/total*100 for v in values],start_angle_degrees=-90,sector_angles_degrees=[360*v/sum(values) for v in values]),dict(use_case='重複しない三つの区分が全体をどう分けるかを説明する。',message='各区分の合計が一つの全体になる。',reading=['区分Aは50%、区分Bは30%、区分Cは20%。','扇形の角度と面積は各割合に比例する。','三つの割合を足すと100%。'],avoid='数値は作例。重複する区分や合計が全体と一致しない値には使わない。'))


def donut_chart(data=None):
    data=normalize('donut',data)
    values=data['series'][0]['values'];categories=data['categories'];colors=[BLUE,SERIES_SECONDARY,MID];total=sum(values)
    cx=360;cy=352;outer=214;inner=124;start=-90;b='';labels=[]
    for i,(value,label,color) in enumerate(zip(values,categories,colors)):
        percentage=value/total*100;end=start+360*value/total
        b+=annular_sector(cx,cy,outer,inner,start,end,color)
        tx,ty=polar(cx,cy,169,(start+end)/2)
        if percentage>=12:b+=number(f'{percentage:g}%',tx,ty-13,27,INK if color==MID else WHITE,max_width=105)
        y=226+i*111
        b+=rect(729,y+20,24,24,color,3)+number(value,1062,y+11,34)
        labels.append(slot(784,y,189,67,label,align='left'))
        start=end
    for angle in [-90]+[-90+360*sum(values[:i])/total for i in range(1,len(values))]:
        p=polar(cx,cy,inner,angle);q=polar(cx,cy,outer,angle);b+=line(*p,*q,WHITE,1.8)
    b+=number(total,cx,304,60,max_width=200)
    labels.extend([slot(255,384,210,57,'合計（'+data['unit']+'）'),slot(710,113,419,66,'内訳（'+data['unit']+'）')])
    return chart('内訳確認_合計と構成比を同時に示す_ドーナツグラフ作例','合計と内訳を同時に示す','合計200件を80・70・50件に分け、外周に40%・35%・25%を示す作例。','ドーナツ 合計 内訳 構成比 割合 件数 donut chart',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=data['series'],chart_type='donut',total=total,percentages=[v/total*100 for v in values],start_angle_degrees=-90,outer_radius=outer,inner_radius=inner),dict(use_case='合計件数と、その内訳の割合を一枚で説明する。',message='全体の規模と各区分の構成を同時に確認できる。',reading=['中央は合計200件。','右の内訳は80件・70件・50件。','外周の40%・35%・25%は各件数を200件で割った割合。'],avoid='数値は作例。件数を変更する場合は合計・割合・弧の角度を同時に更新する。'))


def grouped_bars(data=None):
    data=normalize('grouped_bar',data)
    categories=data['categories'];previous=data['series'][0]['values'];current=data['series'][1]['values'];maximum=data['domain'][1];ticks=[maximum*i/4 for i in range(5)]
    baseline=570;height=420;centers=[343,648,953];b=''
    for tick in ticks:
        y=baseline-height*tick/maximum
        b+=line(198,y,1095,y,INK if tick==0 else PALE,3 if tick==0 else 1.5)+number(tick,165,y-12,24,GRAY,'right')
    b+=rect(681,67,22,22,MID,3)+rect(897,67,22,22,BLUE,3)
    labels=[slot(65,49,360,63,'単位：'+data['unit']),slot(722,47,151,61,data['series'][0]['label'],align='left'),slot(938,47,210,61,data['series'][1]['label'],align='left')]
    for i,(x,label) in enumerate(zip(centers,categories)):
        for offset,value,color in [(-84,previous[i],MID),(16,current[i],BLUE)]:
            bar_height=height*value/maximum;left=x+offset;top=baseline-bar_height
            b+=rect(left,top,68,bar_height,color)+number(value,left+34,top-42,28,max_width=91)
        labels.append(slot(x-126,594,252,63,label))
    return chart('期間比較_項目ごとの前期と当期を比べる_集合棒グラフ作例','項目ごとに前期と当期を比べる','各項目の前期と当期を同じゼロ基準で並べる、二系列の集合棒グラフの作例。','集合棒 グループ 棒グラフ 前期 当期 比較 カテゴリ grouped clustered bar',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=data['series'],chart_type='grouped_bar',baseline=0,domain=data['domain'],ticks=ticks,plot=dict(x=198,y=150,width=897,height=height)),dict(use_case='複数項目について前期と当期の件数を比較する。',message='項目ごとの変化と項目間の差を同じ目盛りで読める。',reading=['各組の左が前期、右が当期。','棒の底は共通の0件、上端の数値は各作例値。','淡色と主色は期間の違いを示す。'],avoid='数値は作例。各組で左右の期間や縦軸の尺度を入れ替えない。'))


def stacked_percent(data=None):
    data=normalize('stacked_percent_bar',data)
    categories=data['categories'];rows=[[s['values'][i] for s in data['series']] for i in range(3)];names=[s['label'] for s in data['series']];colors=[BLUE,SERIES_SECONDARY,MID]
    x0=263;width=838;b=''
    for tick in [0,25,50,75,100]:
        x=x0+width*tick/100;b+=line(x,155,x,568,PALE,1.5)+number(f'{tick}%',x,103,23,GRAY)
    labels=[]
    for i,(category,values) in enumerate(zip(categories,rows)):
        y=189+i*150;left=x0
        labels.append(slot(65,y-2,169,74,category))
        for value,color in zip(values,colors):
            segment=width*value/100;b+=rect(left,y,segment,70,color)
            if value>=10:b+=number(f'{value:g}%',left+segment/2,y+23,27,INK if color==MID else WHITE,max_width=max(20,segment-14))
            left+=segment
        for boundary in [x0+width*sum(values[:j])/100 for j in range(1,len(values))]:
            if x0<boundary<x0+width:b+=line(boundary,y,boundary,y+70,WHITE,1.8)
        assert abs(left-(x0+width))<1e-9
    for i,(label,color) in enumerate(zip(names,colors)):
        x=294+i*286;b+=rect(x,638,22,22,color,3);labels.append(slot(x+43,618,179,63,label,align='left'))
    series=[dict(label=label,values=[row[i] for row in rows]) for i,label in enumerate(names)]
    return chart('構成比較_同じ全体にそろえて内訳を比べる_100パーセント積上げ作例','全体を100%にそろえて構成を比べる','各行の合計を100%にそろえ、三つの区分の割合を比較する積上げ棒の作例。','積上げ 100パーセント 構成比 内訳 比較 割合 stacked normalized bar',b,labels,dict(is_sample=data['is_sample'],unit='%',categories=categories,series=series,chart_type='stacked_percent_bar',baseline=0,domain=[0,100],ticks=[0,25,50,75,100],totals=[sum(row) for row in rows],plot=dict(x=x0,y=189,width=width,height=370)),dict(use_case='総量の異なる複数の対象について、内訳の割合を比較する。',message='全体の長さをそろえることで構成の違いを読める。',reading=['どの行も左端が0%、右端が100%。','三つの区分は全行で同じ色と並び順。','各区分の長さは表示した割合と一致する。'],avoid='数値は作例。各対象の総量の大小はこの図から比較できない。'))


def waterfall(data=None):
    data=normalize('waterfall',data)
    categories=data['categories'];values=data['series'][0]['values'];types=['total','change','change','change','total']
    baseline=577;height=420;maximum=data['domain'][1];centers=[270,450,630,810,990];bar_width=100
    b=''
    for tick in [maximum*i/4 for i in range(5)]:
        y=baseline-height*tick/maximum;b+=line(192,y,1090,y,INK if tick==0 else PALE,3 if tick==0 else 1.5)+number(tick,158,y-12,24,GRAY,'right')
    labels=[slot(65,55,350,65,'単位：'+data['unit'])];running=0;totals=[]
    for i,(x,value,kind,label) in enumerate(zip(centers,values,types,categories)):
        before=0 if kind=='total' else running
        after=value if kind=='total' else running+value
        low=min(before,after);high=max(before,after);color=INK if kind=='total' else POSITIVE if value>=0 else NEGATIVE
        top=baseline-height*high/maximum;bar_height=height*(high-low)/maximum
        b+=rect(x-bar_width/2,top,bar_width,bar_height,color)
        display=f'{value:g}' if kind=='total' else f'{value:+g}'
        b+=number(display,x,top-43,28,color)
        labels.append(slot(x-88,602,176,63,label))
        running=after;totals.append(running)
        if i<len(centers)-1:
            y=baseline-height*running/maximum;b+=line(x+bar_width/2,y,centers[i+1]-bar_width/2,y,GRAY,2,'5 6')
    assert abs(totals[-1]-(values[0]+sum(values[1:-1])))<=max(1e-9,abs(totals[-1])*1e-9)
    return chart('増減説明_期初から期末への変化を分解する_ウォーターフォール作例','期初から期末までの増減を分解する','100万円に40万円を加え、25万円を減らし、15万円を加えて130万円になる作例。','ウォーターフォール 滝 増減 差分 要因 分解 ブリッジ 期初 期末 waterfall',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=data['series'],chart_type='waterfall',step_types=types,running_totals=totals,baseline=0,domain=[0,maximum],ticks=[maximum*i/4 for i in range(5)],plot=dict(x=192,y=157,width=898,height=height)),dict(use_case='期初と期末の差を、増加要因と減少要因に分けて説明する。',message='各要因を足し引きすると最終値に一致する。',reading=['左端と右端の棒は期初100万円と期末130万円の合計。','プラスは増加要因、マイナスは減少要因。','破線は各段階の残高を次の棒へつなぐ。','100＋40−25＋15＝130で始点と終点が一致する。'],avoid='数値は作例。増減を変更した場合は積算結果と期末値も更新する。'))


def slope_comparison(data=None):
    data=normalize('slope',data)
    categories=data['categories'];series=data['series'];colors=[BLUE,SERIES_SECONDARY,MID];maximum=data['domain'][1];ticks=[maximum*i/4 for i in range(5)]
    baseline=566;height=420;left=341;right=937;b=''
    for tick in ticks:
        y=baseline-height*tick/maximum;b+=line(209,y,1090,y,INK if tick==0 else FAINT,3 if tick==0 else 1.5)+number(f'{tick:g}'+('%' if data['unit']=='%' else ''),171,y-12,23,GRAY,'right',max_width=120)
    b+=line(left,146,left,566,PALE,2)+line(right,146,right,566,PALE,2)
    labels=[slot(left-105,64,210,61,categories[0]),slot(right-105,64,210,61,categories[1]),slot(40,64,200,61,'単位：'+data['unit'])]
    def spread(values):
        positions=sorted(enumerate(values),key=lambda item:item[1]);placed=[]
        for i,y in positions:placed.append([i,max(151,y,placed[-1][1]+37 if placed else 151)])
        if placed[-1][1]>548:
            placed[-1][1]=548
            for j in range(len(placed)-2,-1,-1):placed[j][1]=min(placed[j][1],placed[j+1][1]-37)
        return dict(placed)
    left_labels=spread([baseline-height*item['values'][0]/maximum for item in series])
    right_labels=spread([baseline-height*item['values'][1]/maximum for item in series])
    for i,(item,color) in enumerate(zip(series,colors)):
        a,c=item['values'];ya=baseline-height*a/maximum;yc=baseline-height*c/maximum
        b+=line(left,ya,right,yc,WHITE,11)+line(left,ya,right,yc,color,5)
        b+=circle(left,ya,7,WHITE,color,4)+circle(right,yc,7,WHITE,color,4)
        ly,ry=left_labels[i],right_labels[i]
        if abs(ly-ya)>2:b+=path(f'M{left-10} {ya}L{left-22} {ly}H{left-34}',stroke=color,sw=1.5)
        if abs(ry-yc)>2:b+=path(f'M{right+10} {yc}L{right+19} {ry}H{right+25}',stroke=color,sw=1.5)
        b+=rect(left-167,ly-17,126,34,WHITE)+rect(right+27,ry-17,139,34,WHITE)
        b+=number(a,left-43,ly-13,27,color,'right',max_width=118)+number(c,right+29,ry-13,27,color,'left',max_width=135)
        x=287+i*286;b+=rect(x,646,22,22,color,3);labels.append(slot(x+41,625,176,64,item['label'],align='left'))
    return chart('前後比較_二つの時点の変化を追う_スロープグラフ作例','二つの時点の変化を追う','三つの区分の前期と当期を同じ百分率の目盛りで結ぶ比較グラフの作例。','スロープ 前後比較 前期 当期 変化 比率 割合 slope comparison',b,labels,dict(is_sample=data['is_sample'],unit=data['unit'],categories=categories,series=series,chart_type='slope',baseline=0,domain=data['domain'],ticks=ticks,interpolation='linear',plot=dict(x=209,y=146,width=881,height=height)),dict(use_case='複数の区分について、前期と当期の比率の変化を比較する。',message='増減の方向と二時点の順位の入れ替わりを確認できる。',reading=['左が前期、右が当期で、両側とも同じ0〜100%の目盛り。','同じ色の二つの点が同じ区分を表す。','線の交差は区分Aと区分Bの順位の入れ替わり。'],avoid='数値は作例。二点の間は実測推移ではなく、両時点の値を結ぶ線。'))


def make_assets():
    return [progress_ring(),semicircle_gauge(),pictogram(),horizontal_bars(),vertical_bars(),line_chart(),pie_chart(),donut_chart(),grouped_bars(),stacked_percent(),waterfall(),slope_comparison()]


_CHARTS = dict(progress_ring=progress_ring, semicircle_gauge=semicircle_gauge, pictogram=pictogram, horizontal_bar=horizontal_bars, vertical_bar=vertical_bars, line=line_chart, pie=pie_chart, donut=donut_chart, grouped_bar=grouped_bars, stacked_percent_bar=stacked_percent, waterfall=waterfall, slope=slope_comparison)

def render_chart(chart_type, data):
    """Render validated supplied data with a fixed, purpose-specific chart layout."""
    if chart_type not in _CHARTS:raise ValueError(f'Unknown chart_type: {chart_type}')
    if data is None:raise ValueError('data must be supplied; call make_assets() for sample artwork')
    return _CHARTS[chart_type](data)
