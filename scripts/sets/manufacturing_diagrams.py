"""Manufacturing explanations with explicit checks, boundaries and return paths."""
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER
from vector import path, rect, circle, line, poly, arrow, check, slot
from sets.operations import item


def D(key,title,description,keywords,body,labels,message,reading,avoid,relation):
    return item('manufacturing/'+key,title+'_製造業務の関係図',title,description,keywords,body,labels,
                dict(use_case=description,message=message,reading=reading,avoid=avoid),relation)


def nonconforming_segregation():
    b=rect(72,223,212,151,FAINT,12,INK,3)
    for x in (98,157,216):b+=rect(x,265,43,66,PALE,4,INK,2)
    b+=arrow(291,298,397,298,BLUE,6,22)+poly('402,298 490,213 578,298 490,383',WHITE,INK,3)
    b+=path('M578 298H651V164H759',stroke=BLUE,sw=6)+poly('782,164 758,152 758,176',BLUE)
    b+=rect(791,89,325,151,PALE,9,BLUE,3)+circle(833,132,18,BLUE)+check(823,125,.6)
    b+=path('M490 383V472H656',stroke=AMBER,sw=6)+poly('679,472 655,460 655,484',AMBER)
    b+=path('M674 371H1126V577H674Z',stroke=AMBER,sw=2.5,extra='stroke-dasharray="9 7"')
    b+=rect(698,395,394,156,WHITE,9,AMBER,3)
    b+=rect(725,414,32,46,PALE,3,INK,2)+rect(770,414,32,46,PALE,3,INK,2)+line(851,414,851,460,AMBER,4)
    b+=circle(860,507,13,AMBER)+path('M860 498V509M860 516V517',stroke=WHITE,sw=2.5)
    b+=path('M698 526H609V624H182V398',stroke=INK,sw=4)+poly('182,376 172,399 192,399',INK)
    ls=[slot(68,115,220,76,'検査する製品','対象'),slot(418,264,144,68,'基準に\n適合するか','判定'),slot(655,61,126,56,'適合','分岐'),slot(854,106,229,54,'次工程へ渡す','正常処理'),slot(827,173,250,45,'識別を保持して出す','識別'),slot(492,405,168,56,'不適合','分岐'),slot(876,409,200,57,'通常品と分離','隔離'),slot(887,477,191,59,'処置を判断','処置'),slot(288,637,436,55,'再検査が必要な処置は、検査へ戻す','再検査')]
    return D('nonconforming-segregation','不適合品を分けて処置する','検査で不適合となった製品を通常の流れから分離し、処置を判断する。','不適合 品質 隔離 処置 再検査 nonconforming segregation disposition',b,ls,'不適合の製品を識別し、処置と再検査を経るまで通常品へ混ぜない。',['中央の判定から適合品だけが右上へ進む。','右下の囲みが隔離して処置を判断する範囲。','再検査が必要な処置は下側の経路から最初の検査へ戻る。'],'処置には廃棄や特別採用等もある。再検査が必要な経路のみを示している。','segregation-and-reinspection')


def engineering_change_impact():
    b=circle(158,320,82,WHITE,BLUE,5)+poly('124,341 136,312 178,270 204,296 162,338 124,350',PALE,BLUE,4)+line(172,282,192,302,BLUE,4)+poly('124,350 136,320 152,340',INK)
    b+=path('M240 320H300V145H388M300 320H388M300 320V495H388',stroke=INK,sw=4)
    for y in (145,320,495):
        b+=rect(397,y-58,331,116,WHITE,9,INK,3)+arrow(734,y,826,y,BLUE,5,20)
        b+=circle(854,y,21,WHITE,BLUE,3)+check(842,y-8,.65,BLUE)
    b+=rect(887,118,12,404,INK,3)+line(877,145,886,145,BLUE,4)+line(877,320,886,320,BLUE,4)+line(877,495,886,495,BLUE,4)
    b+=arrow(908,320,963,320,BLUE,6,20)+rect(976,244,163,152,PALE,10,BLUE,3)
    ls=[slot(61,412,195,68,'変更する内容','変更'),slot(418,107,287,74,'製品・部品への影響','影響対象'),slot(418,282,287,74,'工程・治具への影響','影響対象'),slot(418,457,287,74,'図面・手順への影響','影響対象'),slot(747,24,360,60,'必要な確認をそろえる','確認条件'),slot(993,277,129,86,'変更を\n適用する','適用'),slot(384,610,750,61,'関係する対象の確認がそろってから、変更を適用する','関係の説明')]
    return D('engineering-change-impact','変更の影響を横断して確認する','設計や仕様の変更が製品・工程・文書へ与える影響を確認する。','設計変更 変更管理 影響範囲 図面 工程 engineering change impact review',b,ls,'一箇所の変更でも関連する対象を確認し、必要な条件がそろってから適用する。',['左は変更の起点。','三つの枝が異なる影響対象を表す。','右の共通ゲートに必要な確認を集めて適用へ進む。'],'三つの枝は例。実際の変更では調達、在庫、顧客等の必要な対象も確認する。','cross-domain-change-review')


