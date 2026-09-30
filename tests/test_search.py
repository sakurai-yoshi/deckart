"""Intent retrieval must expose every asset and agree across CLI and browser."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from library import search
from search import prepare, rank


# Real task wording, with a small set of assets that directly express each intent.
# New additions may outrank older examples when they convey the same relation.
BUSINESS_INTENTS=[
    ('共有部品でコストを減らす', ('illustration/shared-components',)),
    ('事故の原因と被害をそれぞれ防ぐ', ('safety/bowtie-barriers', 'safety/hierarchy-of-controls')),
    ('設備の故障前に予防保全を計画する', ('icon/preventive-maintenance', 'illustration/preventive-maintenance', 'production/maintenance-window')),
    ('検査で見つけた不良品を隔離する', ('icon/defect-isolation', 'illustration/issue-isolation')),
    ('材料ロットをさかのぼって出荷先まで追跡する', ('quality/lot-genealogy', 'illustration/product-traceability')),
    ('引継ぎを受領確認まで確実に行う', ('part/handover-and-acknowledgment',)),
    ('需要の変化が上流で大きくなる理由を示す', ('supply/bullwhip-amplification',)),
    ('代替の調達先を用意して供給停止に備える', ('supply/qualified-dual-sourcing',)),
    ('ボトルネック工程の前に余裕を持たせる', ('production/constraint-buffer-release', 'process/bottleneck-bypass', 'icon/bottleneck')),
    ('作業者とフォークリフトの通路を分ける', ('icon/pedestrian-separation',)),
    ('材料を繰り返し使う再利用を説明する', ('illustration/material-reuse', 'environment/material-recovery-routes')),
    ('電力の有効利用と損失を分ける', ('environment/energy-use-boundary',)),
    ('抜取検査の標本と母集団の関係を説明する', ('part/sample-and-population', 'quality/lot-sampling')),
    ('測定器を標準の基準へつなげて校正する', ('quality/calibration-chain', 'illustration/calibration-reference')),
    ('新入社員の入社手続きを案内する', ('icon/onboarding', 'illustration/newcomer-orientation')),
    ('現場の知識と判断理由を次の担当者へ引き継ぐ', ('people/knowledge-handover', 'icon/knowledge-transfer')),
    ('顧客の声から改善して結果を返す', ('customer/closed-feedback-loop', 'illustration/customer-feedback')),
    ('導入時の初期費用と繰り返す運用費を分ける', ('part/one-time-and-recurring-cost',)),
    ('固定費と数量で増減する変動費を説明する', ('finance/fixed-variable-cost', 'part/fixed-and-variable-cost')),
    ('購入から回収までの資金繰りを整理する', ('finance/working-capital-cycle',)),
    ('データの重複を取り除く', ('icon/duplicate-removal', 'icon/data-cleansing')),
    ('仕様書を最新版へ切り替えて変更点を確認する', ('part/version-and-change', 'development/design-freeze-change', 'illustration/version-comparison')),
    ('相関と因果の違いを示す', ('part/association-and-causation',)),
    ('変更前と変更後の増減率を示す', ('part/difference-and-rate',)),
    ('戻せる判断は小さく試してから調整する', ('part/decision-reversibility',)),
    ('設計の要件と試験結果をひも付ける', ('development/requirements-traceability',)),
    ('技術が実用化できる段階にあるかを説明する', ('development/technology-readiness',)),
    ('reduce downtime with preventive maintenance', ('illustration/preventive-maintenance', 'icon/preventive-maintenance', 'production/maintenance-window')),
    ('trace data from its source through transformations', ('data/transformation-lineage', 'icon/data-lineage')),
    ('separate fixed cost from variable cost', ('finance/fixed-variable-cost', 'part/fixed-and-variable-cost')),
]


class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))['assets']
        cls.config=json.loads((ROOT/'search.json').read_text(encoding='utf-8'))
        cls.prepared=prepare(cls.rows,cls.config)

    def ids(self,query,filters=None):
        return [asset['id'] for asset in rank(self.prepared,query,filters)[0]]

    def test_natural_japanese_and_english_find_matching_intents(self):
        examples=[
            ('品質改善の取り組みを説明したい','framework/pdca'),
            ('工場の安全対策を説明する資料','illustration/safe-work-preparation'),
            ('部署間の連携','strategy/cross-functional-handoffs'),
            ('手順を説明する','illustration/instructions-and-product'),
            ('コストを削減する取り組み','illustration/budget-review'),
            ('製造業の生産性を向上する','framework/pdca'),
            ('quality improvement','framework/pdca'),
            ('team collaboration','relation/shared-responsibility'),
            ('reduce manufacturing cost','illustration/budget-review'),
        ]
        for query,expected in examples:
            with self.subTest(query=query):self.assertIn(expected,self.ids(query)[:10])
        process_candidates={'part/local-and-whole-result','quality/control-plan','process/bottleneck-bypass','production/constraint-buffer-release','production/line-work-balance','framework/pdca'}
        for query in ('manufacturing process improvement','製造工程の改善'):
            self.assertIn(self.ids(query)[0],process_candidates)
            self.assertGreaterEqual(len(set(self.ids(query)[:10]) & process_candidates),3)
        self.assertEqual(self.ids('quality improvement'),self.ids('品質改善'))

    def test_instruction_words_do_not_bury_the_intent(self):
        self.assertEqual(self.ids('品質改善'),self.ids('品質改善の取り組みを説明したい'))
        self.assertEqual(self.ids('品質 改善'),self.ids('品質改善'))
        self.assertEqual(self.ids('ｑｕａｌｉｔｙ　ｉｍｐｒｏｖｅｍｅｎｔ'),self.ids('QUALITY IMPROVEMENT'))

    def test_concrete_topics_outweigh_generic_goals(self):
        self.assertEqual(self.ids('共有部品でコストを減らす')[0],'illustration/shared-components')
        self.assertIn(self.ids('工場の安全対策を説明する資料')[0],{'illustration/safe-work-preparation','icon/safety-footwear','icon/safety-helmet','icon/machine-guard','safety/hierarchy-of-controls'})
        equipment=self.ids('設備の故障を減らす改善活動')
        for expected in ('illustration/equipment-maintenance','illustration/preventive-maintenance','icon/preventive-maintenance'):
            self.assertLess(equipment.index(expected),equipment.index('illustration/energy-saving'))
        self.assertEqual(set(self.ids('spare parts')[:2]),{'icon/spare-parts','illustration/spare-parts-readiness'})
        self.assertEqual(self.ids('report',{'kind':'illustration'})[0],'illustration/reporting')
        self.assertIn('icon/risk',self.ids('risk management')[:3])
        self.assertTrue(set(self.ids('risk management')[:3]) <= {'decision/risk-benefit-balance','icon/risk','planning/risk-response-matrix','part/residual-risk','safety/bowtie-barriers'})
        self.assertIn(self.ids('energy management')[0],{'environment/energy-use-boundary','illustration/energy-saving','icon/energy-efficiency'})

    def test_business_sentences_retrieve_the_specific_subject(self):
        first_matches=0
        for query,expected in BUSINESS_INTENTS:
            with self.subTest(query=query):
                ids=self.ids(query)
                self.assertTrue(set(ids[:5]) & set(expected),(query,ids[:5]))
                first_matches+=bool(ids and ids[0] in expected)
        self.assertGreaterEqual(first_matches,24,'At least 80% of the task sentences should have a directly relevant first result')

    def test_compound_phrases_do_not_double_count_their_fragments(self):
        _,terms=rank(self.prepared,'共有部品でコストを減らす')
        self.assertIn('共通部品',terms)
        self.assertNotIn('共有',terms)
        self.assertNotIn('部品',terms)
        _,terms=rank(self.prepared,'spare parts')
        self.assertIn('予備部品',terms)
        self.assertNotIn('部品',terms)
        # A separate occurrence still carries meaning: it must survive deduplication.
        _,terms=rank(self.prepared,'shared components and other parts')
        self.assertIn('共通部品',terms)
        self.assertIn('部品',terms)
        _,terms=rank(self.prepared,'不可逆')
        self.assertIn('不可逆',terms)
        self.assertNotIn('可逆',terms)

    def test_rewording_does_not_change_a_concrete_topic(self):
        for query in ('共通部品','共有部品','部品の共通化','shared components','common components'):
            with self.subTest(query=query):
                self.assertEqual(self.ids(query)[0],'illustration/shared-components')
        self.assertEqual(self.ids('材料 再利用'),self.ids('材料を再利用することを説明したい'))
        self.assertIn('people/knowledge-handover',self.ids('知識を次の担当へ引き継ぐ')[:3])
        self.assertIn('data/transformation-lineage',self.ids('trace data through transformations')[:3])

    def test_every_title_finds_its_own_asset_and_partial_titles_work(self):
        for asset in self.rows:
            with self.subTest(title=asset['title']):self.assertEqual(self.ids(asset['title'])[0],asset['id'])
        self.assertEqual(self.ids('声を集'),['illustration/customer-feedback'])
        self.assertIn('illustration/customer-feedback',self.ids('声を集めるイラスト')[:3])

    def test_exact_id_wins_and_unknown_intent_is_empty(self):
        for asset in self.rows:
            with self.subTest(id=asset['id']):self.assertEqual(self.ids(asset['id'])[0],asset['id'])
        for query in ('zzzxqv unfoundword','宇宙旅行のチケット','regex.* + [unmatched]','意図'):
            with self.subTest(query=query):self.assertEqual(self.ids(query),[])
        self.assertEqual({asset['kind'] for asset in rank(self.prepared,'図')[0]}, {'diagram'})

    def test_every_asset_is_accessible_and_equal_scores_mix_kinds(self):
        all_ids=self.ids('')
        self.assertEqual(len(all_ids),len(self.rows))
        self.assertEqual(set(all_ids),{asset['id'] for asset in self.rows})
        self.assertEqual(len({asset['kind'] for asset in rank(self.prepared,'')[0][:6]}),6)
        result=search('',limit=0)
        self.assertEqual(result['returned'],len(self.rows));self.assertIsNone(result['next_offset'])
        paged=[];offset=0
        while True:
            page=search('',limit=37,offset=offset);paged.extend(asset['id'] for asset in page['assets'])
            self.assertEqual(page['returned'],len(page['assets']))
            if page['next_offset'] is None:break
            offset=page['next_offset']
        self.assertEqual(paged,all_ids)
        self.assertEqual(search('',offset=len(self.rows)+1)['returned'],0)

    def test_filters_are_explicit_exact_and_never_inferred(self):
        self.assertEqual(search('品質')['filters'],{})
        self.assertGreater(len({asset['kind'] for asset in search('品質',limit=0)['assets']}),1)
        result=search('品質',kind='illustration',format='png',transparent=True,limit=0)
        self.assertEqual(result['filters'],dict(kind='illustration',format='png',transparent=True))
        self.assertTrue(result['assets'])
        self.assertTrue(all(asset['kind']=='illustration' and asset['format']=='png' and asset['transparent'] is True for asset in result['assets']))
        self.assertEqual(search('',kind='background',themeable=True)['total'],0)
        category=self.rows[0]['category']
        self.assertEqual(set(self.ids('',{'category':category})),{asset['id'] for asset in self.rows if asset['category']==category})
        icons=search('',kind='icon',limit=0)
        self.assertEqual(icons['total'],sum(asset['kind']=='icon' for asset in self.rows))
        self.assertEqual(icons['returned'],icons['total'])

    def test_compact_index_and_full_metadata_have_same_results(self):
        full=[json.loads((ROOT/asset['metadata_path']).read_text(encoding='utf-8')) for asset in self.rows]
        full_index=prepare(full,self.config)
        for query in ['', '管理', '背景', '計画', '品質改善', '部署間の連携', '右向き', '承認 差戻し', *[query for query,_ in BUSINESS_INTENTS]]:
            with self.subTest(query=query):
                self.assertEqual(self.ids(query),[asset['id'] for asset in rank(full_index,query)[0]])

    def test_invalid_paging_is_an_error(self):
        for options in ({'limit':-1},{'offset':-1},{'limit':True},{'offset':1.5}):
            with self.assertRaises(ValueError):search('',**options)

    @unittest.skipUnless(shutil.which('node'),'Node is only needed to verify browser search parity')
    def test_browser_and_python_ranking_and_filters_agree(self):
        queries=['','品質改善の取り組みを説明したい','品質 改善','quality improvement','manufacturing process improvement','How can we improve product quality?','部署間の連携','team collaboration','工場の安全対策を説明する資料','コストを削減する取り組み','共有部品でコストを減らす','設備の故障を減らす改善活動','管理','背景','青い抽象的な背景','承認 差戻し','右向き','parts','spare parts','ＰＤＣＡ','図','意図','risk management','energy management','声を集める','声を集','illustration/explaining','zzzxqv unfoundword','regex.* + [unmatched]']
        queries.extend(query for query,_ in BUSINESS_INTENTS)
        queries.extend(['shared components and other parts','不可逆','trace data through transformations'])
        cases=[dict(query=query,filters=filters) for query in queries for filters in ({},{'kind':'illustration'},{'format':'svg','themeable':True},{'transparent':True},{'kind':'background','transparent':False},{'category':self.rows[0]['category']})]
        script="const fs=require('fs'),search=require('./web/search.js'),input=JSON.parse(fs.readFileSync(0,'utf8')),prepared=search.prepare(input.rows,input.config);process.stdout.write(JSON.stringify(input.cases.map(({query,filters})=>{const result=search.rank(prepared,query,filters);return {ids:result.assets.map(a=>a.id),terms:result.terms};})));"
        result=subprocess.run([shutil.which('node'),'-e',script],cwd=ROOT,input=json.dumps(dict(rows=self.rows,config=self.config,cases=cases)).encode('utf-8'),capture_output=True,check=True)
        actual=json.loads(result.stdout)
        for case,browser in zip(cases,actual):
            with self.subTest(**case):
                ranked,terms=rank(self.prepared,case['query'],case['filters'])
                self.assertEqual(browser,dict(ids=[asset['id'] for asset in ranked],terms=terms))


if __name__=='__main__':unittest.main()
