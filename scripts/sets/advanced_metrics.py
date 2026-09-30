"""Data-driven comparison, uncertainty, concentration, and relationship charts."""
from chart_inputs import normalize
from sets.metrics import chart, number, category_pitch
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY
from vector import path, rect, circle, line, slot


def dot_comparison(supplied=None):
    d=normalize('dot',supplied);values=d['series'][0]['values'];maximum=d['domain'][1]
    x0=300;width=660;rows=len(values);bottom=190+rows*94;canvas=max(720,bottom+125);ticks=[maximum*i/4 for i in range(5)]
    b='';labels=[slot(764,48,361,65,'単位：'+d['unit'])];points=[]
    for tick in ticks:
        x=x0+width*tick/maximum;b+=line(x,150,x,bottom,INK if tick==0 else PALE,3 if tick==0 else 1.5)+number(tick,x,bottom+30,25,GRAY)
    for i,(name,value) in enumerate(zip(d['categories'],values)):
        y=204+i*94;x=x0+width*value/maximum
        b+=line(x0,y,x0+width,y,FAINT,2)+circle(x,y,12,BLUE)+number(value,1121,y-14,28,INK,'right',max_width=106)
        labels.append(slot(51,y-37,220,77,name));points.append(dict(x=x,y=y,value=value))
    return chart('水準比較_項目ごとの位置を同じ尺度で見る_ドットプロット作例','項目別の水準を点の位置で比較する','共通の尺度に各項目の値を点で置き、位置と数値で比較する作例。','ドットプロット 点 比較 水準 順位 dot plot comparison level',b,labels,dict(**d,chart_type='dot',baseline=0,ticks=ticks,points=points,plot=dict(x=x0,y=150,width=width,height=bottom-150)),dict(use_case='複数の項目について、同じ単位の水準を余白を保って比較する。',message='棒の面積を使わず、共通の尺度上の位置で差を読める。',reading=['同じ高さの項目名・点・右端の数値が一組。','横位置だけが値を表し、点の大きさはすべて同じ。','数値は作例で、0から100の尺度に対応する。']),size=(1200,canvas))


def actual_target(supplied=None):
    d=normalize('actual_target',supplied);actual,target=[a['values'] for a in d['series']];maximum=d['domain'][1]
    x0=295;width=668;bottom=225+len(actual)*124;canvas=max(720,bottom+123);ticks=[maximum*i/4 for i in range(5)]
    b='';labels=[slot(66,38,327,61,'単位：'+d['unit']),slot(841,31,294,60,'棒：'+d['series'][0]['label']),slot(841,91,294,60,'線：'+d['series'][1]['label'])];marks=[]
    for t in ticks:
        x=x0+width*t/maximum;b+=line(x,188,x,bottom,INK if t==0 else PALE,3 if t==0 else 1.5)+number(t,x,bottom+26,24,GRAY)
    for i,(a,t,name) in enumerate(zip(actual,target,d['categories'])):
        y=246+i*124;ax=x0+width*a/maximum;tx=x0+width*t/maximum
        b+=rect(x0,y-22,ax-x0,44,BLUE)+line(tx,y-39,tx,y+39,INK,5)
        b+=number(a,1087,y-32,29,BLUE,max_width=137)+number(t,1087,y+12,26,INK,max_width=137)
        labels.append(slot(60,y-39,207,80,name));marks.append(dict(actual_x=ax,target_x=tx,y=y))
    return chart('目標対比_実績の棒と目標線を重ねる_実績目標グラフ作例','実績と目標の位置を同じ尺度で比べる','実績を横棒、目標を細い縦線として重ね、達成と差を確認する作例。','実績 目標 達成 ギャップ バレット actual target bullet comparison goal',b,labels,dict(**d,chart_type='actual_target',baseline=0,ticks=ticks,marks=marks,plot=dict(x=x0,y=188,width=width,height=bottom-188)),dict(use_case='項目ごとの実績と目標を同じ単位で比較し、届いた範囲を共有する。',message='実績が目標を超えたか、どの程度届いていないかを同じ尺度で読める。',reading=['主色の棒が実績、濃い縦線が目標。','右端の上の値が実績、下の値が目標。','目標の線を棒が越える項目も、そのまま比較できる。']),size=(1200,canvas))


