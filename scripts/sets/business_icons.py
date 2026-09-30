"""Distinct business actions, tools and facilities on a 160-unit icon grid."""
from math import cos, sin, pi
from vector import INK, BLUE, MID, PALE, WHITE
from vector import path, rect, circle, ellipse, line, poly, arrow, group, asset


def _icon(key, name, title, description, keywords, body, use_case, message, reading):
    item=asset(name,'08-アイコンとピクトグラム',title,description,keywords,body,size=(160,160))
    item.update(key='icon/'+key,kind='icon',guidance=dict(use_case=use_case,message=message,reading=reading))
    return item


def _invoice():
    b=path('M37 18H123V143L109 134L94 143L80 134L66 143L51 134L37 143Z',WHITE,INK,7)
    b+=line(55,42,88,42,BLUE,8)+line(55,68,79,68,INK,6)+line(98,68,106,68,BLUE,6)
    b+=line(55,89,79,89,INK,6)+line(98,89,106,89,BLUE,6)
    b+=line(53,110,107,110,INK,5)+rect(80,118,29,8,BLUE,2)
    return _icon('invoice','請求管理_明細と金額を通知する_請求明細','請求','支払を求める金額と明細を示す。','請求 請求書 明細 売掛 支払依頼 invoice billing receivable',b,
        '取引の請求書発行や請求内容の確認を示す。','項目別の明細をまとめ、支払を求める。',
        ['紙の下端の切り取り形が請求明細を表す。','左右に分かれた行が項目と金額、下の線が合計を示す。'])


def _manufacturing():
    b=rect(30,22,19,51,INK,2)+rect(58,35,17,40,INK,2)
    b+=path('M19 137V80L59 58V80L99 58V80L140 58V137Z',PALE,INK,7)
    for x in (37,71,105):b+=rect(x,98,17,17,BLUE,1)
    b+=line(15,139,145,139,INK,7)
    return _icon('manufacturing','生産管理_製品を製造する_工場','製造','原料や部品を製品にする製造工程を示す。','製造 工場 生産 加工 製品 manufacturing factory production',b,
        '製造部門や生産工程を業務フローに配置する。','工場で製品を生産する。',
        ['連続する鋸屋根が工場の作業棟を表す。','煙突と窓の並びが製造設備のある場所を示す。'])


def _authentication():
    b=path('M31 67C31 34 54 18 80 18C108 18 132 38 132 70V91M21 88V71',stroke=INK,sw=7)
    b+=path('M44 92V70C44 47 59 33 80 33C102 33 117 49 117 71V91C117 116 111 133 100 144',stroke=BLUE,sw=7)
    b+=path('M29 112C32 105 32 97 32 89M45 132C57 118 59 107 59 86V71C59 58 67 49 80 49C93 49 102 59 102 72V90C102 111 97 130 84 143',stroke=INK,sw=7)
    b+=path('M62 142C78 125 85 107 85 86V74C85 69 81 65 77 68M72 82V93C72 107 68 118 62 127',stroke=BLUE,sw=7)
    return _icon('authentication','本人確認_利用者を識別する_指紋','本人認証','登録された本人かを確かめる認証を示す。','本人確認 認証 指紋 ログイン identity authentication fingerprint login',b,
        '本人認証やログイン確認の工程を示す。','利用者の同一性を確かめる。',
        ['曲線の層が指紋の固有な模様を表す。','中央へ巻き込む線が一人に対応する特徴を示す。'])


def _sustainability():
    b=path('M56 83C48 42 82 18 134 24C138 72 110 100 70 91Z',PALE,INK,7)
    b+=path('M62 94L111 48M80 77L78 53M93 65L117 68',stroke=BLUE,sw=6)
    b+=path('M18 116L46 99Q54 94 64 98L89 109H106Q117 109 115 118L132 105Q139 101 143 108Q146 113 139 120L112 140H59L37 134L23 143Z',WHITE,INK,7)
    b+=line(67,119,107,119,BLUE,6)
    return _icon('sustainability','環境配慮_自然資源を守る_手の上の葉','環境への配慮','事業活動で自然資源を守る取り組みを示す。','環境 資源 自然 サステナビリティ sustainability environment ecology',b,
        '環境保全や資源への配慮を事業方針で示す。','自然資源を支えながら事業を続ける。',
        ['葉が自然と資源を表す。','下の手が保全し支える行為を表す。'])


def _star(cx,cy,outer=18,inner=8,fill=BLUE):
    points=[]
    for i in range(10):
        angle=-pi/2+i*pi/5;r=outer if i%2==0 else inner
        points.append(f'{cx+r*cos(angle):.3f},{cy+r*sin(angle):.3f}')
    return poly(' '.join(points),fill)


def _yen(x,y,scale=1,color=INK):
    return group(path('M0 0L14 15L28 0M14 15V37M2 18H26M2 27H26',stroke=color,sw=5),x,y,scale)


def _recruitment():
    b=circle(61,49,24,INK)+path('M18 137V119C18 99 34 87 61 87C88 87 105 99 105 119V137Z',PALE,INK,7)
    b+=line(119,65,119,111,BLUE,10)+line(96,88,142,88,BLUE,10)
    return _icon('recruitment','採用活動_新たな人材を迎える_人物と追加','採用','新しい人材を組織に迎えることを示す。','採用 募集 入社 人材 増員 recruitment hiring join',b,
        '採用計画や募集する職種の見出しに添える。','組織に新たな人材を加える。',['人物の輪郭が迎える人材を表す。','右の加号が新たに加わることを表す。'])


