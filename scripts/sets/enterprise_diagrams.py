"""Individually composed explanations for the decisions and work of a manufacturer."""
from math import sin, cos, radians
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER
from vector import path, rect, circle, ellipse, line, poly, arrow, check, slot, asset


class Drawing:
    def __init__(self): self.body=''; self.labels=[]
    def add(self, *shapes): self.body+=''.join(shapes)
    def text(self,x,y,w,h,text,role='説明',color=INK): self.labels.append(slot(x,y,w,h,text,role,color=color))
    def box(self,x,y,w,h,text,fill=WHITE,stroke=INK,role='対象'):
        self.add(rect(x,y,w,h,fill,10,stroke,3)); self.text(x+18,y+12,w-36,h-24,text,role,WHITE if fill in (BLUE,INK) else INK)
    def dot(self,x,y,text,r=56,fill=WHITE):
        self.add(circle(x,y,r,fill,BLUE,3));self.text(x-r+12,y-42,r*2-24,84,text,'対象',WHITE if fill in (BLUE,INK) else INK)
    def finish(self,key,title,use,meaning,words,reading,relation,direction='left-to-right'):
        a=asset(title+'_業務の関係を示す図解',title,meaning,words,self.body,self.labels)
        a.update(key=key,kind='diagram',guidance=dict(use_case=use,message=meaning,reading=reading),layout=dict(relation=relation,reading_direction=direction))
        return a


def requirements_traceability():
    d=Drawing()
    for y in (175,325,475): d.add(line(248,y+44,960,y+44,MID,3))
    for x in (250,595,960):
        for y in (175,325,475): d.add(circle(x,y+44,8,BLUE))
    for i,t in enumerate(('使う人の要求','実現する設計','確かめる試験')): d.text(100+i*365,66,270,70,t,'対応の種類')
    for i,(a,b,c) in enumerate((('持ち運べる','軽量な構造','重量を測る'),('静かに使える','振動を抑える','動作音を測る'),('長く使える','摩耗しにくい','耐久試験'))):
        y=175+i*150
        for x,t in ((105,a),(470,b),(835,c)): d.box(x,y,260,88,t,PALE if x==470 else WHITE)
    d.add(path('M237 570V607H964V570',stroke=BLUE,sw=4))
    d.text(335,618,530,58,'変更時も、対応する要求と試験をたどる')
    return d.finish('development/requirements-traceability','要求・設計・試験をひも付ける','要求の抜け漏れや変更時の再確認範囲をレビューする。','要求から設計と試験までの対応を保持し、何を確認したかをたどれるようにする。','要求管理 トレーサビリティ 検証 設計 試験 対応 requirements traceability test coverage',['各行が一つの要求と、その実現手段・確認方法の組。','横の線は対応関係であり、数値の比較ではない。','下の括りは対応表を変更時にも維持することを示す。'],'requirements-design-test-links')


def tolerance_chain():
    d=Drawing();d.add(rect(95,252,980,157,FAINT,8))
    for x,w,t,c in ((135,200,'部品 A',PALE),(335,265,'部品 B',MID),(600,210,'部品 C',PALE)):
        d.add(rect(x,272,w,117,c,0,INK,3));d.text(x+18,307,w-36,50,t)
        d.add(line(x,207,x+w,207,BLUE,4),line(x,193,x,221,BLUE,3),line(x+w,193,x+w,221,BLUE,3))
    d.add(rect(810,272,160,117,WHITE,0,AMBER,3),path('M826 373L954 287M854 373L954 306M883 373L954 325',stroke=AMBER,sw=2))
    d.text(791,145,200,52,'残るすきま','結果');d.add(line(889,204,889,258,AMBER,3))
    d.add(line(135,456,970,456,INK,4),line(135,440,135,472,INK,3),line(970,440,970,472,INK,3))
    d.text(273,489,650,70,'部品寸法のばらつきが、組立寸法へ積み上がる')
    d.text(166,62,864,65,'一つずつの許容差と、組み合わせた結果を確認')
    return d.finish('development/tolerance-chain','部品の許容差が組立へ積み上がる','組立品のすきまや干渉が、部品寸法の組み合わせで変わることを説明する。','個々の部品が許容範囲でも、組み合わせた寸法を確認する必要がある。','公差 許容差 寸法 ばらつき 組立 干渉 tolerance stackup assembly dimensional variation',['上の寸法線が個々の部品、下の長い寸法線が組立全体。','右端の斜線部が、寸法の組み合わせで変わるすきま。','長さは関係を説明する概念図で、実際の公差計算値ではない。'],'serial-dimensional-accumulation')


def design_space():
    d=Drawing();d.add(rect(154,142,904,435,FAINT,4),poly('211,515 403,203 751,181 1001,427 850,535',PALE,BLUE,3))
    d.add(path('M395 184L698 555M585 154L934 506',stroke=INK,sw=3,extra='stroke-dasharray="8 8"'))
    d.add(poly('532,259 682,255 834,443 676,497',BLUE))
    d.add(circle(679,375,25,WHITE),check(665,364,.75,BLUE))
    d.text(204,45,790,61,'制約を重ね、成立する設計の範囲を探す')
    d.text(225,279,215,89,'性能の条件','条件');d.text(852,192,226,88,'製造の条件','条件')
    d.text(516,593,394,62,'両方を満たす設計候補','成立範囲')
    d.add(path('M683 496V576',stroke=BLUE,sw=3))
    return d.finish('development/feasible-design-space','複数の制約から設計の成立範囲を探す','性能・製造性・寸法などの条件を同時に満たす設計を検討する。','一つの性能だけを最大化せず、条件が重なる範囲から設計案を選ぶ。','設計空間 制約条件 実現可能 成立範囲 最適化 design space feasibility constraints',['淡い多角形は一つの条件を満たす範囲。','斜めの境界が別の制約、主色の領域が共通の成立範囲。','形と広さは条件の重なりを示す概念図。'],'intersecting-design-constraints')


def experiment_factors():
    d=Drawing();d.text(380,38,590,58,'要因 A の条件を変える','横の要因')
    for x,t in ((384,'A：低い条件'),(724,'A：高い条件')):d.text(x,114,308,59,t)
    for y,t in ((220,'B：低い条件'),(431,'B：高い条件')):d.text(52,y+47,274,100,t,'縦の要因')
    for i,(x,y,t) in enumerate(((384,215,'条件 1'),(724,215,'条件 2'),(384,426,'条件 3'),(724,426,'条件 4'))):
        d.add(rect(x,y,308,174,PALE if i in (1,2) else FAINT,8,BLUE,2))
        d.add(circle(x+54,y+49,19,BLUE));d.text(x+94,y+25,177,53,t)
        d.text(x+35,y+100,238,49,'同じ方法で測る')
    d.add(arrow(354,181,1103,181,INK,3,14),arrow(342,188,342,608,INK,3,14));d.text(333,631,775,53,'組み合わせをそろえて、単独効果と相互作用を調べる')
    return d.finish('development/factorial-experiment','二つの要因を組み合わせて試験する','試作や工程条件の検討で、二つの要因を系統的に変えて試す。','組み合わせた条件を比較することで、一方だけを変える試験では見えにくい関係を調べる。','実験計画 要因 組合せ 試験 相互作用 factorial experiment DOE interaction',['列が要因A、行が要因Bの条件。','四つの交点が試験する条件の組み合わせ。','結果の数値は入れておらず、比較する設計を示す。'],'two-factor-experimental-design')


def platform_variants():
    d=Drawing();d.add(rect(105,456,990,105,INK,8));d.text(318,480,565,54,'共通プラットフォーム','共通部',WHITE)
    for x,t in ((148,'標準モデル'),(481,'高機能モデル'),(814,'用途別モデル')):
        d.add(rect(x,212,237,186,WHITE,10,BLUE,3),rect(x+30,356,177,42,PALE,4),line(x+118,400,x+118,454,BLUE,5))
        d.text(x-8,120,252,57,t,'派生製品')
    d.add(rect(182,248,64,61,PALE,4),rect(274,248,77,61,PALE,4),rect(517,243,57,87,MID,3),rect(595,243,88,87,BLUE,3),circle(883,281,32,MID),poly('946,244 983,281 946,318 909,281',BLUE))
    d.text(185,603,836,57,'変える部分と、共通で維持する部分を分ける')
    return d.finish('development/platform-variants','共通基盤から用途別の製品を展開する','製品シリーズで共通化する部分と差別化する部分を整理する。','共通基盤を維持しながら、顧客の用途に合わせた機能を組み合わせる。','製品系列 共通基盤 モジュール 派生機種 標準化 platform product variants modular architecture',['下の一続きの帯が全モデルの共通基盤。','上の三つの構成の違いが派生機能。','同じ接続形状が共通のインターフェースを表す。'],'shared-platform-with-distinct-variants')


def technology_readiness():
    d=Drawing()
    for x,y,w,h,t in ((110,395,282,153,'原理を確認'),(408,286,282,262,'使用条件で試す'),(706,177,365,371,'実際の環境で確かめる')):
        d.add(rect(x,y,w,h,FAINT,0),line(x,y,x+w,y,BLUE,7));d.text(x+20,y+34,w-40,88,t,'確認する環境')
    d.add(arrow(99,590,1108,590,INK,4,19))
    for x,y in ((251,395),(549,286),(888,177)):
        d.add(circle(x,y,21,WHITE,BLUE,3),check(x-12,y-8,.63,BLUE))
    d.text(226,44,768,66,'実用に近い条件へ進めて、確からしさを高める')
    d.text(321,620,543,55,'確認の範囲が、実環境へ近づく')
    return d.finish('development/technology-readiness','技術を実用の条件へ段階的に近づける','研究成果を製品化する前に、どの環境まで確認したかを共有する。','原理の成立と実環境での成立を分け、確認済みの範囲を明らかにする。','技術成熟度 研究開発 実用化 検証 実環境 readiness prototype technology validation',['左から原理、使用条件、実環境の順に確認範囲が広がる。','各上端の印が、その段階での確認を示す。','段差は金額や正式な成熟度スコアではなく、確認範囲の違い。'],'expanding-validation-environments')


def prototype_learning():
    d=Drawing();d.add(line(155,213,1045,213,PALE,22),line(155,493,1045,493,PALE,22))
    for x,t in ((182,'疑問を絞る'),(597,'試作品で\n調べる'),(1012,'判断を更新')):d.dot(x,213,t,84,BLUE if x==597 else WHITE)
    d.add(arrow(273,213,500,213,BLUE,6,19),arrow(690,213,915,213,BLUE,6,19))
    d.add(path('M1012 303V493H186V312',stroke=BLUE,sw=5),poly('186,293 176,315 196,315',BLUE))
    d.box(353,443,494,100,'残った疑問を次の試作へ',WHITE,BLUE)
    d.text(205,60,795,66,'試作品を「完成形」よりも「学ぶ道具」として使う')
    d.text(383,604,441,58,'確かめる問いを一つずつ明確にする')
    return d.finish('development/prototype-learning','試作で疑問を減らして設計判断へ戻す','試作の目的を、見栄えの完成から技術や顧客の疑問の検証へ整理する。','試作で得た結果を設計判断へ返し、残った疑問を次の試作に引き継ぐ。','試作 プロトタイプ 仮説 検証 開発 学習 prototype learning hypothesis design experiment',['上段は問いを絞り、試作品で確かめて判断を更新する流れ。','下段の戻り線が未解決の疑問を次回へ渡す。','中央の試作が目的ではなく、疑問を減らす手段として描かれている。'],'question-driven-prototype-loop')


def design_freeze():
    d=Drawing();d.add(rect(70,190,454,341,FAINT,12),rect(550,190,576,341,PALE,12),rect(520,151,17,428,INK,4))
    for i,y in enumerate((254,357,460)):
        d.add(path(f'M105 {y}C218 {y-60} 341 {y+55} 502 {y}',stroke=MID,sw=4))
        d.add(line(559,y,956,y,BLUE,5),circle(583,y,8,BLUE))
    d.add(path('M855 418V564M1006 564V440',stroke=AMBER,sw=4),poly('1006,418 996,441 1016,441',AMBER))
    d.box(820,322,275,96,'合意した仕様',WHITE,BLUE)
    d.box(776,565,255,78,'変更を審議',WHITE,AMBER)
    d.text(129,77,338,63,'検討して変えられる期間');d.text(625,77,415,63,'基準を定めて作る期間')
    d.text(400,603,319,56,'仕様を確定する節目','確定点')
    return d.finish('development/design-freeze-change','仕様を確定し、以後の変更を管理する','設計の検討期間と量産準備で基準を固定する期間の違いを説明する。','確定した仕様を基準に進め、後から必要になった変更は影響を確認して判断する。','設計凍結 仕様確定 変更審議 基準 量産準備 design freeze baseline change control',['左の揺れる線は検討中の案、右の直線は確定した基準。','中央の縦線が仕様確定の節目。','下の別経路が確定後の変更審議を示す。'],'baseline-freeze-and-change-route')


def make_buy_decision():
    d=Drawing();d.add(rect(85,176,462,349,FAINT,12),rect(653,176,462,349,PALE,12))
    d.text(171,77,293,65,'自社で作る','選択肢');d.text(739,77,293,65,'外部から調達','選択肢')
    for y,a,b in ((225,'技術を蓄積する','外部の専門性を使う'),(322,'設備と人材を持つ','供給能力を確かめる'),(419,'改善を自社で回す','継続条件を合意する')):
        d.text(125,y,382,64,a);d.text(693,y,382,64,b)
    d.add(line(154,301,476,301,MID,2),line(154,398,476,398,MID,2),line(722,301,1044,301,MID,2),line(722,398,1044,398,MID,2))
    d.add(path('M312 546V580H885V546',stroke=INK,sw=4));d.text(276,598,652,67,'重要な能力と、外部への依存を合わせて判断')
    return d.finish('development/make-or-buy','内製と外部調達を能力・継続性で比べる','部品や機能を自社で作るか外部調達するかを検討する。','単価だけでなく、持つべき能力と継続的な供給条件を比較する。','内製 外製 外注 調達 垂直統合 能力 make buy outsource sourcing capability',['左右が内製と外部調達の選択肢。','同じ高さに、対応して確認する観点を並べる。','下の括りが複数観点を合わせた判断を示す。'],'paired-capability-sourcing-comparison')


