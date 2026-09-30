"""Original, text-free cycle and framework diagrams for business presentations."""
from math import cos, sin, radians, sqrt
from vector import (
    INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER,
    path, rect, circle, line, poly, arrow, check, slot, asset,
)


CATEGORY = '09-循環とフレームワーク'


def _item(name, title, description, keywords, body, labels, guidance):
    item = asset(name, CATEGORY, title, description, keywords, body, labels)
    item['kind'] = 'diagram'
    item['guidance'] = guidance
    return item


def _point(cx, cy, radius, angle):
    return (round(cx + radius*cos(radians(angle)), 4),
            round(cy + radius*sin(radians(angle)), 4))


def _annular_arrow(cx, cy, outer, inner, start, body_end, tip_advance, color):
    p = _point(cx, cy, outer, start)
    q = _point(cx, cy, outer, body_end)
    outer_shoulder = _point(cx, cy, outer+16, body_end)
    inner_shoulder = _point(cx, cy, inner-16, body_end)
    centre = _point(cx, cy, (outer+inner)/2, body_end)
    t = (round(centre[0]-sin(radians(body_end))*tip_advance,4),
         round(centre[1]+cos(radians(body_end))*tip_advance,4))
    r = _point(cx, cy, inner, body_end)
    s = _point(cx, cy, inner, start)
    return path(f'M{p[0]} {p[1]}A{outer} {outer} 0 0 1 {q[0]} {q[1]}'
                f'L{outer_shoulder[0]} {outer_shoulder[1]}L{t[0]} {t[1]}'
                f'L{inner_shoulder[0]} {inner_shoulder[1]}L{r[0]} {r[1]}'
                f'A{inner} {inner} 0 0 0 {s[0]} {s[1]}Z', color)


def pdca_cycle():
    b = ''
    for start,color in ((-127,BLUE),(-37,INK),(53,MID),(143,PALE)):
        b += _annular_arrow(600,360,245,145,start,start+55,99,color)
    b += line(600,115,600,97,INK,2.5)+line(845,360,900,360,INK,2.5)
    b += line(600,605,600,623,INK,2.5)+line(355,360,327,360,INK,2.5)
    labels = [
        slot(527,137,82,62,'計画','計画',color=WHITE),
        slot(751,297,82,62,'実行','実行',color=WHITE),
        slot(591,521,82,62,'評価','評価'),
        slot(367,361,82,62,'改善','改善'),
        slot(432,32,336,52,'目標と手順を決める','計画の内容'),
        slot(922,313,234,94,'計画したことを\n実行','実行の内容'),
        slot(432,636,336,52,'結果を基準と比べる','評価の内容'),
        slot(46,313,257,94,'結果を\n次の計画へ','改善の内容'),
        slot(490,313,220,94,'品質を高める','目的'),
    ]
    return _item('継続改善_計画と実行と評価と改善を回す_4段階PDCA',
        '計画・実行・評価・改善を回す','四つの活動を繰り返し、改善を次の計画へ反映する。',
        'PDCA 計画 実行 評価 改善 継続改善 サイクル 品質 cycle', b, labels,
        dict(use_case='業務や品質改善を継続して進める基本サイクルを共有する。',
             message='評価と改善を次の計画へつなぎ、同じ仕事の質を高める。',
             reading=['四つの帯が計画・実行・評価・改善。','矢印の向きに沿って時計回りに繰り返す。','中央の領域は、継続して改善する対象を表す。', '四つの帯は計画・実行・評価・改善の種類を区別する。']))


