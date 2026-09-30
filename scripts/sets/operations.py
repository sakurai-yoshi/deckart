"""Operational diagrams for handoffs, exceptions and service recovery."""
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER
from vector import path, rect, circle, line, poly, arrow, check, slot, asset


def item(key,name,title,description,keywords,body,labels,guidance,relation,direction='left-to-right'):
    a=asset(name,'01-業務プロセス',title,description,keywords,body,labels)
    a.update(key=key,kind='diagram',guidance=guidance,
             layout=dict(relation=relation,reading_direction=direction))
    return a


def responsibility_swimlane():
    # One responsibility row per role; crossings are actual ownership handoffs.
    b=''
    for y,fill in ((126,FAINT),(292,PALE),(458,FAINT)):
        b+=rect(70,y,1060,150,fill,0)
        b+=rect(70,y,166,150,INK if y==292 else WHITE,0)
        b+=line(237,y,237,y+150,MID,2)
    b+=path('M363 244V365H474',stroke=BLUE,sw=6)+poly('490,365 470,354 470,376',BLUE)
    b+=path('M678 365H700V531',stroke=BLUE,sw=6)+arrow(700,531,726,531,BLUE,6,16)
    b+=path('M927 531H1040V429',stroke=BLUE,sw=6)+poly('1040,408 1029,431 1051,431',BLUE)
    for x,y,w in ((273,158,180),(490,323,188),(726,489,202),(958,323,164)):
        b+=rect(x,y,w,84,WHITE,9,BLUE,3)
        b+=rect(x+15,y+15,5,54,BLUE,2)
    b+=circle(1040,253,22,BLUE)+check(1027,244,.72)
    b+=arrow(1040,319,1040,279,BLUE,4,15)
    return item('operations/responsibility-swimlane',
        '役割分担_担当をまたぐ引継ぎを追う_三者のスイムレーン',
        '担当をまたぐ引継ぎを追う','依頼者・受付・専門担当の担当範囲と、仕事を渡す順序を示す。',
        '責任分担 スイムレーン 引継ぎ 担当 業務フロー 窓口 依頼 swimlane handoff responsibility',b,
        [slot(81,165,143,76,'依頼者','役割'),slot(81,331,143,76,'受付窓口','役割',color=WHITE),
         slot(81,497,143,76,'専門担当','役割'),slot(300,171,138,60,'依頼する','作業'),
         slot(516,337,148,57,'内容を確認','作業'),slot(751,503,160,57,'処理する','作業'),
         slot(984,337,125,57,'回答する','作業')],
        dict(use_case='問い合わせ対応で、受付窓口と専門担当のどちらが何を担うかを説明する。',
             message='横の領域が担当範囲、領域をまたぐ矢印が引継ぎを表す。',
             reading=['上から依頼者・受付窓口・専門担当の担当範囲。','依頼は受付確認を経て専門担当へ渡る。','処理結果は受付窓口に戻り、回答で完了する。', '横位置は仕事を渡す順序を表す概念的な時間軸。']),
        'responsibility-swimlane')


