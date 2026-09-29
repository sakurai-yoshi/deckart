"""Eighteen authored diagrams: operations, delivery and organizational relationships."""
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER
from vector import path, rect, circle, ellipse, line, poly, group, arrow, check, slot, asset


def value_stream():
    b = path('M92 344H1092V428H92Z',PALE)
    b += path('M92 363H1056L1098 386L1056 409H92Z',BLUE)
    b += rect(104,267,104,82,WHITE,7,MID,3)+rect(120,251,104,82,WHITE,7,MID,3)
    b += rect(136,235,104,82,WHITE,7,INK,3)
    b += line(157,258,216,258,MID,4)+line(157,279,204,279,MID,4)
    b += rect(523,238,126,102,WHITE,5,INK,3)
    b += line(543,261,613,261,MID,3)+line(543,279,591,279,MID,3)
    b += poly('576,318 640,252 655,267 591,333 571,338',BLUE)
    b += poly('576,318 591,333 571,338',INK)
    b += line(635,257,650,272,WHITE,2)
    for x in (365,815):
        b += rect(x-22,272,44,207,WHITE,9,INK,3)
        b += circle(x,284,29,BLUE)+check(x-16,272,.9)
        b += line(x,480,x,529,INK,2.5)+circle(x,529,4,INK)
    b += arrow(265,386,324,386,WHITE,4,13)
    b += arrow(423,386,753,386,WHITE,4,15)
    b += arrow(871,386,1011,386,WHITE,4,15)
    b += poly('968,235 1042,235 1072,265 1072,334 968,334',WHITE,INK,3)
    b += path('M1042 235V265H1072',stroke=INK,sw=3)+check(990,284,.9,BLUE)
    return asset('業務改善_検査で品質を守る価値の流れ_二段階ゲート','01-業務プロセス','検査で品質を守る価値の流れ','作業の流れと品質確認を分け、手戻りを防ぐ検査位置を示す。','工程 品質保証 品質管理 検査 ゲート バリューストリーム 手戻り',b,[slot(78,145,245,70,'受付・要件整理'),slot(444,145,302,70,'価値を加える作業'),slot(864,145,286,70,'成果物の引き渡し'),slot(228,552,275,66,'着手条件'),slot(678,552,275,66,'完成基準')])


def bottleneck():
    b = path('M85 295H344C424 295 454 351 524 351H650C720 351 750 313 826 313H1097V477H826C750 477 720 439 650 439H524C454 439 424 495 344 495H85Z',PALE)
    b += path('M85 373H349C425 373 455 382 524 382H1065L1096 395L1065 408H524C455 408 425 422 349 422H85Z',BLUE)
    b += path('M350 395V204Q350 180 374 180H844Q868 180 868 204V360',stroke=BLUE,sw=8)
    b += poly('868,385 856,359 880,359',BLUE)+circle(868,395,10,WHITE,BLUE,3)
    b += circle(350,395,11,WHITE,BLUE,3)
    b += rect(514,327,146,21,INK,3)+rect(514,443,146,21,INK,3)
    b += line(525,348,525,443,INK,4)+line(649,348,649,443,INK,4)
    for x in (142,207,272):
        b += rect(x,317,41,35,INK,4)+rect(x,439,41,35,MID,4)
    b += arrow(729,395,1033,395,WHITE,4,15)
    b += line(587,465,587,531,INK,2.5)+circle(587,531,4,INK)
    return asset('業務改善_ボトルネックを迂回して負荷を逃がす_待ち行列と迂回路','01-業務プロセス','ボトルネックと負荷の逃がし方','処理待ちが集中する工程と、負荷を別経路へ逃がす改善策を示す。','ボトルネック 待ち行列 混雑 負荷分散 迂回 処理能力 業務改善',b,[slot(79,556,315,70,'着手待ちが集中'),slot(421,556,330,70,'処理能力の制約'),slot(799,556,319,70,'後工程へ安定供給'),slot(425,82,376,70,'別経路で負荷を吸収')])


def approval_gateway():
    b = path('M292 370H1054',stroke=PALE,sw=29)
    b += path('M600 507V559Q600 587 572 587H239Q211 587 211 559V498',stroke=AMBER,sw=6)
    b += poly('211,475 199,502 223,502',AMBER)
    b += poly('450,370 600,208 750,370 600,532',WHITE,INK,4)
    b += poly('600,208 750,370 600,532 600,506 725,370 600,234',BLUE)
    b += arrow(296,370,441,370,BLUE,7,21)+arrow(758,370,1001,370,BLUE,9,25)
    b += poly('129,268 252,268 294,310 294,474 129,474',WHITE,INK,3)
    b += path('M252 268V310H294',stroke=INK,sw=3)
    b += line(154,335,267,335,MID,4)+line(154,357,241,357,MID,4)+line(154,379,257,379,MID,4)
    b += rect(154,411,33,33,PALE,3)+line(202,427,260,427,MID,4)
    b += path('M572 338h30v68M602 370h34',stroke=BLUE,sw=6)
    b += circle(572,338,8,BLUE)+poly('648,370 628,359 628,381',BLUE)+poly('602,419 591,399 613,399',BLUE)
    b += circle(1051,370,42,INK)+check(1029,355,1.2)
    return asset('意思決定_承認と差戻しの経路を分ける_判断ゲートと復帰路','01-業務プロセス','承認と差戻しを分ける判断ゲート','承認後の前進と、修正して再申請する経路を一つの図で説明する。','承認 決裁 稟議 差戻し 再申請 判断 審査',b,[slot(70,157,283,72,'申請・提出'),slot(438,104,324,72,'承認基準を確認'),slot(802,252,311,66,'基準を満たして次へ'),slot(684,501,416,66,'条件未達なら修正'),slot(235,614,343,58,'修正後に再申請')])