def _development():
    b=path('M58 139V114H86V88H114V62H142V139Z',PALE,INK,7)
    b+=circle(37,54,17,BLUE)+path('M18 119V98Q18 80 37 80Q56 80 56 98V119Z',BLUE)
    b+=arrow(64,58,119,23,INK,6,18)
    return _icon('development','人材育成_能力を段階的に伸ばす_人物と成長段階','人材育成','能力や経験を段階的に伸ばす育成を示す。','育成 成長 能力 スキル キャリア development growth skills coaching',b,
        '育成計画や段階別のスキル習得を紹介する。','経験を積みながら能力の段階を上げる。',['人物の横の階段が習得段階を表す。','上向きの矢印が成長する方向を示す。'])


def _performance():
    b=_star(35,38,17,8,INK)+_star(80,28,22,10,BLUE)+_star(125,38,17,8,INK)
    b+=circle(80,81,20,INK)+path('M37 143V128Q37 111 62 111H98Q123 111 123 128V143Z',PALE,INK,7)
    return _icon('performance','人事評価_個人の成果を振り返る_人物と評価','人事評価','個人の成果や行動を評価する場面を示す。','評価 成果 人事査定 査定 フィードバック performance appraisal evaluation',b,
        '人事評価や成果の振り返りの項目に添える。','個人の仕事ぶりを評価する。',['下の人物が評価の対象を表す。','上の星の並びが評価という観点を表す。'])


def _transfer():
    b=circle(40,48,18,INK)+path('M16 99V91Q16 76 40 76Q64 76 64 91V99Z',INK)
    b+=circle(120,103,18,BLUE)+path('M95 147V142Q95 129 120 129Q145 129 145 142V147Z',BLUE)
    b+=path('M82 40H122Q140 40 140 58V61',stroke=BLUE,sw=7)+poly('130,60 140,78 150,60',BLUE)
    b+=path('M78 136H40Q20 136 20 125',stroke=INK,sw=7)+poly('10,125 20,107 30,125',INK)
    return _icon('staff-transfer','配置変更_担当者の異動を示す_人員の入替','異動・配置変更','人員を別の役割や所属へ移すことを示す。','異動 配置 転任 人員 交代 staff transfer reassignment rotation',b,
        '人事異動や担当の入れ替えを説明する。','人員の配置が変わる。',['二つの人物が異なる配置先を表す。','逆向きの矢印が配置の入れ替えを示す。'])


def _attendance():
    b=rect(30,44,100,98,PALE,8,INK,7)+rect(53,17,54,38,WHITE,3,INK,7)
    b+=line(64,29,96,29,BLUE,5)+line(45,59,115,59,INK,6)
    b+=circle(80,102,27,WHITE,BLUE,6)+path('M80 85V103L93 111',stroke=INK,sw=6)
    return _icon('attendance','勤怠記録_出退勤時刻を記録する_打刻時計','勤怠・打刻','出退勤時刻を記録する勤怠管理を示す。','勤怠 打刻 出勤 退勤 労働時間 attendance timecard timekeeping',b,
        '出退勤の記録や勤怠管理の見出しに使う。','働いた時刻を記録する。',['上から差し込むカードが記録を表す。','下の時計が出退勤の時刻を表す。'])


def _payroll():
    b=path('M18 79L80 36L142 79V139H18Z',PALE,INK,7)
    b+=rect(38,19,84,91,WHITE,3,INK,7)+_yen(66,35,.9,BLUE)
    b+=path('M18 79L80 119L142 79V139H18Z',PALE,INK,7)
    b+=line(18,139,56,105,INK,6)+line(142,139,104,105,INK,6)
    return _icon('payroll','給与管理_報酬を支給する_給与封筒','給与・報酬','働いた人へ報酬を支給することを示す。','給与 報酬 賃金 給料 人件費 payroll salary compensation wages',b,
        '給与計算や報酬制度の見出しに添える。','従業員へ仕事の対価を支給する。',['封筒が個人へ渡す支給物を表す。','中の金額記号が金銭の報酬を表す。'])


def _remote_work():
    b=path('M17 74L80 20L143 74M31 64V140H129V64',stroke=INK,sw=7)
    b+=rect(48,74,65,42,PALE,3,BLUE,6)+line(81,117,81,127,INK,6)+line(65,129,97,129,INK,6)
    b+=path('M110 24V42L127 57V24Z',INK)
    return _icon('remote-work','勤務形態_自宅から働く_住居と業務端末','在宅勤務','住居から業務端末を使って働く形態を示す。','在宅勤務 テレワーク リモート勤務 自宅 remote work home office telework',b,
        '在宅勤務の制度や勤務場所を説明する。','自宅を仕事の場所として利用する。',['家の輪郭が住居を表す。','内部の画面が業務用の端末を表す。'])


def _contract():
    b=path('M30 18H94L117 41V141H30Z',WHITE,INK,7)+path('M94 18V42H117',PALE,INK,7)
    b+=line(47,57,85,57,INK,6)+line(47,78,83,78,INK,6)
    b+=path('M48 119Q57 104 61 117Q63 127 73 112L82 117',stroke=BLUE,sw=5)
    b+=poly('91,96 124,45 141,56 108,107 87,115',BLUE,INK,6)+line(119,54,135,64,WHITE,4)
    return _icon('contract','契約手続_合意内容に署名する_契約書とペン','契約','合意した条件を文書で取り交わす手続きを示す。','契約 署名 合意 契約書 締結 contract signature agreement',b,
        '契約確認や署名の手続きを示す。','合意した内容を文書に残す。',['本文のある紙が合意条件を表す。','署名とペンが文書を取り交わす行為を表す。'])