def design_verification():
    b=''
    for x,y,w,fill in ((62,98,274,INK),(215,285,270,PALE),(458,504,284,BLUE),(715,285,270,PALE),(864,98,274,INK)):
        b+=rect(x,y,w,104,fill,9,INK if fill==PALE else fill,3)
    b+=arrow(265,210,324,274,BLUE,6,20)+arrow(426,402,517,492,BLUE,6,20)
    b+=arrow(683,492,774,402,BLUE,6,20)+arrow(877,274,937,210,BLUE,6,20)
    b+=line(348,149,852,149,MID,2,'7 7')+line(496,337,704,337,MID,2,'7 7')
    b+=circle(600,149,8,WHITE,BLUE,3)+circle(600,337,8,WHITE,BLUE,3)
    ls=[slot(80,123,238,56,'何を実現するか','要求',color=WHITE),slot(235,310,230,56,'どう実現するか','設計'),slot(480,529,240,56,'形にして試す','試作',color=WHITE),slot(735,310,230,56,'設計どおりか','検証'),slot(884,123,234,56,'要求を満たすか','妥当性確認',color=WHITE),slot(383,50,434,57,'要求と結果を対応させる','対応'),slot(467,231,266,55,'設計と検証を対応','対応'),slot(179,440,212,53,'具体化する','設計側'),slot(798,440,210,53,'確かめる','検証側'),slot(263,635,674,52,'作る前の条件と、作った後の確認を一組にする','説明')]
    return D('design-verification','要求と設計に対応した検証を行う','要求から設計・試作へ具体化し、それぞれの条件に対応する確認を行う。','要求 設計 検証 妥当性確認 試作 Vモデル design verification validation',b,ls,'作った結果を、事前に決めた要求と設計条件に対応させて確かめる。',['左側を下へ進み要求から試作へ具体化する。','右側を上へ進み設計と要求の適合を確認する。','同じ高さの破線は確認対象の対応で、作業を飛ばす矢印ではない。'],'特定業界の規格適合手順を網羅した図ではない。','requirements-and-test-correspondence')


def fault_isolation():
    b=rect(60,221,1080,165,FAINT,12)
    xs=(122,417,712,1007)
    for i,x in enumerate(xs):
        b+=rect(x,251,88,105,WHITE,8,INK,3)
        if i<3:b+=arrow(x+95,303,x+282,303,BLUE if i<1 else MID,6,20)
    for x in (286,579,874):b+=line(x,209,x,396,INK,2)
    b+=circle(286,184,24,BLUE)+check(273,175,.72)
    b+=circle(579,184,24,WHITE,AMBER,3)+line(569,174,589,194,AMBER,4)+line(589,174,569,194,AMBER,4)
    b+=circle(874,184,24,WHITE,GRAY,3)+circle(874,184,5,GRAY)
    b+=path('M292 405V432H573V405',stroke=AMBER,sw=4)+rect(292,448,281,86,WHITE,0,AMBER,2)
    ls=[slot(99,268,133,64,'入力','設備区分'),slot(395,268,132,64,'工程 A','設備区分'),slot(690,268,132,64,'工程 B','設備区分'),slot(984,268,133,64,'出力','設備区分'),slot(171,87,230,56,'正常を確認','確認状態'),slot(464,87,230,56,'異常を確認','確認状態'),slot(759,87,230,56,'未確認','確認状態'),slot(311,465,242,52,'先にこの区間を調べる','絞り込み'),slot(289,589,653,66,'正常と異常の境界から、確認する範囲を絞る','説明')]
    return D('fault-isolation','正常と異常の境界で原因を絞る','工程の途中で状態を確認し、最初に調べる区間を絞り込む。','故障 原因 切り分け 診断 確認 不具合 fault isolation troubleshooting',b,ls,'最初に異常が確認された地点と、その直前の正常な地点の間を優先して調べる。',['上の印が工程途中の確認状態を表す。','正常と異常の境界となる一区間を括っている。','右の点は未確認であり、正常を意味しない。'],'異常の原因がこの区間に確定したという意味ではない。相互作用や上流起因も検証する。','verified-boundary-isolation')