def parallel_validation():
    b = path('M188 400H275M275 210V590',stroke=MID,sw=5)
    for y in (210,400,590):
        b += line(275,y,825,y,PALE,30)
        b += arrow(277,y,337,y,BLUE,4,14)+arrow(730,y,824,y,BLUE,4,14)
        b += rect(347,y-61,370,122,WHITE,15,MID,2.5)
        b += path(f'M363 {y-61}H410V{y+61}H363Q347 {y+61} 347 {y+45}V{y-45}Q347 {y-61} 363 {y-61}Z',PALE)
        b += circle(379,y,17,BLUE)+check(368,y-7,.6)
    b += rect(832,151,20,498,INK,4)
    b += circle(842,210,10,WHITE,BLUE,3)+circle(842,400,10,WHITE,BLUE,3)+circle(842,590,10,WHITE,BLUE,3)
    b += circle(145,400,43,INK)+poly('133,382 163,400 133,418',WHITE)
    b += arrow(855,400,982,400,BLUE,8,22)
    b += circle(1044,400,55,PALE)+circle(1044,400,40,BLUE)+check(1023,385,1.15)
    return asset('品質保証_並行検証を揃えて次へ進む_三系統の同期','01-業務プロセス','並行検証を揃えて次へ進む','独立した確認作業を並行で進め、必要な結果が揃う条件を示す。','並行検証 並列処理 同期 合流 リリース判定 品質 審査',b,[slot(425,173,269,74,'機能・動作を確認'),slot(425,363,269,74,'運用・保守を確認'),slot(425,553,269,74,'安全性を確認'),slot(721,59,413,66,'必要な結果が揃う'),slot(896,491,283,70,'次の工程へ')])


def escalation():
    b = path('M88 554H343V424H603V294H863V164H1112V623H88Z',FAINT)
    b += path('M88 554H343V424H603V294H863V164H1112',stroke=MID,sw=3)
    for x,y in ((210,507),(470,377),(730,247),(990,117)):
        b += circle(x,y,35,WHITE,INK,4)
        b += circle(x,y,13,BLUE)
    for x,y in ((210,507),(470,377),(730,247)):
        b += path(f'M{x+37} {y}H{x+89}Q{x+108} {y} {x+108} {y-19}V{y-111}Q{x+108} {y-130} {x+127} {y-130}H{x+203}',stroke=BLUE,sw=7)
        b += poly(f'{x+224},{y-130} {x+201},{y-142} {x+201},{y-118}',BLUE)
    b += circle(990,117,24,BLUE)+check(975,107,.8)
    return asset('障害対応_判断権限を段階的に引き継ぐ_責任者へのエスカレーション','01-業務プロセス','判断権限を段階的に引き継ぐ','現場で解決できない問題を、判断できる責任者へ引き継ぐ流れを示す。','エスカレーション 障害対応 責任者 権限 委譲 判断 報告 引継ぎ',b,[slot(107,565,205,49,'一次対応'),slot(367,435,205,64,'専門担当へ'),slot(627,305,205,72,'部門責任者へ'),slot(887,175,205,64,'経営判断へ'),slot(342,643,639,52,'解決に必要な権限まで引き継ぐ')])


def double_loop():
    b = path('M916 283V171Q916 137 882 137H252Q218 137 218 171V302',stroke=PALE,sw=30)
    b += path('M916 283V171Q916 137 882 137H252Q218 137 218 171V302',stroke=INK,sw=5)
    b += poly('218,326 206,300 230,300',INK)
    b += path('M995 366H1041V539Q1041 570 1010 570H618Q587 570 587 539V484',stroke=PALE,sw=28)
    b += path('M995 366H1041V539Q1041 570 1010 570H618Q587 570 587 539V484',stroke=BLUE,sw=6)
    b += poly('587,458 574,486 600,486',BLUE)
    b += rect(78,333,280,117,WHITE,19,INK,3)
    b += rect(436,300,303,157,WHITE,19,BLUE,3)
    b += path('M455 300H720Q739 300 739 319V329H436V319Q436 300 455 300Z',PALE)
    b += circle(916,366,83,PALE)+circle(916,366,64,WHITE,BLUE,3)
    b += path('M882 380l22-25 22 12 29-29',stroke=BLUE,sw=5)
    b += arrow(365,385,428,385,BLUE,6,17)+arrow(746,378,823,378,BLUE,6,18)
    b += circle(916,283,8,WHITE,INK,3)+circle(999,366,8,WHITE,BLUE,3)
    return asset('組織学習_実行改善と前提見直しを分ける_二重のフィードバック','01-業務プロセス','実行の改善と前提の見直し','結果から手順を直す学習と、方針そのものを見直す学習を分けて示す。','組織学習 ダブルループ フィードバック 改善 振り返り 前提 方針 PDCA',b,[slot(94,354,250,74,'方針・前提'),slot(455,351,265,76,'手順を実行'),slot(793,464,229,62,'結果を観測'),slot(586,611,429,66,'手順を改善する'),slot(365,47,461,66,'方針・前提から見直す')])