def _payment():
    b=rect(17,37,126,87,PALE,9,INK,7)+rect(20,56,120,20,INK)
    b+=rect(35,89,22,17,BLUE,3)+line(82,103,140,103,BLUE,8)+poly('123,84 145,103 123,122',BLUE)
    return _icon('payment','支払手続_代金を決済する_カード決済','支払・決済','商品やサービスの代金を支払う行為を示す。','支払 決済 代金 カード 振込 payment settlement checkout',b,
        '代金支払や決済の工程に配置する。','取引の代金を支払う。',['カードの帯とチップが決済手段を表す。','外向きの矢印が代金を渡す行為を表す。'])


def _budget():
    b=rect(24,18,83,125,PALE,7,INK,7)+rect(40,34,52,25,BLUE,3)
    for x,y in ((43,78),(67,78),(43,101),(67,101),(43,124),(67,124)):b+=rect(x,y,10,10,INK,2)
    b+=circle(114,111,30,WHITE,INK,7)+_yen(101,92,.92,BLUE)
    return _icon('budget','予算管理_必要な金額を計画する_計算機と資金','予算','必要な費用を見積もり金額を計画することを示す。','予算 計画 見積 金額 配分 budget planning estimate finance',b,
        '予算策定や費用計画の項目を示す。','使える金額と必要な費用を計画する。',['計算機が金額の検討を表す。','横の硬貨が計画する資金を表す。'])


def _expense():
    b=path('M25 47L113 23V61H25Z',PALE,INK,7)+rect(18,54,124,83,WHITE,9,INK,7)
    b+=path('M141 80H101Q90 80 90 95Q90 110 101 110H141Z',BLUE,INK,6)+circle(107,95,5,WHITE)
    b+=arrow(53,86,53,135,BLUE,7,18)
    return _icon('expense','経費管理_業務に必要な費用を支出する_財布と支出','経費','業務に必要な費用を支出することを示す。','経費 支出 費用 精算 立替 expense cost reimbursement spending',b,
        '経費精算や支出項目の見出しに添える。','仕事に必要な費用が発生する。',['開いた財布が支払に使う資金を表す。','下向きの矢印が資金の支出を表す。'])


def _tax():
    b=poly('18,51 80,17 142,51',PALE,INK,7)+line(18,139,142,139,INK,8)+line(27,123,133,123,INK,7)
    b+=rect(31,65,13,48,INK,1)+rect(116,65,13,48,INK,1)
    b+=line(65,109,96,67,BLUE,7)+circle(66,73,9,WHITE,BLUE,6)+circle(95,104,9,WHITE,BLUE,6)
    return _icon('tax','税務手続_公的な負担を計算する_行政と税率','税務','税額の計算や申告などの税務を示す。','税 税務 税金 申告 納税 消費税 tax taxation filing',b,
        '税務処理や申告・納付の項目を示す。','公的な税の負担を扱う。',['正面の柱と屋根が公的な制度を表す。','中央の百分率記号が税率と税額の計算を表す。'])


def _cash_flow():
    b=circle(51,61,29,WHITE,INK,7)+_yen(39,42,.87,BLUE)
    b+=circle(110,111,29,PALE,INK,7)+_yen(98,92,.87,BLUE)
    b+=path('M87 26H121Q140 26 140 46V59',stroke=BLUE,sw=7)+poly('128,49 140,69 152,49',BLUE)
    b+=path('M75 140H39Q19 140 19 120V107',stroke=INK,sw=7)+poly('7,116 19,96 31,116',INK)
    return _icon('cash-flow','資金管理_入金と出金の流れを捉える_循環する資金','資金繰り','資金の入金と出金の流れを示す。','資金繰り 資金 キャッシュフロー 入金 出金 cash flow liquidity finance',b,
        '入出金や運転資金の流れを説明する。','資金が入出金を通じて動く。',['二つの硬貨が異なる時点の資金を表す。','上下の矢印が資金の流れを表す。'])

def _parcel(x,y,w=70,h=64):
    b=rect(x,y,w,h,PALE,2,INK,6)+rect(x+w*.4,y,w*.2,h*.38,BLUE)
    b+=line(x+w*.2,y+h*.75,x+w*.42,y+h*.75,INK,5)
    return b


def _procurement():
    b=path('M16 31H31L48 111H127L143 58H39',PALE,INK,7)
    b+=circle(57,133,10,INK)+circle(120,133,10,INK)
    b+=arrow(89,18,89,77,BLUE,8,21)+line(53,95,127,95,INK,5)
    return _icon('procurement','購買活動_必要な物品を調達する_購買カート','調達・購買','必要な物品や原材料を購入することを示す。','調達 購買 仕入 購入 原材料 procurement purchasing sourcing',b,
        '調達や仕入の工程を業務フローに配置する。','必要な物品を外部から購入する。',['カートが購買を表す。','中へ入る矢印が必要な物品を取り入れる行為を表す。'])


def _warehouse():
    b=path('M18 64L80 23L142 64V140H18Z',WHITE,INK,7)+rect(39,68,82,72,PALE,0,INK,6)
    b+=line(43,84,118,84,INK,5)+line(43,99,118,99,INK,5)
    b+=_parcel(67,112,34,28)+_parcel(26,115,34,25)
    return _icon('warehouse','保管管理_物品を倉庫に置く_倉庫と荷物','倉庫・保管','入出庫する物品の保管場所を示す。','倉庫 保管 物流 拠点 ストック warehouse storage depot',b,
        '物品の保管場所や物流拠点を示す。','物品をまとめて保管する場所がある。',['大きな入口を持つ建物が倉庫を表す。','入口付近の箱が保管する荷物を示す。'])


