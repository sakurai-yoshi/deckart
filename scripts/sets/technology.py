"""Meaning-led explanations of AI, integration and data operations."""
from vector import INK, BLUE, MID, PALE, FAINT, WHITE, GRAY, AMBER
from vector import path, rect, circle, ellipse, line, poly, arrow, check, slot, asset, group

CATEGORY='12-AIとデータ基盤'
POSITIVE='#137D66'
NEGATIVE='#B5473A'


def _asset(key,name,title,description,keywords,body,labels,guidance):
    a=asset(name,CATEGORY,title,description,keywords,body,labels)
    a.update(key=key,kind='diagram',guidance=guidance)
    return a


def _page(x,y,w,h,color=BLUE,mark=True):
    return (path(f'M{x} {y}H{x+w-30}L{x+w} {y+30}V{y+h}H{x}Z',WHITE,INK,3)
        +poly(f'{x+w-30},{y} {x+w-30},{y+30} {x+w},{y+30}',PALE)
        +(rect(x+20,y+24,36,10,color,2) if mark else ''))


def _server(x,y,w=180,h=210):
    b=''
    for i in range(3):
        top=y+i*h/3
        b+=rect(x,top,w,h/3-9,INK,5)
        b+=line(x+20,top+21,x+w-62,top+21,MID,4)
        b+=circle(x+w-26,top+29,6,BLUE)
    return b


def _person(x,y,fill=INK):
    return circle(x,y,24,fill)+path(f'M{x-41} {y+93}V{y+70}Q{x-41} {y+38} {x} {y+38}Q{x+41} {y+38} {x+41} {y+70}V{y+93}Z',fill)


def rag_evidence():
    b=_page(85,158,192,176,mark=False)+_page(85,405,192,176,INK,mark=False)
    b+=circle(111,201,10,BLUE)+poly('101,448 111,438 121,448 111,458',INK)
    for y in (222,249,272,469,496,519):b+=line(111,y,247 if y not in (272,519) else 216,y,MID,5)
    b+=rect(105,239,153,22,PALE)+line(116,250,241,250,BLUE,4)
    b+=rect(105,486,153,22,PALE)+line(116,497,241,497,INK,4)
    b+=path('M286 250H342V316H410M286 497H342V404H410',stroke=MID,sw=4)
    b+=arrow(397,316,429,316,BLUE,4,15)+arrow(397,404,429,404,INK,4,15)
    b+=line(598,432,655,489,INK,22)+line(606,440,649,483,BLUE,11)
    b+=circle(531,357,112,WHITE,INK,10)
    b+=rect(462,305,138,37,PALE,4)+circle(479,323,6,BLUE)+line(496,323,582,323,BLUE,5)
    b+=rect(462,373,138,37,FAINT,4)+poly('473,391 479,385 485,391 479,397',INK)+line(496,391,582,391,INK,5)
    b+=path('M458 84H604Q621 84 621 101V157Q621 174 604 174H547L531 193L515 174H458Q441 174 441 157V101Q441 84 458 84Z',PALE)
    b+=arrow(531,206,531,234,BLUE,4,15)
    b+=arrow(665,357,820,357,BLUE,6,22)
    b+=_page(842,157,278,399)
    for y,w in ((215,218),(245,200),(275,218),(314,213),(344,170),(391,208)):
        b+=line(866,y,866+w,y,MID,5)
    b+=line(865,431,1096,431,PALE,3)
    b+=circle(878,471,10,BLUE)+line(904,471,1088,471,BLUE,4)
    b+=poly('868,511 878,501 888,511 878,521',INK)+line(904,511,1057,511,INK,4)
    b+=path('M651 499V599H984V556',stroke=MID,sw=3,extra='stroke-dasharray="7 7"')
    return _asset('technology/rag-evidence','AI活用_参照資料から根拠付き回答へ_検索と出典の対応',
        '参照資料から根拠付き回答へ','質問に関係する箇所を検索し、出典の対応を保って回答へ渡す。',
        'AI RAG 検索拡張生成 根拠 出典 引用 資料 検索 ナレッジ retrieval evidence citation grounding',b,
        [slot(73,76,221,61,'参照資料','検索対象'),slot(453,105,156,51,'質問','検索する問い'),
         slot(391,536,276,57,'関連する根拠','抽出する内容'),slot(817,75,330,61,'根拠付き回答','利用する結果')],
        dict(use_case='社内資料を参照するAIが、回答の根拠をどのように取り込むか説明する。',
             message='見つけた資料の内容と出典を、回答まで対応させる。',
             reading=['左の二枚が参照資料、上の吹き出しが質問。','拡大鏡の中で関連する箇所を選ぶ。','回答の下の丸と菱形が、元の資料との対応を示す。']))