def triage():
    b = path('M488 295C634 192 776 180 1065 180',stroke=PALE,sw=70)
    b += path('M530 365H1065',stroke=FAINT,sw=70)
    b += path('M488 435C634 539 776 550 1065 550',stroke=PALE,sw=70)
    b += path('M147 185H233Q270 185 302 224L393 332M153 365H350M153 545H233Q270 545 302 506L393 398',stroke=MID,sw=4)
    b += circle(126,185,25,WHITE,INK,3.5)+poly('127,340 152,365 127,390 102,365',WHITE,INK,3.5)+rect(102,520,50,50,WHITE,5,INK,3.5)
    b += poly('350,365 440,215 530,365 440,515',INK)
    b += poly('385,365 440,273 495,365 440,457',WHITE)+circle(440,365,21,BLUE)
    b += path('M488 295C634 192 776 180 1053 180',stroke=BLUE,sw=5)+poly('1080,180 1051,166 1051,194',BLUE)
    b += arrow(532,365,1080,365,BLUE,5,28)
    b += path('M488 435C634 539 776 550 1053 550',stroke=BLUE,sw=5)+poly('1080,550 1051,536 1051,564',BLUE)
    return asset('問い合わせ対応_内容と緊急度で担当へ振り分ける_三方向のトリアージ','01-業務プロセス','問い合わせを担当へ振り分ける','窓口へ集まる依頼を分類し、適切な対応経路へ振り分ける。','問い合わせ トリアージ 振り分け 受付 窓口 分類 緊急度 ルーティング',b,[slot(54,74,291,65,'依頼を一つの窓口へ'),slot(286,554,316,77,'内容・緊急度を判断'),slot(726,231,375,67,'専門担当が対応'),slot(726,414,375,67,'標準手順で回答'),slot(706,604,400,68,'継続課題として管理')])


def phased_delivery():
    b = path('M93 512H370V442H665V372H1101V556H93Z',FAINT)
    b += path('M93 512H370V442H665V372H1101',stroke=INK,sw=3)
    def slab(x,y,front=PALE):
        shape = poly(f'{x},{y} {x+164},{y} {x+206},{y-23} {x+42},{y-23}',WHITE,INK,2)
        shape += poly(f'{x},{y} {x+164},{y} {x+164},{y+28} {x},{y+28}',front,INK,2)
        shape += poly(f'{x+164},{y} {x+206},{y-23} {x+206},{y+5} {x+164},{y+28}',MID,INK,2)
        return shape
    b += slab(120,484,BLUE)
    b += slab(417,414)+slab(417,386,BLUE)
    b += slab(715,344)+slab(715,316)+slab(715,288,BLUE)
    for x,y,base in ((345,446,512),(641,348,442),(1028,250,372)):
        b += line(x,y+29,x,base,INK,3)
        b += circle(x,y,27,BLUE)+check(x-16,y-10,.87)
    b += arrow(138,589,1079,589,BLUE,5,21)
    return asset('導入推進_受入確認を重ねて成果を積み上げる_段階納品','01-業務プロセス','受入確認を重ねる段階納品','小さな成果を確認しながら、完成範囲を段階的に積み上げる。','段階納品 受入検査 段階導入 フェーズ インクリメント 検収 納品',b,[slot(75,342,254,70,'最初の成果'),slot(391,248,257,70,'機能を拡張'),slot(711,148,267,70,'全体を完成'),slot(773,434,336,72,'段階ごとに受入確認'),slot(294,621,614,65,'合意した成果から順に引き渡す')])


def expanding_rollout():
    b = circle(419,366,272,FAINT,INK,3)
    b += circle(419,366,191,PALE,BLUE,3)
    b += circle(419,366,110,WHITE,BLUE,3)
    b += circle(419,366,45,BLUE)+check(395,350,1.3)
    b += arrow(348,366,171,366,INK,5,20)
    b += path('M594 158H680V144H731',stroke=INK,sw=2.5)
    b += path('M610 366H731',stroke=BLUE,sw=2.5)
    b += path('M490 450H680V534H731',stroke=BLUE,sw=2.5)
    b += circle(594,158,9,INK)+circle(610,366,9,BLUE)+circle(490,450,9,BLUE)
    return asset('展開計画_利用範囲を確かめながら広げる_段階的な展開範囲','04-計画と進捗','利用範囲を確かめながら広げる','検証対象から全社利用へ、確認を重ねて展開範囲を広げる計画を示す。','段階展開 ロールアウト パイロット 全社導入 試行 利用範囲 横展開',b,[slot(753,107,374,74,'全社・全拠点へ展開',align='left'),slot(753,329,374,74,'関連部門へ拡大',align='left'),slot(753,497,374,74,'対象チームで検証',align='left'),slot(226,654,789,50,'確認できた範囲から広げる')])