def _delivery():
    b=path('M18 39H95V118H18Z',PALE,INK,7)+path('M95 65H122L144 91V118H95Z',WHITE,INK,7)
    b+=path('M105 77H117L132 94H105Z',BLUE)
    b+=circle(47,124,14,WHITE,INK,7)+circle(120,124,14,WHITE,INK,7)
    b+=line(9,62,39,62,BLUE,6)+line(10,82,30,82,BLUE,6)
    return _icon('delivery','配送管理_荷物を届ける_配送トラック','配送','荷物を目的地へ運ぶ配送を示す。','配送 配達 輸送 運送 物流 delivery shipping logistics truck',b,
        '出荷後の配送工程や輸送手段の項目に添える。','荷物を次の場所へ届ける。',['荷台のある車が荷物の運搬を表す。','車輪と前方の窓が移動する向きを示す。'])


def _inventory():
    b=_parcel(54,20,54,50)+_parcel(23,82,54,50)+_parcel(88,82,54,50)
    b+=line(17,144,147,144,INK,7)
    return _icon('inventory','在庫管理_保有する物品を数える_積み上げた箱','在庫','保有している物品や在庫のまとまりを示す。','在庫 棚卸 保有 物品 stock inventory goods',b,
        '在庫管理や棚卸の見出しに添える。','保有している物品の量を管理する。',['並ぶ箱が保有する物品を表す。','積み上がったまとまりが在庫を表す。'])


def _inspection():
    b=_parcel(19,49,84,86)
    b+=line(115,92,144,121,BLUE,10)+circle(105,63,34,WHITE,INK,7)
    b+=path('M89 64L101 76L122 50',stroke=BLUE,sw=7)
    return _icon('inspection','検品作業_受け取った品物を確認する_荷物と検査','検品','物品の状態を調べて受入基準を確認する。','検品 検査 受入 不良 確認 inspection checking acceptance',b,
        '納品された品物の検品工程を示す。','品物の状態を確認して受け入れる。',['箱が検品する物品を表す。','拡大鏡とチェックが状態を確かめる行為を表す。'])


def _returns():
    b=_parcel(38,78,86,65)
    b+=path('M133 62V48Q133 26 109 26H44',stroke=BLUE,sw=8)+poly('54,12 30,26 54,40',BLUE)
    return _icon('returns','返品手続_品物を差し戻す_荷物と戻り矢印','返品','受け取った品物を返す手続きを示す。','返品 返送 交換 返却 return reverse logistics',b,
        '返品受付や返送の工程に配置する。','品物を送り元へ戻す。',['箱が返す品物を表す。','上を戻る矢印が返送の向きを表す。'])


def _database():
    b=path('M29 43V119C29 133 51 143 80 143C109 143 131 133 131 119V43Z',PALE,INK,7)
    b+=path('M29 80C29 94 51 104 80 104C109 104 131 94 131 80M29 111C29 125 51 135 80 135C109 135 131 125 131 111',stroke=BLUE,sw=6)
    b+=ellipse(80,43,51,23,WHITE,INK,7)
    return _icon('database','データ管理_構造化した情報を蓄積する_データベース','データベース','構造化した情報をまとめて蓄積する場所を示す。','データベース DB データ 保存 蓄積 database storage structured data',b,
        'システム構成でデータの保管先を示す。','データを一か所に蓄積して利用する。',['円柱の輪郭がデータベースを表す。','横に区切られた層が蓄積する情報を表す。'])


def _synchronization():
    b=path('M28 65C37 27 82 16 113 36L132 52',stroke=INK,sw=9)+poly('140,64 112,54 132,33',BLUE)
    b+=path('M132 96C123 134 78 145 47 125L28 109',stroke=INK,sw=9)+poly('20,97 48,107 28,128',BLUE)
    return _icon('synchronization','同期処理_情報の状態をそろえる_双方向の循環','同期','複数の場所にある情報の状態をそろえる処理を示す。','同期 更新 双方向 データ sync synchronization refresh',b,
        '端末間やシステム間の同期処理を示す。','双方の情報を同じ状態へ更新する。',['円周に沿う二つの矢印が更新の往復を表す。','一周する経路が繰り返し同期することを表す。'])


def _analytics():
    b=line(22,139,143,139,INK,7)+line(22,139,22,23,INK,7)
    b+=rect(39,99,22,34,MID,2)+rect(76,76,22,57,BLUE,2)+rect(113,50,22,83,INK,2)
    b+=path('M38 77L80 51L116 25',stroke=BLUE,sw=7)+poly('106,17 135,13 126,42',BLUE)
    return _icon('analytics','分析活動_傾向と差を読み取る_棒と推移','分析','数値の比較や変化から傾向を読み取ることを示す。','分析 数値 データ 傾向 可視化 analytics analysis insights',b,
        'データ分析や実績の検討の見出しに添える。','データから傾向を読み取る。',['高さの異なる棒が比較対象の違いを表す。','上の線が変化の傾向を表す。'])


def _automation():
    b=rect(22,126,70,18,INK,3)+path('M39 125V109L78 72L92 86L65 122Z',PALE,INK,7)
    b+=path('M82 70L48 40L66 22L110 62Z',BLUE,INK,7)+circle(88,76,13,WHITE,INK,6)
    b+=circle(57,31,12,WHITE,INK,6)+line(65,22,103,22,INK,8)
    b+=path('M103 22L130 42V70M130 54L111 67V85M130 54L147 67V85',stroke=INK,sw=7)
    return _icon('automation','自動化_繰り返す作業を機械へ任せる_自動アーム','自動化','決まった作業を機械や仕組みに任せることを示す。','自動化 自動処理 省力 ロボット RPA automation robotic process',b,
        '繰り返し作業の自動化や省力化を紹介する。','決まった作業を仕組みが実行する。',['関節を持つアームが自動で動く機構を表す。','先端の爪が作業を実行する部分を表す。'])