def test_coverage():
    d=Drawing();d.text(352,47,680,63,'必要な機能 × 使用条件で、確認の抜けを見る')
    for x,t in ((405,'通常条件'),(652,'厳しい条件'),(899,'境界条件')):d.text(x,141,202,55,t,'使用条件')
    for y,t in ((254,'基本機能'),(405,'保護機能'),(556,'復旧機能')):d.text(94,y-30,232,60,t,'機能')
    for i,y in enumerate((254,405,556)):
        for j,x in enumerate((506,753,1000)):
            d.add(rect(x-101,y-58,202,116,FAINT,6,MID,2))
            if (i,j) in ((1,2),(2,1)):
                d.add(circle(x,y,22,WHITE,AMBER,3));d.text(x-35,y-26,70,51,'?','未確認',AMBER)
            else:d.add(circle(x,y,22,BLUE),check(x-13,y-9,.75))
    d.text(415,640,630,52,'チェックは確認済み、？は追加確認の候補')
    return d.finish('development/test-coverage-matrix','機能と使用条件から試験の抜けを見つける','試験計画やレビューで、確認済みの組み合わせと未確認箇所を共有する。','機能別の確認だけでなく、使用条件との組み合わせを見渡す。','試験 網羅性 カバレッジ 機能 条件 テスト test coverage matrix validation',['行が機能、列が使用条件。','交点のチェックが確認済み、疑問符が未確認の組み合わせ。','確認状態は説明のための作例で、特定製品の試験結果ではない。'],'function-condition-coverage')


def fishbone_causes():
    d=Drawing();d.add(arrow(113,362,973,362,INK,6,22));d.box(977,290,170,144,'起きた\n問題',BLUE,BLUE)
    for x,t,top in ((274,'人・手順',True),(537,'設備・道具',True),(800,'材料・部品',True),(355,'方法・条件',False),(625,'測定・確認',False),(856,'環境',False)):
        y=183 if top else 539;endx=x+84 if top else x-73
        d.add(line(x,y,endx,362,BLUE,4));d.text(x-109,y-90 if top else y+17,218,62,t,'原因の観点')
        for delta in (52,101):
            yy=y+delta if top else y-delta;xx=x+(endx-x)*delta/abs(362-y)
            d.add(line(xx-57,yy,xx,yy,MID,3))
    d.text(132,25,788,60,'原因の候補を観点ごとに広げ、事実で確かめる')
    return d.finish('quality/cause-fishbone','問題につながる原因候補を観点ごとに広げる','品質や業務の問題について、原因候補の偏りや抜けを減らす。','複数の観点から原因候補を挙げ、確認する仮説を整理する。','特性要因図 魚骨 原因分析 4M 要因 問題解決 fishbone Ishikawa root cause',['右の対象が調べる問題、主骨に合流する枝が原因の観点。','小枝が各観点から挙げる候補。','線は原因の候補を分類するもので、因果関係が確認済みという意味ではない。'],'categorized-cause-hypotheses')


def cause_verification():
    d=Drawing();d.box(78,258,249,157,'原因の仮説',FAINT,INK)
    d.add(arrow(334,337,463,337,BLUE,6,20));d.add(poly('470,337 601,216 732,337 601,458',WHITE,INK,3))
    d.text(506,294,190,87,'事実と\n一致するか','照合')
    d.add(path('M734 337H777V174H850',stroke=BLUE,sw=5),poly('871,174 847,163 847,185',BLUE));d.box(875,123,254,102,'裏付けがある',PALE,BLUE)
    d.add(path('M734 337H777V500H850',stroke=AMBER,sw=5),poly('871,500 847,489 847,511',AMBER));d.box(875,449,254,102,'仮説を見直す',WHITE,AMBER)
    d.add(path('M1000 554V631H203V433',stroke=AMBER,sw=4),poly('203,414 193,437 213,437',AMBER))
    d.text(393,60,618,69,'思いついた原因を、そのまま真因にしない')
    d.text(365,543,374,60,'観察・再現・測定で確認','確認手段')
    return d.finish('quality/cause-evidence-check','原因の仮説を事実で確かめる','不具合対策で、原因の思い込みと確認済みの原因を分ける。','仮説に合う事実を確認し、一致しなければ別の仮説へ戻る。','真因 原因検証 仮説 事実 再現 根拠 root cause evidence hypothesis verification',['中央で原因の仮説と実際の観察結果を照合する。','上が裏付けを得た経路、下が見直す経路。','戻り線が仮説を更新することを示す。'],'hypothesis-evidence-revision')


def defect_propagation():
    d=Drawing();d.add(rect(90,191,1012,360,FAINT,12))
    for x,t in ((189,'加工'),(469,'組立'),(749,'検査'),(1031,'出荷')):d.text(x-80,93,160,60,t,'工程')
    for i,x in enumerate((189,469,749,1031)):
        d.add(circle(x,341,48,WHITE,INK,3))
        if i<3:d.add(arrow(x+54,341,x+222,341,BLUE,6,20))
    d.add(circle(189,341,16,AMBER),circle(469,341,16,AMBER),circle(749,341,16,AMBER))
    d.add(path('M749 392V456H574',stroke=AMBER,sw=5),poly('552,456 577,444 577,468',AMBER));d.box(345,416,208,85,'後工程で発見',WHITE,AMBER)
    d.add(path('M446 505V612H189V405',stroke=AMBER,sw=4),poly('189,386 179,410 199,410',AMBER))
    d.text(459,590,560,70,'発生した工程へ戻し、流出を止める')
    return d.finish('quality/defect-origin-detection','不具合が生まれた工程と見つかった工程を分ける','工程不良の対策で、検出工程だけでなく発生工程へ対策を戻す。','発見場所と発生場所を区別し、不良を作る原因と流す原因の両方を見る。','不良 発生 流出 後工程 検出 品質 源流 defect origin detection escape',['注意色の点が工程を通過した不具合。','下へ外れる線が後工程での発見。','戻り線は発生した工程へ原因対策を返す。'],'origin-versus-detection-and-return')


def prevention_detection():
    d=Drawing();d.add(line(75,357,1113,357,PALE,24))
    d.add(circle(222,357,42,WHITE,INK,4),circle(611,357,42,AMBER),circle(1032,357,42,WHITE,BLUE,4))
    d.add(arrow(271,357,561,357,INK,5,19),arrow(660,357,982,357,INK,5,19))
    d.add(rect(420,232,17,248,BLUE,4),rect(812,232,17,248,INK,4))
    d.text(104,129,377,66,'発生を防ぐ','予防');d.text(731,129,377,66,'流出前に見つける','検出')
    d.text(91,517,377,94,'起こりにくい設計\n間違えにくい手順');d.text(727,517,377,94,'検査・監視\n出荷前の確認')
    d.text(486,413,252,63,'不具合の発生');d.add(line(603,182,603,244,AMBER,4));d.text(455,53,310,73,'予防と検出は別の働き')
    return d.finish('quality/prevention-and-detection','発生を防ぐ対策と流出を見つける対策を分ける','品質改善で、予防策と検出策の役割を説明する。','起こりにくくする仕組みと、起きた不具合を通さない仕組みを組み合わせる。','未然防止 検出 予防 検査 ポカヨケ 流出防止 prevention detection quality control',['注意色の点が不具合の発生時点。','左の主色の境界が発生前の予防、右の濃色の境界が発生後の検出。','左右の境界は異なる働きで、単なる作業の順番ではない。'],'prevent-before-and-detect-after')


def lot_sampling():
    d=Drawing();d.add(rect(82,163,405,354,FAINT,12,INK,3))
    for i in range(4):
        for j in range(5):d.add(circle(137+j*75,224+i*74,20,BLUE if (i,j) in ((0,1),(1,3),(2,0),(3,4)) else WHITE,BLUE if (i,j) in ((0,1),(1,3),(2,0),(3,4)) else MID,2))
    d.add(arrow(498,340,658,340,BLUE,5,20));d.add(rect(680,249,432,181,PALE,9,BLUE,3))
    for x in (737,842,947,1052):d.add(circle(x,339,24,BLUE))
    d.text(115,71,337,63,'対象のロット','母集団');d.text(717,148,358,71,'抽出したものを検査','標本')
    d.add(path('M901 438V587H284V539',stroke=INK,sw=4),poly('284,519 274,542 294,542',INK));d.text(440,606,602,58,'抜取の条件と結果から、ロットを判断')
    return d.finish('quality/lot-sampling','ロットから抽出して全体の判断につなげる','抜取検査で、検査する対象と判断する対象の違いを説明する。','抽出した対象の検査結果を、定めた抜取条件に沿ってロットの判断へ使う。','抜取検査 ロット 標本 抽出 検査 sampling lot inspection population',['左が判断するロット全体、主色の点が抽出対象。','右の少数の点が実際に検査する対象。','下の線は検査結果をロット判断へ戻す。点の数は抜取規格の指定ではない。'],'sample-inspection-to-lot-decision')


def lot_genealogy():
    d=Drawing()
    for y,t in ((150,'材料ロット A'),(380,'材料ロット B')):d.box(67,y,270,114,t,FAINT,INK)
    d.add(path('M340 207H441V284H519M340 437H441V359H519',stroke=BLUE,sw=4))
    d.box(524,259,245,123,'製造ロット',BLUE,BLUE)
    for y,t in ((139,'出荷先 X'),(390,'出荷先 Y')):
        d.add(path(f'M770 319H827V{y+58}H893',stroke=BLUE,sw=4));d.box(896,y,237,116,t,PALE,BLUE)
    d.add(arrow(360,584,1010,584,BLUE,4,18),arrow(1010,626,360,626,INK,4,18));d.text(170,565,177,39,'前方へ追う');d.text(170,610,177,39,'元へたどる')
    d.text(257,30,691,66,'材料・製造・出荷の識別をつないで残す')
    return d.finish('quality/lot-genealogy','材料から製造・出荷先までたどる','追跡調査や対象範囲の特定で、ロットと出荷先の対応を共有する。','材料から出荷先へも、出荷品から材料へも履歴をたどれるようにする。','ロット 追跡 追溯 リコール 材料 履歴 genealogy traceability batch recall',['左が材料、中央が製造ロット、右が出荷先。','枝分かれと合流が実際に保持する対応関係。','下の二方向の矢印は前方追跡と遡及を区別する。'],'many-to-one-to-many-traceability')


def measurement_variation():
    d=Drawing();d.add(circle(588,304,103,FAINT,INK,3));d.text(509,263,158,83,'同じ\n対象物','対象')
    for x,y,t in ((227,213,'測る人'),(949,213,'測定器'),(588,572,'測る条件')):
        d.dot(x,y,t,74,PALE)
    d.add(arrow(308,233,478,280,BLUE,5,20),arrow(866,233,699,280,BLUE,5,20),arrow(588,490,588,415,BLUE,5,20))
    d.text(97,410,302,99,'対象の違い以外にも\n測定値が変わる要因');d.text(805,410,302,99,'繰り返し測定で\nばらつきを分ける')
    d.text(241,42,718,65,'測定値のばらつきは、製品だけから生まれない')
    return d.finish('quality/measurement-system-variation','製品のばらつきと測定のばらつきを分ける','測定値の信頼性を検討し、測定者・機器・条件の影響を共有する。','同じ対象でも測り方によって値が変わるため、測定の仕組みを確かめる。','測定システム MSA ゲージ 測定者 反復性 再現性 measurement variation gage repeatability reproducibility',['中央は同じ対象物。','周囲からの三つの矢印が測定値に影響する要因。','製品差を表す図ではなく、測定側のばらつきを分ける概念図。'],'measurement-influence-model')


def calibration_chain():
    d=Drawing()
    for i,(x,y,w,t) in enumerate(((90,132,328,'参照する基準'),(436,293,328,'校正した標準器'),(781,454,328,'現場の測定器'))):
        d.add(rect(x,y,w,107,INK if i==0 else PALE,8,INK,3));d.text(x+22,y+21,w-44,64,t,'基準の階層',WHITE if i==0 else INK)
        if i<2:d.add(path(f'M{x+164} {y+109}V{y+134}H{x+498}V{y+142}',stroke=BLUE,sw=4),poly(f'{x+498},{y+161} {x+488},{y+139} {x+508},{y+139}',BLUE))
    for x,y in ((228,302),(570,463)):
        d.text(x-111,y,262,63,'比較して差を記録','校正')
    d.add(path('M127 607H1121',stroke=MID,sw=3));d.text(270,621,662,59,'基準までのつながりと、校正結果を保持する')
    return d.finish('quality/calibration-chain','測定器を基準へつながる比較で校正する','測定器管理で、校正結果と参照基準のつながりを説明する。','現場の測定器から参照基準まで、比較と記録の連鎖を保持する。','校正 計測 標準器 基準 トレーサビリティ measurement calibration traceability reference',['上から基準・標準器・現場の測定器へ比較をつなぐ。','折れた矢印は校正の比較関係。','各段の差や不確かさは記録で管理する。'],'reference-comparison-chain')


def control_plan():
    d=Drawing();d.add(rect(92,114,1016,476,WHITE,9,INK,3))
    cols=((115,240,'工程'),(365,280,'管理する特性'),(654,217,'確認方法'),(878,205,'外れた場合'))
    for x,w,t in cols:d.add(rect(x,137,w,65,INK,5));d.text(x+12,148,w-24,44,t,'管理項目',WHITE)
    for y,values in ((246,('加工','重要な寸法','ゲージ','止めて確認')),(389,('組立','締結の状態','記録','隔離して処置'))):
        d.add(rect(115,y,968,105,FAINT,6))
        for (x,w,_),t in zip(cols,values):d.text(x+12,y+23,w-24,58,t)
    d.add(line(367,202,367,548,MID,2),line(656,202,656,548,MID,2),line(880,202,880,548,MID,2));d.text(217,617,771,59,'「何を測るか」と「外れたらどうするか」を一組に')
    return d.finish('quality/control-plan','工程・管理特性・確認・異常時対応を一組にする','工程の品質管理を、測定だけで終わらない運用に整理する。','各工程で見る特性と確認方法、基準から外れたときの対応をつなぐ。','管理計画 コントロールプラン 工程 特性 反応計画 control plan characteristic reaction process',['行が工程、列が管理特性・確認方法・異常時対応。','同じ行を横に読むと、確認から行動までがつながる。','記載した工程と確認内容は構成を示す作例。'],'process-characteristic-method-reaction')