def learning_cycle():
    outgoing = 'M676 214C750 257 799 323 829 393'
    returning = 'M364 414C407 330 461 263 506 226'
    b = path(outgoing,stroke=PALE,sw=32)+line(768,495,430,495,PALE,32)+path(returning,stroke=PALE,sw=32)
    b += path(outgoing,stroke=BLUE,sw=5)+arrow(829,393,837,413,BLUE,5,20)
    b += arrow(768,495,430,495,BLUE,5,24)
    b += path(returning,stroke=BLUE,sw=5)+arrow(506,226,524,214,BLUE,5,20)
    b += circle(600,170,88,WHITE,INK,3)
    b += circle(870,495,88,BLUE)
    b += circle(330,495,88,PALE,BLUE,3)
    return _item('学習改善_気づきから小さな実験を繰り返す_3段階学習サイクル',
        '気づきから小さな実験を繰り返す','気づき・実験・学習を往復し、改善の確からしさを高める。',
        '学習 実験 気づき 検証 振り返り 仮説 継続改善 learning iteration', b,
        [slot(532,123,136,94,'変化に\n気づく','気づき'),slot(802,448,136,94,'小さく\n試す','実験',color=WHITE),
         slot(262,448,136,94,'結果から\n学ぶ','学習'),slot(467,333,266,92,'学びを次の実験へ','目的')],
        dict(use_case='業務改善のアイデアを小さく試し、結果から次の手を考える。',
             message='一度で答えを決めず、気づき・実験・学習を繰り返す。',
             reading=['上の丸が変化や課題への気づき。','右下で小さく試し、左下で結果から学ぶ。','戻りの矢印が次の気づきにつながる。']))


def two_set_overlap():
    radius = 235
    height = sqrt(radius*radius-150*150)
    top,bottom = 365-height,365+height
    lens = f'M600 {top:.5f}A235 235 0 0 1 600 {bottom:.5f}A235 235 0 0 1 600 {top:.5f}Z'
    b = circle(450,365,radius,FAINT)+circle(750,365,radius,PALE)
    b += path(lens,BLUE)
    b += circle(450,365,radius,'none',INK,3)+circle(750,365,radius,'none',BLUE,3)
    return _item('価値提案_顧客の期待と自社の強みを重ねる_2集合の共通領域',
        '顧客の期待と自社の強みを重ねる','二つの条件が重なる領域を、提供価値や共通課題として示す。',
        'ベン図 Venn 共通領域 重なり 価値提案 顧客ニーズ 強み 条件 overlap intersection',b,
        [slot(303,50,294,67,'顧客の期待','集合A'),slot(603,50,294,67,'自社の強み','集合B'),
         slot(256,310,218,110,'求められること','Aのみ'),slot(726,310,218,110,'提供できること','Bのみ'),
         slot(535,301,130,128,'提供価値','共通領域',color=WHITE)],
        dict(use_case='商品提案で、顧客の期待と自社の強みが重なる領域を検討する。',
             message='顧客が求め、自社が提供できる領域に価値が生まれる。',
             reading=['左の円が顧客の期待、右の円が自社の強み。','主色の重なりが両方の条件を満たす領域。', '円と重なりは対象の共通点を示す概念的な表現。']))


def _intersections(a, b, radius):
    dx,dy=b[0]-a[0],b[1]-a[1]
    distance=sqrt(dx*dx+dy*dy)
    mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    height=sqrt(radius*radius-distance*distance/4)
    return ((mx-dy*height/distance,my+dx*height/distance),
            (mx+dy*height/distance,my-dx*height/distance))


def _lens(a, b, radius, fill):
    p,q=_intersections(a,b,radius)
    return path(f'M{p[0]:.5f} {p[1]:.5f}A{radius} {radius} 0 0 1 {q[0]:.5f} {q[1]:.5f}'
                f'A{radius} {radius} 0 0 1 {p[0]:.5f} {p[1]:.5f}Z',fill)


