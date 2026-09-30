"""Compact symbols for concepts formerly drawn as detailed SVG scenes."""
from vector import INK, BLUE, MID, PALE, WHITE, path, rect, circle, ellipse, line, poly, arrow
from sets.business_icons import _icon


def make_assets():
    out=[]
    def add(key,title,words,b,scene,message,reading):
        out.append(_icon(key,title+'_業務の象徴',title,message,words,b,scene,message,reading))

    b=circle(45,45,20,INK)+path('M16 131V109Q16 79 45 79Q68 79 74 98V131Z',PALE,INK,7)
    b+=path('M93 24H137V104L115 92L93 104Z',WHITE,INK,7)
    b+=path('M101 56L112 67L130 45',stroke=BLUE,sw=7)+line(87,125,141,125,BLUE,7)+line(87,140,125,140,INK,6)
    add('professional-expertise','専門性と実務','専門家 専門性 資格 経験 人材 professional expertise qualification',b,'担当者の専門性や実務を裏付ける資格・経歴を紹介する。','人の経験と専門知識を仕事に生かす。',['左の人物が専門性を持つ担当者を表す。','資格のしおりと経歴の線が専門知識と実務経験を表す。'])

    b=path('M80 78V100M31 100H129M31 100V114M129 100V114',stroke=INK,sw=6)
    b+=rect(54,17,52,62,WHITE,3,INK,7)+rect(70,54,20,25,BLUE)
    b+=rect(16,114,30,29,PALE,2,INK,6)+rect(114,114,30,29,PALE,2,INK,6)
    b+=rect(66,30,9,10,BLUE)+rect(85,30,9,10,BLUE)
    add('company-network','本社と拠点','本社 支社 拠点 事業所 組織 headquarters branch sites network',b,'本社と支社、複数の事業拠点の関係を説明する。','複数の拠点を一つのネットワークで結ぶ。',['中央上の大きな建物が本社を示す。','下の二つの拠点へ接続線が分かれる。'])

    b=circle(51,54,21,PALE,INK,7)+path('M22 61V48A29 29 0 0 1 80 48V72Q80 87 65 87',stroke=BLUE,sw=6)
    b+=rect(16,47,11,25,BLUE,4)+rect(75,47,11,25,BLUE,4)+rect(56,83,14,9,BLUE,4)
    b+=path('M21 128V119Q21 100 51 100Q77 100 81 119',stroke=INK,sw=7)
    b+=path('M101 24H132Q142 24 142 34V64Q142 74 132 74H120L103 88V74H99Q94 74 94 67V34Q94 24 101 24Z',PALE,INK,6)
    b+=line(107,41,130,41,BLUE,5)+line(107,57,123,57,BLUE,5)+line(15,140,145,140,INK,7)
    add('support-desk','相談に応える窓口','窓口 相談 回答 受付 ヘルプデスク helpdesk inquiry answer support desk',b,'問い合わせの受付と回答を担う窓口を紹介する。','相談を受けて回答を返す。',['ヘッドセットを着けた担当者が受付窓口を表す。','内容のある吹き出しが返す回答を示す。'])

    b=rect(27,18,94,126,WHITE,5,INK,7)+rect(27,18,17,126,INK,3)
    b+=rect(121,38,17,18,BLUE,2)+rect(121,71,17,18,MID,2)+rect(121,104,17,18,INK,2)
    b+=line(58,38,106,38,BLUE,7)+rect(58,71,10,29,PALE,1)+rect(76,58,10,42,BLUE,1)+rect(94,79,10,21,INK,1)
    b+=line(58,116,105,116,INK,5)+line(58,131,91,131,INK,5)
    add('structured-report','構造化されたレポート','報告書 レポート 章 索引 図表 report structured index chapters',b,'章や図表に整理した業務レポートを案内する。','情報を整理して参照しやすくする。',['冊子の中の図表と本文が報告内容を表す。','側面の三つのタブが章の区切りを表す。'])

    b=rect(22,18,85,123,WHITE,3,INK,7)+path('M38 49L47 58L63 38M38 88L47 97L63 77',stroke=BLUE,sw=6)
    b+=line(76,49,91,49,INK,5)+line(76,88,91,88,INK,5)
    b+=path('M114 75V66Q99 60 99 46Q99 29 117 29Q135 29 135 46Q135 60 122 66V75Z',PALE,INK,6)
    b+=path('M99 83H137L147 110H89Z',BLUE,INK,6)+line(94,124,142,124,INK,6)
    add('document-approval','確認と承認','確認 承認 書類 決裁 稟議 document review approval signoff',b,'書類の項目確認から決裁へ進む手続きを説明する。','内容を確認したうえで承認を確定する。',['チェックの付いた紙が項目の確認を表す。','右の印が決裁を確定する行為を表す。'])

    b=path('M19 25V137H142',stroke=INK,sw=7)+path('M30 117L55 89L76 104L116 45',stroke=BLUE,sw=7)
    b+=circle(87,71,35,WHITE,INK,7)+path('M59 90L75 65L89 78L110 46',stroke=BLUE,sw=6)+line(112,98,141,127,INK,11)
    add('analytic-insight','変化点を見つける','変化点 傾向 分析 発見 インサイト trend change point analytic insight',b,'データの変化に注目して原因や改善の手掛かりを探す。','変化の前後を詳しく確かめる。',['折れ線が前後で変わるデータを表す。','拡大鏡が折れ曲がる部分へ注意を向ける。'])

    b=circle(80,37,24,PALE,INK,6)+path('M69 27L80 39L91 27M80 39V51M68 39H92M68 46H92',stroke=BLUE,sw=4)
    b+=path('M80 63V88M30 88H130M30 88V108M80 88V108M130 88V108',stroke=INK,sw=6)
    b+=ellipse(30,126,18,10,PALE,INK,5)+ellipse(80,132,18,10,BLUE,INK,5)+ellipse(130,126,18,10,PALE,INK,5)
    b+=ellipse(80,118,18,10,BLUE,INK,5)
    add('budget-allocation','用途に応じた資金配分','予算 配分 資金 用途 投資 budget allocation funding distribution',b,'一つの予算を複数の用途へ振り分ける方針を説明する。','共通の資金を目的に応じて配分する。',['上の硬貨が配分元の予算を示す。','枝分かれする線と下の硬貨が用途別の配分を表す。'])

    b=rect(32,19,91,123,PALE,4,INK,7)+rect(50,38,56,85,WHITE,2,INK,5)
    b+=line(64,61,91,61,BLUE,5)+line(64,79,91,79,BLUE,5)
    b+=path('M51 39L17 59V140L51 121Z',BLUE,INK,6)+circle(35,92,5,WHITE)
    b+=circle(122,106,17,WHITE,INK,6)+path('M111 119L87 143M97 133L103 139',stroke=BLUE,sw=7)
    add('access-protection','許可された入口','アクセス 権限 許可 情報 保管庫 access protection authorization vault',b,'保管情報へのアクセスを権限に応じて開く仕組みを示す。','権限を持つ人が保管情報へアクセスする。',['扉の奥の紙が保管された情報を表す。','開いた扉と鍵が許可に基づく入口を表す。'])

    b=path('M48 109H80V67M80 109H112',stroke=BLUE,sw=6)
    b+=path('M55 59C40 59 34 50 38 39Q42 28 54 30Q59 13 76 18Q93 15 99 32Q119 30 121 46Q121 60 105 60Z',PALE,INK,6)
    b+=rect(14,87,35,57,WHITE,4,INK,6)+line(23,103,39,103,BLUE,5)+line(23,122,39,122,BLUE,5)
    b+=rect(110,87,38,37,WHITE,3,INK,6)+path('M129 127V141M117 143H142',stroke=INK,sw=5)
    add('connected-systems','データをつなぐ基盤','システム 基盤 クラウド サーバー 端末 system integration infrastructure connected',b,'サーバー・端末・クラウド間のデータ連携を説明する。','異なるシステムを接続して情報を扱う。',['サーバー、画面、雲が異なる接続先を表す。','中央の線がデータのつながりを表す。'])
    return out