def corrective_preventive():
    d=Drawing();d.box(78,257,226,150,'起きた不具合',WHITE,AMBER)
    d.add(path('M308 332H391V181H475M391 332V487H475',stroke=INK,sw=4))
    d.box(480,119,300,124,'今回の対象を直す',FAINT,INK);d.box(480,425,300,124,'原因を取り除く',PALE,BLUE)
    d.add(arrow(788,181,885,181,INK,4,18),arrow(788,487,885,487,BLUE,4,18))
    d.box(895,119,240,124,'影響を収める',WHITE,INK);d.box(895,425,240,124,'再発を防ぐ',BLUE,BLUE)
    d.text(381,298,736,70,'同じ「対策」でも、対象と狙いが異なる')
    d.text(342,595,778,64,'原因対策は、似た工程や製品にも展開して確認')
    return d.finish('quality/correction-and-cause-removal','今回の修正と再発を防ぐ原因対策を分ける','不具合対応を、製品の修正だけで終わらせず原因の除去へつなげる。','今回の対象を直す処置と、再発を防ぐ原因対策を並行して考える。','是正 処置 修正 再発防止 横展開 不具合 CAPA correction corrective action recurrence',['上の枝は今回の対象に対する修正と影響の収束。','下の枝は原因を取り除いて再発を防ぐ対策。','上下は代替案ではなく、狙いの異なる取り組み。'],'correction-versus-cause-removal')


def takt_alignment():
    d=Drawing();d.text(106,80,988,62,'需要の間隔と、工程が完成させる間隔を合わせる')
    for y,t in ((217,'必要な間隔'),(437,'作る間隔')):
        d.text(57,y-22,223,56,t);d.add(arrow(292,y,1124,y,INK,4,18))
    for x in (353,523,693,863,1033):
        d.add(line(x,153,x,492,MID,2,'7 7'),circle(x,217,19,BLUE),rect(x-21,416,42,42,WHITE,2,BLUE,3))
    d.add(path('M353 538V557H523V538',stroke=BLUE,sw=4));d.text(319,579,248,57,'一つ必要になる間隔')
    d.text(697,580,388,57,'需要に合わせて工程を設計')
    return d.finish('production/takt-alignment','必要な間隔と完成する間隔を合わせる','生産計画で、顧客の需要から工程の目標ペースを考える。','必要な数を必要な間隔で届けられるよう、需要のペースと工程のペースを照合する。','タクトタイム サイクルタイム 需要 ペース 生産 takt cycle time production rhythm',['上段の丸が必要になるタイミング、下段の四角が完成するタイミング。','縦の破線は同じ時点の対応。','図はペースをそろえた概念例で、実際の生産時間ではない。'],'demand-completion-rhythm')


def kanban_pull():
    d=Drawing();d.box(82,299,278,173,'前の工程',WHITE,INK);d.box(841,299,278,173,'次の工程',WHITE,INK)
    d.add(rect(479,304,240,165,FAINT,8,BLUE,3))
    for x in (506,572,638):d.add(rect(x,333,46,79,PALE,4,BLUE,2))
    d.add(arrow(369,390,467,390,BLUE,6,19),arrow(728,390,829,390,BLUE,6,19))
    d.add(path('M980 285V142H223V280',stroke=INK,sw=4),poly('223,299 213,278 233,278',INK))
    d.add(rect(482,98,236,91,WHITE,8,INK,3));d.text(500,116,200,57,'補充の合図','情報')
    d.text(431,526,338,66,'使った分だけ補充','仕組み');d.text(885,535,191,54,'取り出す');d.text(121,535,202,54,'必要分を作る')
    return d.finish('production/kanban-pull','後工程の使用を合図に補充する','作り過ぎを抑えるため、物の流れと補充指示の流れを分けて説明する。','後工程が使ったことを前工程へ伝え、必要な分を補充する。','かんばん 引取 補充 プル生産 後工程 kanban pull replenishment',['下段の主色の矢印が前工程から後工程への物の移動。','上段の逆向きの経路が後工程からの補充の合図。','中央の置場が両工程の受け渡し点。'],'material-forward-signal-backward')


def wip_limit():
    d=Drawing();d.box(68,219,259,262,'次に行う\n仕事',FAINT,INK)
    for y in (265,350,435):d.add(line(360,y,433,y,MID,3),line(433,y-14,433,y+14,INK,4))
    d.add(rect(471,203,414,294,PALE,10,BLUE,3))
    for x in (510,630,750):d.add(rect(x,256,95,180,WHITE,8,BLUE,2),circle(x+47,281,9,BLUE))
    d.add(arrow(891,350,1001,350,BLUE,6,20));d.dot(1060,350,'完了',57,BLUE)
    d.text(484,112,388,64,'着手中の上限を決める');d.text(442,541,665,68,'空きができてから、次の仕事を入れる')
    d.add(path('M1074 429V633H367V508',stroke=INK,sw=4),poly('367,485 356,511 378,511',INK));d.text(758,646,296,51,'空きを知らせる')
    return d.finish('production/wip-limit','着手中の量を決めて仕事の滞留を抑える','作業の掛け持ちや仕掛品の増加を抑える運用を説明する。','進行中の枠が空いてから次の仕事を始め、着手し過ぎを抑える。','仕掛 上限 WIP 滞留 着手制限 カンバン work in progress limit flow',['中央の囲みが着手中の上限、左が待っている仕事。','入口の止め線は枠が埋まっている状態。','完了によって空いたことを戻りの経路で知らせる。枠数は概念例。'],'bounded-work-in-progress')


def setup_separation():
    d=Drawing();d.text(70,111,255,58,'変更前');d.text(70,439,255,58,'分けた後')
    d.add(rect(312,150,798,99,PALE,5));d.box(461,150,431,99,'止めて準備・交換・確認',INK,INK)
    d.add(rect(312,458,798,99,PALE,5));d.box(569,458,213,99,'交換・確認',INK,INK)
    d.box(321,332,286,86,'動いている間に準備',WHITE,BLUE)
    d.add(path('M492 265V302H464V318',stroke=BLUE,sw=4),poly('464,333 455,312 473,312',BLUE));d.add(path('M625 266V409H674V438',stroke=INK,sw=4),poly('674,458 664,435 684,435',INK))
    d.text(266,614,841,62,'停止が必要な仕事と、事前にできる仕事を分ける')
    return d.finish('production/internal-external-setup','止めて行う段取りと事前準備を分ける','品種切替や設備交換の停止時間を短くする考え方を説明する。','設備を止める必要がある作業だけを停止中に残し、準備は稼働中に進める。','段取り替え 内段取り 外段取り SMED 停止時間 setup changeover external internal',['上は準備から確認までを停止中に行う状態。','下は事前準備を停止の帯から外へ分けた状態。','帯の長さは概念的な比較で、改善率の数値を表さない。'],'separate-offline-preparation')


def maintenance_window():
    d=Drawing();d.add(arrow(100,563,1113,563,INK,4,18))
    d.add(rect(95,331,1009,112,PALE,7),rect(495,215,221,296,WHITE,8,BLUE,3))
    d.text(124,349,329,73,'通常の運転','稼働');d.text(755,349,313,73,'確認して再開','復帰')
    d.add(rect(521,265,169,128,BLUE,8));d.text(539,297,133,65,'計画保全','保全',WHITE)
    d.add(circle(495,443,20,WHITE,INK,3),circle(716,443,20,BLUE),check(703,434,.73))
    d.text(392,113,422,64,'停止する範囲と復帰条件を合意');d.text(148,597,298,65,'前に資材・人員を準備');d.text(733,597,351,65,'後に機能と安全を確認')
    return d.finish('production/maintenance-window','保全のための停止枠と復帰条件を確保する','計画保全を生産計画へ組み込み、停止前後に必要な準備を共有する。','保全作業の時間だけでなく、停止前の準備と再開前の確認を計画する。','計画保全 停止計画 定修 保全窓 再開 maintenance shutdown window restart',['横の帯が通常運転、中央の囲みが計画した停止の範囲。','左の印が停止への入り口、右のチェックが再開確認。','時間の長さは特定設備の作業時間ではなく構造の説明。'],'planned-stop-with-restart-conditions')


def equipment_loss_layers():
    d=Drawing();d.text(82,111,261,61,'使える時間');d.text(82,278,261,61,'動いている時間');d.text(82,445,261,61,'良品を作る時間')
    d.add(rect(361,112,732,90,FAINT,4,INK,2),rect(361,279,596,90,PALE,4,BLUE,2),rect(361,446,451,90,BLUE,4))
    d.add(rect(957,279,136,90,WHITE,4,AMBER,2),rect(812,446,145,90,WHITE,4,AMBER,2))
    d.add(path('M1093 209V266M957 376V432',stroke=AMBER,sw=3),arrow(1093,241,1093,272,AMBER,3,13),arrow(957,404,957,438,AMBER,3,13))
    d.text(967,292,116,64,'停止','損失');d.text(821,459,127,63,'遅れ\n不良','損失')
    d.text(379,593,700,65,'どの段階で有効な時間が失われるかを見る')
    return d.finish('production/equipment-loss-layers','設備の時間損失を段階に分けて見る','設備改善の会議で、停止・速度低下・不良を分けて優先課題を整理する。','使える時間から、実際に良品を作る時間までの減少要因を分ける。','設備効率 OEE 稼働 停止 速度 不良 ロス equipment effectiveness downtime speed quality loss',['上から利用可能・稼働・良品に使われる時間へ絞る。','注意色の枠が段階ごとの損失。','帯の長さは概念図で、設備効率の計算値や実績ではない。'],'nested-effective-time-loss')


def line_work_balance():
    d=Drawing();d.add(line(160,213,1065,213,BLUE,3,'8 7'),line(160,536,1065,536,INK,3))
    for x,n,t in ((254,3,'工程 A'),(575,5,'工程 B'),(896,2,'工程 C')):
        for i in range(n):d.add(rect(x,486-i*62,152,47,BLUE if i>2 else PALE,4,BLUE,2))
        d.text(x-25,568,202,64,t)
    d.add(path('M741 238H832V382H893',stroke=BLUE,sw=5),poly('912,382 889,371 889,393',BLUE))
    d.text(384,60,438,64,'工程間で作業を再配分する');d.text(133,145,261,55,'目標の処理枠');d.text(830,284,274,62,'分担を移せるか確認')
    return d.finish('production/line-work-balance','長い工程の作業を余力のある工程へ分担する','ライン設計で、工程ごとの作業量と再配分できる範囲を共有する。','長い工程だけを急がせず、作業を分けて全体の処理ペースをそろえる。','ラインバランス 作業配分 工程 工数 負荷 line balancing workload allocation',['積み重なった短い帯が工程内の作業。','破線が目標の処理枠、中央の上段が枠を超える作業。','曲がる矢印は移せる作業の再配分。数と高さは構造の作例。'],'redistribute-work-across-stations')


def constraint_buffer():
    d=Drawing();d.box(66,318,232,134,'投入する',FAINT,INK)
    d.add(rect(359,296,220,178,PALE,8,BLUE,3));d.text(381,326,176,47,'手前の余裕','緩衝');
    for x in (392,449,506):d.add(rect(x,395,35,43,BLUE,3))
    d.add(rect(665,240,97,291,INK,6));d.text(624,559,179,71,'制約の工程','制約')
    d.add(arrow(304,385,349,385,BLUE,6,17),arrow(589,385,653,385,BLUE,6,17),arrow(775,385,922,385,BLUE,6,20));d.dot(1001,385,'完成',64,BLUE)
    d.add(path('M712 224V127H183V289',stroke=INK,sw=4),poly('183,316 172,290 194,290',INK));d.text(296,56,509,56,'制約のペースに合わせて投入')
    return d.finish('production/constraint-buffer-release','制約工程を基準に投入と余裕を調整する','全体の生産量を左右する工程に合わせて、仕掛と投入を管理する。','制約工程の前に必要な余裕を持ち、上流の投入を同じペースへ合わせる。','制約理論 TOC ドラム バッファ ロープ ボトルネック 投入 constraint drum buffer rope',['中央の濃い細長い形が全体のペースを決める制約。','その手前の囲みが制約を待たせないための余裕。','上の戻り線が制約のペースを投入へ伝える。'],'constraint-paced-release-and-buffer')


def batch_piece_flow():
    d=Drawing();d.text(82,79,281,64,'まとめて渡す');d.text(82,398,281,64,'一つずつ渡す')
    for y in (212,531):
        for x in (412,724,1036):d.add(circle(x,y,51,WHITE,INK,3))
        d.add(arrow(470,y,661,y,BLUE,4,18),arrow(782,y,973,y,BLUE,4,18))
    for x in (385,414,443):
        for y in (160,188,216):d.add(rect(x-12,y,23,23,BLUE,2))
    for x in (385,542,697,855,1009):d.add(rect(x,512,34,37,BLUE,3))
    d.text(364,290,412,70,'全部そろうまで次が待つ');d.text(610,600,482,69,'完成したものから先へ渡す')
    d.add(line(93,359,1107,359,MID,2,'7 7'))
    return d.finish('production/batch-and-piece-flow','まとめ渡しと一個流しの待ち方を比べる','工程間の受け渡し量が待ち時間や仕掛に与える違いを説明する。','同じ処理でも、まとめて渡すか完成ごとに渡すかで後工程の待ちが変わる。','一個流し バッチ ロット 受渡 待ち リードタイム batch one piece flow transfer',['上段は一つの工程にまとまった処理対象がたまる。','下段は対象が工程間に順に流れる。','丸が工程、四角が対象で、矢印は同じ進行方向。'],'batch-versus-piece-transfer')


