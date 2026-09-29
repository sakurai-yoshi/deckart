"""Purpose-specific decision, strategy and relationship diagrams."""
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER
from vector import path, rect, circle, ellipse, line, poly, group, arrow, check, slot, asset

COMPARISON = '02-比較と意思決定'
STRATEGY = '05-組織と戦略'
RELATIONS = '03-関係と連携'


def selection():
    # Unselected routes stop at the review boundary; only the chosen route continues.
    b = rect(105,124,426,128,FAINT,14)+rect(105,296,426,128,PALE,14)+rect(105,468,426,128,FAINT,14)
    b += rect(533,110,134,500,FAINT,20,INK,3)
    b += line(384,188,579,188,MID,5)+line(384,532,579,532,MID,5)
    b += line(579,166,579,210,INK,5)+line(579,510,579,554,INK,5)
    b += arrow(384,360,1016,360,BLUE,10,26)
    b += circle(600,360,37,WHITE,BLUE,5)+check(578,345,1.2,BLUE)
    b += circle(1054,360,38,BLUE)+check(1032,345,1.2)
    return asset('企画提案_選択肢を比較して一案を選ぶ_判断基準と採用案',COMPARISON,'比較して一案を選ぶ','同じ判断基準で候補を比較し、採用した一案だけを実行へ進める。','比較 選定 採用案 企画 選択肢 意思決定 判断基準 コンペ',b,[slot(132,150,245,76,'候補 A'),slot(132,322,245,76,'候補 B'),slot(132,494,245,76,'候補 C'),slot(431,34,340,64,'共通の判断基準'),slot(760,412,340,80,'採用した案を実行へ')])


def standardization():
    # A closed network of individual routes is replaced by a clear sequence.
    b = line(157,253,453,253,MID,5)+line(157,489,453,489,MID,5)+line(157,253,157,489,MID,5)+line(453,253,453,489,MID,5)
    b += line(157,253,453,489,BLUE,7)+line(453,253,157,489,INK,7)
    b += path('M157 253C211 155 400 155 453 253M157 489C211 587 400 587 453 489',stroke=MID,sw=4)
    b += circle(157,253,31,WHITE,INK,4)+circle(453,253,31,WHITE,INK,4)+circle(157,489,31,WHITE,INK,4)+circle(453,489,31,WHITE,INK,4)
    b += line(600,139,600,601,MID,2,'7 12')
    b += rect(733,168,338,104,PALE,18)+rect(733,319,338,104,PALE,18)+rect(733,470,338,104,PALE,18)
    b += arrow(902,274,902,312,BLUE,6,17)+arrow(902,425,902,463,BLUE,6,17)
    b += rect(733,190,8,60,BLUE,4)+rect(733,341,8,60,BLUE,4)+rect(733,492,8,60,BLUE,4)
    return asset('業務改善_複雑な連携の整理_個別対応から共通運用',COMPARISON,'個別対応から共通の手順へ','担当者ごとに異なる連携を、受付・判断・実行の共通手順へ整理する。','改善前後 ビフォーアフター AsIs ToBe 業務改善 標準化 簡素化 共通化 属人化 DX',b,[slot(96,60,429,76,'個別の経路で対応'),slot(697,60,412,76,'共通の手順にそろえる'),slot(766,188,273,64,'受付をそろえる'),slot(766,339,273,64,'判断をそろえる'),slot(766,490,273,64,'実行をそろえる')])