def migration():
    b = rect(109,193,995,89,FAINT,19)+rect(109,443,995,89,PALE,19)
    b += path('M603 155V568M799 155V568',stroke=MID,sw=2,extra='stroke-dasharray="5 8"')
    b += line(620,238,1080,238,MID,4,'10 10')
    b += line(1080,220,1080,256,INK,3)
    b += arrow(132,488,770,488,BLUE,5,20)
    b += path('M132 238H602C691 238 712 488 800 488H1054',stroke=WHITE,sw=33)
    b += path('M132 238H602C691 238 712 488 800 488H1054',stroke=INK,sw=16)+poly('1085,488 1050,470 1050,506',INK)
    b += circle(603,238,21,WHITE,INK,4)+circle(799,488,21,WHITE,BLUE,4)
    b += path('M304 282V415',stroke=BLUE,sw=4,extra='stroke-dasharray="7 7"')+poly('304,439 292,414 316,414',BLUE)
    b += rect(253,325,40,52,WHITE,3,BLUE,2.5)+line(263,339,283,339,MID,2.5)+line(263,351,279,351,MID,2.5)
    b += path('M132 592V606H798V592',stroke=BLUE,sw=3)
    return asset('移行計画_並行運用から稼働系を切り替える_新旧の切替経路','04-計画と進捗','並行運用から稼働系を切り替える','旧環境と新環境の並行期間、データ移行、稼働系の切替点を説明する。','システム移行 切替 並行運用 データ移行 カットオーバー 新旧 更改',b,[slot(108,103,418,68,'現在の稼働環境',align='left'),slot(107,538,425,46,'移行先を準備・検証',align='left'),slot(839,140,292,62,'旧環境を終了'),slot(815,552,316,65,'新環境で稼働'),slot(332,327,252,76,'データを引き継ぐ',align='left'),slot(175,629,643,55,'並行運用しながら段階的に切替'),slot(538,59,329,68,'稼働系を切り替える')])


def converging_launch():
    upper = 'M95 152H329C496 152 549 359 809 359'
    middle = 'M95 359H810'
    lower = 'M95 566H329C496 566 549 359 809 359'
    b = path(upper,stroke=PALE,sw=65)+path(middle,stroke=FAINT,sw=65)+path(lower,stroke=PALE,sw=65)
    b += path(upper,stroke=BLUE,sw=6)+path(middle,stroke=INK,sw=6)+path(lower,stroke=BLUE,sw=6)
    b += circle(123,152,14,WHITE,BLUE,3)+circle(123,359,14,WHITE,INK,3)+circle(123,566,14,WHITE,BLUE,3)
    b += poly('821,330 1017,330 1017,295 1118,359 1017,423 1017,388 821,388',BLUE)
    b += circle(810,359,35,WHITE,INK,4)+check(790,345,1.05,BLUE)
    b += line(810,324,810,285,INK,2.5)
    return asset('リリース計画_部門の準備を一つの公開日に揃える_三系統の合流','04-計画と進捗','部門の準備を一つの公開日に揃える','開発・運用・事業の準備を合流させ、共通の公開条件へつなぐ。','リリース 公開 ローンチ 部門連携 準備 合流 開発 運用 営業',b,[slot(87,213,331,65,'開発の準備'),slot(87,412,331,65,'運用の準備'),slot(87,620,331,65,'事業の準備'),slot(600,192,419,73,'公開条件を揃える'),slot(863,463,287,72,'共通の公開日へ')])


def critical_path():
    b = path('M109 441H1092',stroke=PALE,sw=46)
    for x in (225,491,757):
        b += arrow(x,240,x,398,MID,4,19)
        b += poly(f'{x},182 {x+29},211 {x},240 {x-29},211',WHITE,INK,3)
    b += arrow(110,441,183,441,BLUE,7,19)
    b += arrow(263,441,451,441,BLUE,7,23)+arrow(529,441,717,441,BLUE,7,23)+arrow(795,441,990,441,BLUE,7,23)
    for x in (225,491,757):
        b += circle(x,441,34,WHITE,BLUE,5)+circle(x,441,10,PALE)
    b += circle(1030,441,35,BLUE)+check(1010,427,1.04)
    b += path('M157 581V594H1093V581',stroke=BLUE,sw=2.5)
    return asset('計画管理_完了日を左右する依存関係を示す_主要経路と補助工程','04-計画と進捗','完了日を左右する依存関係','完了日につながる主要経路と、それを支える工程の依存関係を示す。','クリティカルパス 依存関係 先行工程 マイルストーン 納期 工程 計画',b,[slot(112,93,226,66,'準備条件'),slot(376,93,230,66,'必要な確認'),slot(642,93,230,66,'関連作業'),slot(101,490,248,76,'着手条件を満たす'),slot(369,490,244,76,'中間成果を確定'),slot(635,490,244,76,'最終確認を終える'),slot(345,622,600,63,'下段が完了日を左右する主要経路')])