def capacity_skills():
    d=Drawing();d.text(370,30,737,64,'人数だけでなく、できる工程を対応させる')
    for y,t in ((233,'担当 A'),(387,'担当 B'),(541,'担当 C')):d.box(80,y-43,238,86,t,FAINT,INK)
    for x,t in ((591,'工程 1'),(947,'工程 2')):
        d.add(rect(x-123,185,246,415,WHITE,10,BLUE,3));d.text(x-104,123,208,55,t)
    for x,y in ((591,233),(591,387),(947,387),(947,541)):d.add(line(325,y,x-30,y,MID,3))
    for x,y in ((591,233),(591,387),(947,387),(947,541)):d.add(circle(x,y,23,BLUE),check(x-13,y-9,.75))
    d.add(rect(520,477,142,124,WHITE,5,AMBER,2));d.text(530,500,122,70,'育成の\n候補','不足')
    d.text(136,633,974,54,'同じ人が複数工程を担う場合は、時間の重複も確認')
    return d.finish('production/skill-capacity-coverage','工程に対応できる人材と不足を見渡す','生産要員の計画で、人数と技能の組み合わせを確認する。','人数の合計だけでなく、各工程を担当できる人と不足している技能を確認する。','多能工 技能 要員 能力 工程 配置 capacity skills cross training coverage',['行が担当者、列が工程。','チェックが対応できる組み合わせ。','下の注意色は育成する候補で、同じ人の同時稼働を意味しない。'],'people-to-station-qualification')


def reorder_trigger():
    d=Drawing();d.add(arrow(127,565,1120,565,INK,3,17),arrow(127,565,127,117,INK,3,17));d.text(18,83,207,55,'在庫の量');d.text(946,597,199,56,'時間の経過')
    d.add(line(146,370,1100,370,AMBER,3,'8 7'));d.text(130,603,322,56,'破線：補充を頼む水準')
    d.add(path('M162 191L633 463L633 185L1074 432',stroke=BLUE,sw=6))
    d.add(circle(471,370,15,WHITE,AMBER,4),line(471,389,471,552,AMBER,2,'6 6'),line(633,464,633,551,BLUE,2,'6 6'))
    d.add(path('M471 516V532H633V516',stroke=INK,sw=3));d.text(723,130,333,64,'入荷して在庫が増える')
    d.text(345,46,420,65,'入荷までの時間を見込んで発注');d.text(411,438,216,60,'入荷までの期間')
    return d.finish('supply/reorder-point-lead-time','入荷までの時間を見込んで補充する','在庫切れを防ぐため、発注点と調達リードタイムの関係を説明する。','在庫がなくなってから頼むのではなく、入荷までに使う分を見込んで補充を始める。','発注点 補充 在庫 安全在庫 リードタイム reorder point lead time replenishment',['右下がりは在庫の使用、立ち上がりは入荷。','破線の水準に達した丸印で補充を依頼する。','横の括りが入荷までの期間。数量や日数は概念例。'],'inventory-trigger-before-receipt')


def dual_sourcing():
    d=Drawing();d.box(101,118,323,141,'主な供給先',FAINT,INK);d.box(101,433,323,141,'代替の供給先',PALE,BLUE)
    d.add(path('M429 188H673V355H828',stroke=MID,sw=5,extra='stroke-dasharray="8 8"'));d.add(line(514,166,550,210,AMBER,5),line(550,166,514,210,AMBER,5))
    d.add(path('M429 503H673V382H814',stroke=BLUE,sw=7),poly('841,382 813,369 813,395',BLUE));d.box(845,285,253,155,'必要な供給を\n確保する',WHITE,INK)
    d.text(487,68,608,64,'主な供給が止まったときの代替経路');d.text(455,559,627,76,'同じ要求を満たせるか、平常時に確認')
    return d.finish('supply/qualified-dual-sourcing','要求を満たす代替供給先を備える','部材の供給停止リスクに備え、調達先の代替性を説明する。','供給先の数を増やすだけでなく、代替先でも必要な仕様と量を確保できるようにする。','複数購買 代替調達 二社購買 供給停止 認定 dual sourcing alternate supplier qualification',['上の点線が停止した主な供給経路。','下の主色の経路が確認済みの代替先からの供給。','右の共通の到達点が満たすべき同じ要求。'],'qualified-alternate-source')


def postponement():
    d=Drawing();d.add(rect(65,232,547,240,FAINT,10));d.box(97,292,226,120,'共通の状態',WHITE,INK);d.add(arrow(330,351,469,351,BLUE,6,20))
    for x in (476,517,558):d.add(rect(x,295,28,112,PALE,3,BLUE,2))
    d.add(rect(658,134,14,463,INK,4));d.text(523,41,277,70,'受注で仕様が決まる','確定点')
    for y,t,c in ((186,'仕様 A',BLUE),(351,'仕様 B',INK),(516,'仕様 C',MID)):
        d.add(path(f'M679 350H759V{y}H860',stroke=BLUE,sw=4),poly(f'883,{y} 860,{y-10} 860,{y+10}',BLUE));d.box(890,y-54,232,108,t,PALE,BLUE)
    d.text(132,533,404,69,'先に共通部分まで準備');d.text(728,622,410,62,'必要な仕様へ仕上げる')
    return d.finish('supply/postponed-differentiation','共通部分を準備し、受注後に仕様を分ける','多品種の在庫を抑えながら納期へ対応する生産・調達方式を説明する。','共通部分を先に準備し、顧客ごとの差が決まる工程を注文の後へ置く。','延期差別化 受注生産 共通化 多品種 在庫 postponement delayed differentiation order',['左が先に準備する共通部分。','中央の縦線が注文により仕様が確定する地点。','右の分岐が必要な仕様への仕上げ。'],'common-stock-order-differentiation')


def demand_decoupling():
    d=Drawing();d.add(rect(68,236,434,185,FAINT,9),rect(706,236,425,185,PALE,9));d.add(rect(527,194,153,269,WHITE,9,BLUE,4))
    for y in (225,300,375):d.add(rect(554,y,99,49,PALE,3,BLUE,2))
    d.add(arrow(115,328,509,328,BLUE,7,20),arrow(693,328,1082,328,BLUE,7,20))
    d.text(115,117,337,64,'需要を見込んで準備');d.text(746,117,344,64,'注文に合わせて進める')
    d.text(469,515,267,69,'二つをつなぐ在庫');d.text(111,587,391,68,'予測で動く範囲');d.text(728,587,391,68,'注文で動く範囲')
    return d.finish('supply/demand-decoupling-point','予測で準備する範囲と受注で動く範囲を分ける','見込生産と受注生産の境界を整理し、在庫の役割を説明する。','予測と実際の注文を、意図した在庫地点でつなぐ。','デカップリングポイント 見込 受注 在庫 需要 forecast order decoupling point push pull',['左は需要予測による準備、右は注文による実行。','中央の在庫が二つの範囲の変動を受け止める。','矢印は物の流れで、予測情報と注文情報は上の説明で区別する。'],'forecast-order-decoupling-boundary')


def milk_run():
    d=Drawing();d.add(path('M286 172H944Q1025 172 1025 253V457Q1025 541 941 541H281Q196 541 196 456V255Q196 172 286 172Z',stroke=PALE,sw=27))
    d.add(arrow(412,172,715,172,BLUE,5,20),arrow(1025,291,1025,415,BLUE,5,20),arrow(895,541,522,541,BLUE,5,20),arrow(196,428,196,283,BLUE,5,20))
    for x,y,t in ((286,172,'供給先 A'),(944,172,'供給先 B'),(944,541,'供給先 C')):d.box(x-122,y-43,244,86,t,WHITE,BLUE)
    d.box(149,491,274,102,'共通の受入先',INK,INK);d.text(353,293,497,90,'一つの巡回で\n複数の供給先から集める')
    d.text(273,629,704,58,'受け取り時刻と必要量を巡回に合わせる')
    return d.finish('supply/milk-run-collection','複数の供給先を一つの経路で巡回する','調達物流で、個別便から定期巡回へまとめる考え方を説明する。','複数の供給先を決まった経路で回り、共通の受入先へまとめて運ぶ。','ミルクラン 巡回 集荷 調達物流 定期便 milk run route collection logistics',['四角が供給先と共通の受入先。','閉じた経路と同じ向きの矢印が一回の巡回。','時刻・積載量・供給先の順序は実際の条件で決める。'],'multi-stop-collection-loop')


def supplier_segmentation():
    d=Drawing();d.add(arrow(207,584,1118,584,INK,3,16),arrow(207,584,207,82,INK,3,16))
    for x,y,c in ((250,129,FAINT),(673,129,PALE),(250,365,FAINT),(673,365,FAINT)):d.add(rect(x,y,391,200,c,5))
    d.text(268,174,355,90,'代替を備える\n供給を優先');d.text(691,174,355,90,'共同で計画\n関係を深める');d.text(268,410,355,90,'手順を簡潔に\n効率よく調達');d.text(691,410,355,90,'条件を比較\n購買力を生かす')
    d.text(38,112,131,157,'上ほど\n供給上の\nリスク');d.text(579,616,517,63,'右ほど、事業への影響が大きい')
    d.add(circle(868,148,10,BLUE));d.text(316,31,763,60,'取引先の特性に応じて、関わり方を変える')
    return d.finish('supply/supplier-relationship-strategy','供給リスクと事業への影響で調達方針を分ける','取引先を同じ方法で扱わず、関係づくりや代替準備の重点を整理する。','供給リスクと事業への影響を合わせ、調達の関わり方を決める。','調達戦略 仕入先分類 供給リスク 取引 関係 supplier segmentation procurement portfolio',['縦軸が供給リスク、横軸が事業への影響。','各領域の文章が取引先への関わり方の例。','相対的な分類で、金額やリスク確率の値は示していない。'],'supply-risk-impact-strategies')


def bullwhip_orders():
    d=Drawing()
    for x,t in ((92,'最終需要'),(446,'販売側の発注'),(800,'上流側の発注')):
        d.add(rect(x,196,310,286,FAINT,8),line(x+19,341,x+291,341,MID,2,'5 5'));d.text(x,100,310,63,t)
    d.add(path('M116 346L161 335L206 353L251 329L296 343L341 332L377 345',stroke=BLUE,sw=5))
    d.add(path('M470 365L510 305L550 370L590 282L630 387L670 306L727 361',stroke=BLUE,sw=5))
    d.add(path('M824 402L864 245L904 432L944 221L984 461L1024 266L1081 396',stroke=BLUE,sw=5))
    d.add(arrow(411,340,435,340,INK,4,13),arrow(765,340,789,340,INK,4,13))
    d.text(120,531,969,72,'小さな需要変動が、まとめ発注や情報の遅れで増幅');d.text(246,620,714,60,'需要の情報を共有し、変動をそのまま増やさない')
    return d.finish('supply/bullwhip-amplification','需要の小さな変化が上流で大きくなる','需給会議で、需要と発注の変動が同じではないことを説明する。','情報の遅れやまとめ発注が、上流に伝わる変動を増幅することがある。','ブルウィップ 鞭効果 需要変動 発注増幅 需給 bullwhip demand amplification orders',['左から最終需要、販売側の発注、上流側の発注。','波の振れ幅が増える構造が変動の増幅を表す。','線は概念例で、実際の時系列や変動倍率ではない。'],'upstream-order-variability-amplification')


def split_delivery():
    d=Drawing();d.add(rect(93,210,323,322,FAINT,10,INK,3))
    for y in (247,326,405):
        for x in (141,230,319):d.add(rect(x,y,52,57,PALE,4,BLUE,2))
    d.text(92,104,324,66,'一つの製造ロット')
    for y,t,n in ((181,'先に必要な分',3),(473,'後で必要な分',6)):
        d.add(path(f'M425 369H602V{y+46}H790',stroke=BLUE,sw=4),poly(f'809,{y+46} 787,{y+36} 787,{y+56}',BLUE));d.box(818,y-21,300,134,t,WHITE,BLUE)
        d.text(794,y+115,350,45,'納期に合わせて渡す' if n==3 else '保管して次の納期へ')
    d.text(245,650,720,47,'作る単位と、届ける単位を分けて考える')
    return d.finish('supply/production-delivery-lot-split','製造ロットを納期に合わせて分納する','生産効率のためのロットと、顧客へ届ける単位の違いを説明する。','作る量をまとめても、届ける量と時期は顧客の必要に合わせて分けられる。','分納 製造ロット 出荷ロット 納期 保管 split shipment production lot delivery',['左のまとまりが一つの製造ロット。','右の二つの行き先が異なる納期の受け渡し。','中央の分岐が作る単位と届ける単位の分離。'],'one-production-lot-multiple-deliveries')


def receiving_consolidation():
    d=Drawing();d.box(516,203,238,324,'受入を\nまとめる',PALE,BLUE)
    for y,t in ((178,'便 A'),(347,'便 B'),(516,'便 C')):
        d.box(83,y-47,206,95,t,WHITE,INK);d.add(path(f'M297 {y}H367V361H503',stroke=BLUE,sw=4))
    d.add(arrow(762,361,875,361,BLUE,7,22));d.box(883,289,233,144,'行き先別に\nまとめて渡す',WHITE,INK)
    d.add(line(425,156,425,565,INK,3,'7 7'));d.text(356,73,577,69,'受入時刻・行き先・荷姿をそろえる')
    d.text(376,608,725,61,'到着便ごとではなく、後工程が使う単位へ整える')
    return d.finish('supply/receiving-consolidation','複数の入荷を受け渡す単位へまとめる','物流センターや工場の受入で、到着便と払出単位の違いを説明する。','別々に届く物を、後工程の行き先と必要時刻に合わせてまとめ直す。','共同配送 荷揃え 集約 受入 仕分け クロスドック inbound consolidation cross dock staging',['左の複数便が中央の受入へ集まる。','中央の長い囲みで時刻や行き先をそろえる。','右は便別ではなく、使う単位での受け渡し。'],'multiple-arrivals-to-use-oriented-dispatch')