def api_exchange():
    b=rect(62,203,275,300,WHITE,7,INK,4)+rect(62,203,275,42,INK,5)
    b+=circle(81,223,4,WHITE)+circle(96,223,4,MID)
    b+=rect(91,271,217,43,PALE,4)+rect(91,335,142,12,MID,3)+rect(91,363,190,12,MID,3)
    b+=rect(91,414,123,51,BLUE,5)
    b+=_server(899,212,231,289)
    b+=rect(523,210,152,288,FAINT,8,INK,3)
    b+=line(539,246,659,246,PALE,3)+line(539,463,659,463,PALE,3)
    b+=arrow(352,287,508,287,BLUE,5,20)+arrow(690,287,883,287,BLUE,5,20)
    b+=arrow(883,420,690,420,INK,5,20)+arrow(508,420,352,420,INK,5,20)
    b+=circle(599,287,25,WHITE,BLUE,5)+path('M585 278L594 287L585 296M603 278L612 287L603 296',stroke=BLUE,sw=3)
    b+=circle(599,420,25,WHITE,INK,5)+path('M613 411L604 420L613 429M595 411L586 420L595 429',stroke=INK,sw=3)
    b+=path('M558 332L545 354L558 376M640 332L653 354L640 376',stroke=INK,sw=5)
    b+=line(608,330,590,378,BLUE,5)
    return _asset('technology/api-request-response','システム連携_要求と応答を対応させる_APIの往復',
        'APIの要求と応答を対応させる','呼び出す側と提供する側の間で、要求と応答を別の経路として示す。',
        'API 連携 要求 応答 接続 インターフェース request response integration service',b,
        [slot(58,543,290,71,'呼び出すアプリ','呼び出し元'),slot(492,104,214,62,'共通のAPI','接続の窓口'),
         slot(885,543,264,71,'提供するサービス','呼び出し先'),slot(365,199,136,58,'要求','行きの情報'),slot(725,442,133,58,'応答','戻りの情報')],
        dict(use_case='二つのシステムをAPIで連携する際の基本的な通信方向を説明する。',
             message='要求を受けたサービスが、呼び出したアプリへ応答を返す。',
             reading=['上の矢印がアプリからサービスへの要求。','中央の二つの入口がAPIで受け渡す窓口。','下の矢印が元のアプリへ戻る応答。']))


def access_boundary():
    b=rect(450,118,680,479,FAINT,16,BLUE,3)
    b+=rect(447,250,8,104,WHITE)
    b+=_person(158,239,INK)+_person(158,464,GRAY)
    b+=rect(197,286,69,44,WHITE,4,BLUE,3)+circle(212,307,7,BLUE)+line(226,301,250,301,MID,3)+line(226,314,244,314,MID,3)
    b+=arrow(278,306,415,306,BLUE,5,21)
    b+=rect(418,251,97,111,WHITE,6,BLUE,3)
    b+=path('M466 268L495 280V306Q495 328 466 344Q437 328 437 306V280Z',PALE,INK,3)+check(448,295,.9,BLUE)
    b+=arrow(534,306,793,306,BLUE,6,23)
    b+=_server(813,215,235,252)
    b+=path('M238 509H383',stroke=GRAY,sw=4)
    b+=circle(409,509,21,WHITE,NEGATIVE,4)+path('M400 500L418 518M418 500L400 518',stroke=NEGATIVE,sw=4)
    return _asset('technology/access-boundary','情報保護_許可した要求だけを通す_権限確認と保護境界',
        '許可した要求だけを通す','権限確認を境界に置き、保護対象へ進む要求と止める要求を分ける。',
        'アクセス制御 認証 認可 権限 境界 保護 セキュリティ security boundary authorization access control',b,
        [slot(85,149,236,61,'権限のある利用者','許可される側'),slot(74,571,270,70,'権限のない利用者','拒否される側'),
         slot(666,136,389,60,'保護対象の領域','守る範囲'),slot(597,488,461,63,'許可した要求だけを通す','境界の働き')],
        dict(use_case='業務システムのアクセス制御で、権限確認を行う位置を説明する。',
             message='利用者の権限を確かめてから、保護対象へのアクセスを許可する。',
             reading=['囲まれた右側が保護対象の範囲。','上の要求は権限確認を通り、システムへ届く。','下の要求は境界の外で止まる。']))