def _api():
    b=path('M53 28L15 80L53 132M107 28L145 80L107 132',stroke=INK,sw=8)
    b+=line(92,27,68,133,BLUE,8)
    b+=circle(32,80,8,BLUE)+circle(128,80,8,BLUE)
    return _icon('api','外部連携_機能をインターフェースで呼び出す_コード接続','API連携','定められたインターフェースで機能を呼び出す連携を示す。','API インターフェース 連携 プログラム 接続 integration interface code API',b,
        'システム間のAPI連携やプログラムとの接続を示す。','決まった形式で機能を呼び出す。',['左右の括弧がプログラムのインターフェースを表す。','両側の点が接続の両端を表す。'])


def _server():
    b=''
    for y in (20,65,110):
        b+=rect(24,y,112,32,PALE,5,INK,7)+circle(43,y+16,5,BLUE)+line(70,y+16,116,y+16,INK,6)
    return _icon('server','設備表示_処理を提供する_サーバー','サーバー','データ処理やサービスを提供する機器を示す。','サーバー 機器 インフラ ホスティング server infrastructure hosting compute',b,
        'システム構成で処理を担う機器を示す。','サービスを提供する処理基盤がある。',['積み重なる筐体がサーバー機器を表す。','各段の点と横線が稼働部を示す。'])


def _version_control():
    b=line(45,39,45,125,INK,9)+path('M115 40V73Q115 94 89 94H69Q45 94 45 113',stroke=BLUE,sw=8)
    for x,y,c in ((45,28,INK),(45,133,INK),(115,28,BLUE)):b+=circle(x,y,14,WHITE,c,7)
    return _icon('version-control','変更管理_別の変更を統合する_分岐と合流','版管理','変更の履歴や別の作業の統合を示す。','版管理 バージョン 履歴 ブランチ 統合 Git version control merge',b,
        '文書やコードの変更管理を説明する。','別の変更を履歴として管理し統合する。',['縦の線と点が変更の履歴を表す。','横から合流する線が別の変更の統合を表す。'])


def _key():
    b=circle(55,54,32,PALE,INK,8)+circle(49,48,9,WHITE,BLUE,6)
    b+=path('M78 77L138 137M104 103L119 88M121 120L136 105',stroke=INK,sw=13)
    return _icon('key','アクセス管理_解錠に使う情報を扱う_鍵','鍵・認証情報','対象を開くための鍵や認証情報を示す。','鍵 秘密鍵 キー 認証情報 パスワード key credentials secret password',b,
        'アクセスに必要な鍵や認証情報の項目に添える。','開くために管理する鍵が必要になる。',['丸い持ち手と歯が鍵の道具を表す。','先端へ伸びる軸が解錠に使う部分を表す。'])


def _access_control():
    b=circle(46,51,22,INK)+path('M15 136V114Q15 93 45 93Q75 93 75 114V136Z',PALE,INK,7)
    b+=path('M95 55L109 69L138 38',stroke=BLUE,sw=8)+path('M101 99L132 130M132 99L101 130',stroke=INK,sw=8)
    return _icon('access-control','権限管理_できる操作を分ける_利用者と許可','アクセス権限','利用者ごとに許可する操作と制限する操作を分ける。','権限 許可 制限 アクセス ロール permission authorization access control role',b,
        '利用者の権限や操作制限を説明する。','利用者に応じてできる操作を分ける。',['人物が権限を持つ利用者を表す。','チェックと交差線が許可と制限を表す。'])


def _monitoring():
    b=path('M13 80Q39 37 80 37Q121 37 147 80Q121 123 80 123Q39 123 13 80Z',PALE,INK,7)
    b+=circle(80,80,27,WHITE,INK,7)+circle(80,80,12,BLUE)
    b+=line(34,22,43,36,BLUE,6)+line(80,11,80,27,BLUE,6)+line(126,22,117,36,BLUE,6)
    return _icon('monitoring','運用監視_状態を継続して見守る_観察する目','監視','システムや業務の状態を継続して観察することを示す。','監視 モニタリング 運用 可観測 状態 monitoring observability watch',b,
        '状態監視や継続的な確認の項目を示す。','状態の変化を見逃さず観察する。',['開いた目が状態を見る行為を表す。','上の短い線が注意を向けていることを示す。'])


def _backup():
    b=path('M34 85H125L141 123V143H19V123Z',PALE,INK,7)+line(21,123,139,123,INK,6)+circle(121,133,4,BLUE)
    b+=path('M37 65C24 31 58 11 87 20C108 27 118 44 114 65',stroke=BLUE,sw=7)
    b+=poly('98,51 112,77 130,52',BLUE)
    return _icon('backup','保全作業_復旧用のデータを保存する_保存装置と戻り','バックアップ','後で復旧できるようにデータの控えを保存する。','バックアップ 保存 復旧 保全 backup restore recovery copy',b,
        'バックアップや復旧用データの保存を示す。','元の状態に戻せる控えを残す。',['下の装置がデータの保存先を表す。','戻る矢印が復旧できる状態を表す。'])