def delivery_evidence():
    d=Drawing();d.box(80,221,231,213,'出荷側',WHITE,INK);d.box(882,221,237,213,'受入側',WHITE,INK)
    d.add(arrow(321,280,870,280,BLUE,7,22),arrow(870,389,321,389,INK,5,20))
    d.box(427,140,345,88,'物を渡す',PALE,BLUE);d.box(427,443,345,88,'受取の事実を返す',FAINT,INK)
    d.add(path('M194 446V603H997V446',stroke=MID,sw=3));d.text(314,626,574,59,'品目・数量・受取時点を対応させる')
    d.text(383,44,436,65,'出荷と受領を同じ識別でつなぐ')
    return d.finish('supply/delivery-receipt-evidence','物の引渡しと受領の記録を対応させる','出荷・納品・受入の確認で、物と記録のつながりを説明する。','送ったという記録と、受け取ったという記録を同じ対象で照合する。','納品 受領 検収 引渡 証跡 物流 proof delivery receipt shipment',['上の矢印が物の移動、下の逆向き矢印が受領の確認。','下の括りが品目・数量・時点を共通の識別で対応させることを表す。','物の流れと確認情報の方向を分けている。'],'goods-delivery-receipt-confirmation')


def buying_committee():
    d=Drawing();d.add(circle(596,347,119,BLUE));d.text(504,305,184,84,'顧客の\n購入判断','判断',WHITE)
    positions=((214,190,'使う人','使いやすさ'),(979,190,'技術の確認者','仕様・適合'),(214,535,'予算の決裁者','費用・効果'),(979,535,'調達の担当者','条件・供給'))
    for x,y,t,sub in positions:
        ex=x+143 if x<600 else x-143;ey=y+44 if y<300 else y-44
        d.add(arrow(ex,ey,494 if x<600 else 698,304 if y<300 else 390,BLUE,4,16));d.box(x-144,y-52,288,104,t,WHITE,INK);d.text(x-153,y+58,306,57,sub,'判断観点')
    d.text(339,52,520,64,'一人の窓口の先に、異なる判断がある')
    return d.finish('customer/buying-committee','顧客の購入に関わる判断者と観点を見渡す','法人営業で、利用者・技術・予算・調達の関係者を整理する。','同じ購入でも関係者ごとに確認したい内容が異なるため、それぞれの判断を支える。','購買委員会 意思決定者 法人営業 顧客 関係者 buying committee stakeholder B2B purchase',['中央が購入判断、四方が異なる判断を担う関係者。','各枠の下に重視する観点を示す。','内向きの矢印が購入判断への関わりで、全員が同じ決裁権を持つ意味ではない。'],'stakeholder-specific-buying-contributions')


def customer_problem_outcome():
    d=Drawing();d.add(rect(74,226,386,292,FAINT,10),rect(740,226,386,292,PALE,10))
    d.text(124,138,286,64,'顧客が困ること');d.text(790,138,286,64,'顧客が得たい状態')
    d.text(108,280,318,157,'何度も入力する\nミスに気づきにくい\n確認に時間がかかる');d.text(774,280,318,157,'一度で入力が済む\nその場で確認できる\n早く次の作業へ進める')
    d.add(arrow(477,363,720,363,BLUE,10,31));d.text(474,423,250,107,'解決した後の\n行動の変化')
    d.text(239,603,729,61,'機能の名前より先に、顧客の変化を定める')
    return d.finish('customer/problem-to-outcome','困りごとを顧客が得たい状態へ言い換える','商品企画や提案で、解決すべき課題と顧客側の成果を整理する。','自社が何を作るかより先に、顧客の行動や状態がどう変わるかを明確にする。','顧客課題 成果 ニーズ 価値提案 困りごと customer problem outcome jobs value',['左が現状の困りごと、右が実現したい状態。','同じ高さの文章が変化前後の対応。','中央の矢印は製品そのものではなく顧客側の変化。'],'customer-problem-outcome-pairs')


def benefit_evidence():
    d=Drawing();d.add(rect(420,124,373,469,PALE,12));d.text(447,148,319,68,'顧客に起きる良い変化','提供価値')
    d.text(454,284,305,119,'作業を中断せず\n状態を確認できる','顧客の便益')
    d.box(72,266,281,154,'提供する機能\n離れた所から監視',WHITE,INK);d.box(865,266,266,154,'確かめる根拠\n使用場面の試験',WHITE,BLUE)
    d.add(arrow(360,341,411,341,BLUE,5,17),arrow(856,341,804,341,INK,5,17));d.text(139,132,244,76,'何ができるか');d.text(851,132,282,76,'何で裏付けるか')
    d.text(179,627,845,60,'機能・顧客の便益・根拠をつなげて提案する')
    return d.finish('customer/feature-benefit-evidence','機能から顧客の便益を示し、根拠を添える','営業提案で、機能の説明を顧客にとっての価値へ結びつける。','機能がもたらす便益を示し、その説明を試験や事例などの根拠で支える。','機能 便益 根拠 提案 訴求 実証 feature benefit evidence value proposition',['左が提供する機能、中央が顧客に生まれる便益。','右は便益の説明を支える根拠。','二つの矢印が中央の価値説明を支える。'],'feature-and-proof-support-benefit')


def customer_feedback_loop():
    d=Drawing();d.box(63,255,251,151,'顧客の声',WHITE,INK);d.box(474,148,268,123,'原因と背景を整理',PALE,BLUE);d.box(876,255,259,151,'改善して届ける',BLUE,BLUE)
    d.add(path('M319 330H383V210H457',stroke=BLUE,sw=5),poly('476,210 452,199 452,221',BLUE));d.add(path('M748 210H815V330H858',stroke=BLUE,sw=5),poly('877,330 853,319 853,341',BLUE))
    d.add(path('M1005 414V567H189V429',stroke=INK,sw=4),poly('189,408 179,432 199,432',INK));d.box(439,521,342,97,'顧客の結果を確かめる',WHITE,INK)
    d.text(345,50,514,61,'集めて終わらず、改善後の結果まで返す')
    return d.finish('customer/closed-feedback-loop','顧客の声を改善し、結果まで確かめる','顧客フィードバックを商品や業務の改善へつなぐ運用を説明する。','受け取った声を整理して改善し、顧客の困りごとが解消したか確かめる。','顧客の声 VOC フィードバック 改善 満足 customer feedback closed loop improvement',['上の経路が顧客の声から改善まで。','下の戻り線が改善後の顧客の結果確認。','結果確認によって次の声や課題を更新する。'],'customer-feedback-result-loop')


def product_service_envelope():
    d=Drawing();d.add(rect(90,105,1020,516,FAINT,25,INK,3),rect(191,226,818,279,PALE,20,BLUE,3),rect(407,295,387,132,BLUE,12))
    d.text(435,329,331,64,'製品が果たす機能','製品',WHITE);d.text(304,236,595,57,'導入・運用・保全を支えるサービス','支援')
    d.text(194,129,813,61,'顧客が使い続けて成果を得る体験','顧客の成果');d.text(213,542,774,59,'機能だけでなく、使い始めと使い続ける間も設計')
    for x in (241,955):d.add(circle(x,363,21,WHITE,BLUE,3),check(x-12,355,.66,BLUE))
    return d.finish('customer/product-service-envelope','製品の周りに使い続ける支援を設計する','製品販売に導入支援・保守・運用支援を組み合わせる価値を説明する。','製品の機能を中心に、顧客が成果を得るまでの支援を重ねる。','サービス化 導入支援 保守 顧客体験 製品 servitization product service customer success',['中央が製品の機能、その周りがサービス。','一番外側が顧客が成果を得る体験全体。','入れ子は提供範囲の広がりで、金額の内訳ではない。'],'product-service-outcome-envelope')


def installed_base():
    d=Drawing();d.add(circle(600,341,95,INK));d.text(528,303,144,77,'共通の\n支援窓口','支援',WHITE)
    for x,y,t in ((230,170,'導入先 A'),(967,170,'導入先 B'),(230,530,'導入先 C'),(967,530,'導入先 D')):
        d.box(x-140,y-59,280,118,t,WHITE,BLUE)
        xx=490 if x<600 else 710;yy=294 if y<300 else 398
        d.add(arrow(x+(148 if x<600 else -148),y,xx,yy,BLUE,4,15))
    d.add(path('M600 451V601',stroke=MID,sw=3));d.text(426,621,351,59,'使用履歴に応じた点検・提案')
    d.text(354,37,491,62,'納入後も、稼働と支援の履歴をつなぐ')
    return d.finish('customer/installed-base-support','納入した製品の稼働と支援をつなぐ','納入後の保守や更新提案に向け、導入先ごとの情報を共有する。','導入先ごとの稼働・保守履歴を集め、必要な支援や更新につなげる。','納入実績 設置台帳 保守 履歴 アフターサービス installed base service maintenance fleet',['周囲が別々の導入先、中央が共通の支援窓口。','内向きの矢印が導入先ごとの稼働や支援履歴。','下の経路は履歴を点検や提案へ使うことを示す。'],'installed-product-support-network')


def opportunity_qualification():
    d=Drawing();d.add(path('M119 200H1050',stroke=PALE,sw=30))
    for x,t in ((194,'課題が明確'),(549,'実現できる'),(904,'合意できる')):
        d.add(circle(x,200,32,BLUE),check(x-18,188,.96));d.text(x-139,73,278,73,t,'確認する根拠')
        d.add(line(x,234,x,433,MID,3));d.box(x-130,444,260,105,'確認が足りない\n情報を集める',WHITE,INK)
    d.add(arrow(230,200,510,200,BLUE,5,18),arrow(585,200,865,200,BLUE,5,18),arrow(942,200,1120,200,BLUE,5,18))
    d.text(333,305,540,70,'根拠を得て、次の提案へ進む');d.text(266,602,692,60,'未確認を失注と決めず、次に調べる内容を定める')
    return d.finish('customer/opportunity-qualification','商談の確からしさを根拠で確認する','案件会議で、営業の感触だけでなく次の行動につながる確認事項を共有する。','顧客課題・実現性・合意条件の根拠を確認し、足りない情報を次の行動へ変える。','商談 案件 確度 営業 パイプライン 要件 opportunity qualification sales evidence',['上の横方向は根拠を得ながら提案を進める経路。','各確認点から下に、足りない情報を調べる仕事を分ける。','下の枠は失注の出口ではなく未確認の課題。'],'sales-evidence-and-open-questions')


def customer_adoption():
    d=Drawing();d.add(rect(77,127,1046,465,FAINT,15))
    d.add(path('M171 473H316V387H525V291H770V203H1017',stroke=BLUE,sw=15))
    for x,y,t in ((245,473,'試してみる'),(421,387,'使えるようになる'),(647,291,'日常の仕事に使う'),(952,203,'成果を得る')):
        d.add(circle(x,y,20,WHITE,BLUE,3))
        if x==245:d.text(141,516,208,66,t,'利用の状態')
        elif x==421:d.text(338,418,248,66,'使えるように\nなる','利用の状態')
        elif x==647:d.text(560,325,239,66,'日常の仕事に\n使う','利用の状態')
        else:d.text(828,247,248,66,t,'利用の状態')
    d.text(356,48,490,61,'契約後の利用と成果まで支援する');d.text(322,624,594,56,'利用開始は、顧客成果への途中の節目')
    return d.finish('customer/adoption-to-value','使い始めから日常利用と成果へ進める','導入後の支援を、初期設定だけでなく業務定着まで計画する。','利用を始めた状態と、仕事に定着して成果を得た状態を区別する。','定着 活用 導入 顧客成功 カスタマーサクセス adoption activation customer success value',['段差が利用の状態の変化。','左から試用・習得・日常利用・成果へ進む。','高さは成果の数値ではなく、利用が深まる段階。'],'adoption-depth-staircase')


def voice_to_requirement():
    d=Drawing();d.add(path('M73 141H406V336H297L252 391V336H73Z',FAINT,INK,3));d.text(100,183,279,119,'「手間をかけず\n安心して使いたい」','顧客の言葉')
    d.add(arrow(426,237,547,237,BLUE,6,20));d.box(558,148,303,178,'どの場面で\n何が困るかを確認',WHITE,BLUE)
    d.add(path('M864 237H1011V450',stroke=BLUE,sw=5),poly('1011,472 1000,447 1022,447',BLUE))
    d.box(560,483,547,132,'確認できる要求へ\n操作の回数・確認の方法・応答の条件',PALE,BLUE)
    d.text(83,493,345,122,'曖昧な言葉を\n勝手に仕様へ\n置き換えない')
    return d.finish('customer/voice-to-testable-requirement','顧客の言葉を確認できる要求へ変える','顧客インタビューから製品やサービスの要求を整理する。','顧客の言葉の背景を確かめ、使用場面と確認可能な条件へ具体化する。','顧客要求 VOC 要求定義 インタビュー 仕様 voice customer requirements testable needs',['左の吹き出しが顧客の言葉。','右上で使用場面と困りごとを確認する。','右下が観察や試験で確認できる条件としての要求。'],'voice-context-testable-requirement')


def sales_delivery_handoff():
    d=Drawing();d.add(rect(81,163,438,342,FAINT,12),rect(681,163,438,342,PALE,12))
    d.text(119,205,362,63,'提案・契約の担当','営業');d.text(719,205,362,63,'導入・提供の担当','提供')
    d.add(arrow(402,353,790,353,BLUE,6,21),arrow(790,432,402,432,INK,4,18));d.box(429,311,343,83,'約束・条件・背景',WHITE,BLUE)
    d.text(82,550,435,62,'何を約束したかを渡す');d.text(681,550,437,62,'実現条件と不明点を返す')
    d.add(path('M298 609V637H898V609',stroke=INK,sw=3));d.text(359,52,487,69,'顧客との約束を、提供の条件へつなぐ')
    return d.finish('customer/sales-delivery-handoff','営業の約束と提供側の条件を引き継ぐ','契約後の認識違いを減らすため、提案から導入への引継ぎ内容を整理する。','契約内容だけでなく、顧客の背景や前提を渡し、提供側が条件を確認する。','営業引継ぎ 導入 契約 約束 提供 sales delivery handoff commitment onboarding',['左右が提案担当と提供担当。','上の主色の矢印が顧客への約束・条件・背景の引渡し。','下の逆方向の矢印が不明点や実現条件の確認。'],'commercial-operational-handoff')