def three_set_overlap():
    radius=205
    a,b,c=(475,235),(725,235),(600,235+125*sqrt(3))
    body=circle(*a,radius,FAINT)+circle(*b,radius,FAINT)+circle(*c,radius,FAINT)
    body += _lens(a,b,radius,PALE)+_lens(a,c,radius,PALE)+_lens(b,c,radius,PALE)
    nearest=lambda points,centre:min(points,key=lambda p:(p[0]-centre[0])**2+(p[1]-centre[1])**2)
    left=nearest(_intersections(b,c,radius),a)
    right=nearest(_intersections(a,c,radius),b)
    bottom=nearest(_intersections(a,b,radius),c)
    body += path(f'M{left[0]:.5f} {left[1]:.5f}'
                 f'A205 205 0 0 1 {right[0]:.5f} {right[1]:.5f}'
                 f'A205 205 0 0 1 {bottom[0]:.5f} {bottom[1]:.5f}'
                 f'A205 205 0 0 1 {left[0]:.5f} {left[1]:.5f}Z',BLUE)
    for centre in (a,b,c):
        body += circle(*centre,radius,'none',INK,2.5)
    return _item('企画判断_必要性と実現性と継続性を満たす_3集合の成立領域',
        '必要性・実現性・継続性を満たす','三つの条件を満たす案を、中央の共通領域として示す。',
        'ベン図 Venn 3集合 企画判断 必要性 実現性 継続性 事業性 共通領域 feasibility viability desirability',body,
        [slot(325,158,180,94,'顧客に必要','必要性'),slot(695,158,180,94,'実現できる','実現性'),
         slot(500,508,200,94,'継続できる','継続性'),slot(540,286,120,62,'成立領域','三条件の共通領域',color=WHITE)],
        dict(use_case='新規サービス案が顧客・技術・事業の三つの条件を満たすか検討する。',
             message='一つの条件だけでなく、三つが重なる案を選ぶ。',
             reading=['上の二つの円が顧客の必要性と実現性。','下の円が事業としての継続性。','中央の主色が三つをすべて満たす領域。', '三つの円と重なりは条件の組み合わせを示す概念的な表現。']))


def swot_matrix():
    positive,negative='#137D66','#B5473A'
    b = rect(269,156,400,74,PALE,0)+rect(687,156,400,74,FAINT,0)
    b += rect(269,248,400,177,WHITE,0,MID,2)+rect(687,248,400,177,WHITE,0,MID,2)
    b += rect(269,443,400,177,WHITE,0,MID,2)+rect(687,443,400,177,WHITE,0,MID,2)
    b += rect(269,248,8,177,positive,0)+rect(269,443,8,177,positive,0)
    b += rect(687,248,8,177,negative,0)+rect(687,443,8,177,negative,0)
    b += line(323,193,343,193,positive,4)+line(333,183,333,203,positive,4)
    b += line(741,193,761,193,negative,4)
    b += path('M244 248H225V425H244M244 443H225V620H244',stroke=INK,sw=3)
    for x,y in ((269,248),(687,248),(269,443),(687,443)):
        b += line(x+28,y+66,x+371,y+66,PALE,2)
    return _item('戦略検討_内部と外部の有利不利を整理する_SWOT4象限',
        '内部と外部の有利・不利を整理する','強み・弱み・機会・脅威を、要因の出所と影響に分けて整理する。',
        'SWOT 強み 弱み 機会 脅威 内部環境 外部環境 戦略 4象限 analysis',b,
        [slot(357,166,287,54,'プラスに働く要因','有利な要因'),slot(775,166,287,54,'妨げになる要因','不利な要因'),
         slot(52,286,154,94,'内部の要因','内部環境'),slot(52,481,154,94,'外部の要因','外部環境'),
         slot(298,255,338,51,'強み','内部・有利'),slot(716,255,338,51,'弱み','内部・不利'),
         slot(298,450,338,51,'機会','外部・有利'),slot(716,450,338,51,'脅威','外部・不利'),
         slot(301,335,338,68,'蓄積した専門性','強みの例'),slot(719,335,338,68,'人員・体制の不足','弱みの例'),
         slot(301,530,338,68,'新しい顧客ニーズ','機会の例'),slot(719,530,338,68,'競合・制度の変化','脅威の例')],
        dict(use_case='事業や施策の現状を整理し、戦略上の論点を出す。',
             message='自社の内側と外側、有利と不利を分けて考える。',
             reading=['上段が内部要因、下段が外部要因。','左列が有利な要因、右列が不利な要因。','四つの枠は強み・弱み・機会・脅威の区分を表す。']))