def range_comparison(supplied=None):
    d=normalize('range',supplied);lower,middle,upper=[s['values'] for s in d['series']];maximum=d['domain'][1]
    x0=292;width=491;bottom=205+len(lower)*118;canvas=max(720,bottom+140);ticks=[maximum*i/4 for i in range(5)]
    b='';labels=[slot(64,38,345,62,'単位：'+d['unit'])];marks=[]
    for x,s in zip((865,973,1081),d['series']):labels.append(slot(x,110,96,71,s['label']))
    for t in ticks:
        x=x0+width*t/maximum;b+=line(x,184,x,bottom,INK if t==0 else PALE,3 if t==0 else 1.5)+number(t,x,bottom+28,24,GRAY,max_width=103)
    for i,(lo,mid,hi,name) in enumerate(zip(lower,middle,upper,d['categories'])):
        y=237+i*118;lx=x0+width*lo/maximum;mx=x0+width*mid/maximum;hx=x0+width*hi/maximum
        b+=line(lx,y,hx,y,BLUE,7)+line(lx,y-18,lx,y+18,BLUE,3)+line(hx,y-18,hx,y+18,BLUE,3)+circle(mx,y,10,WHITE,INK,4)
        for x,v in zip((913,1021,1129),(lo,mid,hi)):b+=number(v,x,y-14,27,INK,max_width=93)
        labels.append(slot(45,y-40,218,80,name));marks.append(dict(lower_x=lx,representative_x=mx,upper_x=hx,y=y))
    return chart('範囲比較_下限と代表値と上限を同時に示す_範囲グラフ作例','範囲の広さと代表値を同時に比較する','各項目の下限・代表値・上限を同じ目盛りへ置く範囲グラフの作例。','範囲 幅 最小 最大 区間 不確実性 見積 range interval uncertainty min max estimate',b,labels,dict(**d,chart_type='range',baseline=0,ticks=ticks,marks=marks,plot=dict(x=x0,y=184,width=width,height=bottom-184)),dict(use_case='見積もりや観測値を一点で断定せず、範囲と代表値を合わせて比較する。',message='区間の位置と広さ、区間内の代表値を一緒に読める。',reading=['横線の左端が下限、右端が上限、丸が代表値。','右の三列は同じ順番で値を示す。','区間は系列名で意味を定め、信頼区間などと自動的に解釈しない。']),size=(1200,canvas))


def diverging_bars(supplied=None):
    d=normalize('diverging_bar',supplied);values=d['series'][0]['values'];low,high=d['domain'];span=high-low
    x0=300;width=688;zero=x0+width*(0-low)/span;bottom=197+len(values)*99;canvas=max(720,bottom+127);ticks=sorted(set([low,high,0]+[low+span*i/4 for i in range(1,4)]))
    b='';labels=[slot(762,44,366,62,'単位：'+d['unit'])];marks=[]
    for t in ticks:
        x=x0+width*(t-low)/span;b+=line(x,151,x,bottom,INK if t==0 else PALE,3 if t==0 else 1.5)+number(t,x,bottom+29,24,GRAY,max_width=104)
    for i,(name,v) in enumerate(zip(d['categories'],values)):
        y=202+i*99;x=x0+width*(v-low)/span;color=BLUE if v>=0 else INK
        b+=rect(min(x,zero),y,abs(x-zero),43,color)+number(f'{v:+g}',1121,y+6,28,color,'right',max_width=104)
        if v==0:b+=circle(zero,y+21.5,6,WHITE,INK,3)
        labels.append(slot(40,y-18,231,78,name));marks.append(dict(x=x,zero_x=zero,y=y,width=abs(x-zero)))
    return chart('差分比較_共通のゼロから正負の差を見る_発散棒グラフ作例','ゼロを境に正と負の差を比べる','共通の基準からの差を、右向きと左向きの棒で区別する作例。','発散棒 差分 増減 正負 基準差 diverging bar signed difference deviation',b,labels,dict(**d,chart_type='diverging_bar',baseline=0,ticks=ticks,marks=marks,plot=dict(x=x0,y=151,width=width,height=bottom-151)),dict(use_case='基準や前期からの差を、増加と減少の方向で比較する。',message='共通のゼロから左右へ分かれた長さで差の方向と大きさを示す。',reading=['濃い中央の線が基準との差0。','右は正、左は負で、数字にも符号を付ける。','色と符号は差の方向であり、良し悪しの評価ではない。']),size=(1200,canvas))