def cost_structure():
    d=Drawing();d.box(71,275,213,156,'原価の全体',INK,INK)
    d.add(path('M290 353H361V182H451M361 353V518H451',stroke=INK,sw=4));d.box(457,129,235,107,'直接ひも付く',PALE,BLUE);d.box(457,465,235,107,'共通で支える',FAINT,INK)
    for cy,t,yy in ((182,'材料・加工',182),(518,'設備・支援',518)):
        d.add(arrow(700,cy,806,cy,BLUE,4,18));d.box(814,cy-66,307,132,t,WHITE,INK)
    d.text(252,33,741,65,'製品に直接ひも付く費用と、共通の費用を分ける');d.text(750,335,383,82,'配賦の考え方も\n合わせて確認')
    return d.finish('finance/cost-structure','直接原価と共通費用を分けて原価を読む','製品原価の説明で、直接費と共通費の違いを整理する。','原価の全体を、対象に直接ひも付く費用と共通で支える費用へ分ける。','原価 直接費 間接費 配賦 材料 加工 cost structure direct indirect overhead',['左が原価の全体。','上の枝が直接ひも付く費用、下の枝が共通の費用。','右は構成要素の例で、費用比率を表さない。'],'direct-shared-cost-structure')


def working_capital_cycle():
    d=Drawing();d.box(81,256,213,126,'現金',INK,INK);d.box(447,123,307,126,'在庫',PALE,BLUE);d.box(890,256,234,126,'売上債権',WHITE,INK)
    d.add(path('M299 319H353V186H424',stroke=BLUE,sw=5),poly('445,186 421,175 421,197',BLUE));d.add(path('M760 186H824V319H866',stroke=BLUE,sw=5),poly('888,319 864,308 864,330',BLUE))
    d.add(path('M1007 390V563H188V407',stroke=INK,sw=5),poly('188,384 177,410 199,410',INK))
    d.text(103,130,253,62,'材料を購入');d.text(811,130,274,62,'販売して請求');d.text(384,460,440,70,'代金を回収する')
    d.text(263,627,679,55,'支払から回収まで、資金が必要になる')
    return d.finish('finance/working-capital-cycle','購入・在庫・請求・回収の資金循環を見る','運転資金を説明し、在庫や売掛の期間が資金需要につながることを共有する。','販売が成立しても代金を回収するまで資金は戻らず、循環全体を管理する。','運転資金 キャッシュ 在庫 売掛 回収 資金繰り working capital cash conversion inventory receivable',['左の現金が購入で在庫へ変わり、販売で売上債権へ変わる。','下の戻り線が代金回収。','仕入の支払条件などによって必要資金が変わる概念図。'],'cash-inventory-receivable-cycle')


def profit_drivers():
    d=Drawing();d.box(826,268,296,166,'利益',INK,INK)
    d.box(82,113,272,111,'単価と販売量',PALE,BLUE);d.box(82,488,272,111,'使用量と単位費用',FAINT,INK)
    d.box(495,113,226,111,'収益',WHITE,BLUE);d.box(495,488,226,111,'費用',WHITE,INK)
    d.add(arrow(362,169,481,169,BLUE,5,19),arrow(362,543,481,543,INK,5,19))
    d.add(path('M729 169H787V319H813',stroke=BLUE,sw=5),poly('829,319 806,309 806,329',BLUE));d.add(path('M729 543H787V387H812',stroke=INK,sw=5),poly('829,387 806,377 806,397',INK))
    d.add(circle(917,176,28,BLUE),line(902,176,932,176,WHITE,4),line(917,161,917,191,WHITE,4),circle(917,542,28,INK),line(902,542,932,542,WHITE,4))
    d.text(353,309,309,85,'売上の伸びと\n費用の変化を見る');d.text(494,636,616,50,'利益は、収益と費用の両方で変わる')
    return d.finish('finance/profit-drivers','収益と費用の要因から利益を考える','収益改善の会議で、売上拡大と費用改善の両面を整理する。','単価・販売量による収益と、使用量・単位費用による費用の変化を分ける。','利益構造 利益改善 売上 原価 単価 数量 profit drivers revenue cost margin',['上段が収益につながる要因、下段が費用につながる要因。','プラスとマイナスの記号が利益への関係を表す。','実際の数式や数値ではなく要因の分解。'],'revenue-cost-profit-drivers')


def profit_cash_timing():
    d=Drawing();d.text(58,180,262,66,'売上の認識');d.text(58,447,262,66,'現金の動き')
    d.add(arrow(342,216,1124,216,INK,4,18),arrow(342,483,1124,483,INK,4,18))
    d.add(circle(565,216,28,BLUE),circle(963,483,28,INK),line(565,254,565,516,MID,2,'7 7'),line(963,179,963,446,MID,2,'7 7'))
    d.text(410,105,308,65,'提供した時点');d.text(805,542,310,65,'代金を受け取る時点')
    d.add(path('M565 332V351H963V332',stroke=BLUE,sw=4));d.text(605,371,319,65,'時点がずれる')
    d.text(315,631,800,58,'売上があっても、同じ時点に現金が入るとは限らない')
    return d.finish('finance/profit-cash-timing','売上を認識する時点と入金の時点を分ける','損益と資金繰りの違いを、身近な取引の時点で説明する。','取引の成果と代金の受け取りは時点が異なり、両方を確認する必要がある。','損益 現金 キャッシュ 売上 入金 タイミング profit cash accrual collection timing',['上段の点が提供に伴う売上認識の例、下段の点が入金。','縦の破線でそれぞれの時点を対応させる。','認識の条件や支払日は個々の取引で決まる。'],'recognition-versus-cash-timeline')


def fixed_variable_structure():
    d=Drawing();d.add(rect(142,446,915,122,INK,7));d.text(347,478,511,62,'操業量によらず発生する基盤の費用','固定的な費用',WHITE)
    for x,n,t in ((183,1,'少ない操業'),(501,2,'中間の操業'),(819,3,'多い操業')):
        for i in range(n):d.add(rect(x,368-i*75,192,62,PALE,4,BLUE,2))
        d.text(x-35,607,262,65,t)
    d.text(249,42,704,66,'量で増える費用と、維持に必要な費用');d.text(350,130,443,66,'操業量に応じて増える費用')
    return d.finish('finance/fixed-variable-cost','量で変わる費用と基盤を維持する費用を分ける','操業度の変化が原価や利益へどう関わるかを説明する。','仕事量に応じた費用と、仕事量にかかわらず持つ費用を分けて見る。','固定費 変動費 操業度 損益 費用構造 fixed variable cost utilization',['下の共通の帯が固定的な費用。','上の積み重なる帯が操業量とともに変わる費用。','段の数は関係の説明で、金額や厳密な比例関係ではない。'],'fixed-base-variable-workload')


def staged_investment():
    d=Drawing();d.box(80,256,245,140,'小さく確かめる',PALE,BLUE);d.add(arrow(333,325,449,325,BLUE,5,19));d.add(poly('457,325 577,214 697,325 577,436',WHITE,INK,3));d.text(494,284,166,86,'結果を\n評価する','判断')
    for y,t,c in ((154,'広げる',BLUE),(351,'待って確かめる',INK),(548,'ここで止める',GRAY)):
        d.add(path(f'M704 325H770V{y}H872',stroke=c,sw=4),poly(f'894,{y} 870,{y-10} 870,{y+10}',c));d.box(898,y-48,237,96,t,WHITE,c)
    d.text(225,82,523,65,'知見が増えた時点で、次の投資を判断');d.text(149,519,543,88,'最初から全額を固定せず\n判断できる節目を設ける')
    return d.finish('finance/staged-investment-options','検証結果を見て投資を広げる・待つ・止める','不確実性の高い新規事業や設備投資を段階的に判断する。','得られた結果で次の選択を行い、判断の余地を残して投資する。','段階投資 リアルオプション 投資判断 不確実性 撤退 staged investment real options uncertainty',['左で小さく確かめ、中央で結果を評価する。','右の三つの経路が拡大・追加確認・停止の選択肢。','判断の節目を通じて投資の次の範囲を決める。'],'investment-option-branching')


def portfolio_horizons():
    d=Drawing();d.add(rect(82,516,1037,97,INK,7));d.text(334,537,532,55,'現在の事業が全体を支える','現在',WHITE)
    d.add(path('M143 483C195 347 347 350 486 355S777 352 862 225S999 119 1090 109',stroke=PALE,sw=34));d.add(path('M143 483C195 347 347 350 486 355S777 352 862 225S999 119 1090 109',stroke=BLUE,sw=5))
    for x,y,t in ((235,378,'既存を強くする'),(637,351,'次の成長を育てる'),(995,128,'新しい可能性を試す')):
        d.add(circle(x,y,17,WHITE,BLUE,4))
        if x==235:d.text(161,421,290,58,t,'投資の狙い')
        elif x==637:d.text(468,407,338,65,t,'投資の狙い')
        else:d.text(803,300,350,60,t,'投資の狙い')
    d.text(109,62,645,64,'現在の収益と、将来の成長へ配分する');d.text(428,640,676,49,'取り組みごとに期待する成果と判断時点を分ける')
    return d.finish('strategy/business-horizons','現在の事業と次の成長へ取り組みを配分する','事業ポートフォリオで短期の収益と将来の探索の役割を整理する。','既存事業を支えながら、次の成長と新しい可能性を異なる時間軸で育てる。','事業ポートフォリオ 成長 既存 新規 探索 horizon portfolio growth exploration',['下の基盤が現在の事業、上の経路が次の成長へ向かう取り組み。','経路上の三つの点が狙いの異なる活動。','曲線の高さは売上予測ではなく、取り組む時間軸の広がり。'],'current-business-and-future-horizons')


def central_local_balance():
    d=Drawing();d.add(circle(601,352,235,FAINT,INK,3),circle(601,352,116,BLUE));d.text(511,310,180,87,'全体でそろえる\n共通の基準','共通基準',WHITE)
    for x,y,t in ((265,208,'現場 A'),(935,208,'現場 B'),(601,590,'現場 C')):
        d.box(x-128,y-52,256,104,t,WHITE,BLUE)
    d.add(line(399,239,506,301,INK,4),line(803,239,696,301,INK,4),line(601,474,601,526,INK,4))
    d.text(63,451,326,109,'共通基準の内側で\n現場に合う実行');d.text(811,451,326,109,'現場の学びから\n共通基準を更新')
    d.text(261,28,680,66,'全体の一貫性と、現場の適応を両立する')
    return d.finish('strategy/common-standard-local-action','共通の基準と現場ごとの実行を分ける','複数拠点の運営で、統一する内容と現場へ委ねる内容を整理する。','共通の基準を保ちながら、現場の条件に合った実行を可能にする。','本社 現場 分権 集権 標準 裁量 common standard local adaptation autonomy',['中央が全体でそろえる基準、外側が各現場。','つながる線が共通基準に基づく関係。','周囲の余白が現場ごとに具体化する実行の範囲。'],'shared-core-local-execution')


def value_chain_support():
    d=Drawing();d.add(rect(93,111,1011,125,INK,9));d.text(230,143,738,63,'人材・技術・情報・調達が横断して支える','支援活動',WHITE)
    for i,(x,t) in enumerate(((93,'開発'),(300,'調達'),(507,'製造'),(714,'販売'),(921,'保守'))):
        d.add(poly(f'{x},323 {x+166},323 {x+195},400 {x+166},477 {x},477 {x+24},400',PALE,BLUE,2));d.text(x+24,361,140,79,t,'価値を渡す活動');d.add(line(x+96,244,x+96,309,MID,3))
    d.add(arrow(117,557,1092,557,BLUE,6,20));d.text(260,600,685,62,'活動をつなげて、顧客へ価値を届ける')
    return d.finish('strategy/value-chain-support','価値を生む活動と共通の支援を結ぶ','事業の活動を俯瞰し、横断する機能との関係を説明する。','開発から保守までの活動が連携し、人材や情報などの共通機能が全体を支える。','価値連鎖 バリューチェーン 支援活動 事業 活動 value chain primary support activities',['下段の矢形が顧客へ価値を渡す主要活動。','上段の共通の帯が活動全体を支える機能。','短い縦線が各活動と共通支援の接続。'],'primary-value-chain-cross-support')


def strategic_focus():
    d=Drawing();d.add(circle(201,352,89,INK));d.text(136,312,130,81,'限りある\n資源','資源',WHITE)
    d.add(path('M298 351H424',stroke=INK,sw=6),circle(438,351,13,WHITE,INK,3))
    d.add(path('M454 343C601 251 614 216 721 216H961',stroke=BLUE,sw=15),poly('998,216 962,196 962,236',BLUE))
    d.add(path('M455 360C590 442 660 467 853 467',stroke=MID,sw=4),line(852,443,852,491,INK,5))
    d.text(580,101,487,77,'重点へ厚く配分');d.text(604,508,441,66,'今は優先しない範囲')
    d.text(213,611,802,60,'何を強めるかと、何を後にするかを一緒に決める')
    return d.finish('strategy/focus-and-tradeoffs','重点と後にする範囲を同時に決める','戦略の優先順位を資源配分に結びつけ、選択の意味を説明する。','すべてを同じ強さで進めず、重点と見送る範囲を明確にする。','戦略 集中 選択 トレードオフ 資源 優先 strategy focus tradeoffs resource priority',['左が限りある資源。','太い主色の経路が重点への配分、止め線のある細い経路が今は優先しない範囲。','太さは重点の違いを示す概念表現。'],'resource-focus-with-deferred-scope')