def _incident():
    b=line(13,94,29,94,INK,8)+line(131,94,147,94,INK,8)
    b+=rect(28,69,34,51,PALE,6,INK,7)+rect(100,69,34,51,PALE,6,INK,7)
    b+=line(63,81,73,81,INK,6)+line(63,106,73,106,INK,6)
    b+=line(89,81,99,81,INK,6)+line(89,106,99,106,INK,6)
    b+=path('M89 17L69 43H90L73 62',stroke=BLUE,sw=7)
    return _icon('incident','障害対応_接続の中断を扱う_途切れた接続','障害・中断','正常な接続や処理が中断した状態を示す。','障害 中断 不具合 停止 インシデント incident outage disruption',b,
        '障害発生やサービス中断の対応を説明する。','接続や処理が途中で止まる。',['離れた二つのプラグが接続の中断を表す。','上の稲妻が異常の発生を表す。'])


def _privacy():
    b=path('M34 18H99L126 45V142H34Z',WHITE,INK,7)+path('M99 18V45H126',PALE,INK,6)
    b+=line(49,61,110,61,MID,5)+rect(49,75,61,13,INK,2)
    b+=line(49,103,62,103,MID,5)+rect(77,97,33,13,BLUE,2)+line(49,126,92,126,MID,5)
    return _icon('privacy','機密管理_公開する情報を制限する_伏せられた文書','機密情報','公開する範囲を制限した情報を示す。','機密 個人情報 秘密 非公開 マスキング privacy confidential redaction',b,
        '機密情報や公開範囲を制限する資料を示す。','情報の一部を許可された相手にだけ見せる。',['細い行が公開できる内容を表す。','太い帯で伏せた箇所が非公開の内容を表す。'])

def _email():
    b=rect(17,35,126,93,WHITE,8,INK,7)+path('M20 42L80 88L140 42',PALE,INK,7)
    b+=line(21,121,60,86,BLUE,6)+line(139,121,100,86,BLUE,6)
    return _icon('email','連絡手段_文章を送受信する_封筒','メール','文章や資料を送受信するメールを示す。','メール 電子メール 連絡 送信 受信 email mail message',b,
        '連絡先やメールでの連絡手順を示す。','文章や資料を相手へ届ける。',['封筒の輪郭がメッセージを表す。','中央へ折り込まれた面が内容を包む形を表す。'])


def _phone():
    b=path('M36 20L61 23L67 53L51 65C59 84 76 101 95 109L107 93L137 99L140 124Q138 141 121 141C75 136 24 85 19 39Q19 22 36 20Z',PALE,INK,8)
    b+=path('M95 23C119 28 132 41 137 64M92 43C106 46 115 55 118 69',stroke=BLUE,sw=7)
    return _icon('phone','連絡手段_音声で話す_電話','電話','電話で直接話す連絡手段を示す。','電話 通話 音声 連絡 コール phone call telephone voice',b,
        '電話での問い合わせ先や連絡方法を示す。','音声で相手と直接話す。',['受話器の形が電話を表す。','外側の波が音声のやり取りを表す。'])


def _meeting():
    b=ellipse(80,88,45,31,PALE,INK,7)
    b+=circle(80,25,15,BLUE)+path('M55 57Q55 47 65 46H95Q105 47 105 57',stroke=INK,sw=7)
    b+=circle(29,121,14,INK)+circle(131,121,14,INK)
    b+=path('M12 147Q10 137 23 134H39Q51 137 48 147M112 147Q110 137 123 134H139Q151 137 148 147',stroke=INK,sw=7)
    b+=line(71,80,91,80,BLUE,5)+line(67,94,85,94,BLUE,5)
    return _icon('meeting','会議運営_同じ場で論点を話す_会議卓','会議','同じ場で論点を共有し話し合う会議を示す。','会議 打合せ 協議 議論 meeting discussion conference',b,
        '会議や打合せの実施項目を示す。','参加者が同じ論点を囲んで話し合う。',['中央の卓が共有する場を表す。','周囲の人物が会議の参加者を表す。'])


def _notification():
    b=path('M35 112Q46 94 46 69C46 48 58 36 80 36C102 36 114 48 114 69Q114 94 125 112Z',PALE,INK,8)
    b+=circle(80,24,8,BLUE)+path('M67 128Q80 148 93 128',stroke=INK,sw=8)
    b+=line(18,54,28,63,BLUE,7)+line(142,54,132,63,BLUE,7)
    return _icon('notification','通知管理_注意を促す知らせを送る_ベル','通知','更新や連絡に気付くための通知を示す。','通知 お知らせ 更新 アラート notification alert bell',b,
        '通知設定や更新のお知らせを示す。','相手に気付いてほしい知らせがある。',['ベルが通知を表す。','左右の短い線が鳴って知らせる行為を表す。'])


def _sharing():
    b=line(48,79,112,38,INK,8)+line(48,81,112,122,INK,8)
    b+=circle(34,80,20,BLUE)+circle(125,30,18,PALE,INK,7)+circle(125,130,18,PALE,INK,7)
    return _icon('sharing','情報共有_複数の相手に届ける_共有ノード','共有','一つの情報を複数の相手へ共有することを示す。','共有 配布 展開 情報共有 share sharing distribution',b,
        '資料や情報の共有先を示す。','一つの情報を複数の相手へ広げる。',['一つの点が共有元を表す。','枝分かれする線と二つの点が共有先を表す。'])


def _presentation():
    b=rect(62,23,82,78,PALE,3,INK,7)+line(101,102,101,136,INK,6)+line(84,141,120,141,INK,6)
    b+=circle(31,60,17,INK)+path('M15 143V102Q15 85 32 85Q45 85 51 95L63 79L72 85L52 117L46 111V143Z',BLUE)
    b+=rect(79,69,11,17,INK,1)+rect(99,55,11,31,BLUE,1)+rect(119,42,11,44,INK,1)
    return _icon('presentation','説明活動_相手へ内容を発表する_発表者と画面','発表・説明','資料を使って内容を説明する発表を示す。','発表 説明 プレゼン 報告 登壇 presentation briefing speaker',b,
        '発表や説明会の項目に添える。','資料を示しながら相手へ説明する。',['画面が説明する資料を表す。','横の人物と指す腕が発表する行為を表す。'])


