"""Business pictograms drawn on a 160-unit grid."""
from math import cos, sin, pi
from vector import INK, BLUE, MID, PALE, WHITE, path, rect, circle, ellipse, line, poly, asset


def _icon(name, title, description, keywords, body, use_case, message, reading):
    item = asset(name, '08-アイコンとピクトグラム', title, description,
                 keywords, body, size=(160, 160))
    item['kind'] = 'icon'
    item['guidance'] = dict(use_case=use_case, message=message, reading=reading)
    return item


def make_assets():
    result = []
    b = circle(80, 48, 21, BLUE)
    b += path('M30 140V123C30 101 48 88 70 88H90C112 88 130 101 130 123V140Z', INK)
    result.append(_icon(
        '人物表示_担当者を示す_ひとりの人物', '担当者', '個人や担当者を示す人物のピクトグラム。',
        '人物 個人 担当者 人材 利用者 メンバー person individual owner', b,
        '担当者や利用者を、資料内で短く示す場面。', 'ひとりの人、または個人の担当を示す。',
        ['丸い頭部が人物を示す。', '一つの肩の輪郭が個人を表す。']))

    # The two cuffs remain outside the joint; one clear thumb crosses the palm.
    b = path('M47 69L65 49Q74 44 83 49L110 71L119 85Q123 91 117 97L112 101L109 110Q103 118 98 113L93 120Q87 125 81 120L65 108L42 88Z', PALE, INK, 6)
    b += path('M113 67L94 49Q86 44 82 49L64 70Q59 75 63 79Q67 83 76 78L87 70L108 91L117 83Z', WHITE, INK, 6)
    b += line(81, 101, 95, 114, INK, 5)+line(93, 94, 108, 108, INK, 5)
    b += poly('16,62 36,49 58,90 38,105', BLUE, INK, 6)
    b += poly('144,62 124,49 102,90 122,105', BLUE, INK, 6)
    result.append(_icon(
        '協業表示_合意と協力を示す_握手', '協業と合意', '互いに手を取り、協力する関係を示す。',
        '協業 合意 協力 連携 パートナー 提携 握手 partnership agreement handshake', b,
        '協力会社や社内外の協業関係を示す場面。', '双方が合意して協力する。',
        ['左右から差し出した手が双方の参加を表す。', '中央の握手が合意と協力を表す。']))
    b = path('M13 137V121C13 106 23 98 36 98C49 98 58 107 58 121V137Z', PALE, INK, 7)
    b += path('M102 137V121C102 107 111 98 124 98C137 98 147 106 147 121V137Z', PALE, INK, 7)
    b += circle(36, 74, 15, INK)+circle(124, 74, 15, INK)
    b += path('M47 142V120C47 102 59 92 80 92C101 92 113 102 113 120V142Z', BLUE)
    b += circle(80, 55, 21, BLUE)
    result.append(_icon(
        'チーム表示_複数の担当者を示す_三人のチーム', 'チーム', '複数人で働くチームや部門を示す。',
        'チーム 部門 集団 複数人 組織 メンバー team group department', b,
        '個人とチームの担当を区別する場面。', '複数人が一つのチームをつくる。',
        ['三つの頭部が複数人を示す。', '重なった肩の輪郭が集団を表す。']))

    b = rect(32, 20, 96, 120, WHITE, 3, INK, 8)
    for x in (44, 74, 104):
        for y in (44, 75):
            b += rect(x, y, 12, 14, BLUE, 1)
    b += rect(68, 112, 24, 28, INK)
    result.append(_icon(
        '企業表示_会社や事業所を示す_オフィスビル', '企業・事業所', '企業や事業所を示すオフィスビルの記号。',
        '企業 会社 事業所 オフィス 法人 建物 company enterprise office building', b,
        '取引先、会社、事業所を人物と区別する場面。', '組織としての会社や事業所を示す。',
        ['まとまった外壁が建物を表す。', '並んだ窓と入口が業務を行う場所を表す。']))

    b = rect(26, 31, 108, 80, PALE, 5, INK, 8)
    b += path('M14 116H146L136 135H24Z', BLUE, INK, 7)
    b += line(64, 119, 96, 119, WHITE, 5)
    result.append(_icon(
        '端末表示_仕事用のPCを示す_ノートパソコン', 'ノートパソコン', '業務用端末やPCで行う作業を示す。',
        '端末 PC パソコン ノートパソコン デジタル 業務端末 laptop computer device', b,
        'PCを使う作業や、業務端末を示す場面。', 'パソコンで行う仕事や操作を示す。',
        ['上の四角い面が画面を表す。', '下の開いた面がノートパソコンの操作面を表す。']))

    b = path('M42 126C27 126 15 113 15 97C15 82 26 73 45 73C49 49 69 40 82 42C103 41 121 57 121 74C137 76 146 90 146 104C146 117 134 126 121 126H42Z', PALE, INK, 8)
    result.append(_icon(
        '基盤表示_クラウドを示す_共有サービス', 'クラウド', 'クラウド上のサービスや保管先を示す。',
        'クラウド 共有 オンライン サービス 保管 cloud online service hosting', b,
        '端末の外にある共有サービスを示す場面。', 'ネットワークを通して利用するサービスを示す。',
        ['雲の輪郭がクラウドを表す。', '一つにつながった面が共有されるサービスを表す。']))

    b = path('M61 106V100C61 88 40 79 40 61C40 38 58 20 80 20C102 20 120 38 120 61C120 79 99 88 99 100V106Z', PALE, INK, 8)
    b += path('M64 66L80 83L96 66M80 83V105', stroke=BLUE, sw=7)
    b += rect(58, 116, 44, 10, INK, 3)+rect(67, 136, 26, 8, BLUE, 3)
    result.append(_icon(
        '発想表示_アイデアを示す_ひらめきの電球', 'アイデア', '発想、気付き、改善のヒントを示す。',
        '発想 アイデア ひらめき 気付き 改善 工夫 idea lightbulb insight', b,
        '新しい案や改善の着眼点を示す場面。', '仕事を変える発想や気付きがある。',
        ['電球の輪郭がひらめきを表す。', '内部の発光部がアイデアに焦点を当てる。']))

    b = circle(80, 80, 55, BLUE, INK, 8)
    b += path('M48 81L71 103L114 57', stroke=WHITE, sw=10)
    result.append(_icon(
        '確認表示_完了を示す_チェック', '確認・完了', '確認済みや作業完了を簡潔に示す。',
        '確認 完了 チェック 済み 合格 承認 check complete done confirmed', b,
        '一覧の中で、確認済みや完了した状態を示す場面。', '対象の確認や作業が終わっている。',
        ['チェック形が肯定・確認済みを表す。', '丸い面が一つの状態として見分けやすくする。']))

    b = path('M80 18L130 40V77C130 105 111 128 80 142C49 128 30 105 30 77V40Z', PALE, INK, 8)
    b += path('M54 78L74 98L107 61', stroke=BLUE, sw=9)
    result.append(_icon(
        '保護表示_安全対策を示す_チェック付きシールド', '保護・安全対策', '守る対象や安全対策を示す盾の記号。',
        '保護 安全 対策 セキュリティ 盾 防御 security shield protection safeguard', b,
        '情報や業務を守る対策を紹介する場面。', '対象を守るための対策がある。',
        ['盾の輪郭が保護を表す。', '内側のチェックが対策を確認する意味を添える。']))

    b = rect(26, 36, 108, 102, WHITE, 7, INK, 8)
    b += rect(30, 40, 100, 27, BLUE, 2)
    b += line(54, 22, 54, 47, INK, 8)+line(106, 22, 106, 47, INK, 8)
    for x, y in ((50,89),(110,89),(50,115),(80,115),(110,115)):
        b += circle(x, y, 5, INK)
    b += circle(80, 89, 10, BLUE)
    result.append(_icon(
        '予定表示_日程を示す_カレンダー', '日程・予定', '会議や作業の日程を示すカレンダー。',
        '予定 日程 日付 会議 スケジュール 期限 calendar schedule date deadline', b,
        '会議日や作業期限など、日付に関わる項目を示す場面。', '予定として確認する日がある。',
        ['とじ具と日付の並びがカレンダーを表す。', '強調された一つの点が注目する日を表す。']))

    b = path('M40 20H94L122 48V140H40Z', WHITE, INK, 8)
    b += path('M94 20V48H122', PALE, INK, 8)
    b += line(59, 76, 103, 76, BLUE, 7)+line(59, 98, 103, 98, BLUE, 7)+line(59, 120, 89, 120, BLUE, 7)
    result.append(_icon(
        '書類表示_文書を示す_折り角ドキュメント', '文書・書類', '文書、資料、書類を示す一枚の紙。',
        '文書 書類 資料 ドキュメント ファイル 帳票 document file paper report', b,
        '添付資料や入力・確認する書類を示す場面。', '参照または作成する文書がある。',
        ['折り角のある輪郭が紙の文書を表す。', '横の線が文章を含む内容を表す。']))

    b = line(100, 100, 138, 138, BLUE, 13)
    b += circle(70, 70, 43, PALE, INK, 8)
    result.append(_icon(
        '検索表示_情報を探す_拡大鏡', '検索・調査', '情報を探すことや対象を詳しく見ることを示す。',
        '検索 調査 探索 発見 確認 拡大 search find inspect research', b,
        '検索する項目や、調査する工程を示す場面。', '必要な情報を探して詳しく見る。',
        ['丸いレンズが対象を拡大して見る行為を表す。', '持ち手が検索・調査の道具として見分けやすくする。']))

    points = []
    for tooth in range(8):
        for offset, radius in ((-22.5,46),(-12,46),(-12,62),(12,62),(12,46),(22.5,46)):
            angle = (tooth*45+offset-90)*pi/180
            points.append(f'{80+radius*cos(angle):.3f},{80+radius*sin(angle):.3f}')
    b = poly(' '.join(points), PALE, INK, 7)
    b += circle(80, 80, 20, WHITE, BLUE, 8)
    result.append(_icon(
        '業務表示_仕組みを動かす_プロセスギア', '業務の仕組み', '業務プロセスや設定、仕組みを示す歯車。',
        '業務 プロセス 仕組み 設定 運用 工程 gear process operation settings', b,
        '業務を動かす仕組みや、設定に関わる項目を示す場面。', '仕事を進めるための仕組みがある。',
        ['かみ合う歯を持つ輪郭が仕組みを表す。', '中心の穴が回転する部品として見分けやすくする。']))

    b = rect(61, 64, 83, 65, BLUE, 13)
    b += poly('110,126 137,145 137,120', BLUE)
    b += path('M34 24H108Q122 24 122 38V88Q122 102 108 102H58L34 122V102Q20 102 20 88V38Q20 24 34 24Z', PALE, INK, 8)
    b += circle(48, 64, 5, BLUE)+circle(71, 64, 5, BLUE)+circle(94, 64, 5, BLUE)
    result.append(_icon(
        '対話表示_意見を交わす_ふたつの吹き出し', '対話・コミュニケーション', '相手との対話や意見のやり取りを示す。',
        '対話 会話 連絡 意見 コミュニケーション 相談 communication conversation chat dialogue', b,
        '話し合いや意見交換が必要な場面。', '相手と情報や考えを交わす。',
        ['重なった二つの吹き出しが双方の発言を表す。', '前の吹き出しの点が話している内容を表す。']))

    b = path('M20 130V38Q49 30 80 42Q111 30 140 38V130Q109 122 80 134Q51 122 20 130Z', PALE, INK, 8)
    b += line(80, 43, 80, 133, BLUE, 7)
    b += path('M36 61L62 67M36 82L62 88M98 67L124 61M98 88L124 82', stroke=BLUE, sw=6)
    result.append(_icon(
        '学習表示_知識を身につける_開いた本', '学習・知識', '学習や研修、知識を参照することを示す。',
        '学習 知識 研修 教育 マニュアル 本 learning education knowledge book training', b,
        '研修、手順書、知識を参照する項目を示す場面。', '知識を読み、学び、仕事に生かす。',
        ['左右に開いたページが読書と学習を表す。', 'ページの内容線が参照する知識を表す。']))

    b = circle(80, 80, 55, WHITE)
    b += path('M30 57.088C57 70 103 70 130 57.088M30 102.912C57 90 103 90 130 102.912', stroke=BLUE, sw=6)
    b += ellipse(80, 80, 23, 55, 'none', BLUE, 6)
    b += line(25, 80, 135, 80, INK, 6)
    b += circle(80, 80, 55, 'none', INK, 8)
    result.append(_icon(
        '地域表示_世界とのつながりを示す_グローブ', '世界・海外', '海外や世界規模の活動を示す地球の記号。',
        '世界 海外 国際 グローバル 地域 多言語 globe global international worldwide', b,
        '海外展開や世界とのつながりを示す場面。', '地域を越えた広がりやつながりを示す。',
        ['丸い輪郭が地球全体を表す。', '経線と緯線が地域を越える広がりを表す。']))
    keys = [
        'icon/person', 'icon/handshake', 'icon/team', 'icon/company',
        'icon/laptop', 'icon/cloud', 'icon/idea', 'icon/check',
        'icon/shield', 'icon/calendar', 'icon/document', 'icon/search',
        'icon/gear', 'icon/conversation', 'icon/book', 'icon/globe',
    ]
    for item, key in zip(result, keys):
        item['key'] = key
    return result