def organization_tree():
    b = path('M600 160V230M224 230H976M224 230V279M600 230V279M976 230V279',stroke=INK,sw=3.5)
    for parent,first,second in ((224,130,318),(600,506,694),(976,882,1070)):
        b += path(f'M{parent} 374V446M{first} 446H{second}M{first} 446V518M{second} 446V518',stroke=MID,sw=3)
    b += rect(422,68,356,92,INK,4)
    for centre in (224,600,976):
        b += rect(centre-127,279,254,95,PALE,3,INK,2.5)+rect(centre-127,279,254,8,BLUE,0)
    for centre in (130,318,506,694,882,1070):
        b += rect(centre-83,518,166,95,WHITE,3,MID,2.5)+rect(centre-83,518,7,95,BLUE,0)
    return _item('組織紹介_所属と指揮命令系統を示す_3階層組織図',
        '所属と指揮命令系統を示す','責任者・部門・担当の三階層を、正式な所属関係として示す。',
        '組織図 階層 部門 所属 責任者 指揮命令 組織紹介 hierarchy organization chart',b,
        [slot(443,84,314,59,'代表・事業責任者','統括責任者',color=WHITE),
         slot(110,299,228,56,'営業部門','部門'),slot(486,299,228,56,'開発部門','部門'),slot(862,299,228,56,'管理部門','部門'),
         slot(59,537,142,58,'法人営業','担当'),slot(247,537,142,58,'顧客支援','担当'),slot(435,537,142,58,'製品開発','担当'),
         slot(623,537,142,58,'品質保証','担当'),slot(807,537,150,58,'人事・総務','担当'),slot(995,537,150,58,'財務・経理','担当')],
        dict(use_case='会社や部門の体制を、正式な所属と責任範囲で説明する。',
             message='各担当がどの部門と責任者に属するかを示す。',
             reading=['上段が全体の責任者。','中段が部門、下段が担当。','縦横の接続線が所属関係を示す。']))


def decision_tree():
    b = circle(330,64,11,BLUE)+arrow(330,80,330,107,BLUE,4,17)
    b += poly('330,115 495,220 330,325 165,220',WHITE,INK,3)
    b += poly('330,390 495,495 330,600 165,495',WHITE,INK,3)
    b += arrow(503,220,773,220,BLUE,5,22)
    b += arrow(330,333,330,383,INK,4,20)
    b += arrow(503,495,773,495,BLUE,5,22)
    b += path('M330 607V626Q330 646 350 646H750',stroke=INK,sw=4)+arrow(747,646,774,646,INK,4,20)
    b += rect(781,170,303,100,BLUE,5)
    b += rect(781,445,303,100,PALE,5,BLUE,2.5)
    b += rect(781,596,303,100,FAINT,5,INK,2.5)
    return _item('対応判断_二つの質問で対応先を決める_はいといいえの決定木',
        '二つの質問で対応先を決める','条件を順に確認し、標準対応・専門対応・継続管理を選ぶ。',
        '決定木 判断条件 分岐 はい いいえ 対応先 振り分け decision tree routing',b,
        [slot(231,169,198,102,'標準手順で\n対応できるか','最初の判断'),slot(231,444,198,102,'専門判断が\n必要か','次の判断'),
         slot(551,157,160,45,'はい','最初の肯定条件',color=BLUE),slot(359,333,170,45,'いいえ','最初の否定条件'),
         slot(551,432,160,45,'はい','次の肯定条件',color=BLUE),slot(508,590,175,43,'いいえ','次の否定条件'),
         slot(800,190,265,60,'標準手順で回答','標準対応',color=WHITE),slot(800,465,265,60,'専門担当へ依頼','専門対応'),
         slot(800,616,265,60,'継続課題として管理','継続管理')],
        dict(use_case='問い合わせや依頼の対応先を、担当者が同じ基準で判断する。',
             message='質問に順番に答えると、必要な対応先にたどり着く。',
             reading=['菱形が答えるべき質問。','はいは右へ、いいえは下へ進む。','右側の枠が選ばれる対応先。']))