def delivery_schedule():
    b = rect(285,143,828,461,FAINT,21)
    for x in (355,513,671,829):
        b += line(x,143,x,604,PALE,2)
    b += path('M322 188H756L782 214V273H322Z',PALE)
    b += path('M471 343H906L932 369V429H471Z',PALE)
    b += path('M674 499H985V585H674Z',PALE)
    b += path('M322 188V273H782V214',stroke=BLUE,sw=3)
    b += path('M471 343V429H932V369',stroke=BLUE,sw=3)
    b += path('M674 499V585H985',stroke=BLUE,sw=3)
    b += path('M531 273V304Q531 321 548 321H615V322',stroke=INK,sw=4)+arrow(615,321,615,342,INK,4,15)
    b += path('M735 429V460Q735 477 752 477H814V478',stroke=INK,sw=4)+arrow(814,477,814,498,INK,4,15)
    b += circle(531,273,7,WHITE,INK,3)+circle(735,429,7,WHITE,INK,3)
    b += line(783,230,975,230,MID,3,'7 8')+line(933,386,975,386,MID,3)
    b += rect(983,128,14,489,INK,4)
    b += circle(990,230,12,WHITE,BLUE,3)+circle(990,386,12,WHITE,BLUE,3)+circle(990,542,12,WHITE,BLUE,3)
    b += arrow(307,655,1081,655,BLUE,3,16)
    return asset('進行管理_作業期間と引継ぎを同時に見る_連携するワークストリーム','04-計画と進捗','作業期間と引継ぎを同時に見る','複数の作業期間を並べ、次の担当へ渡す成果と完了条件を示す。','スケジュール ガント 作業計画 ワークストリーム 引継ぎ 並行作業 期間',b,[slot(60,194,201,73,'要件・設計'),slot(60,349,201,73,'制作・実装'),slot(60,505,201,73,'検証・準備'),slot(709,45,411,67,'共通の完了条件'),slot(351,199,373,58,'成果を次の担当へ渡す')])


def completion():
    b = ''
    for i,x in enumerate((104,462,820)):
        c=x+136
        b += poly(f'{x},480 {c},425 {x+272},480 {c},535',PALE if i<2 else FAINT,INK,2.5)
        if i == 0:
            b += rect(x+55,296,139,248,PALE,5,MID,2.5)
            b += poly(f'{x+67},279 {x+169},279 {x+207},317 {x+207},544 {x+67},544',WHITE,INK,3)
            b += path(f'M{x+169} 279V317H{x+207}',stroke=INK,sw=3)
            b += circle(c,387,40,BLUE)+check(c-22,371,1.23)
        elif i == 1:
            b += rect(x+66,279,141,265,WHITE,5,INK,3)
            b += line(x+87,304,x+168,304,MID,3)
            b += circle(c,387,49,PALE)
            b += path(f'M{c} 329A58 58 0 1 1 {c-58} 387',stroke=BLUE,sw=6)
            b += poly(f'{c-58},367 {c-69},392 {c-47},392',BLUE)
            b += rect(c-18,367,36,41,WHITE,3,BLUE,2.5)+line(c-9,379,c+8,379,MID,2.5)
        else:
            b += path(f'M{x+66} 544V279H{x+207}V544Z',WHITE,MID,3,extra='stroke-dasharray="9 8"')
            b += line(x+89,315,x+184,315,MID,3,'7 8')+line(x+89,338,x+168,338,MID,3,'7 8')
        b += poly(f'{x},480 {c},535 {x+272},480 {x+272},536 {c},591 {x},536',WHITE,INK,2.5)
        b += line(c,535,c,591,INK,2.5)
        b += poly(f'{x+16},500 {c-10},548 {c-10},561 {x+16},514',BLUE if i<2 else PALE)
    return asset('進捗報告_完了と進行中と未着手を分ける_成果の状態別整理','04-計画と進捗','成果を状態で分けて報告する','数量や達成率を仮定せず、完了・進行中・未着手の成果を整理する。','進捗 完了 進行中 未着手 残作業 成果 状態 ステータス',b,[slot(91,163,294,82,'受入済みの成果'),slot(440,163,316,82,'現在進めている作業'),slot(799,163,316,82,'これから取り組む範囲')])


def coordinating_hub():
    from math import hypot
    b = circle(600,360,178,FAINT)
    nodes = ((186,205),(1014,205),(186,515),(1014,515))
    for x,y in nodes:
        dx,dy=600-x,360-y
        length=hypot(dx,dy);ux,uy=dx/length,dy/length;nx,ny=-uy,ux
        sx,sy=x+ux*51,y+uy*51;ex,ey=600-ux*153,360-uy*153
        b += line(sx,sy,ex,ey,FAINT,35)
        b += arrow(sx+nx*10,sy+ny*10,ex+nx*10,ey+ny*10,BLUE,4,18)
        b += arrow(ex-nx*10,ey-ny*10,sx-nx*10,sy-ny*10,MID,4,18)
    b += circle(600,360,145,WHITE,INK,3)+circle(600,360,122,WHITE,BLUE,2.5)
    for x,y in nodes:
        b += circle(x,y,43,WHITE,INK,3)
    b += circle(186,194,12,BLUE)+path('M166 225q20-25 40 0',stroke=BLUE,sw=6)
    b += rect(994,185,40,40,BLUE,6)+check(1000,194,.8)
    b += path('M168 516l13 13 25-28',stroke=BLUE,sw=6)
    b += path('M997 515h34M1014 498v34',stroke=BLUE,sw=6)
    return asset('組織連携_調整役を中心に情報と判断を往復する_役割のハブ','03-関係と連携','調整役を中心に情報と判断を往復する','部門間の情報収集と判断の共有を担う調整役の位置づけを示す。','調整役 ハブ PMO 部門連携 情報共有 司令塔 コーディネーション',b,[slot(488,317,224,88,'全体を調整する役割'),slot(58,84,324,79,'現場の状況を集める'),slot(835,84,324,79,'方針を各担当へ'),slot(58,571,324,79,'課題を持ち寄る'),slot(835,571,324,79,'決定を実行へ')])