def skill_development():
    d=Drawing();d.add(rect(84,501,1023,94,INK,6));d.text(279,522,632,54,'実際の仕事で、できたことを確かめる','実践',WHITE)
    for x,y,t in ((81,320,'説明を受ける'),(450,240,'支援を受けて行う'),(821,160,'一人で行い\n教えられる')):
        d.add(rect(x,y,294,106,PALE,8,BLUE,3));d.text(x+15,y+14,264,78,t,'技能の状態');d.add(line(x+147,y+114,x+147,487,BLUE,3))
    d.add(arrow(382,355,442,302,BLUE,4,16),arrow(752,275,813,222,BLUE,4,16));d.text(154,50,545,60,'知っている状態と、できる状態を分ける')
    d.text(263,630,669,56,'受講の有無だけでなく、実践での到達を確認')
    return d.finish('people/skill-development','知識の習得から自立した実践へ技能を育てる','研修や技能育成の計画で、受講と仕事での到達度の違いを説明する。','説明を受けたことを出発点に、支援付きの実践から自立した実践へ進める。','技能育成 研修 習得 OJT 自立 到達 skill development learning proficiency training',['三つの高さの枠が技能の状態。','各枠から共通の実践の帯へつなぎ、仕事で確認する。','高さは点数ではなく自立の段階。'],'knowledge-supported-independent-practice')


def delegation_boundary():
    d=Drawing();d.add(rect(100,165,696,393,PALE,18,BLUE,3));d.text(165,188,566,64,'担当者へ委ねた判断の範囲','委譲範囲')
    d.dot(353,386,'担当者',76,WHITE);d.add(path('M437 386H583V324H676',stroke=BLUE,sw=5),poly('697,324 673,313 673,335',BLUE));d.text(486,269,272,50,'範囲内で進める')
    d.add(path('M438 425H611V478H853',stroke=INK,sw=4),poly('875,478 849,466 849,490',INK));d.box(877,405,236,145,'上位者へ\n相談・判断',WHITE,INK)
    d.text(583,599,529,66,'範囲を超える条件は、先に合意');d.text(294,63,647,60,'任せる内容と、相談する境界を明確にする')
    return d.finish('people/delegation-boundary','委ねる判断の範囲と相談する境界を決める','権限委譲で、担当者が判断してよい範囲と相談条件を整理する。','すべてを上位者へ戻さず、合意した範囲は担当者が判断し、境界を超える場合に相談する。','権限委譲 裁量 相談 判断 責任 delegation authority decision boundary escalation',['囲みの内側が委ねられた判断の範囲。','囲み内の主色の経路が担当者の判断。','囲みを出る経路が合意した相談・上位判断への引継ぎ。'],'delegated-decision-envelope')


def knowledge_handover():
    d=Drawing();d.add(rect(85,147,1018,128,FAINT,9),rect(85,461,1018,128,PALE,9))
    d.text(111,181,251,59,'経験を持つ人','伝える側');d.text(849,495,233,59,'引き継ぐ人','受け取る側')
    d.add(path('M356 211H462V383H637V523H832',stroke=BLUE,sw=7),poly('853,523 827,511 827,535',BLUE))
    d.add(rect(365,309,450,111,WHITE,12,INK,3));d.text(389,332,402,66,'一緒に行い、判断理由を言葉にする','共同実践')
    d.text(574,165,444,79,'手順にない気づき・例外の判断');d.text(96,495,410,63,'再現して、不明点を確かめる')
    d.add(path('M837 603V663H52V211H64',stroke=INK,sw=3),poly('85,211 63,201 63,221',INK));d.text(455,600,420,51,'できたかを双方で確認')
    return d.finish('people/knowledge-handover','共同実践で判断理由まで引き継ぐ','業務の引継ぎや熟練技能の継承で、文書にない判断を共有する。','手順書を渡すだけでなく、一緒に実践し判断の理由と例外への対応を確かめる。','技能伝承 暗黙知 引継ぎ 熟練 ナレッジ knowledge transfer tacit handover mentoring',['上段が経験を持つ側、下段が引き継ぐ側。','中央の共同行為が判断理由を言葉にする場。','下の戻り線で受け手が再現できたかを確認する。'],'joint-practice-knowledge-transfer')


def coaching_dialogue():
    d=Drawing();d.dot(219,329,'本人',92,PALE);d.dot(972,329,'支援者',92,WHITE)
    d.add(arrow(327,293,858,293,BLUE,5,20),arrow(858,369,327,369,INK,5,20))
    d.text(401,187,392,65,'経験と考えを話す');d.text(401,402,392,65,'問いかけて整理を助ける')
    d.box(439,533,323,111,'次の行動を本人が決める',BLUE,BLUE)
    d.add(path('M219 431V590H415',stroke=BLUE,sw=4),poly('440,590 413,578 413,602',BLUE));d.text(274,53,656,60,'答えを渡す前に、本人の考えを引き出す')
    return d.finish('people/coaching-dialogue','対話で経験を整理し、次の行動を決める','育成面談や振り返りで、支援者の役割と本人の主体性を説明する。','本人が経験を言葉にし、支援者の問いかけを通して次の行動を考える。','コーチング 面談 問いかけ 振り返り 主体性 coaching dialogue reflection development',['二本の逆向き矢印が、本人の共有と支援者の問いかけ。','下の行動は本人側からつながる。','支援者が一方的に指示する図ではなく、対話による整理を表す。'],'reflection-dialogue-owned-action')


def succession_coverage():
    d=Drawing();d.text(78,72,355,65,'継続が必要な役割');d.text(729,72,381,65,'引き継げる人の準備')
    for y,t in ((206,'重要な役割 A'),(424,'重要な役割 B')):d.box(85,y-62,327,124,t,INK,INK)
    for x,y,t in ((883,181,'候補者 1'),(883,367,'候補者 2')):d.box(x-147,y-51,294,102,t,PALE,BLUE)
    d.add(path('M420 206H616V181H727M616 206V367H727',stroke=BLUE,sw=4));d.add(path('M420 424H600V563H727',stroke=AMBER,sw=4))
    d.add(rect(736,510,294,106,WHITE,9,AMBER,3));d.text(757,530,252,66,'引継ぎ候補が不足','不足')
    d.text(95,566,517,74,'一人に依存する役割を先に見つける')
    return d.finish('people/succession-coverage','重要な役割と引き継げる人の不足を見つける','後継者計画や業務継続の検討で、特定の人への依存を整理する。','重要な役割ごとに引き継げる人を対応させ、準備が必要な空白を見つける。','後継者 属人化 継承 要員 業務継続 succession coverage key person dependency',['左が継続すべき役割、右が引き継げる候補。','上の分岐は複数候補を持つ役割。','下の注意色の空白が候補や準備の不足。'],'critical-role-successor-coverage')


def hierarchy_controls():
    d=Drawing()
    levels=((70,1070,'危険そのものをなくす',INK),(181,890,'危険の小さいものへ替える',BLUE),(292,710,'設備・構造で隔てる',MID),(403,530,'手順・教育で管理する',PALE),(514,350,'保護具を使う',FAINT))
    for y,w,t,c in levels:
        x=(1200-w)/2;d.add(poly(f'{x},{y} {x+w},{y} {x+w-75},{y+91} {x+75},{y+91}',c,INK,2));d.text(x+89,y+17,w-178,58,t,'対策の種類',WHITE if c in (INK,BLUE) else INK)
    d.text(82,613,1040,60,'上位の対策から検討し、必要な層を組み合わせる')
    return d.finish('safety/hierarchy-of-controls','危険をなくす対策から優先して検討する','安全対策で、除去・代替・工学的対策・管理的対策・保護具の違いを説明する。','人の注意だけに頼らず、危険そのものや接触する仕組みから対策を考える。','リスク低減 危険源 除去 代替 工学 管理 保護具 hierarchy controls elimination substitution engineering PPE',['上から危険の除去、代替、設備・構造、手順・教育、保護具。','幅は対策の優先的な検討順を示す概念表現。','必要な対策を複数重ねて、残るリスクも確認する。'],'hierarchy-of-risk-controls')


def bowtie_risk():
    d=Drawing();d.add(circle(600,352,87,AMBER));d.text(536,310,128,87,'制御を\n失う事象','中心事象',WHITE)
    for y in (169,352,535):
        d.add(line(272,y,501,352,INK,4),line(699,352,928,y,INK,4));d.add(rect(345,y+(352-y)*.37-40,16,80,BLUE,3),rect(831,352+(y-352)*.58-40,16,80,BLUE,3))
    for y,t,u in ((169,'原因 A','影響 A'),(352,'原因 B','影響 B'),(535,'原因 C','影響 C')):
        d.box(69,y-48,203,96,t,WHITE,INK);d.box(929,y-48,203,96,u,WHITE,INK)
    d.text(252,33,291,64,'起こさないための壁');d.text(674,33,306,64,'影響を抑えるための壁');d.text(307,620,587,60,'原因側の予防と、影響側の低減を分ける')
    return d.finish('safety/bowtie-barriers','事故の原因側と影響側に対策を置く','重要なリスクについて、発生を防ぐ対策と被害を抑える対策を整理する。','中心となる事象の前後で、予防の壁と影響を抑える壁の役割を分ける。','ボウタイ分析 リスク 危険源 バリア 予防 緩和 bowtie risk barriers prevention mitigation',['左の枝が中心事象に至る原因、右の枝が生じる影響。','原因側の短い縦の壁が予防策、影響側の壁が低減策。','同じ位置の壁が各経路に効くという概念構造を示す。'],'threat-event-consequence-barriers')


def near_miss_learning():
    d=Drawing();d.box(64,211,281,181,'事故には至らなかった\n危険な出来事',WHITE,AMBER)
    d.add(arrow(352,301,469,301,BLUE,5,20));d.box(478,221,265,161,'起きた条件を共有',PALE,BLUE)
    d.add(arrow(752,301,861,301,BLUE,5,20));d.box(868,211,270,181,'作業と仕組みを\n変える',BLUE,BLUE)
    d.add(path('M1003 402V562H206V414',stroke=INK,sw=4),poly('206,394 196,416 216,416',INK));d.text(322,590,555,66,'同じ危険が残っていないか確かめる')
    d.text(219,87,782,65,'小さな兆候を、事故を防ぐ学びへ変える');d.text(416,446,392,62,'報告した件数で終わらせない')
    return d.finish('safety/near-miss-learning','ヒヤリとした出来事を仕組みの改善へ変える','ヒヤリハット報告を、安全な作業条件の改善へつなぐ。','事故に至らなかった出来事の条件を共有し、同じ危険を減らしたか確認する。','ヒヤリハット 未然防止 危険 報告 学習 near miss safety learning incident prevention',['左が事故に至らなかった出来事。','中央で起きた条件を共有し、右で作業や仕組みを改善する。','戻り線が危険の残りを再確認する。'],'near-miss-condition-change-verification')


def material_recovery_routes():
    d=Drawing();d.box(81,248,239,165,'使用した製品',WHITE,INK);d.add(arrow(330,330,439,330,BLUE,5,18));d.dot(521,330,'状態を\n確かめる',75,PALE)
    for y,t in ((159,'そのまま再使用'),(352,'修理して再使用'),(545,'材料として回収')):
        d.add(path(f'M604 330H710V{y}H833',stroke=BLUE,sw=4),poly(f'851,{y} 830,{y-9} 830,{y+9}',BLUE));d.box(856,y-49,281,98,t,WHITE,BLUE)
    d.text(96,535,515,91,'状態に応じて、保つ価値が\n高い回収経路を選ぶ');d.text(281,38,639,64,'回収した物を、同じ方法で扱わない')
    return d.finish('environment/material-recovery-routes','状態に合わせて再使用・修理・材料回収へ分ける','資源循環の説明で、回収後の利用方法の違いを整理する。','回収物の状態を確かめ、製品として使うか、修理するか、材料として生かすかを選ぶ。','循環 再使用 リユース 修理 リサイクル 資源 circularity reuse repair material recovery',['左が回収する使用済み製品、中央が状態確認。','右の枝が異なる価値の保ち方。','分岐は状態や条件による選択で、回収量の比率ではない。'],'condition-based-circular-routes')


def energy_boundary():
    d=Drawing();d.add(rect(362,154,558,403,FAINT,17,INK,3));d.text(482,175,313,64,'対象とする工程','対象範囲')
    d.add(arrow(80,354,346,354,BLUE,11,30));d.text(59,252,287,70,'投入するエネルギー')
    d.add(arrow(931,290,1117,290,BLUE,11,27));d.text(910,180,237,68,'仕事に使う分')
    d.add(path('M637 384V575H1007',stroke=AMBER,sw=9),poly('1040,575 1005,559 1005,591',AMBER));d.text(867,599,267,59,'外へ逃げる分')
    d.add(rect(443,300,389,137,WHITE,10,BLUE,3));d.text(470,330,334,73,'変換・加工・移動')
    d.text(147,627,660,56,'同じ対象範囲で、投入と有効利用と損失を見る')
    return d.finish('environment/energy-use-boundary','工程へ入るエネルギーと有効利用・損失を分ける','省エネルギーの検討で、対象範囲とエネルギーの行き先を整理する。','対象範囲をそろえ、入るエネルギーが仕事と損失へどう分かれるかを見る。','省エネ エネルギー 熱損失 境界 有効利用 energy balance boundary useful work loss',['囲みが対象工程、左からが投入。','右上が仕事に使う分、右下が外へ逃げる分。','矢印は行き先を示す概念図で、流量の比率を表さない。'],'energy-input-use-loss-boundary')


def transformation_lineage():
    d=Drawing();d.box(70,140,250,113,'元データ A',WHITE,INK);d.box(70,433,250,113,'元データ B',WHITE,INK)
    d.add(path('M327 196H404V320H478M327 489H404V371H478',stroke=BLUE,sw=4));d.box(485,271,260,150,'結合・変換',PALE,BLUE)
    d.add(arrow(753,346,862,346,BLUE,5,19));d.box(870,271,263,150,'派生したデータ',BLUE,BLUE)
    d.add(path('M1000 434V628H195V565',stroke=INK,sw=3,extra='stroke-dasharray="8 7"'),poly('195,546 187,567 203,567',INK));d.text(366,579,640,57,'出所と変換内容をたどれるように残す')
    d.text(344,73,727,64,'完成したデータだけでなく、作られた経路も管理')
    return d.finish('data/transformation-lineage','データの出所と変換をたどる','分析結果の確認や修正影響の調査で、派生データの来歴を説明する。','データの出所と変換処理を記録し、結果から元へたどれるようにする。','データリネージ 来歴 変換 結合 派生 追跡 data lineage transformation provenance',['二つの元データが結合・変換を通り派生データになる。','下の破線が来歴をたどる参照関係。','元の値を保持するだけでなく、どう変換したかも対応させる。'],'source-transform-derived-lineage')