def _broadcast():
    b=path('M21 66H49L119 30V122L49 97H21Z',PALE,INK,7)+rect(20,66,28,31,BLUE,0,INK,6)
    b+=path('M47 98L54 139H80L68 105',PALE,INK,7)+line(134,49,147,40,BLUE,6)+line(136,77,151,77,BLUE,6)+line(134,105,147,114,BLUE,6)
    return _icon('broadcast','社内周知_広い相手へ伝える_拡声器','周知・告知','多くの相手へ情報を知らせる周知を示す。','周知 告知 案内 社内広報 広報 announcement broadcast communication',b,
        '社内告知や広報の見出しに添える。','広い範囲の相手へ情報を伝える。',['拡声器が多くの相手への発信を表す。','外へ広がる短い線が知らせの広がりを示す。'])


def _customer():
    b=circle(52,48,22,INK)+path('M16 138V112Q16 85 53 85Q88 85 88 112V138Z',PALE,INK,7)
    b+=path('M101 95V77Q101 62 116 62Q131 62 131 77V95',stroke=BLUE,sw=7)+rect(92,89,49,51,WHITE,2,INK,7)
    return _icon('customer','顧客表示_商品やサービスの利用者を示す_人物と買い物袋','顧客','商品やサービスを購入する顧客を示す。','顧客 利用者 購入者 ユーザー customer client buyer consumer',b,
        '顧客の声や購入者を示す見出しに添える。','商品やサービスを利用する相手がいる。',['人物が顧客を表す。','手提げ袋が購入や利用の関係を表す。'])


def _customer_support():
    b=path('M26 86V66C26 33 48 18 80 18C112 18 134 33 134 66V91',stroke=INK,sw=9)
    b+=circle(80,69,29,PALE,INK,6)+rect(19,64,19,38,BLUE,6)+rect(122,64,19,38,BLUE,6)
    b+=path('M130 101V115Q130 130 109 130H91',stroke=INK,sw=7)+rect(71,123,25,14,BLUE,6)
    b+=path('M37 142V132Q37 111 58 106M102 106Q112 107 117 114',stroke=INK,sw=7)
    return _icon('customer-support','顧客対応_問い合わせを受ける_ヘッドセット担当者','顧客サポート','顧客からの問い合わせに対応する窓口を示す。','顧客対応 サポート CS 問合せ 相談 customer support helpdesk service',b,
        '顧客向けの相談窓口やサポート工程を示す。','問い合わせを受けて対応する。',['ヘッドセットが相手との通話を表す。','人物とマイクが対応する担当者を表す。'])


def _survey():
    b=rect(30,25,101,119,WHITE,7,INK,7)+rect(55,16,51,24,BLUE,5)
    for y in (65,95,125):b+=circle(51,y,7,WHITE,INK,5)+line(72,y,110,y,INK,6)
    b+=circle(51,95,3,BLUE)
    return _icon('survey','意見収集_回答を集める_選択式アンケート','アンケート','同じ設問に対する回答を集める調査を示す。','アンケート 調査 回答 設問 質問票 survey questionnaire feedback',b,
        '顧客や従業員へのアンケートを示す。','同じ質問で複数の意見を集める。',['綴じた用紙が質問票を表す。','行ごとの選択欄が回答を表す。'])


def _target():
    b=circle(76,86,56,WHITE,INK,7)+circle(76,86,36,PALE,BLUE,7)+circle(76,86,14,BLUE)
    b+=line(78,83,133,27,INK,8)+path('M114 19V43H139',stroke=INK,sw=7)
    return _icon('target','目標設定_目指す到達点を定める_的と矢','目標','目指す到達点や達成したい目標を示す。','目標 達成 KPI 目的 到達 target objective goal',b,
        '事業目標や達成指標の見出しに添える。','目指す到達点を明確にする。',['同心円が目指す中心を表す。','中心へ向かう矢が目標に取り組む行為を表す。'])


def _risk():
    b=path('M74 22Q80 11 86 22L147 129Q154 141 140 141H20Q6 141 13 129Z',PALE,INK,8)
    b+=line(80,61,80,101,BLUE,11)+circle(80,122,6,BLUE)
    return _icon('risk','リスク管理_注意すべき可能性を示す_警告三角形','リスク・注意','注意して確認すべきリスクを示す。','リスク 注意 危険 留意 警告 risk warning caution',b,
        '計画のリスクや留意点を示す。','注意して検討する必要がある。',['三角形が警告や注意を表す。','中央の感嘆符が見落とせない項目を示す。'])


def _quality():
    b=poly('48,91 30,144 60,133 74,148 83,105',BLUE)+poly('83,105 90,148 106,133 135,144 116,91',BLUE)
    b+=circle(81,66,43,PALE,INK,8)+_star(81,66,27,12,INK)
    return _icon('quality','品質管理_望ましい基準を保つ_品質メダル','品質','製品や業務で望ましい品質を保つことを示す。','品質 品質管理 基準 検証 信頼 quality assurance standard',b,
        '品質への取り組みや品質管理の項目に添える。','求める基準を満たす品質を目指す。',['中央のメダルが望ましい品質を表す。','星とリボンが価値を認める印を表す。'])