def balance():
    # The axle and support touch; equal level means consideration, not equal scores.
    b = path('M600 264V569',stroke=INK,sw=16)+poly('600,478 503,616 697,616',PALE,INK,4)+rect(460,612,280,20,INK,6)
    b += line(266,246,934,246,INK,14)+circle(600,246,32,BLUE)+circle(600,246,11,WHITE)
    b += path('M266 249L147 459M266 249L385 459M934 249L815 459M934 249L1053 459',stroke=MID,sw=4)
    b += path('M117 457H415Q403 548 266 548Q129 548 117 457Z',BLUE)
    b += path('M785 457H1083Q1071 548 934 548Q797 548 785 457Z',INK)
    b += line(123,457,409,457,PALE,6)+line(791,457,1077,457,PALE,6)
    b += circle(266,398,37,WHITE,BLUE,4)+line(248,398,284,398,BLUE,5)+line(266,380,266,416,BLUE,5)
    b += poly('934,356 977,431 891,431',WHITE,AMBER,4)+line(934,378,934,407,AMBER,5)+circle(934,419,3,AMBER)
    return asset('意思決定_期待効果と懸念の比較_均衡する天秤',COMPARISON,'効果と懸念を同じ場で判断する','期待する効果と備えるべき懸念を、どちらも判断材料として扱う。','費用対効果 リスク リターン メリット デメリット 懸念 ベネフィット 判断 稟議',b,[slot(110,109,312,80,'期待する効果'),slot(778,109,312,80,'備えるべき懸念'),slot(412,37,376,68,'両面を踏まえて判断する'),slot(92,584,348,74,'実現したい価値'),slot(760,584,348,74,'確認する対策と条件')])


def priority():
    # The axes classify options; no invented route implies that priorities are stages.
    b = rect(214,142,407,217,FAINT)+rect(636,142,421,217,PALE)+rect(214,374,407,217,FAINT)+rect(636,374,421,217,FAINT)
    b += arrow(192,610,1102,610,INK,4,17)+arrow(192,610,192,108,INK,4,17)
    b += line(628,142,628,591,MID,2,'6 11')+line(214,366,1057,366,MID,2,'6 11')
    b += circle(417,295,20,WHITE,MID,4)+circle(417,526,20,WHITE,MID,4)+circle(845,526,20,WHITE,MID,4)
    b += circle(846,294,34,BLUE)+check(825,279,1.15)
    return asset('施策評価_優先順位の整理_効果と実行しやすさの二軸',COMPARISON,'効果と実行しやすさで優先する','効果が高く実行しやすい施策を、最初に取り組む領域として示す。','優先順位 優先度 二軸 マトリクス マトリックス 期待効果 実現性 施策 ポジショニング',b,[slot(259,174,317,70,'条件を整えて育てる'),slot(686,174,321,70,'優先して取り組む'),slot(259,406,317,70,'着手を見直す'),slot(686,406,321,70,'小さく効率よく進める'),slot(181,25,395,66,'上ほど期待効果が高い',align='left'),slot(686,627,410,64,'右ほど実行しやすい')])


def gap_bridge():
    # A single flat stair has three spans and no conflicting perspective faces.
    b = rect(101,421,219,200,PALE)+rect(880,253,219,368,PALE)
    b += path('M320 389H500V321H680V253H880V297H724V365H544V433H320Z',BLUE)
    b += line(101,421,320,421,INK,4)+line(880,253,1099,253,INK,4)
    b += line(410,411,410,339,MID,3)+line(590,343,590,258,MID,3)+line(779,275,779,177,MID,3)
    b += circle(410,411,10,WHITE)+circle(590,343,10,WHITE)+circle(779,275,10,WHITE)
    b += path('M342 606V640H858V606',stroke=INK,sw=3)
    return asset('変革計画_現状と目標の差を埋める_三つの橋渡し',COMPARISON,'三つの施策で目標へ近づく','現在と目指す状態をつなぐ三つの施策を、橋渡しする段階として示す。','ギャップ分析 現状 目標 理想 改革 変革 課題 施策 実現方法 ロードマップ',b,[slot(111,467,199,90,'現在の状態'),slot(890,390,199,90,'目指す状態'),slot(283,254,255,68,'仕組みを整える'),slot(459,176,263,68,'能力を育てる'),slot(648,94,263,68,'運用に定着させる'),slot(390,649,420,58,'埋めるべき隔たり')])