def bounded_retry():
    # A failed execution has a bounded retry loop and a separate recovery exit.
    b=path('M100 284H1087',stroke=PALE,sw=44)
    b+=arrow(112,284,248,284,BLUE,7,23)
    b+=rect(252,224,271,120,WHITE,12,INK,3)
    b+=arrow(530,284,612,284,BLUE,6,21)
    b+=poly('616,284 705,190 794,284 705,378',WHITE,INK,3)
    b+=arrow(800,284,989,284,BLUE,7,23)+circle(1037,284,40,BLUE)+check(1015,269,1.15)
    b+=path('M705 380V454H642',stroke=AMBER,sw=6)+poly('620,454 644,442 644,466',AMBER)
    b+=poly('291,454 455,381 619,454 455,527',WHITE,AMBER,3)
    b+=path('M291 454H70V178Q70 150 98 150H359Q387 150 387 178V205',stroke=BLUE,sw=6)
    b+=poly('387,224 376,201 398,201',BLUE)
    b+=path('M455 529V577H791',stroke=AMBER,sw=6)+poly('816,577 789,564 789,590',AMBER)
    b+=rect(818,529,281,96,FAINT,12,INK,3)
    b+=circle(853,577,18,AMBER)+path('M853 565V579M853 587V588',stroke=WHITE,sw=3)
    return item('operations/bounded-retry',
        '例外対応_再試行と手動復旧を分ける_回数を制限した復帰路',
        '再試行と手動復旧を分ける','失敗した処理を条件付きで再試行し、解消しない場合は担当者へ引き継ぐ。',
        '例外 エラー 再試行 リトライ 手動復旧 回数制限 障害 自動処理 retry exception recovery',b,
        [slot(274,248,226,72,'処理を実行','処理'),slot(625,250,160,69,'成功したか','成功条件'),
         slot(825,202,166,57,'成功','結果'),slot(733,385,155,58,'失敗','分岐条件'),
         slot(350,414,210,80,'再試行\nできるか','再試行条件'),
         slot(153,68,321,62,'条件内なら再試行','再試行'),slot(480,594,285,62,'上限到達・再試行不可','例外'),
         slot(885,541,195,70,'担当者が復旧','復旧対応')],
        dict(use_case='自動処理が失敗したときの再試行条件と、担当者へ渡すタイミングを共有する。',
             message='同じ失敗を無制限に繰り返さず、復旧を担う人へ切り替える。',
             reading=['上段は実行から成功確認、完了への通常経路。','失敗した処理は下段の再試行条件へ進む。','条件内は実行へ戻り、上限到達や再試行不可は手動復旧へ進む。']),
        'bounded-retry-with-recovery')


def incident_containment():
    # A localized failure is isolated below a continuous unaffected service lane.
    b=rect(80,171,1040,145,PALE,15)+rect(80,409,1040,179,FAINT,15)
    b+=path('M92 244H1065',stroke=WHITE,sw=32)+arrow(95,244,1103,244,BLUE,10,29)
    b+=circle(257,244,34,WHITE,BLUE,3)+check(238,231,1.02,BLUE)
    b+=circle(966,244,34,BLUE)+check(947,231,1.02)
    b+=path('M112 422H947V574H112Z',stroke=AMBER,sw=2.5,extra='stroke-dasharray="8 7"')
    b+=rect(132,446,252,104,WHITE,12,AMBER,3)
    b+=circle(168,497,17,AMBER)+path('M168 486V499M168 507V508',stroke=WHITE,sw=3)
    b+=arrow(390,498,535,498,AMBER,6,22)
    b+=rect(550,446,238,104,WHITE,12,INK,3)
    b+=arrow(795,498,858,498,BLUE,6,21)
    b+=circle(900,498,38,WHITE,BLUE,3)+check(879,483,1.13,BLUE)
    b+=path('M941 498H1040V281',stroke=BLUE,sw=6)+poly('1040,257 1027,284 1053,284',BLUE)
    b+=circle(1040,244,10,WHITE,BLUE,3)
    return item('operations/incident-containment',
        '障害対応_影響箇所を隔離して通常提供を続ける_封じ込めと復旧確認',
        '影響箇所を隔離して提供を続ける','影響のない提供を継続しながら、障害箇所を隔離して復旧確認後に戻す。',
        '障害 影響範囲 隔離 封じ込め 復旧 サービス継続 インシデント containment incident isolation',b,
        [slot(107,64,447,76,'影響のない提供を継続','継続する範囲'),slot(190,463,178,70,'障害箇所','影響箇所'),
         slot(106,599,441,69,'影響箇所を隔離して対処','隔離'),slot(568,463,202,69,'原因を除く','復旧作業'),
         slot(812,584,284,66,'確認後に復帰','復帰条件')],
        dict(use_case='障害対応で、全体を止めずに影響箇所を切り離す方針と復旧条件を説明する。',
             message='影響範囲を限定し、確認が済むまで通常系へ戻さない。',
             reading=['上の太い経路は影響のない提供を続ける範囲。','下の破線の囲みが切り離して対処する影響範囲。','原因の除去と確認を経た経路だけが上段へ戻る。']),
        'isolation-and-verified-rejoin')