def company_timeline():
    b = line(92,362,1105,362,PALE,24)+arrow(93,362,1114,362,BLUE,5,21)
    dates=['2016年','2018年','2021年','2024年','現在']
    events=['創業・\n事業開始','顧客基盤を\n拡大','新領域へ\n展開','事業を\n多角化','次の成長へ']
    labels=[]
    for i,x in enumerate((165,370,575,780,985)):
        above=i%2==0
        b += line(x,342 if above else 382,x,282 if above else 443,INK,2.5)
        b += circle(x,282 if above else 443,4,INK)
        b += circle(x,362,21,WHITE,BLUE,4)
        if i==4:
            b += circle(x,362,12,BLUE)
        y=110 if above else 472
        b += rect(x-77,y,154,43,PALE,3)
        labels += [slot(x-75,y+2,150,39,dates[i],'年・時期'),
                   slot(x-96,177 if above else 536,192,83,events[i],'節目の出来事')]
    return _item('企業紹介_事業の節目を時系列で伝える_5つの沿革',
        '事業の節目を時系列で伝える','創業から現在までの主要な出来事を、時間の流れに沿って示す。',
        '沿革 企業紹介 歴史 年表 タイムライン 成長 節目 history timeline milestones',b,labels,
        dict(use_case='会社紹介で、創業から現在までの事業の歩みを伝える。',
             message='事業の成長を、主要な節目の連なりとして示す。',
             reading=['左から右へ時間が進む。','丸が主要な節目。','上下の説明がその時期に起きた出来事。', '節目の間隔は時系列の順序を読み取りやすくする概念的な配置。']))


def phased_roadmap():
    b = arrow(95,577,1107,577,BLUE,5,22)
    labels=[]
    phases=[('第1期','基盤を整える','ルール・データを\n揃える'),
            ('第2期','運用を定着させる','担当者へ広げる'),
            ('第3期','全体を最適化する','成果を見て見直す')]
    for i,(x,phase) in enumerate(zip((82,435,788),phases)):
        centre=x+156
        b += rect(x,164,312,339,FAINT,0)
        b += rect(x,164,312,73,INK if i==0 else BLUE if i==1 else PALE,0)
        b += path(f'M{x} 253V503H{x+312}V253',stroke=MID,sw=2.5)
        b += line(x+26,360,x+286,360,PALE,2.5)
        b += line(centre,504,centre,550,INK,2.5)
        b += poly(f'{centre},553 {centre+24},577 {centre},601 {centre-24},577',WHITE,BLUE,3)
        labels += [slot(x+22,176,268,48,phase[0],'時期',color=WHITE if i<2 else INK),
                   slot(x+25,267,262,71,phase[1],'その時期の目標'),
                   slot(x+25,393,262,79,phase[2],'取り組み')]
    return _item('実行計画_時期ごとの目標と施策を揃える_3段階ロードマップ',
        '時期ごとの目標と施策を揃える','段階ごとの目標と取り組みを、共通の時間軸に沿って配置する。',
        'ロードマップ 段階計画 短期 中期 長期 実行計画 施策 目標 roadmap phased plan',b,labels,
        dict(use_case='施策を立ち上げ、定着させ、改善するまでの見通しを共有する。',
             message='各時期に何を目指し、何に取り組むかを揃える。',
             reading=['左から右へ三つの時期が進む。','各列の上が時期、中が目標、下が取り組み。','下の菱形が段階の到達点。']))


def onboarding():
    b = arrow(372,304,483,304,BLUE,6,22)+arrow(715,304,817,304,BLUE,6,22)
    b += poly('178,210 287,210 326,249 326,389 178,389',WHITE,INK,3.5)
    b += path('M287 210V249H326',stroke=INK,sw=3.5)
    b += circle(230,269,17,BLUE)+path('M204 311q26-37 52 0',stroke=BLUE,sw=7)
    b += line(204,341,280,341,MID,3.5)+line(204,356,258,356,MID,3.5)
    b += circle(323,372,31,BLUE)+path('M307 372h32M323 356v32',stroke=WHITE,sw=5)
    b += rect(517,212,181,181,PALE,10)
    for y,knob in ((250,567),(300,637),(350,593)):
        b += line(541,y,674,y,INK,5)+circle(knob,y,15,WHITE,BLUE,4)
    b += rect(848,226,213,158,WHITE,6,INK,3.5)+rect(848,226,213,28,INK,5)
    b += circle(864,240,3,WHITE)+circle(877,240,3,MID)+line(869,278,988,278,MID,4)
    b += rect(869,300,54,58,PALE,0)+rect(935,300,54,58,PALE,0)
    b += circle(1048,374,40,BLUE)+check(1026,359,1.2)
    return _item('利用開始_登録から設定を経て使い始める_3ステップ導入',
        '登録・設定を経て使い始める','サービスの利用開始までに必要な三つの行動を順番に示す。',
        '導入 初期設定 利用開始 登録 オンボーディング 3ステップ onboarding getting started',b,
        [slot(113,448,279,86,'アカウントを登録','登録'),slot(468,448,279,86,'利用条件を設定','設定'),slot(822,448,296,86,'サービスを使い始める','利用開始')],
        dict(use_case='新しいサービスを利用する担当者へ、開始までの流れを示す。',
             message='登録・設定・利用開始の三つを順に進める。',
             reading=['人物付きの文書がアカウント登録。','調整つまみが利用条件の設定。','チェック付きの画面が利用開始。']))