def data_quality_pipeline():
    b=_page(43,225,184,242)+_page(66,202,184,242)+_page(89,179,184,242)
    b+=line(111,237,245,237,MID,5)+line(111,274,154,274,MID,5)+line(186,274,245,274,MID,5)
    b+=line(111,311,222,311,MID,5)+line(111,348,245,348,MID,5)
    b+=arrow(289,299,369,299,BLUE,5,18)
    b+=rect(386,177,173,250,WHITE,6,INK,3)
    for y in (236,299,362):b+=rect(406,y-15,37,30,PALE,3)+line(463,y,537,y,MID,4)
    b+=check(412,222,.65,BLUE)+check(412,285,.65,BLUE)
    b+=path('M415 355L434 374M434 355L415 374',stroke=NEGATIVE,sw=4)
    b+=arrow(575,267,656,267,BLUE,5,18)
    b+=path('M683 216V405a88 26 0 0 0 176 0V216',PALE,INK,3)
    b+=ellipse(771,216,88,26,WHITE,INK,3)
    b+=path('M683 276a88 26 0 0 0 176 0M683 339a88 26 0 0 0 176 0',stroke=MID,sw=3)
    b+=arrow(875,298,932,298,BLUE,5,18)
    b+=rect(950,198,207,186,WHITE,5,INK,4)+rect(950,198,207,25,INK,4)
    b+=rect(975,315,28,43,MID)+rect(1020,282,28,76,BLUE)+rect(1065,250,28,108,INK)
    b+=line(1035,385,1035,419,INK,4)+line(992,420,1080,420,INK,4)
    b+=path('M472 444V528',stroke=NEGATIVE,sw=4)+arrow(472,521,472,548,NEGATIVE,4,16)
    b+=rect(333,566,277,89,WHITE,5,NEGATIVE,3)+rect(333,566,11,89,NEGATIVE)
    return _asset('technology/data-quality-pipeline','データ運用_品質を確かめて利用へ渡す_検証と保留のデータ経路',
        '品質を確かめてデータを渡す','取り込んだデータを検証し、確認が必要なものを分けて利用へ渡す。',
        'データ パイプライン 取込 検証 品質 保留 整形 ETL validation data pipeline quality quarantine',b,
        [slot(45,83,267,61,'取込データ','入力'),slot(362,83,221,61,'品質の確認','検証'),
         slot(658,83,228,61,'整理された保存先','保存'),slot(933,457,237,61,'分析・業務で利用','利用先'),
         slot(356,582,232,57,'確認待ちのデータ','保留')],
        dict(use_case='データを取り込み、品質を確認して分析や業務へ提供する流れを説明する。',
             message='確認が必要なデータを分け、利用可能なデータだけを次へ渡す。',
             reading=['左の資料が取り込むデータ。','中央の検証で通過と確認待ちに分かれる。','上の経路は保存先と利用先へ、下の経路は確認待ちへ進む。']))