def filters():
    # Each visible narrowing is a condition; one centerline leads to the survivor.
    b = poly('169,113 730,113 653,242 246,242',PALE,BLUE,3)
    b += poly('247,287 652,287 584,414 315,414',PALE,BLUE,3)
    b += poly('316,459 583,459 522,565 377,565',PALE,BLUE,3)
    b += path('M246 226H653V242H246Z',BLUE)+path('M315 398H584V414H315Z',BLUE)+path('M377 549H522V565H377Z',BLUE)
    b += arrow(449,246,449,278,BLUE,5,16)+arrow(449,418,449,450,BLUE,5,16)+arrow(449,569,449,608,BLUE,5,16)
    b += circle(449,642,27,BLUE)+check(433,631,.86)
    b += line(709,178,800,178,MID,3)+line(635,349,800,349,MID,3)+line(570,510,800,510,MID,3)
    return asset('調達選定_判断条件による絞り込み_段階式フィルター',COMPARISON,'条件を重ねて候補を絞る','必須条件、運用への適合、期待する価値を順に確認し、候補を絞り込む。','選定 調達 ベンダー 製品評価 条件 必須要件 フィルター 選考 絞り込み',b,[slot(814,138,307,82,'必須条件を満たす',align='left'),slot(814,308,307,82,'運用に適合する',align='left'),slot(814,469,307,82,'期待する価値がある',align='left'),slot(513,608,343,68,'条件を満たした候補')])


def allocation():
    # A single junction splits into equal-width policy routes; no percentages implied.
    b = line(392,360,503,360,INK,11)
    b += path('M503 360C624 360 617 174 750 174H1052',stroke=PALE,sw=32)
    b += path('M503 360H1052',stroke=PALE,sw=32)
    b += path('M503 360C624 360 617 546 750 546H1052',stroke=PALE,sw=32)
    b += path('M503 360C624 360 617 174 750 174H1024',stroke=BLUE,sw=6)+poly('1057,174 1022,159 1022,189',BLUE)
    b += arrow(503,360,1057,360,INK,6,35)
    b += path('M503 360C624 360 617 546 750 546H1024',stroke=BLUE,sw=6)+poly('1057,546 1022,531 1022,561',BLUE)
    b += circle(503,360,13,WHITE,INK,4)+circle(260,360,130,WHITE,INK,15)+circle(260,360,107,WHITE,MID,2)
    return asset('経営計画_資源配分の方針_重点維持探索',COMPARISON,'資源の使い道を目的で分ける','同じ経営資源を、成長への重点投資、安定運営、新しい可能性の探索へ振り分ける。','ポートフォリオ 資源配分 経営資源 投資配分 人員配分 重点 維持 探索 事業計画',b,[slot(162,311,196,98,'経営資源'),slot(770,91,297,68,'重点を置く'),slot(770,277,297,68,'安定を保つ'),slot(770,463,297,68,'可能性を探る'),slot(430,625,629,64,'使い道ごとに配分の狙いを決める')])


def tradeoff():
    # All option marks lie exactly on the quadratic illustrative frontier.
    b = path('M250 540Q450 250 650 210Q850 170 1050 170V590H250Z',FAINT)
    b += path('M250 540Q450 250 650 210Q850 170 1050 170',stroke=MID,sw=19)
    b += path('M250 540Q450 250 650 210Q850 170 1050 170',stroke=BLUE,sw=4)
    b += arrow(193,610,1115,610,INK,4,17)+arrow(192,610,192,119,INK,4,17)
    b += line(650,251,650,590,MID,2,'6 10')+line(209,210,608,210,MID,2,'6 10')
    b += circle(350,410.625,18,WHITE,BLUE,4)+circle(650,210,34,WHITE,BLUE,6)+check(630,195,1.1,BLUE)+circle(950,172.5,18,WHITE,BLUE,4)
    b += line(365,433,410,475,MID,3)+line(673,237,705,280,BLUE,3)+line(950,122,950,148,MID,3)
    return asset('施策選定_効果と負担の均衡点_定性的な選択境界',COMPARISON,'効果の上積みと負担を見比べる','負担を増やしたときの効果の上積みを比べ、どの案を選ぶか説明する。','トレードオフ 費用対効果 効率 最適化 均衡 限界効用 投資対効果 施策選定',b,[slot(182,25,402,68,'上ほど期待効果が高い',align='left'),slot(754,631,379,62,'右ほど必要な負担が大きい'),slot(357,489,276,77,'小さく始める案'),slot(711,287,345,86,'均衡を重視する案'),slot(796,34,308,70,'大きく投資する案')])