def controlled_rollback():
    # The new version receives a verification branch; rollback rejoins retained stable service.
    b=rect(99,181,1011,103,FAINT,14)+rect(371,408,739,103,PALE,14)
    b+=arrow(120,234,1082,234,INK,10,27)
    b+=circle(411,234,20,WHITE,INK,4)
    b+=path('M412 257V435Q412 459 438 459H542',stroke=BLUE,sw=7)+poly('565,459 540,447 540,471',BLUE)
    b+=rect(569,408,226,103,WHITE,10,BLUE,3)
    b+=arrow(803,459,867,459,BLUE,6,20)
    b+=poly('870,459 947,381 1024,459 947,537',WHITE,INK,3)
    b+=path('M947 540V603H200Q168 603 168 571V283',stroke=AMBER,sw=6)
    b+=poly('168,257 155,286 181,286',AMBER)+circle(168,234,10,WHITE,INK,3)
    b+=arrow(1027,459,1094,459,BLUE,6,18)
    b+=circle(1120,459,24,BLUE)+check(1107,450,.73)
    return item('operations/controlled-rollback',
        '変更管理_確認できない変更を安定版へ戻す_限定適用と切戻し',
        '確認できない変更を安定版へ戻す','安定版を残して変更を限定適用し、確認結果によって継続か切戻しかを分ける。',
        'リリース ロールバック 切戻し 変更管理 限定適用 安定版 確認 rollback release change',b,
        [slot(181,81,654,72,'安定版を残して提供を続ける','保持する状態'),slot(460,319,310,72,'変更を限定適用','変更範囲'),
         slot(589,424,186,71,'新しい版','変更後の状態'),slot(885,425,124,68,'確認','確認条件'),
         slot(1014,323,165,79,'問題なし\n継続','継続'),slot(301,625,550,60,'問題があれば安定版へ切り戻す','切戻し')],
        dict(use_case='システム変更時に、確認が取れない場合の戻り先と切戻し経路を共有する。',
             message='変更を試す前に戻り先を残し、結果で継続と切戻しを判断する。',
             reading=['上段は引き続き利用できる安定版。','分岐した下段で新しい版を限定適用し、確認する。','主色の出口は継続、注意色の経路は安定版への切戻し。']),
        'controlled-change-with-rollback')


def data_reconciliation():
    # Matching row identities expose one mismatch; correction returns to reconciliation.
    b=rect(85,192,314,340,WHITE,12,INK,3)+rect(801,192,314,340,WHITE,12,BLUE,3)
    b+=rect(85,192,314,57,INK,10)+rect(801,192,314,57,BLUE,10)
    for y in (293,377,461):
        b+=rect(107,y-23,270,47,FAINT,5)+rect(823,y-23,270,47,FAINT,5)
    b+=circle(139,293,11,INK)+circle(855,293,11,INK)
    b+=poly('139,365 151,377 139,389 127,377',BLUE)+poly('855,365 867,377 855,389 843,377',BLUE)
    b+=rect(128,450,22,22,MID,2)+rect(844,450,22,22,MID,2)
    for x in (174,890):
        b+=line(x,293,x+151,293,MID,4)+line(x,461,x+119,461,MID,4)
    b+=line(174,377,321,377,BLUE,4)+line(890,377,976,377,AMBER,5)
    b+=line(408,293,791,293,MID,3)+line(408,461,791,461,MID,3)
    b+=circle(600,293,22,BLUE)+check(587,284,.72)
    b+=circle(600,461,22,BLUE)+check(587,452,.72)
    b+=path('M407 377H558M642 377H791',stroke=AMBER,sw=4)
    b+=poly('563,377 600,340 637,377 600,414',WHITE,AMBER,3)
    b+=path('M588 365L612 389M612 365L588 389',stroke=AMBER,sw=3)
    correction='M600 417Q600 424 610 424H755Q775 424 775 444V575Q775 594 794 594H1138Q1162 594 1162 570V404Q1162 377 1135 377H1114'
    b+=path(correction,stroke=AMBER,sw=5)
    b+=line(775,449,775,473,WHITE,12)+line(775,449,775,473,AMBER,5)
    b+=poly('1090,377 1115,365 1115,389',AMBER)
    return item('operations/data-reconciliation',
        '移行検証_転記元と転記先の対応を照合する_不一致の検出と修正',
        '転記元と転記先の対応を照合する','同じ項目を左右で対応づけ、一致した項目と修正が必要な項目を分ける。',
        '照合 突合 検算 データ移行 転記 不一致 整合性 差異 修正 reconciliation matching',b,
        [slot(105,118,274,61,'転記元','照合元'),slot(821,118,274,61,'転記先','照合先'),
         slot(424,205,353,59,'同じ項目同士を照合','比較関係'),slot(444,493,306,61,'不一致だけを修正','差異への対応'),
         slot(503,620,570,64,'修正後に同じ項目を再照合','再確認')],
        dict(use_case='移行や転記の検証で、元データと反映先の不一致を確認して修正する。',
             message='全体を見比べるだけでなく、同じ項目の対応と不一致を確かめる。',
             reading=['左右の同じ記号が対応する項目。','チェックの行は一致し、注意色の行は不一致。','不一致の行を転記先で修正し、同じ対応で再照合する。', '行の長さは照合対象を区別する概念的な表現。']),
        'pairwise-reconciliation-with-correction')


