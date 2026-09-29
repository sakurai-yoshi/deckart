"""Planning diagrams for risk, experience, uncertainty, measures, and scope."""
from vector import INK, BLUE, MID, PALE, FAINT, WHITE
from vector import path, rect, circle, line, poly, arrow, check, slot, asset


def _diagram(key, name, category, title, description, keywords, body, labels,
             use_case, message, reading, avoid):
    item = asset(name, category, title, description, keywords, body, labels)
    item['key'] = key
    item['kind'] = 'diagram'
    item['guidance'] = dict(use_case=use_case, message=message,
                            reading=reading, avoid=avoid)
    return item


def risk_response():
    # Equal cells classify two qualitative dimensions; they encode no probability.
    b = rect(272, 156, 258, 130, PALE)
    b += rect(542, 156, 258, 130, BLUE)
    b += rect(812, 156, 258, 130, BLUE)
    b += rect(272, 298, 258, 130, FAINT)
    b += rect(542, 298, 258, 130, PALE)
    b += rect(812, 298, 258, 130, BLUE)
    b += rect(272, 440, 258, 130, FAINT)
    b += rect(542, 440, 258, 130, FAINT)
    b += rect(812, 440, 258, 130, PALE)
    b += arrow(236, 598, 1118, 598, INK, 4, 18)
    b += arrow(236, 598, 236, 116, INK, 4, 18)
    b += path('M805 150H1076V292', stroke=INK, sw=5)
    b += poly('942,176 965,216 919,216', WHITE)
    b += line(942,188,942,200,BLUE,4)+circle(942,208,2,BLUE)
    return _diagram(
        'planning/risk-response-matrix',
        'リスク対応_発生しやすさと影響を見分ける_三段階の対応領域',
        '02-比較と意思決定', '発生と影響から対応を決める',
        '発生しやすさと影響の大きさでリスクを配置し、監視・計画・重点対策を分ける。',
        'リスク リスクマトリクス 発生可能性 影響 対応 優先度 予防 risk matrix likelihood impact mitigation',
        b,
        [slot(229, 32, 527, 66, '上ほど影響が大きい', '影響の軸', 'left'),
         slot(711, 622, 420, 66, '右ほど発生しやすい', '発生の軸'),
         slot(286, 477, 231, 61, '監視を継続', '低リスクの対応'),
         slot(555, 337, 231, 61, '対策を計画', '中リスクの対応'),
         slot(825, 222, 231, 55, '重点的に低減', '高リスクの対応', color=WHITE)],
        'プロジェクトのリスクを洗い出し、対策に着手する順序を決める。',
        '起こりやすく影響の大きい事象へ、先に対策を用意する。',
        ['横方向は発生しやすさ、縦方向は影響の大きさ。',
         '同じ大きさの九領域に、定性的にリスクを配置する。',
         '右上の注意記号は、重点的な低減が必要な領域。'],
        '色の濃さを実際の発生確率や損失額として扱わない。')


def customer_journey():
    # The upper route is the customer's sequence; lower work supports each contact.
    b = arrow(116, 242, 1127, 242, BLUE, 7, 24)
    b += rect(88, 472, 1024, 113, PALE, 10)
    for x in (330, 590, 850):
        b += rect(x, 472, 10, 113, WHITE)
    for x in (200, 460, 720, 980):
        b += arrow(x, 467, x, 307, MID, 5, 19)
    b += line(80, 396, 1120, 396, MID, 2, '8 10')
    for x in (200, 460, 720, 980):
        b += circle(x, 242, 58, WHITE, INK, 4)
    b += circle(193, 234, 19, PALE, BLUE, 5)+line(208, 249, 227, 269, BLUE, 7)
    b += path('M429 216H477Q487 216 487 226V252Q487 262 477 262H455L437 275V262H429Q419 262 419 252V226Q419 216 429 216Z', PALE, BLUE, 4)
    b += circle(438, 239, 3, BLUE)+circle(453, 239, 3, BLUE)+circle(468, 239, 3, BLUE)
    b += path('M697 210H727L744 227V275H697Z', PALE, BLUE, 4)
    b += path('M727 210V227H744', stroke=BLUE, sw=4)+check(707, 241, .72, BLUE)
    b += path('M959 256A29 29 0 1 1 1003 258', stroke=BLUE, sw=5)
    b += poly('1010,250 1001,266 993,251', BLUE)
    return _diagram(
        'planning/customer-journey-support',
        '顧客体験_行動と接点を支える業務_表と裏のジャーニー',
        '04-計画と進捗', '顧客の行動と支える業務を結ぶ',
        '知る・比べる・使い始める・使い続ける流れに、各接点を支える業務を対応させる。',
        '顧客体験 顧客行動 カスタマージャーニー サービスブループリント 接点 裏側 継続利用 customer journey touchpoint service blueprint',
        b,
        [slot(72, 25, 416, 60, '顧客の行動と接点', '顧客側の見出し', 'left'),
         slot(96, 113, 208, 59, '知る', '最初の接点'),
         slot(356, 113, 208, 59, '比べる', '検討の接点'),
         slot(616, 113, 208, 59, '使い始める', '開始の接点'),
         slot(876, 113, 208, 59, '使い続ける', '継続の接点'),
         slot(395, 624, 410, 60, '接点の裏で支える業務', '裏側の業務見出し'),
         slot(105, 495, 203, 66, '情報を整える', '認知を支える業務'),
         slot(357, 495, 217, 66, '相談に備える', '比較を支える業務'),
         slot(617, 495, 217, 66, '導入を支える', '開始を支える業務'),
         slot(877, 495, 217, 66, '利用を把握する', '継続を支える業務')],
        '顧客接点の改善を検討し、その体験を支える社内業務を決める。',
        '顧客の行動だけでなく、その裏側の業務も一緒に設計する。',
        ['上の横向きの経路は顧客の行動順序。',
         '破線の下は、接点の裏側で行う業務。',
         '上向きの矢印は、それぞれの業務が支える接点。'],
        '上の経路を顧客の感情点数や、全顧客に共通する実測行動として扱わない。')