def pareto_chart(supplied=None):
    d=normalize('pareto',supplied);values=d['series'][0]['values'];order=sorted(range(len(values)),key=lambda i:(-values[i],i));total=sum(values)
    pitch=category_pitch(d['categories'],139);width=max(815,pitch*len(values));x0=173;baseline=559;height=399;maximum=d['domain'][1];ticks=[maximum*i/4 for i in range(5)]
    b='';labels=[slot(62,30,410,63,'棒の単位：'+d['unit']),slot(x0+width-386,30,434,63,'線：累積構成比（%）')];points=[];cumulative=[]
    for t in ticks:
        y=baseline-height*t/maximum;b+=line(x0,y,x0+width,y,INK if t==0 else PALE,3 if t==0 else 1.5)+number(t,137,y-12,24,GRAY,'right',max_width=105)
    for t in (0,25,50,75,100):b+=number(f'{t}%',x0+width+31,baseline-height*t/100-12,23,GRAY,'left',max_width=111)
    run=0;bar_width=min(91,pitch*.56);lw=min(pitch-16,250)
    for j,i in enumerate(order):
        v=values[i];x=x0+(j+.5)*width/len(values);y=baseline-height*v/maximum
        b+=rect(x-bar_width/2,y,bar_width,baseline-y,MID)
        run+=v;share=run/total*100;py=baseline-height*share/100;points.append((x,py));cumulative.append(share)
        labels.append(slot(x-lw/2,618,lw,82,d['categories'][i]))
    connection='M'+'L'.join(f'{x:.6f} {y:.6f}' for x,y in points);b+=path(connection,stroke=WHITE,sw=11)+path(connection,stroke=INK,sw=4)
    for x,y in points:b+=circle(x,y,6,WHITE,INK,3)
    for j,i in enumerate(order):
        x=x0+(j+.5)*width/len(values);y=baseline-height*values[i]/maximum
        b+=number(values[i],x,575,26,INK,max_width=lw)
    return chart('重点原因_大きい要因と累積割合を読む_パレート図作例','大きい要因から累積の割合を読む','要因を大きい順へ整列した棒と、全体に占める累積割合の線を重ねる作例。','パレート 要因 重点 順位 累積 構成比 pareto concentration cumulative causes',b,labels,dict(**d,chart_type='pareto',baseline=0,ticks=ticks,sorted_indices=order,ordered_categories=[d['categories'][i] for i in order],cumulative_percent=cumulative,cumulative_domain=[0,100],plot=dict(x=x0,y=baseline-height,width=width,height=height)),dict(use_case='不良や問い合わせなどの要因を整理し、全体へ大きく寄与する対象を見つける。',message='要因の大きさと、上位からどれだけ全体を占めるかを同時に読める。',reading=['棒は左の目盛りで読み、大きい順に並ぶ。','濃い線は右の目盛りで累積構成比を示し、最後は100%。','棒の下は件数であり、割合の数値ではない。']),size=(max(1200,x0+width+190),720))


def scatter_chart(supplied=None):
    d=normalize('scatter',supplied);xvalues,yvalues=[s['values'] for s in d['series']];xlo,xhi=d['x_domain'];ylo,yhi=d['domain']
    x0=221;baseline=556;width=837;height=397;xticks=[xlo+(xhi-xlo)*i/4 for i in range(5)];yticks=[ylo+(yhi-ylo)*i/4 for i in range(5)]
    b='';labels=[slot(39,34,680,67,d['series'][1]['label']+'（'+d['unit']+'）'),slot(423,634,704,65,d['series'][0]['label']+'（'+d['x_unit']+'）')];points=[]
    for t in xticks:
        x=x0+width*(t-xlo)/(xhi-xlo);b+=line(x,baseline-height,x,baseline,PALE,1.5)+number(t,x,580,24,GRAY,max_width=122)
    for t in yticks:
        y=baseline-height*(t-ylo)/(yhi-ylo);b+=line(x0,y,x0+width,y,PALE,1.5)+number(t,179,y-12,24,GRAY,'right',max_width=142)
    b+=line(x0,baseline,x0+width,baseline,INK,3)+line(x0,baseline-height,x0,baseline,INK,3)
    for i,(xvalue,yvalue) in enumerate(zip(xvalues,yvalues)):
        x=x0+width*(xvalue-xlo)/(xhi-xlo);y=baseline-height*(yvalue-ylo)/(yhi-ylo)
        b+=circle(x,y,10,WHITE,BLUE,4);points.append(dict(category=d['categories'][i],x=x,y=y,x_value=xvalue,y_value=yvalue))
    return chart('関係確認_二つの数値を観測点で対応させる_散布図作例','二つの数値の関係を点の分布で見る','一つの観測を横軸と縦軸の値へ対応させ、等しい大きさの点で表す散布図の作例。','散布図 相関 関係 分布 観測 外れ値 scatter correlation relationship observation outlier',b,labels,dict(**d,chart_type='scatter',ticks=yticks,x_ticks=xticks,points=points,point_radius=10,plot=dict(x=x0,y=baseline-height,width=width,height=height)),dict(use_case='二つの測定値の関係や、ほかと離れた観測を調べる。',message='各観測の横と縦の値を一組の点として、分布の傾向を読む。',reading=['一つの点が同じ観測に対応する二つの数値。','点の大きさは一定で、値を面積に割り当てない。','同じ座標の観測は重なり、頻度の多さを表さない。','点の並びだけで原因と結果を確定するものではない。']),size=(1200,720))


CHARTS=dict(dot=dot_comparison,actual_target=actual_target,range=range_comparison,diverging_bar=diverging_bars,pareto=pareto_chart,scatter=scatter_chart)