def _milestone():
    b=line(18,133,142,133,INK,7)+circle(28,133,9,WHITE,INK,6)+circle(80,133,10,BLUE)+circle(132,133,9,WHITE,INK,6)
    b+=line(80,124,80,20,INK,7)+path('M84 24H143L126 48L143 71H84Z',BLUE)
    return _icon('milestone','進行管理_重要な到達点を置く_進行線と旗','マイルストーン','進行の途中に置く重要な到達点を示す。','マイルストーン 節目 到達点 進行 納期 milestone checkpoint project',b,
        'プロジェクトの節目や重要な到達点を示す。','途中の重要な到達点を共有する。',['下の線が進行の流れを表す。','旗の立つ点が重要な節目を示す。'])


def _priority():
    b=arrow(31,137,31,23,BLUE,8,23)
    b+=rect(66,27,78,21,INK,3)+rect(66,71,60,21,MID,3)+rect(66,115,40,21,PALE,3,INK,5)
    return _icon('priority','優先整理_先に取り組む順を決める_並びと上向き矢印','優先順位','取り組む順序や重要度を整理することを示す。','優先順位 順位 重要度 順序 優先 priority ranking order',b,
        '施策や作業の優先順位を説明する。','重要な項目から取り組む順を決める。',['上に行くほど強い項目の並びが優先度を表す。','上向きの矢印が先に見る方向を示す。'])


def _decision():
    b=poly('80,15 122,57 80,99 38,57',PALE,INK,7)
    b+=path('M38 57H20V120M122 57H141V120',stroke=INK,sw=7)
    b+=poly('8,110 20,137 32,110',BLUE)+poly('129,110 141,137 153,110',BLUE)
    b+=path('M66 57L76 67L95 45',stroke=BLUE,sw=7)
    return _icon('decision','判断作業_条件に応じて進路を選ぶ_判断の分岐','意思決定','条件や判断に基づいて進む選択肢を決める。','判断 意思決定 選択 分岐 条件 decision choice condition',b,
        '判断が必要な工程や意思決定の項目に添える。','条件を確かめて進む選択肢を決める。',['中央の菱形が判断を表す。','左右に分かれる経路が選べる進路を示す。'])


def _workflow():
    b=rect(16,20,48,38,WHITE,5,INK,7)+rect(97,20,48,38,PALE,5,INK,7)+rect(97,104,48,38,BLUE,5,INK,7)
    b+=arrow(71,39,89,39,BLUE,6,12)+arrow(121,67,121,95,BLUE,7,15)
    return _icon('workflow','業務手順_次の処理へ渡す_工程の受渡','ワークフロー','処理を次の工程へ引き渡して進める手順を示す。','ワークフロー 手順 工程 処理 受渡 workflow process routing',b,
        '業務手順や工程間の受け渡しを示す。','工程をつないで仕事を進める。',['三つの枠が処理を行う工程を表す。','つながる矢印が工程間の受け渡しを表す。'])


def _approval():
    b=path('M55 73V58C55 50 46 46 46 35C46 20 59 14 80 14C101 14 114 20 114 35C114 46 105 50 105 58V73Z',PALE,INK,7)
    b+=path('M39 83H121L138 113H22Z',BLUE,INK,7)+rect(24,123,112,16,INK,3)
    b+=line(40,148,120,148,BLUE,6)
    return _icon('approval','承認手続_責任者が認める_承認印','承認','確認した内容を責任者が認める手続きを示す。','承認 決裁 許可 確認 印 approval authorization signoff',b,
        '申請の承認や決裁が必要な工程を示す。','責任者が内容を確認して認める。',['持ち手と印面が承認に使う印を表す。','下の線が確認結果を残すことを表す。'])


def _download():
    b=path('M23 101V139H137V101',PALE,INK,8)+arrow(80,19,80,113,BLUE,11,31)
    return _icon('download','ファイル操作_手元に取得する_受け取る矢印','ダウンロード','ファイルを手元の保存先へ取得する操作を示す。','ダウンロード 取得 保存 受信 ファイル download retrieve save',b,
        '資料やファイルを取得する操作を示す。','外にあるファイルを手元へ受け取る。',['下の受け皿が保存先を表す。','下向きの矢印が受け取る動きを示す。'])


def _upload():
    b=path('M23 101V139H137V101',PALE,INK,8)+arrow(80,116,80,19,BLUE,11,31)
    return _icon('upload','ファイル操作_外部へ送る_送り出す矢印','アップロード','ファイルを共有先やサービスへ送る操作を示す。','アップロード 送信 提出 共有 ファイル upload submit send',b,
        'ファイルを共有先へ送る操作を示す。','手元のファイルを外の保存先へ送る。',['下の受け皿が手元の保存場所を表す。','上向きの矢印が送り出す動きを示す。'])


def make_assets():
    from sets.manufacturing_icons import make_assets as manufacturing_assets
    return [
        _recruitment(),_development(),_performance(),_transfer(),_attendance(),_payroll(),_remote_work(),
        _contract(),_invoice(),_payment(),_budget(),_expense(),_tax(),_cash_flow(),
        _procurement(),_warehouse(),_delivery(),_inventory(),_manufacturing(),_inspection(),_returns(),
        _database(),_synchronization(),_analytics(),_automation(),_api(),_server(),_version_control(),
        _key(),_authentication(),_access_control(),_monitoring(),_backup(),_incident(),_privacy(),
        _email(),_phone(),_meeting(),_notification(),_sharing(),_presentation(),_broadcast(),
        _customer(),_customer_support(),_survey(),_target(),_risk(),_quality(),_sustainability(),
        _milestone(),_priority(),_decision(),_workflow(),_approval(),_download(),_upload(),
    ] + manufacturing_assets()