def human_review():
    b=rect(79,109,101,77,INK,5)
    for x in (96,120,144,168):b+=line(x,98,x,109,MID,4)+line(x,186,x,197,MID,4)
    b+=circle(102,135,5,WHITE)+circle(102,161,5,WHITE)+circle(158,148,6,BLUE)
    b+=path('M108 135L146 148L108 161',stroke=MID,sw=3)
    b+=_page(115,227,230,288)
    for y in (285,317,349,381,449):b+=line(139,y,314 if y!=449 else 285,y,MID,5)
    b+=rect(133,401,194,28,PALE)+line(145,415,306,415,AMBER,5)
    b+=circle(620,270,27,INK)+rect(607,289,26,29,MID,5)
    b+=path('M551 416V359Q551 317 593 317H649Q687 317 687 359V416Z',BLUE)
    b+=rect(561,346,121,123,WHITE,4,INK,3)+line(581,370,658,370,MID,4)+line(581,392,647,392,MID,4)
    b+=path('M557 353L542 420L571 434M682 353L699 417L671 438',stroke=MID,sw=12)
    b+=circle(574,434,8,PALE)+circle(669,438,8,PALE)
    b+=circle(709,238,34,WHITE,BLUE,4)+check(691,228,1,BLUE)
    b+=arrow(363,358,500,358,BLUE,5,20)+arrow(736,358,861,358,BLUE,5,20)
    b+=_page(880,227,231,288,INK)
    for y in (285,317,349,381):b+=line(904,y,1084 if y!=381 else 1047,y,MID,5)
    b+=circle(998,456,32,BLUE)+check(980,445,1,WHITE)
    b+=path('M620 487V575Q620 595 600 595H250Q230 595 230 575V545',stroke=INK,sw=4)+arrow(230,551,230,530,INK,4,15)
    return _asset('technology/ai-human-review','AI運用_下書きを人が確認して確定する_生成と公開の間の判断',
        'AIの下書きを人が確認する','生成された下書きを人が確認し、修正または確定へ進める。',
        'AI 人手確認 レビュー 下書き 生成 承認 修正 確定 human in the loop review draft approval',b,
        [slot(187,124,239,70,'AIの下書き','生成物'),slot(495,97,253,65,'人による確認','判断'),
         slot(853,124,285,70,'確認して確定','確定結果'),slot(330,611,382,60,'必要に応じて修正へ戻す','戻り経路')],
        dict(use_case='AIが作った文書や回答を、利用前に人が確認する運用を説明する。',
             message='下書きの生成と、利用してよいという判断を分ける。',
             reading=['左はAIが生成した確認前の下書き。','中央の人が内容を確認する。','確認を終えたものは右へ、修正が必要なものは下の経路で戻る。']))


def backup_recovery():
    b=_server(81,285,209,208)+_server(902,285,209,208)
    b+=circle(281,496,27,WHITE,NEGATIVE,4)+path('M270 485L292 507M292 485L270 507',stroke=NEGATIVE,sw=5)
    b+=path('M188 266V154Q188 132 210 132H582Q604 132 604 154V211',stroke=MID,sw=4)+arrow(604,198,604,223,BLUE,4,17)
    b+=circle(367,132,37,WHITE,INK,4)+path('M367 108V132L384 143',stroke=BLUE,sw=4)
    b+=rect(464,268,266,264,PALE,10,INK,3)
    b+=rect(484,247,226,22,MID,4)+rect(504,226,186,22,INK,4)
    b+=rect(491,302,212,182,WHITE,5,INK,3)
    b+=path('M551 371V358a46 46 0 0 1 92 0V371',stroke=INK,sw=6)
    b+=rect(541,357,112,78,BLUE,7)+circle(597,387,8,WHITE)+line(597,394,597,411,WHITE,5)
    b+=arrow(746,390,884,390,BLUE,6,24)
    b+=circle(1093,496,29,WHITE,BLUE,4)+check(1077,485,.95,BLUE)
    return _asset('technology/backup-recovery','事業継続_保存済みの状態から復旧する_事前バックアップと復元',
        '保存済みの状態から復旧する','障害前に保管したバックアップを使い、業務を再開できる状態へ復元する。',
        'バックアップ 復元 復旧 障害 事業継続 データ保全 backup recovery restore continuity snapshot',b,
        [slot(72,557,273,73,'障害が起きた環境','障害時'),slot(442,555,312,73,'保存済みバックアップ','復旧元'),
         slot(873,557,278,73,'復旧した環境','復旧先'),slot(409,51,315,62,'障害前に保存','事前の備え')],
        dict(use_case='バックアップの役割を、障害発生から復旧までの関係として説明する。',
             message='障害が起きた環境とは別に保管した状態から復旧する。',
             reading=['上の経路と時計が障害前の保存を表す。','左の停止した環境と中央の保管先を分けて読む。','右の矢印が保存済みの状態からの復元を表す。']))


def make_assets():
    return [rag_evidence(),api_exchange(),access_boundary(),data_quality_pipeline(),human_review(),backup_recovery()]