def cascade():
    # Wide translation stages advance down-right; the separate return line reconnects.
    b = path('M125 111H543L613 238H195Z',PALE,BLUE,3)+path('M365 291H783L853 418H435Z',PALE,BLUE,3)+path('M605 471H1023L1093 598H675Z',PALE,BLUE,3)
    b += poly('125,111 145,111 215,238 195,238',BLUE)+poly('365,291 385,291 455,418 435,418',BLUE)+poly('605,471 625,471 695,598 675,598',BLUE)
    b += arrow(475,243,500,282,INK,7,20)+arrow(715,423,740,462,INK,7,20)
    b += path('M1070 598V654H76V177H142',stroke=MID,sw=4)+poly('162,177 140,166 140,188',MID)
    return asset('戦略展開_方針から日々の実行へ_連続する段階',STRATEGY,'方針を施策と日々の実行へ落とす','方針を施策へ具体化し、日々の実行から得た学びを方針へ戻す。','戦略 方針展開 実行施策 ブレイクダウン カスケード 戦略実行 経営計画 フィードバック',b,[slot(210,140,322,70,'目指す方向'),slot(450,320,322,70,'実現する施策'),slot(690,500,322,70,'日々の実行'),slot(295,668,610,46,'実行から得た学びを方針へ戻す')])


def governance():
    # Command, feedback and support are three explicit, connected relationships.
    b = circle(249,300,111,WHITE,INK,12)+circle(895,300,111,WHITE,BLUE,12)
    b += arrow(367,265,775,265,BLUE,9,26)+arrow(775,335,367,335,INK,6,22)
    b += rect(468,552,619,105,PALE,16,INK,3)
    b += arrow(895,550,895,418,MID,8,22)
    return asset('運営設計_意思決定と実行と支援_循環する統治',STRATEGY,'判断・実行・支援の関係を分ける','意思決定と実行の間で方針と結果を往復し、共通の支援基盤が実行を支える。','ガバナンス 統治 意思決定 実行 支援 決裁 役割分担 運営体制 推進体制',b,[slot(157,259,184,82,'意思決定'),slot(803,259,184,82,'実行の担当'),slot(478,573,599,66,'実行を支える共通の仕組み'),slot(389,173,365,66,'方針と権限を渡す'),slot(389,386,365,76,'状況と結果を返す')])


def pyramid():
    # Three exact slices share one triangular boundary, without perspective fragments.
    b = poly('600,76 447,280 753,280',PALE,WHITE,4)
    b += poly('447,280 753,280 881,451 319,451',PALE,WHITE,4)
    b += poly('319,451 881,451 1023,641 177,641',PALE,WHITE,4)
    b += path('M600 76L1023 641H177Z',stroke=INK,sw=4)+line(447,280,753,280,BLUE,4)+line(319,451,881,451,BLUE,4)
    b += rect(177,641,846,17,INK,3)
    b += arrow(112,564,331,273,MID,5,21)
    return asset('価値創造_基盤から顧客成果へ_一体型ピラミッド',STRATEGY,'組織の基盤から顧客の成果へ','組織の基盤が価値の提供を支え、その先で顧客の成果につながる関係を示す。','価値創造 バリューチェーン ピラミッド 価値体系 基盤 顧客成果 組織能力 経営理念',b,[slot(500,210,200,56,'顧客の成果'),slot(355,332,490,78,'提供する価値'),slot(276,516,648,80,'価値を支える組織の基盤'),slot(54,132,355,74,'基盤から成果へつなぐ')])


def department_handoffs():
    # One work route crosses explicit ownership boundaries through handoff ports.
    b = rect(105,144,310,423,FAINT)+rect(428,144,343,423,PALE)+rect(784,144,310,423,FAINT)
    b += line(105,119,415,119,INK,7)+line(428,119,771,119,BLUE,7)+line(784,119,1094,119,INK,7)
    b += line(421,153,421,566,MID,2,'7 10')+line(777,153,777,566,MID,2,'7 10')
    b += arrow(163,370,1054,370,BLUE,19,37)
    b += rect(400,316,43,108,WHITE,13,INK,4)+rect(756,316,43,108,WHITE,13,INK,4)
    b += circle(421,370,11,BLUE)+circle(777,370,11,BLUE)+circle(163,370,19,WHITE,BLUE,5)
    b += line(421,435,421,581,INK,2)+line(777,435,777,581,INK,2)
    return asset('組織運営_責任範囲と部門横断業務_境界を越える実行',STRATEGY,'部門を越えて責任を引き継ぐ','一つの仕事が部門を越えるとき、責任を受け渡す場所と条件を明確にする。','責任分界 部門横断 組織横断 オーナーシップ RACI 引き継ぎ ハンドオフ 業務分担 協働',b,[slot(132,181,259,84,'企画の責任'),slot(469,181,259,84,'実行の責任'),slot(811,181,259,84,'提供の責任'),slot(233,598,376,77,'合意する引き渡し条件'),slot(636,598,376,77,'確認する引き渡し条件')])