def traceable_collection():
    b = path('M342 159H438Q477 159 477 198V300Q477 329 506 329H758',stroke=PALE,sw=22)
    b += path('M342 359H596C633 359 630 382 667 382H758',stroke=PALE,sw=22)
    b += path('M342 559H438Q477 559 477 520V467Q477 437 507 437H758',stroke=PALE,sw=22)
    b += path('M342 159H438Q477 159 477 198V300Q477 329 506 329H733',stroke=INK,sw=4)+poly('758,329 733,317 733,341',INK)
    b += path('M342 359H596C633 359 630 382 667 382H733',stroke=BLUE,sw=4)+poly('758,382 733,370 733,394',BLUE)
    b += path('M342 559H438Q477 559 477 520V467Q477 437 507 437H733',stroke=MID,sw=4)+poly('758,437 733,425 733,449',MID)
    b += rect(91,111,250,96,WHITE,10,INK,3)+rect(91,311,250,96,WHITE,10,BLUE,3)+rect(91,511,250,96,WHITE,10,MID,3)
    b += circle(130,159,14,INK)+poly('130,343 146,359 130,375 114,359',BLUE)+rect(116,545,28,28,MID,3)
    b += path('M767 222C767 193 846 170 943 170C1040 170 1119 193 1119 222V521C1119 550 1040 573 943 573C846 573 767 550 767 521Z',WHITE,INK,3)
    b += ellipse(943,222,176,52,PALE,INK,3)
    for y in (329,382,437):
        b += line(767,y,807,y,MID,2.5)+circle(767,y,7,WHITE,INK,2.5)
        b += rect(808,y-17,269,34,FAINT,5)+line(858,y,1040,y,MID,3)
    b += circle(831,329,10,INK)+poly('831,371 842,382 831,393 820,382',BLUE)+rect(821,427,20,20,MID,2)
    return asset('情報管理_出所を保持して情報を集約する_三系統の来歴','03-関係と連携','出所を保持して情報を集約する','複数の情報源をまとめながら、元の出所をたどれる構造を示す。','情報集約 出所 来歴 トレーサビリティ データ統合 収集 ソース 根拠',b,[slot(161,124,166,70,'現場の記録'),slot(161,324,166,70,'顧客の情報'),slot(161,524,166,70,'外部の資料'),slot(783,68,335,64,'共通の情報基盤'),slot(432,615,667,70,'まとめても出所をたどれる')])


def strategy_cascade():
    b = poly('376,85 824,85 775,229 425,229',FAINT,INK,3)
    b += poly('376,85 824,85 813,119 387,119',INK)
    b += path('M475 229V272H300V322M725 229V272H900V322',stroke=BLUE,sw=7)
    b += poly('300,345 288,320 312,320',BLUE)+poly('900,345 888,320 912,320',BLUE)
    b += poly('138,347 462,347 493,430 107,430',PALE,BLUE,3)+poly('738,347 1062,347 1093,430 707,430',PALE,BLUE,3)
    b += path('M300 431V475H179V510M300 475H433V510M900 431V475H769V510M900 475H1023V510',stroke=INK,sw=4)
    for x in (179,433,769,1023):
        b += poly(f'{x},535 {x-10},510 {x+10},510',INK)
        b += poly(f'{x-91},539 {x+91},539 {x+101},654 {x-101},654',WHITE,INK,3)
        b += rect(x-66,641,132,13,BLUE,0)
    return asset('戦略実行_方針を重点領域と実務へ落とす_戦略の展開','03-関係と連携','方針を重点領域と実務へ落とす','経営方針を重点領域に分解し、現場の活動へつなぐ関係を示す。','戦略 方針展開 カスケード 経営計画 重点施策 実行 業務 アラインメント',b,[slot(434,141,332,68,'目指す成果・経営方針'),slot(157,357,286,64,'重点領域を定める'),slot(757,357,286,64,'実現条件を整える'),slot(94,552,170,72,'具体的な活動'),slot(348,552,170,72,'具体的な活動'),slot(684,552,170,72,'具体的な活動'),slot(938,552,170,72,'具体的な活動')])


def shared_bridge():
    b = rect(113,564,982,20,FAINT,0)
    b += rect(200,222,60,347,WHITE,0,INK,3)+rect(940,222,60,347,WHITE,0,INK,3)
    b += rect(193,216,74,28,INK,3)+rect(933,216,74,28,INK,3)
    b += path('M230 244Q600 522 970 244',stroke=BLUE,sw=5)
    for x in (344,458,572,628,742,856):
        t=(x-230)/740
        y=244+556*t*(1-t)
        b += line(x,round(y,3),x,453,MID,3)
    b += rect(123,453,477,55,BLUE,0)+rect(600,453,477,55,INK,0)
    b += path('M123 509H1077',stroke=INK,sw=3)
    b += arrow(282,480,536,480,WHITE,4,18)+arrow(918,480,664,480,WHITE,4,18)
    b += circle(600,480,42,WHITE,INK,3)+check(578,464,1.2,BLUE)
    b += rect(173,568,114,18,INK,3)+rect(913,568,114,18,INK,3)
    return asset('部門連携_共通の成果を両部門で支える_共同責任の橋','03-関係と連携','共通の成果を両部門で支える','部門ごとの役割を残しながら、共通成果に対する共同責任を示す。','共同責任 部門連携 共同作業 役割分担 境界 横断 共通成果 協業',b,[slot(67,113,310,80,'一方の部門・担当'),slot(823,113,310,80,'もう一方の部門・担当'),slot(403,272,394,75,'共通して実現する成果'),slot(79,615,322,67,'担当する役割'),slot(799,615,322,67,'担当する役割')])