def scenario_response():
    # A fan is uncertainty, not proportional flow; each branch has its own response.
    b = path('M373 354C509 354 500 151 693 151H807V557H693C500 557 509 354 373 354Z', FAINT)
    b += line(373, 127, 373, 582, MID, 2, '7 10')
    b += line(204, 354, 373, 354, INK, 7)
    b += path('M373 354C509 354 500 151 693 151H807', stroke=BLUE, sw=6)
    b += line(373, 354, 807, 354, INK, 6)
    b += path('M373 354C509 354 500 557 693 557H807', stroke=MID, sw=6)
    b += circle(164, 354, 42, WHITE, INK, 7)+circle(373, 354, 12, WHITE, BLUE, 4)
    for y, color in ((151, BLUE), (354, INK), (557, MID)):
        b += circle(807, y, 16, WHITE, color, 4)
        b += arrow(826, y, 887, y, color, 5, 17)
        b += rect(896, y-57, 235, 114, PALE, 10)
        b += rect(896, y-57, 7, 114, color, 3)
    return _diagram(
        'planning/scenario-triggered-response',
        'シナリオ計画_先の変化に対応を用意する_三つの分岐と打ち手',
        '04-計画と進捗', '状況の変化に応じた打ち手を持つ',
        '共通の出発点から複数の将来を想定し、変化を捉えた後の対応を先に用意する。',
        'シナリオ計画 不確実性 将来 需要変動 代替計画 トリガー 対応策 scenario planning uncertainty contingency trigger',
        b,
        [slot(51, 417, 254, 77, '共通の出発点', '現在の状態'),
         slot(463, 57, 358, 67, '需要が伸びる', '上振れの条件'),
         slot(463, 261, 358, 67, '想定通りに進む', '想定内の条件'),
         slot(463, 464, 358, 67, '需要が鈍る', '下振れの条件'),
         slot(909, 113, 212, 77, '供給を広げる', '上振れへの対応'),
         slot(909, 316, 212, 77, '計画を続ける', '想定内への対応'),
         slot(909, 519, 212, 77, '固定費を抑える', '下振れへの対応'),
         slot(303, 633, 817, 62, '状況の変化を捉えて、打ち手を切り替える', '切替の考え方')],
        '事業計画で需要の上振れ・想定内・下振れに備える。',
        '一つの将来を決め打ちせず、条件ごとの対応を用意する。',
        ['左の共通点から三つの将来へ経路が分かれる。',
         '各経路の丸い節目は、対応を切り替える条件。',
         '右の領域は、それぞれの条件に対応する打ち手。'],
        '経路の上下・幅・色を予測確率や売上高として扱わない。')