def capabilities():
    # Four readable layers connect to one service spine; no narrow front-face labels.
    b = rect(130,98,660,105,FAINT,4,INK,2)+rect(130,240,660,105,PALE,4,INK,2)+rect(130,382,660,105,PALE,4,INK,2)+rect(130,524,660,105,PALE,4,INK,2)
    b += rect(130,183,660,20,BLUE)+rect(130,325,660,20,BLUE)+rect(130,467,660,20,BLUE)+rect(130,609,660,20,INK)
    b += rect(865,118,15,491,INK,7)
    b += line(792,151,865,151,MID,7)+line(792,293,865,293,MID,7)+line(792,435,865,435,MID,7)+line(792,577,865,577,MID,7)
    b += circle(873,151,12,WHITE,BLUE,4)+circle(873,293,12,WHITE,BLUE,4)+circle(873,435,12,WHITE,BLUE,4)+circle(873,577,12,WHITE,BLUE,4)
    return asset('組織開発_必要な能力の積層_共通基盤で結ぶ四層',STRATEGY,'必要な能力を共通の運用で結ぶ','成果に必要な四つの能力を整理し、共通の運用でつながる構造を示す。','ケイパビリティ 能力開発 人材育成 組織開発 スキル 業務プロセス 共通基盤 定着 DX',b,[slot(169,111,583,63,'成果を生む実践'),slot(169,253,583,63,'仕事の進め方'),slot(169,395,583,63,'知識とスキル'),slot(169,537,583,63,'道具と基盤'),slot(914,287,246,151,'全体を結ぶ\n共通の運用')])


def customer_value():
    # All three roles point to the same customer outcome; surrounding links are mutual.
    b = path('M459 150H364Q248 150 248 267V470M741 150H836Q952 150 952 267V470M379 546H821',stroke=MID,sw=3)
    b += poly('248,463 238,443 258,443',MID)+poly('248,264 238,284 258,284',MID)+poly('952,463 942,443 962,443',MID)+poly('952,264 942,284 962,284',MID)
    b += poly('814,546 794,536 794,556',MID)+poly('386,546 406,536 406,556',MID)
    b += rect(460,89,280,121,PALE,23,BLUE,3)+rect(100,470,280,121,PALE,23,BLUE,3)+rect(820,470,280,121,PALE,23,BLUE,3)
    b += arrow(600,214,600,262,BLUE,7,21)+arrow(373,479,476,425,BLUE,7,21)+arrow(827,479,724,425,BLUE,7,21)
    b += circle(600,381,110,WHITE,INK,12)
    return asset('顧客中心_価値を支える役割_三部門の協働',STRATEGY,'三つの役割で顧客価値を支える','企画・提供・支援が同じ顧客価値を目指し、役割の間でも連携する関係を示す。','顧客中心 カスタマーセントリック CX 顧客体験 部門連携 価値提供 顧客価値 協働',b,[slot(494,340,212,83,'顧客への価値'),slot(480,116,240,67,'価値を企画する'),slot(120,497,240,67,'価値を届ける'),slot(840,497,240,67,'体験を支える'),slot(392,632,415,63,'役割の間でも連携する')])