def workload_leveling():
    b=rect(73,263,368,310,FAINT,7,INK,2)+rect(758,263,368,310,FAINT,7,INK,2)
    b+=line(90,467,424,467,BLUE,3,'8 6')+line(775,467,1109,467,BLUE,3,'8 6')
    for x in (106,213,320):b+=rect(x,491,88,58,BLUE,5)
    for x in (106,213,320):b+=rect(x,391,88,58,PALE,5,INK,2)
    b+=rect(793,491,88,58,BLUE,5)+rect(900,491,88,58,BLUE,5)
    b+=rect(1007,491,88,58,WHITE,5,BLUE,2)
    b+=path('M364 384V179Q364 151 392 151H1023Q1051 151 1051 180V472',stroke=BLUE,sw=6)+poly('1051,489 1040,468 1062,468',BLUE)
    b+=rect(564,286,104,114,WHITE,8,INK,3)+path('M587 324H645M602 348H630',stroke=BLUE,sw=5)
    ls=[slot(101,191,312,57,'同じ時期に集中','移動前'),slot(786,191,312,57,'余力のある時期','移動先'),slot(108,302,291,54,'そのままでは超過','課題'),slot(449,61,520,59,'期限を確かめ、動かせる仕事を移す','調整'),slot(545,416,142,61,'調整する','調整役'),slot(784,392,316,54,'受入可能な量を確認','受入条件'),slot(121,600,962,62,'処理できる範囲と、期限に余裕のある仕事を対応させる','説明')]
    return D('workload-leveling','仕事の集中を余力のある時期へ分散する','処理できる量と納期を確認し、時期を動かせる仕事の集中を解く。','負荷平準化 需給 余力 能力 納期 調整 capacity workload leveling',b,ls,'仕事を無条件に移さず、期限と移動先の処理能力を確認して平準化する。',['左の上段は処理枠を超えて集中する仕事の作例。','下段の点線が処理枠の区切り。','上の経路は動かせる仕事を余力のある右側へ移す。'],'箱の数は関係を説明する作例で、仕事量や能力の実データではない。','capacity-constrained-rescheduling')


def standard_exception_improvement():
    b=rect(86,194,1028,143,PALE,12)
    b+=rect(113,218,250,95,WHITE,9,INK,3)+arrow(371,265,492,265,BLUE,6,22)
    b+=poly('497,265 597,177 697,265 597,353',WHITE,INK,3)
    b+=arrow(704,265,837,265,BLUE,6,22)+rect(847,218,229,95,BLUE,9)
    b+=path('M597 353V462H706',stroke=AMBER,sw=5)+poly('727,462 704,451 704,473',AMBER)
    b+=rect(737,404,339,119,WHITE,9,AMBER,3)
    b+=path('M906 524V604H239V338',stroke=INK,sw=5)+poly('239,315 228,340 250,340',INK)
    b+=rect(383,562,314,83,WHITE,0,BLUE,2)
    ls=[slot(129,234,218,63,'共通の手順で進む','標準作業'),slot(521,230,152,70,'標準内で\n対応できるか','判断'),slot(861,234,201,63,'標準内で完了','通常経路',color=WHITE),slot(762,420,289,82,'例外の理由を記録し\n必要な判断へ渡す','例外対応'),slot(717,149,111,48,'できる','分岐条件'),slot(608,377,116,47,'できない','分岐条件'),slot(407,573,264,60,'標準を見直すか判断','改善判断'),slot(259,71,694,64,'例外を記録し、再利用できる学びを標準へ戻す','説明')]
    return D('standard-exception-improvement','例外の学びを標準へ戻す','共通の手順を適用し、標準内で扱えない例外から手順を見直す。','標準化 例外 改善 学習 手順 見直し standard exception improvement',b,ls,'例外を記録して判断し、必要なものだけを標準の改善に生かす。',['上の通常経路は標準の範囲で完了する仕事。','下の経路は標準内で扱えない例外の記録と判断。','戻る経路には標準を変えるかという判断がある。'],'例外が起きるたびに標準を自動で変更するという意味ではない。','standard-and-exception-learning')


def make_assets():
    return [nonconforming_segregation(),engineering_change_impact(),design_verification(),fault_isolation(),workload_leveling(),standard_exception_improvement()]