def service_delivery():
    b = line(160,382,1040,382,PALE,20)
    for left,right in ((180,360),(400,580),(620,800),(840,1020)):
        b += arrow(left,382,right,382,BLUE,4,18)
    for x in (160,380,600,820,1040):
        b += circle(x,382,16,WHITE,BLUE,3)
        b += line(x,365,x,343,INK,2.5)
    # Intake: a request arrives in a receiving tray.
    b += path('M94 306h36l10 18h40l10-18h36v40H94Z',WHITE,INK,3)
    b += poly('123,205 181,205 199,223 199,301 123,301',PALE,INK,3)
    b += path('M181 205V223H199',stroke=INK,sw=3)+line(139,244,180,244,MID,3)+line(139,260,173,260,MID,3)
    # Requirements: inspect the document before making a proposal.
    b += rect(333,207,84,127,WHITE,3,INK,3)+line(347,231,397,231,MID,3)+line(347,248,387,248,MID,3)
    b += line(403,300,429,329,INK,10)+circle(385,278,29,WHITE,BLUE,4)+path('M372 277l9 9 17-20',stroke=BLUE,sw=3.5)
    # Proposal: a presentation sheet makes the intended result visible.
    b += rect(535,213,130,97,WHITE,3,INK,3)+rect(535,213,130,16,INK,2)
    b += line(600,311,600,345,INK,3)+path('M573 345h54',stroke=INK,sw=3)
    b += rect(553,270,15,23,MID,0)+rect(577,256,15,37,BLUE,0)+rect(601,244,15,49,INK,0)
    b += path('M627 254l9 9 15-18',stroke=BLUE,sw=3)
    # Execution: an open-jaw spanner and work case represent the agreed work.
    b += rect(767,267,107,77,PALE,3,INK,3)+rect(792,251,57,16,WHITE,2,INK,3)
    b += '<g transform="translate(839 226) rotate(38)">'
    b += path('M-17 -30Q-36 -12 -24 13L-9 26V91Q-9 103 0 103Q9 103 9 91V26L24 13Q36 -12 17 -30V-4L0 7L-17 -4Z',BLUE,INK,2.5)
    b += circle(0,87,4,WHITE)+'</g>'
    b += rect(811,300,20,18,BLUE,2)
    # Report: completion is recorded and accepted.
    b += poly('993,207 1059,207 1088,236 1088,344 993,344',WHITE,INK,3)
    b += path('M1059 207V236H1088',stroke=INK,sw=3)+line(1010,254,1068,254,MID,3)
    b += circle(1040,300,27,BLUE)+check(1025,290,.83)
    return _item('業務提供_受付から報告まで一貫して届ける_5工程サービス',
        '受付から報告まで一貫して届ける','依頼の受付から要件確認・提案・実施・報告までを一続きで示す。',
        'サービス提供 業務フロー 受付 要件確認 提案 実施 報告 5工程 delivery service workflow',b,
        [slot(80,437,160,94,'依頼を\n受け付ける','受付'),slot(300,437,160,94,'要件を\n確かめる','要件確認'),slot(520,437,160,94,'進め方を\n提案する','提案'),
         slot(740,437,160,94,'合意内容を\n実施する','実施'),slot(960,437,160,94,'成果を\n報告する','報告')],
        dict(use_case='受託サービスや社内支援の提供範囲を、依頼元へ説明する。',
             message='依頼を受けるだけでなく、成果の報告まで一貫して担う。',
             reading=['左から受付・確認・提案・実施・報告。','各道具や文書がその工程の仕事を表す。','つながる経路が一連の提供範囲。']))