def master_data():
    d=Drawing();d.add(rect(473,231,254,249,INK,11));d.text(495,278,210,135,'共通の識別\n名称・属性\n更新の基準','共通マスター',WHITE)
    for x,y,t in ((197,156,'設計で使う'),(1001,156,'調達で使う'),(197,552,'製造で使う'),(1001,552,'販売で使う')):
        d.box(x-140,y-50,280,100,t,WHITE,BLUE)
        d.add(arrow(463 if x<600 else 737,289 if y<300 else 423,x+147 if x<600 else x-147,y,BLUE,4,17))
    d.text(318,39,576,64,'同じ対象を、部門ごとに別の名前で増やさない');d.text(385,604,431,59,'共通の識別で各業務をつなぐ')
    return d.finish('data/shared-master-data','共通の識別と属性を部門横断で使う','製品・部品・取引先などのマスターデータが担う役割を説明する。','同じ対象を共通の識別と属性で扱い、部門間の対応違いを減らす。','マスターデータ MDM 品番 共通ID 属性 整合 master data shared identifier consistency',['中央が共通の識別・属性と更新基準。','周囲がその情報を使う異なる業務。','外向きの矢印が共通定義の利用で、業務データすべての一元保存を意味しない。'],'shared-identity-multiple-business-uses')


def command_event():
    d=Drawing();d.box(69,238,227,138,'依頼する側',WHITE,INK);d.box(468,238,265,138,'実行する側',PALE,BLUE)
    d.add(arrow(305,307,458,307,BLUE,5,18));d.text(302,202,171,64,'実行を依頼','命令')
    d.add(path('M606 386V517H836V206H947',stroke=INK,sw=4));d.add(path('M836 352H947M836 517H947',stroke=INK,sw=4))
    for y,t in ((206,'在庫を更新'),(352,'記録する'),(517,'知らせる')):
        d.add(poly(f'960,{y} 940,{y-9} 940,{y+9}',INK));d.box(969,y-46,173,92,t,WHITE,INK)
    d.text(498,547,318,80,'起きた事実を通知','イベント');d.text(193,78,813,65,'依頼は実行先へ、事実は関心のある相手へ')
    return d.finish('data/command-and-event','実行の依頼と起きた事実の通知を分ける','システム連携で、処理を頼むメッセージと結果を通知するメッセージを説明する。','命令は実行してほしい相手へ渡し、イベントは起きた事実として複数の処理へ共有する。','コマンド イベント 通知 疎結合 連携 command event publish subscribe integration',['左から中央への矢印が実行の依頼。','中央から下を経由する枝が実行後に起きた事実の通知。','右の複数の受け手がそれぞれ事実を利用する。'],'directed-command-fanout-event')


def read_write_models():
    d=Drawing();d.box(76,160,255,146,'変更する操作',WHITE,INK);d.box(76,456,255,146,'見る操作',WHITE,INK)
    d.box(521,160,279,146,'更新用の記録',BLUE,BLUE);d.box(521,456,279,146,'表示用のデータ',PALE,BLUE)
    d.add(arrow(340,232,509,232,BLUE,5,20),arrow(340,528,509,528,INK,5,20))
    d.add(path('M811 234H1148V528H831',stroke=BLUE,sw=5),poly('806,528 833,516 833,540',BLUE));d.text(850,334,266,95,'変更を反映して\n表示を更新')
    d.text(181,50,837,66,'更新と参照で、扱いやすい形を分ける');d.text(318,635,674,54,'反映のタイミングと、最新性を確認する')
    return d.finish('data/read-write-separation','更新する記録と読みやすい表示を分ける','業務データの更新と参照を分けたシステム構成を説明する。','変更の記録を保持し、参照に適した形へ反映することで役割を分ける。','CQRS 参照 更新 データモデル 最新性 read write model projection consistency',['上段が変更を記録する経路、下段が表示を参照する経路。','右の折れた矢印が更新を表示へ反映する関係。','分離したため、表示へ反映する時点も確認する。'],'write-model-read-projection')


def retention_lifecycle():
    d=Drawing();d.add(arrow(98,559,1111,559,INK,4,18))
    for x,w,t,c in ((93,356,'業務で利用する',BLUE),(469,307,'必要な期間保管',PALE),(796,313,'見直して処分',FAINT)):
        d.add(rect(x,222,w,252,c,10,INK,2));d.text(x+26,289,w-52,92,t,'情報の状態',WHITE if c==BLUE else INK)
    d.add(line(459,179,459,591,INK,3,'7 7'),line(786,179,786,591,INK,3,'7 7'))
    d.text(171,68,864,70,'情報の利用目的と、保管する期間を一緒に決める');d.text(311,610,612,62,'必要性・定めた期間・例外を確認して判断')
    return d.finish('data/retention-lifecycle','利用・保管・処分を情報のライフサイクルで考える','文書やデータの整理で、利用目的と保管の終了条件を共有する。','作成時から利用と保管の目的を定め、必要性と適用条件を確認して処分する。','保存期間 保管 廃棄 ライフサイクル 文書情報 retention lifecycle archive disposal',['左から利用中・保管・見直しと処分の状態。','縦の境界が状態を切り替える確認点。','図は年数を指定せず、適用される条件に基づき管理する構造を表す。'],'information-use-retain-review-dispose')


def data_ownership():
    d=Drawing();d.box(469,247,269,174,'業務で使う\n共通データ',BLUE,BLUE)
    d.box(73,88,289,128,'業務責任者\n意味と利用目的',WHITE,INK);d.box(835,88,289,128,'管理担当\n品質と定義',WHITE,INK);d.box(443,535,325,127,'技術担当\n保存・接続・保護',PALE,BLUE)
    d.add(arrow(313,222,456,293,INK,4,18),arrow(884,222,752,293,INK,4,18),arrow(605,520,605,436,BLUE,4,18))
    d.text(314,17,567,59,'責任・管理・技術を一人の曖昧な担当にしない');d.text(56,476,323,114,'何を決める役割かを\n具体的に分ける')
    return d.finish('data/ownership-stewardship','データの業務責任・品質管理・技術を分担する','データガバナンスの体制づくりで、担当の役割を明確にする。','データの意味と目的、品質と定義、技術的な実装を分けて責任を持つ。','データオーナー スチュワード 責任 品質 ガバナンス data ownership stewardship governance custodian',['中央が共通データ、周囲が異なる責任を持つ役割。','矢印が各役割による管理や支援。','枠の中に何を決めるかを添え、肩書だけの分類を避ける。'],'business-steward-technical-responsibility')


def defense_layers():
    d=Drawing();d.add(rect(227,91,877,547,FAINT,21,INK,3),rect(432,211,635,383,PALE,17,BLUE,3),rect(669,336,342,216,WHITE,14,INK,3))
    d.text(290,124,679,62,'接続を認証する','外側');d.text(471,246,539,62,'操作ごとの権限を確かめる','中間');d.text(694,376,291,88,'重要な情報を\n記録・監視する','内側')
    d.add(arrow(56,504,188,504,BLUE,5,18),line(228,480,228,528,INK,8),line(432,480,432,528,BLUE,8),line(669,480,669,528,INK,8))
    d.add(path('M258 504H397M460 504H634M697 504H962',stroke=BLUE,sw=4));d.text(299,655,731,47,'一つの対策が破られても、次の層で確かめる')
    return d.finish('data/defense-in-depth','認証・権限・監視を重ねて情報を守る','情報セキュリティの多層防御を、役割の異なる確認として説明する。','一つの入口だけに依存せず、接続・操作・情報利用の各段階で守る。','多層防御 認証 認可 権限 監視 情報保護 defense depth authentication authorization monitoring',['外側から認証・操作権限・情報の記録と監視。','下の経路は複数の層を通るアクセス。','入れ子は防御の重なりで、同じ確認を三回繰り返す意味ではない。'],'layered-authentication-authorization-monitoring')


def ai_confidence_escalation():
    d=Drawing();d.box(63,271,244,139,'AI の提案',PALE,BLUE);d.add(arrow(315,341,432,341,BLUE,5,20));d.add(poly('440,341 565,212 690,341 565,470',WHITE,INK,3));d.text(479,296,172,92,'条件を\n満たすか','確認')
    d.add(path('M697 341H774V185H875',stroke=BLUE,sw=5),poly('895,185 871,174 871,196',BLUE));d.box(899,130,234,110,'決めた範囲で利用',WHITE,BLUE)
    d.add(path('M567 474V554H875',stroke=INK,sw=5),poly('895,554 871,543 871,565',INK));d.box(899,492,234,124,'人が確認して\n判断する',WHITE,INK)
    d.text(188,28,817,64,'根拠・影響・適用条件に応じて確認先を分ける');d.text(681,119,191,55,'条件を満たす');d.text(600,453,246,56,'未確認・例外');d.text(116,505,376,103,'未確認や例外を\n見える形で渡す')
    return d.finish('data/ai-exception-review','AIの適用条件から人の確認が必要な例外を分ける','AIを業務へ組み込む際、通常の適用範囲と人が判断する範囲を整理する。','根拠と影響を踏まえた条件を設け、未確認や例外を人の判断へ渡す。','AI 人の確認 例外判断 適用条件 根拠 human review AI escalation exception confidence',['左のAI提案を中央で決めた適用条件と照合。','上が条件内の利用、下が人の確認。','数値の信頼度だけでなく、根拠と影響を条件に含める。'],'ai-conditions-exception-human-review')


def forecast_actual_feedback():
    d=Drawing();d.box(63,243,229,145,'過去と現在の\n情報',WHITE,INK);d.box(488,243,259,145,'予測する',BLUE,BLUE);d.box(917,243,218,145,'判断に使う',WHITE,INK)
    d.add(arrow(301,315,475,315,BLUE,5,20),arrow(756,315,903,315,BLUE,5,20))
    d.add(path('M1026 397V576H617V410',stroke=INK,sw=4),poly('617,389 607,413 627,413',INK));d.box(747,526,251,98,'実績と照合',PALE,BLUE)
    d.text(427,52,636,73,'予測を出した後に、外れ方を確かめる');d.text(126,497,514,128,'変化した条件と、予測の偏りを\n次の更新へ反映する')
    return d.finish('data/forecast-actual-feedback','予測を実績と照合して更新する','需要や保全の予測モデルを使う際、利用後の確認と更新を説明する。','予測の出力だけで終わらず、実績との違いと条件の変化を次の更新へ返す。','予測 実績 照合 モデル更新 精度 偏り forecast actual feedback model monitoring',['上段が情報から予測、判断への流れ。','右下で実績と予測を照合する。','戻り線が外れ方と環境変化を予測の更新へ渡す。'],'forecast-outcome-monitoring-loop')


def evidence_chain():
    d=Drawing();d.add(rect(81,155,309,327,FAINT,11),rect(813,155,309,327,PALE,11))
    d.text(105,187,261,67,'確認できた事実');d.text(837,187,261,67,'説明する結論')
    for y in (302,380):d.add(rect(131,y,210,38,WHITE,3,INK,2),line(152,y+18,320,y+18,MID,3))
    d.add(arrow(400,334,798,334,BLUE,7,21));d.box(463,271,278,126,'なぜつながるか\n推論を明示',WHITE,BLUE)
    d.text(844,308,247,82,'主張することを\n根拠と対応');d.add(path('M234 492V608H972V492',stroke=INK,sw=3))
    d.text(236,625,730,57,'事実・仮定・推論を分けて、後から確かめられる')
    return d.finish('data/evidence-to-claim','根拠と結論の間にある推論を明らかにする','報告やAIの回答を確認する際、事実から結論までのつながりを説明する。','根拠を添えるだけでなく、その事実から結論を導く理由を明らかにする。','根拠 結論 主張 推論 説明可能性 検証 evidence claim reasoning argument traceability',['左が確認できた事実、右が説明する結論。','中央が事実と結論をつなぐ推論。','下の括りは事実・仮定・推論を区別して確認することを示す。'],'evidence-reasoning-claim')


def make_assets():
    return [
        requirements_traceability(),tolerance_chain(),design_space(),experiment_factors(),platform_variants(),
        technology_readiness(),prototype_learning(),design_freeze(),make_buy_decision(),test_coverage(),
        fishbone_causes(),cause_verification(),defect_propagation(),prevention_detection(),lot_sampling(),
        lot_genealogy(),measurement_variation(),calibration_chain(),control_plan(),corrective_preventive(),
        takt_alignment(),kanban_pull(),wip_limit(),setup_separation(),maintenance_window(),
        equipment_loss_layers(),line_work_balance(),constraint_buffer(),batch_piece_flow(),capacity_skills(),
        reorder_trigger(),dual_sourcing(),postponement(),demand_decoupling(),milk_run(),
        supplier_segmentation(),bullwhip_orders(),split_delivery(),receiving_consolidation(),delivery_evidence(),
        buying_committee(),customer_problem_outcome(),benefit_evidence(),customer_feedback_loop(),product_service_envelope(),
        installed_base(),opportunity_qualification(),customer_adoption(),voice_to_requirement(),sales_delivery_handoff(),
        cost_structure(),working_capital_cycle(),profit_drivers(),profit_cash_timing(),fixed_variable_structure(),
        staged_investment(),portfolio_horizons(),central_local_balance(),value_chain_support(),strategic_focus(),
        skill_development(),delegation_boundary(),knowledge_handover(),coaching_dialogue(),succession_coverage(),
        hierarchy_controls(),bowtie_risk(),near_miss_learning(),material_recovery_routes(),energy_boundary(),
        transformation_lineage(),master_data(),command_event(),read_write_models(),retention_lifecycle(),
        data_ownership(),defense_layers(),ai_confidence_escalation(),forecast_actual_feedback(),evidence_chain(),
    ]