def prerequisite():
    # Both piers physically touch the shared beam; the beam enables one outcome.
    b = rect(129,445,300,163,PALE,4,INK,3)+rect(490,445,300,163,PALE,4,INK,3)
    b += rect(248,320,62,125,INK)+rect(609,320,62,125,INK)
    b += rect(129,234,661,86,PALE,5,INK,3)+rect(129,234,661,12,BLUE)
    b += arrow(794,277,924,277,BLUE,8,24)
    b += poly('955,173 1037,173 1091,227 1091,394 955,394',WHITE,BLUE,4)+path('M1037 173V227H1091',stroke=BLUE,sw=4)
    b += line(978,265,1062,265,MID,4)+line(978,286,1046,286,MID,4)+circle(1024,344,29,BLUE)+check(1008,333,.88)
    return asset('基盤整備_成果を支える二つの前提_依存関係の構造',RELATIONS,'二つの前提がそろって成果を生む','情報と運用の両方を整えることで共通機能を使え、成果につながる関係を示す。','依存関係 前提条件 必要条件 基盤整備 共通機能 両輪 インフラ 運用 実現条件',b,[slot(161,481,236,91,'情報の基盤'),slot(522,481,236,91,'運用の基盤'),slot(158,254,602,54,'二つの基盤を使って実現する機能'),slot(227,105,464,74,'両方の前提をそろえる'),slot(879,429,284,91,'実現できる成果')])


def ecosystem():
    # Each pair gets two separate straight routes with arrowheads at the receiving end.
    b = arrow(530,207,286,445,BLUE,8,23)+arrow(324,471,569,232,MID,5,20)
    b += arrow(670,207,914,445,BLUE,8,23)+arrow(876,471,631,232,MID,5,20)
    b += arrow(334,553,866,553,BLUE,8,23)+arrow(866,507,334,507,MID,5,20)
    b += circle(600,150,88,WHITE,INK,12)+circle(240,520,88,WHITE,BLUE,12)+circle(960,520,88,WHITE,BLUE,12)
    return asset('事業連携_相互に価値を交換する_三者のエコシステム',RELATIONS,'三者の間で価値が往復する','三者の各組み合わせに、提供する価値と受け取る価値があることを示す。','エコシステム 事業連携 パートナー 共創 相互利益 価値交換 プラットフォーム 三者関係',b,[slot(521,112,158,76,'事業者'),slot(161,482,158,76,'顧客'),slot(881,482,158,76,'協力者'),slot(83,280,255,89,'価値と対価'),slot(862,280,255,89,'機会と専門性'),slot(418,628,364,64,'体験と参加')])


def controlled_layers():
    # Each layer has its own entry point; the picture does not invent a call sequence.
    b = rect(278,114,813,111,FAINT,9,INK,3)+rect(278,307,813,111,PALE,9,INK,3)+rect(278,500,813,111,PALE,9,INK,3)
    b += arrow(100,170,216,170,BLUE,6,19)+arrow(100,363,216,363,BLUE,6,19)+arrow(100,556,216,556,BLUE,6,19)
    b += path('M278 116L323 132V170C323 199 302 215 278 230C254 215 233 199 233 170V132Z',WHITE,BLUE,4)+check(260,159,.95,BLUE)
    b += poly('278,315 324,341 324,386 278,412 232,386 232,341',WHITE,BLUE,4)+path('M268 350L253 363L268 376M288 350L303 363L288 376',stroke=BLUE,sw=4)
    b += path('M234 530V582C234 603 322 603 322 582V530',WHITE,BLUE,4)+ellipse(278,530,44,17,WHITE,BLUE,4)+path('M234 554C234 576 322 576 322 554',stroke=BLUE,sw=3)
    return asset('システム構成_三つの層と接続の入口_認証APIデータ',RELATIONS,'各層の入口で接続を管理する','利用者との接点、業務処理、データ保持を分け、それぞれの接続の入口を示す。','システム構成 アーキテクチャ 三層 認証 API データアクセス ゲートウェイ 接続 境界',b,[slot(436,134,575,70,'利用者との接点'),slot(436,327,575,70,'業務を処理する層'),slot(436,520,575,70,'データを保持する層'),slot(87,38,386,62,'認証を確認する入口'),slot(87,236,386,62,'処理を受け付ける入口'),slot(87,430,386,62,'データへ接続する入口')])