def standby_failover():
    # The entry point is stable while the active route switches to the ready standby.
    b=rect(89,285,207,151,WHITE,16,INK,3)
    b+=path('M298 361H426',stroke=INK,sw=8)
    b+=circle(441,361,24,WHITE,INK,4)
    b+=path('M458 343L572 224H1018',stroke=MID,sw=6,extra='stroke-dasharray="9 9"')
    b+=path('M458 379L572 498H1018',stroke=BLUE,sw=9)+poly('1042,498 1013,481 1013,515',BLUE)
    b+=rect(632,155,257,138,WHITE,12,INK,3)+rect(632,429,257,138,WHITE,12,BLUE,3)
    b+=rect(652,175,217,30,FAINT,4)+rect(652,449,217,30,PALE,4)
    for x in (665,680,695):
        b+=circle(x,190,3,MID)+circle(x,464,3,BLUE)
    b+=circle(875,168,24,AMBER)+path('M875 155V170M875 179V180',stroke=WHITE,sw=3)
    b+=path('M760 295V388',stroke=MID,sw=3,extra='stroke-dasharray="5 7"')+poly('760,410 749,386 771,386',MID)
    b+=path('M976 213L998 235M998 213L976 235',stroke=AMBER,sw=5)
    b+=line(1018,203,1018,245,INK,3)
    b+=circle(1064,498,22,BLUE)+check(1051,489,.73)
    return item('operations/standby-failover',
        '業務継続_入口を変えずに待機系へ切り替える_主系と待機系の引継ぎ',
        '入口を変えずに待機系へ切り替える','利用者の入口を維持し、主系に問題が発生した場合に準備済みの待機系へ経路を切り替える。',
        'フェイルオーバー 待機系 主系 冗長化 業務継続 可用性 切替 障害 standby failover continuity',b,
        [slot(107,323,171,75,'共通の入口','入口'),slot(650,207,222,80,'障害が起きた\n主系','主系'),
         slot(651,488,220,65,'待機系へ切替','待機系'),slot(807,330,321,65,'平常時に状態を同期','同期'),
         slot(336,607,685,63,'異常時は利用経路を待機系へ切り替える','切替')],
        dict(use_case='業務システムの停止に備え、利用者の入口と主系・待機系の切替関係を説明する。',
             message='入口を保ったまま、準備済みの系へ処理を引き継ぐ。',
             reading=['左の入口から主系と待機系へ経路が分かれる。','上の点線は異常が起きた主系の経路。','下の太い経路が切替後の利用経路で、縦の点線は平常時の状態同期。']),
        'active-standby-failover')


def make_assets():
    from sets.manufacturing_diagrams import make_assets as manufacturing_assets
    return [responsibility_swimlane(), bounded_retry(), incident_containment(),
            controlled_rollback(), data_reconciliation(), standby_failover()] + manufacturing_assets()