def annual_rhythm():
    b=''
    colors=(BLUE,MID,PALE,FAINT)
    for i,color in enumerate(colors):
        start=-90+i*90;end=start+90
        p,q=_point(600,360,254,start),_point(600,360,254,end)
        r,s=_point(600,360,165,end),_point(600,360,165,start)
        b += path(f'M{p[0]} {p[1]}A254 254 0 0 1 {q[0]} {q[1]}L{r[0]} {r[1]}A165 165 0 0 0 {s[0]} {s[1]}Z',color)
    for i in range(12):
        angle=-90+i*30;p=_point(600,360,165,angle);q=_point(600,360,254,angle)
        b += line(*p,*q,WHITE,5 if i%3==0 else 2)
    b += path('M600 220A140 140 0 1 1 559.8 225.9',stroke=INK,sw=3)
    b += arrow(559.8,225.9,582,221,INK,3,17)
    for angle,direction in ((-45,1),(45,1),(135,-1),(225,-1)):
        x,y=_point(600,360,254,angle)
        b += line(x,y,866 if direction==1 else 334,y,INK,2.5)+circle(x,y,5,INK)
    labels=[]
    for i,month in enumerate((4,5,6,7,8,9,10,11,12,1,2,3)):
        x,y=_point(600,360,209,-75+i*30)
        labels.append(slot(x-45,y-22,90,44,f'{month}月','月',color=WHITE if i<3 else INK))
    labels += [slot(891,137,259,86,'計画・体制づくり','4〜6月の活動',align='left'),
               slot(891,495,259,86,'実行・進捗確認','7〜9月の活動',align='left'),
               slot(50,495,259,86,'評価・改善','10〜12月の活動'),
               slot(50,137,259,86,'次年度の準備','1〜3月の活動'),
               slot(494,307,212,106,'年度で繰り返す\n活動','年間の主題')]
    return _item('年間運営_四半期の活動を毎年繰り返す_4月始まりの年間サイクル',
        '四半期の活動を毎年繰り返す','4月から翌3月までの活動を、四半期と月の循環として示す。',
        '年間計画 年度 四半期 月次 年間サイクル 4月始まり 定例 運営 annual rhythm calendar',b,labels,
        dict(use_case='年度の計画・実行・評価・翌年度準備を、年間の運営リズムとして共有する。',
             message='月ごとの活動を四半期にまとめ、翌年度へつなげる。',
             reading=['上から時計回りに4月から翌3月へ進む。','色分けされた四つの区画が四半期。','中央の矢印が毎年繰り返す運営を示す。']))


def make_assets():
    items = [pdca_cycle(), learning_cycle(), two_set_overlap(), three_set_overlap(),
            swot_matrix(), organization_tree(), decision_tree(), company_timeline(),
            phased_roadmap(), onboarding(), service_delivery(), annual_rhythm()]
    identities = [
        ('framework/pdca','four-stage-cycle','clockwise'),
        ('framework/learning-cycle','three-stage-cycle','clockwise'),
        ('framework/two-set-overlap','two-set-intersection','outside-in'),
        ('framework/three-set-overlap','three-set-intersection','outside-in'),
        ('framework/swot','two-by-two-classification','row-by-row'),
        ('framework/organization-tree','three-level-hierarchy','top-to-bottom'),
        ('framework/decision-tree','binary-decision-tree','top-to-bottom'),
        ('framework/company-timeline','ordered-milestones','left-to-right'),
        ('framework/phased-roadmap','phases-with-goals-and-actions','left-to-right'),
        ('framework/onboarding','three-step-sequence','left-to-right'),
        ('framework/service-delivery','five-step-sequence','left-to-right'),
        ('framework/annual-rhythm','twelve-month-cycle','clockwise'),
    ]
    for item, (key, relation, direction) in zip(items, identities):
        item['key'] = key
        item['layout'] = dict(relation=relation, reading_direction=direction)
    return items