def inclusion():
    # Every boundary is fully closed and generously separated from its parent.
    b = rect(94,85,1012,551,PALE,40,INK,4)
    b += rect(366,249,675,325,WHITE,30,BLUE,4)
    b += rect(699,397,286,119,PALE,23,INK,4)
    b += line(135,188,315,188,BLUE,4)+line(408,346,633,346,BLUE,4)
    return asset('責任範囲_全体と部分の包含関係_事業部門チーム',RELATIONS,'全体の中に担当範囲を置く','事業の中に部門、部門の中にチームが含まれる責任範囲を示す。','包含関係 全体と部分 スコープ 責任範囲 担当範囲 事業領域 部門 チーム 内包 階層',b,[slot(129,111,768,68,'事業全体の領域',align='left'),slot(402,270,580,68,'部門が受け持つ範囲',align='left'),slot(715,420,255,72,'チームの担当範囲')])


GUIDANCE = [
    dict(use_case='企画会議で複数の提案から採用案を決める。',message='同じ基準で比べ、選んだ一案だけを実行する。',reading=['左の三つの領域は比較する候補。','中央の縦枠は全候補に適用する判断基準。','上段と下段の経路は止まり、チェックのある経路だけが右へ続く。'],avoid='複数案を統合する説明には使わない。'),
    dict(use_case='問い合わせ対応や受発注業務の標準化を提案する。',message='担当ごとの個別対応を共通の手順へ整理する。',reading=['左の相互接続は担当間で異なる対応経路。','右の三段は全員が使う共通の手順。','下向きの矢印は受付から実行までの順序。'],avoid='線や点の数を実際の業務量として扱わない。'),
    dict(use_case='稟議や投資判断で、期待効果とリスク対策を同時に説明する。',message='効果だけでなく懸念への備えも判断材料にする。',reading=['左のプラスは期待する価値。','右の注意記号は確認する懸念。','中央の支点は両面を扱う意思決定。'],avoid='天秤の高さを金額や評価点の大小として使わない。'),
    dict(use_case='改善施策を期待効果と実行しやすさで整理する。',message='効果が高く実行しやすい施策から取り組む。',reading=['上に行くほど期待効果が高い。','右に行くほど実行しやすい。','右上のチェックは優先して取り組む領域。'],avoid='軸を変更する場合は四領域の意味も合わせて変更する。'),
    dict(use_case='改革提案で、現状から目標へ進むための三つの施策を説明する。',message='目標との差は具体的な施策で埋める。',reading=['左の低い領域は現在、右の高い領域は目標。','主色の三つの段は橋渡しする施策。','下の括弧は解消する隔たり。'],avoid='高さや段の幅を効果量や所要期間として扱わない。'),
    dict(use_case='製品や委託先の選定で、候補を絞る確認順序を共有する。',message='条件を順番に満たす候補を残す。',reading=['上から下へ確認する条件が進む。','狭くなる形は候補の絞り込み。','最後のチェックは条件を満たした候補。'],avoid='幅は候補数や通過率を表さない。'),
    dict(use_case='事業計画で人員や予算を使う方針を説明する。',message='成長・安定・探索の狙いを分けて資源を使う。',reading=['左の円は共通の経営資源。','分岐点から三つの使い道へ進む。','同じ太さの経路は配分の種類を示す。'],avoid='配分比率や投資額のグラフには使わない。'),
    dict(use_case='設備やシステムへの投資案について、追加負担に見合う効果を説明する。',message='負担を増やしたときの効果の上積みを見て選ぶ。',reading=['横軸は必要な負担、縦軸は期待する効果。','主色の曲線は効果の上積みが小さくなる概念的な関係。','チェックは均衡を重視した選択例。'],avoid='実測値や実際の最適点を示すグラフとして使わない。'),
    dict(use_case='年度方針を部門施策と日々の活動へ展開する。',message='方針を具体化し、実行の学びを方針へ戻す。',reading=['左上から右下へ方針・施策・実行の順に具体化する。','短い矢印は次の段階への受け渡し。','外周の経路は実行から方針へのフィードバック。'],avoid='段の位置を役職の上下関係として扱わない。'),
    dict(use_case='プロジェクト運営で意思決定者、実行担当、支援組織の役割を説明する。',message='権限の委譲、結果の報告、実行支援を分けて設計する。',reading=['左の円は意思決定、右の円は実行担当。','上の右向き矢印は方針と権限、下の左向き矢印は状況と結果。','下の基盤から実行を支える。'],avoid='承認の全手順や具体的な決裁権限の一覧には使わない。'),
    dict(use_case='組織への投資が、提供価値を通じて顧客の成果へつながることを説明する。',message='顧客の成果は価値提供と組織基盤の上に成り立つ。',reading=['下段は人材・情報・仕組みなどの組織基盤。','中段は顧客に提供する価値。','上段は顧客が得る成果。'],avoid='面積を構成比や投資配分として扱わない。'),
    dict(use_case='企画から実行、提供へ仕事を渡す部門横断業務を説明する。',message='仕事の流れと責任の引き渡し条件を合わせて決める。',reading=['三つの背景領域は部門の責任範囲。','横向きの矢印は一つの仕事の流れ。','境界の縦枠は責任を引き継ぐ場所。'],avoid='境界の記号を承認・否決の分岐として扱わない。'),
    dict(use_case='人材育成や業務改革に必要な能力を整理する。',message='実践・手順・スキル・道具を共通の運用で結ぶ。',reading=['四つの層は成果に必要な能力の種類。','右側の縦の線は共通する運用。','接続点は各層を別々に整備して終わらせないことを示す。'],avoid='層の順序を成熟度の採点や導入順序として扱わない。'),
    dict(use_case='顧客体験の改善に向け、企画・提供・支援の役割を説明する。',message='三つの役割が同じ顧客価値を目指して連携する。',reading=['中央は実現したい顧客価値。','内向きの矢印は各役割からの貢献。','外側の双方向の経路は役割間の連携。'],avoid='顧客の行動順序を表すジャーニーマップには使わない。'),
    dict(use_case='共通機能を導入する前に、情報整備と運用整備の両方が必要だと説明する。',message='一方の基盤だけでは共通機能を支えられない。',reading=['二つの支柱は両方必要な前提。','上の梁は前提を使って実現する共通機能。','右への矢印は機能から成果へのつながり。'],avoid='どちらか一方で成立する代替条件には使わない。'),
    dict(use_case='顧客、事業者、協力者が参加する事業モデルを説明する。',message='三者の各関係で価値が双方向に交換される。',reading=['三つの円は事業に参加する主体。','各辺の二本の矢印は行きと戻りの価値交換。','辺のそばの言葉は交換する価値の例。'],avoid='金額や流量の大小を矢印の太さで比較しない。'),
    dict(use_case='システムの概念説明で、利用・処理・データの接続管理を分けて示す。',message='各層の入口で接続を管理する。',reading=['三つの横長の領域は利用・処理・データの層。','各領域の左の記号は管理する入口。','右向きの矢印はその層への接続。'],avoid='実際の通信順序や認証方式の仕様図には使わない。'),
    dict(use_case='事業・部門・チームの担当範囲を説明する。',message='小さな担当範囲は上位の範囲に含まれる。',reading=['最も外側が事業全体。','その内側が部門の範囲。','さらに内側がチームの担当範囲。'],avoid='部門をまたいで重複する責任範囲には使わない。'),
]


def make_assets():
    definitions = [
        ('decision/option-selection', selection),
        ('decision/operations-standardization', standardization),
        ('decision/risk-benefit-balance', balance),
        ('decision/impact-feasibility-priority', priority),
        ('decision/current-target-bridge', gap_bridge),
        ('decision/selection-filters', filters),
        ('decision/resource-allocation', allocation),
        ('decision/diminishing-return-tradeoff', tradeoff),
        ('strategy/execution-cascade', cascade),
        ('strategy/governance-roles', governance),
        ('strategy/value-creation-pyramid', pyramid),
        ('strategy/cross-functional-handoffs', department_handoffs),
        ('strategy/capability-stack', capabilities),
        ('strategy/customer-value-roles', customer_value),
        ('relationship/required-foundations', prerequisite),
        ('relationship/reciprocal-ecosystem', ecosystem),
        ('relationship/controlled-system-layers', controlled_layers),
        ('relationship/nested-responsibility', inclusion),
    ]
    out = []
    for (key, compose), guidance in zip(definitions, GUIDANCE):
        item = compose()
        item['key'] = key
        item['guidance'] = guidance
        out.append(item)
    return out