GUIDANCE = {
    '業務改善_検査で品質を守る価値の流れ_二段階ゲート': {
        'use_case': '受注から成果物の納品までに必要な品質確認を説明する。',
        'message': '作業の前後で確認し、手戻りを防ぐ。',
        'reading': ['横の帯が受付から納品への流れ。', '二つのチェックゲートが着手条件と完成基準。', '中央の文書とペンが成果をつくる作業。'],
        'avoid': '帯の長さを作業時間の比率として扱わない。',
    },
    '業務改善_ボトルネックを迂回して負荷を逃がす_待ち行列と迂回路': {
        'use_case': '審査や処理の集中に対し、別担当への振り分けを提案する。',
        'message': '処理の制約に集まる負荷を、別経路で吸収する。',
        'reading': ['左の小さなブロックが処理待ち。', '狭い通路が処理能力の制約。', '上の経路が制約を避け、後工程へ合流する。'],
        'avoid': '通路の幅を処理件数の実数として扱わない。',
    },
    '意思決定_承認と差戻しの経路を分ける_判断ゲートと復帰路': {
        'use_case': '申請書類の承認基準と、不備がある場合の再申請を説明する。',
        'message': '基準を満たした申請は進み、未達の申請は修正へ戻る。',
        'reading': ['左の文書を中央の判断ゲートで確認する。', '主色の経路が承認後の前進。', '下の注意色の経路が提出元への差戻し。'],
        'avoid': '複数段階の決裁を一つの判断にまとめない。',
    },
    '品質保証_並行検証を揃えて次へ進む_三系統の同期': {
        'use_case': 'リリース前に機能・運用・安全性の確認を並行で実施する。',
        'message': '必要な確認結果がすべて揃ってから次へ進む。',
        'reading': ['左で三つの確認経路に分かれる。', '右の縦バーが結果を揃える条件。', '共通の出口から次の工程へ進む。'],
        'avoid': '一つの結果だけで進める条件には使わない。',
    },
    '障害対応_判断権限を段階的に引き継ぐ_責任者へのエスカレーション': {
        'use_case': '現場で解決できない障害を、判断できる責任者へ引き継ぐ。',
        'message': '解決に必要な権限を持つ相手まで、段階的につなぐ。',
        'reading': ['各段の丸が対応を担う相手。', '上向きの経路が次の責任者への引継ぎ。', '段の高さが判断権限の段階を示す。'],
        'avoid': '対応人数や処理時間を階段の大きさで比較しない。',
    },
    '組織学習_実行改善と前提見直しを分ける_二重のフィードバック': {
        'use_case': '施策の振り返りで、手順の修正と方針の再検討を切り分ける。',
        'message': '結果が悪いときは、手順だけでなく前提も見直せる。',
        'reading': ['中央の流れは方針・実行・観測。', '下の短いループが実行手順の改善。', '上の大きなループが方針や前提の見直し。'],
        'avoid': '二つの改善を必ず順番に実施する図として扱わない。',
    },
    '問い合わせ対応_内容と緊急度で担当へ振り分ける_三方向のトリアージ': {
        'use_case': '問い合わせ窓口で、依頼の内容に応じた対応先を決める。',
        'message': '依頼を一つの窓口で受け、適切な経路へ振り分ける。',
        'reading': ['左の異なる形が窓口に集まる依頼。', '中央の判断ゲートで対応方法を分類する。', '右の三つの経路が分類後の行き先。'],
        'avoid': '上下の並びを緊急度の順位として扱わない。',
    },
    '導入推進_受入確認を重ねて成果を積み上げる_段階納品': {
        'use_case': 'システム導入で、合意した機能から段階的に引き渡す。',
        'message': '確認できた成果を積み上げ、完成範囲を広げる。',
        'reading': ['階段が納品の段階。', '積み重なる層が完成済みの範囲。', '各段のチェックが受入確認。'],
        'avoid': '層の枚数を機能数や工数の実数として扱わない。',
    },
    '展開計画_利用範囲を確かめながら広げる_段階的な展開範囲': {
        'use_case': '新しい業務ツールを一部チームから全社へ展開する。',
        'message': '小さな範囲で確認しながら、利用対象を広げる。',
        'reading': ['内側が最初の検証チーム。', '外側の領域ほど利用範囲が広い。', '外向きの矢印が対象の拡大。'],
        'avoid': '円の面積を利用人数や費用の比率として扱わない。',
    },
    '移行計画_並行運用から稼働系を切り替える_新旧の切替経路': {
        'use_case': '既存システムから新環境への更改手順を共有する。',
        'message': '新環境を準備し、データを引き継いで稼働系を移す。',
        'reading': ['上段が旧環境、下段が新環境。', '太い経路が実際に稼働する環境の切替。', '下向きの点線がデータの引継ぎ。', '上段の終端バーが旧環境の終了。'],
        'avoid': '障害時の切戻し手順をこの一方向の経路で説明しない。',
    },
    'リリース計画_部門の準備を一つの公開日に揃える_三系統の合流': {
        'use_case': '開発・運用・事業部門の準備を共通の公開日に合わせる。',
        'message': '部門ごとの準備を揃えて、ひとつの公開判断につなぐ。',
        'reading': ['三つの帯が部門ごとの準備。', '中央のチェックにすべての経路が集まる。', '一本の出口が共通の公開。'],
        'avoid': '帯の長さを準備期間の比較に使わない。',
    },
    '計画管理_完了日を左右する依存関係を示す_主要経路と補助工程': {
        'use_case': '納期を守るために優先して管理する工程と前提条件を共有する。',
        'message': '主要経路の節目は、必要な条件が揃わないと進めない。',
        'reading': ['主色の太い経路が完了日を左右する工程。', '上の菱形が各節目の前提条件。', '下向きの矢印が前提と工程の依存関係。'],
        'avoid': '実際のクリティカルパスは所要期間と依存関係から確認する。',
    },
    '進行管理_作業期間と引継ぎを同時に見る_連携するワークストリーム': {
        'use_case': '要件・制作・検証を並行して進める計画の引継ぎ点を示す。',
        'message': '作業を重ねながら、必要な成果を次の担当へ渡す。',
        'reading': ['横の帯が担当ごとの作業期間。', '帯から出る矢印が成果の引継ぎ。', '右の縦バーが共通の完了条件。'],
        'avoid': '実日付や期間を比較する場合は時間軸を定義する。',
    },
    '進捗報告_完了と進行中と未着手を分ける_成果の状態別整理': {
        'use_case': '週次報告で成果を完了・進行中・未着手に分けて共有する。',
        'message': '成果の状態を分け、現在の仕事と残りの範囲を見せる。',
        'reading': ['チェック付きの文書が受入済み。', '回転矢印の文書が現在進行中。', '点線の文書がこれから取り組む範囲。'],
        'avoid': '三つの図の大きさを件数や達成率の比率として扱わない。',
    },
    '組織連携_調整役を中心に情報と判断を往復する_役割のハブ': {
        'use_case': '部門横断のプロジェクトでPMOや調整担当の役割を共有する。',
        'message': '調整役が情報を集め、判断を各担当へ返す。',
        'reading': ['中央が全体を調整する役割。', '周囲の丸が連携する担当。', '対になった矢印が情報と判断の往復。'],
        'avoid': '上下の指揮命令系統を示す組織図として使わない。',
    },
    '情報管理_出所を保持して情報を集約する_三系統の来歴': {
        'use_case': '現場・顧客・外部資料を集約する情報基盤の考え方を説明する。',
        'message': '情報をまとめても、元の出所との対応は残す。',
        'reading': ['左の形と色が情報源を識別する。', '別々の経路で共通の基盤へ取り込む。', '保存後の各行にも同じ識別記号が残る。'],
        'avoid': 'データへのアクセス権限まで保証する図として使わない。',
    },
    '戦略実行_方針を重点領域と実務へ落とす_戦略の展開': {
        'use_case': '経営方針を重点施策と現場の活動に結びつける。',
        'message': '日々の活動が、どの重点領域と経営方針につながるかを示す。',
        'reading': ['最上段が目指す成果や方針。', '中段が実現に必要な重点領域。', '下段が各領域を進める具体的な活動。'],
        'avoid': '所属や人数を表す組織図として使わない。',
    },
    '部門連携_共通の成果を両部門で支える_共同責任の橋': {
        'use_case': '開発と事業など、二部門が共通の成果を担う体制を説明する。',
        'message': '部門の役割は分かれていても、目指す成果は共通する。',
        'reading': ['左右の支柱がそれぞれの部門。', 'つながった橋が両者で支える取り組み。', '両側の矢印が中央の共通成果へ向かう。'],
        'avoid': '承認権限の上下関係を示す図として使わない。',
    },
}