def outcome_measures():
    # The tree decomposes an outcome; terminal bars are observations, not actions.
    b = path('M307 360H368M368 211V509M368 211H510M368 509H510', stroke=INK, sw=5)
    b += path('M804 211H864M864 143V279M864 143H924M864 279H924', stroke=MID, sw=4)
    b += path('M804 509H864M864 441V577M864 441H924M864 577H924', stroke=MID, sw=4)
    b += circle(197, 360, 108, WHITE, INK, 10)
    b += rect(511, 155, 291, 112, PALE, 14)+rect(511, 453, 291, 112, PALE, 14)
    b += rect(511, 155, 9, 112, BLUE, 4)+rect(511, 453, 9, 112, BLUE, 4)
    for y in (143, 279, 441, 577):
        b += line(924, y-38, 924, y+38, BLUE, 7)
    b += circle(368, 360, 9, WHITE, INK, 3)
    return _diagram(
        'planning/outcome-measure-tree',
        '目標管理_成果を観測できる指標へ分ける_成果要素と測定の樹形',
        '05-組織と戦略', '目指す成果を観測する指標へ分ける',
        '事業で得たい成果を二つの要素に分け、それぞれを確認する指標へ結び付ける。',
        '目標管理 KGI KPI 成果指標 指標ツリー 測定 評価 成果分解 outcome measures metric tree goals indicators',
        b,
        [slot(55, 46, 330, 65, '目指す成果', '全体の見出し'),
         slot(492, 46, 330, 65, '成果を分ける要素', '要素の見出し'),
         slot(897, 46, 270, 65, '観測する指標', '指標の見出し'),
         slot(110, 311, 174, 100, '継続利用を\n増やす', '目標'),
         slot(536, 174, 242, 76, '初回の価値', '第一の成果要素'),
         slot(536, 472, 242, 76, '習慣としての利用', '第二の成果要素'),
         slot(946, 105, 221, 76, '初期設定完了率', '第一の準備指標', 'left'),
         slot(946, 241, 221, 76, '初回利用率', '第一の成果指標', 'left'),
         slot(946, 403, 221, 76, '利用頻度', '第二の行動指標', 'left'),
         slot(946, 539, 221, 76, '継続利用率', '第二の成果指標', 'left')],
        '成果目標を設定し、達成状況を何で確認するかを整理する。',
        '目標の言葉だけで終えず、観測できる指標まで決める。',
        ['左の円は事業で得たい成果。',
         '中央の二領域は、その成果を構成する要素。',
         '右の端点は、それぞれの要素を確認する指標。'],
        '各指標の合計が上位目標になる数式や、因果関係の検証結果として扱わない。')


def scope_boundary():
    # New requests have one controlled entrance; excluded scope remains outside.
    b = rect(81, 144, 679, 450, FAINT, 28, INK, 4)
    b += path('M109 144H732Q760 144 760 172V227H81V172Q81 144 109 144Z', INK)
    b += rect(143, 287, 411, 116, PALE, 10)+rect(143, 287, 9, 116, BLUE, 4)
    b += path('M700 430H607V345H574', stroke=BLUE, sw=6)+poly('554,345 578,334 578,356', BLUE)
    b += path('M802 449L852 499V630H1001', stroke=INK, sw=5)+poly('1018,630 998,620 998,640', INK)
    b += path('M943 329V430H834', stroke=BLUE, sw=6)+poly('814,430 838,419 838,441', BLUE)
    b += poly('760,375 815,430 760,485 705,430', WHITE, BLUE, 5)
    b += path('M747 417C747 403 775 403 775 417C775 426 761 426 761 436', stroke=BLUE, sw=4)+circle(761, 447, 3, BLUE)
    b += path('M870 123H976L1018 165V258H870Z', WHITE, BLUE, 4)
    b += path('M976 123V165H1018', stroke=BLUE, sw=4)
    b += line(895, 189, 990, 189, MID, 5)+line(895, 213, 973, 213, MID, 5)
    b += circle(1055, 630, 35, WHITE, INK, 4)+line(1037, 630, 1073, 630, INK, 5)
    return _diagram(
        'planning/controlled-scope-boundary',
        'スコープ管理_追加要望を合意した範囲へ通す_変更の入口と対象外',
        '04-計画と進捗', '追加要望を一つの入口で判断する',
        '合意した範囲と追加要望を分け、変更として受け入れるものと今回の対象外を示す。',
        'スコープ 範囲 対象外 追加要望 変更管理 合意 受入条件 要件 scope boundary change control requirements',
        b,
        [slot(121, 164, 531, 52, '今回合意した範囲', '対象範囲', 'left', WHITE),
         slot(168, 310, 358, 70, '今回届ける成果', '成果物'),
         slot(136, 489, 345, 79, '合意した受入条件', '受入条件'),
         slot(491, 449, 226, 79, '合意して追加', '追加の扱い'),
         slot(832, 270, 245, 54, '新たな要望', '範囲外の要望'),
         slot(780, 325, 150, 65, '変更判断', '判断の入口'),
         slot(876, 529, 257, 75, '今回の対象外', '含めない範囲')],
        'プロジェクト途中の追加要望を整理し、今回の対応範囲を合意する。',
        '要望をそのまま足さず、範囲の入口で合意してから追加する。',
        ['大きな閉じた枠が、今回合意した範囲。',
         '枠の境界にある菱形が、追加要望を判断する入口。',
         '左の経路は合意して追加し、外側の経路は今回の対象外へ分ける。'],
        '対象外の要望を永久に却下した決定や、契約内容の証明として扱わない。')


def make_assets():
    return [risk_response(), customer_journey(), scenario_response(),
            outcome_measures(), scope_boundary()]