def make_assets():
    items = [value_stream(), bottleneck(), approval_gateway(), parallel_validation(), escalation(), double_loop(), triage(), phased_delivery(), expanding_rollout(), migration(), converging_launch(), critical_path(), delivery_schedule(), completion(), coordinating_hub(), traceable_collection(), strategy_cascade(), shared_bridge()]
    identities = [
        ('process/quality-gates','sequential-flow-with-gates','left-to-right'),
        ('process/bottleneck-bypass','bypass-and-rejoin','left-to-right'),
        ('process/approval-return','decision-and-return','left-to-right'),
        ('process/parallel-validation','parallel-synchronization','left-to-right'),
        ('process/escalation','ordered-escalation','bottom-left-to-top-right'),
        ('process/double-loop-learning','nested-feedback','left-to-right'),
        ('process/inquiry-triage','classification-routing','left-to-right'),
        ('process/phased-acceptance','cumulative-delivery','left-to-right'),
        ('plan/expanding-rollout','nested-scope','inside-out'),
        ('plan/parallel-migration','parallel-tracks-with-switchover','left-to-right'),
        ('plan/converging-launch','converging-readiness','left-to-right'),
        ('plan/critical-dependencies','dependency-path','left-to-right'),
        ('plan/workstream-handoffs','overlapping-workstreams','left-to-right'),
        ('plan/completion-states','categorical-states','left-to-right'),
        ('relation/coordination-hub','bidirectional-hub','center-out'),
        ('relation/traceable-collection','source-preserving-collection','left-to-right'),
        ('relation/strategy-cascade','one-to-many-cascade','top-to-bottom'),
        ('relation/shared-responsibility','shared-outcome','outside-in'),
    ]
    for item, (key, relation, direction) in zip(items, identities):
        item['key'] = key
        item['layout'] = dict(relation=relation, reading_direction=direction)
        item['guidance'] = GUIDANCE[item['id']]
    return items
