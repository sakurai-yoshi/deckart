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
            ('manufacturing process improvement','process/bottleneck-bypass'),
            ('team collaboration','relation/shared-responsibility'),
            ('reduce manufacturing cost','illustration/budget-review'),
        ]
        for query,expected in examples:
            with self.subTest(query=query):self.assertIn(expected,self.ids(query)[:10])
        self.assertEqual(self.ids('quality improvement'),self.ids('品質改善'))

    def test_instruction_words_do_not_bury_the_intent(self):
        self.assertEqual(self.ids('品質改善'),self.ids('品質改善の取り組みを説明したい'))
        self.assertEqual(self.ids('品質 改善'),self.ids('品質改善'))
        self.assertEqual(self.ids('ｑｕａｌｉｔｙ　ｉｍｐｒｏｖｅｍｅｎｔ'),self.ids('QUALITY IMPROVEMENT'))

    def test_concrete_topics_outweigh_generic_goals(self):
        self.assertEqual(self.ids('共有部品でコストを減らす')[0],'illustration/shared-components')
        self.assertEqual(self.ids('工場の安全対策を説明する資料')[0],'illustration/safe-work-preparation')
        equipment=self.ids('設備の故障を減らす改善活動')
        for expected in ('illustration/equipment-maintenance','illustration/preventive-maintenance','icon/preventive-maintenance'):
            self.assertLess(equipment.index(expected),equipment.index('illustration/energy-saving'))
        self.assertEqual(set(self.ids('spare parts')[:2]),{'icon/spare-parts','illustration/spare-parts-readiness'})
        self.assertEqual(self.ids('report',{'kind':'illustration'})[0],'illustration/reporting')
        self.assertIn('icon/risk',self.ids('risk management')[:3])
        self.assertEqual(set(self.ids('risk management')[:3]),{'decision/risk-benefit-balance','icon/risk','planning/risk-response-matrix'})
        self.assertEqual(self.ids('energy management')[0],'illustration/energy-saving')

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
        for query in ('','管理','背景','計画','品質改善','部署間の連携','右向き','承認 差戻し'):
            with self.subTest(query=query):
                self.assertEqual(self.ids(query),[asset['id'] for asset in rank(full_index,query)[0]])

    def test_invalid_paging_is_an_error(self):
        for options in ({'limit':-1},{'offset':-1},{'limit':True},{'offset':1.5}):
            with self.assertRaises(ValueError):search('',**options)

    @unittest.skipUnless(shutil.which('node'),'Node is only needed to verify browser search parity')
    def test_browser_and_python_ranking_and_filters_agree(self):
        queries=['','品質改善の取り組みを説明したい','品質 改善','quality improvement','manufacturing process improvement','How can we improve product quality?','部署間の連携','team collaboration','工場の安全対策を説明する資料','コストを削減する取り組み','共有部品でコストを減らす','設備の故障を減らす改善活動','管理','背景','青い抽象的な背景','承認 差戻し','右向き','parts','spare parts','ＰＤＣＡ','図','意図','risk management','energy management','声を集める','声を集','illustration/explaining','zzzxqv unfoundword','regex.* + [unmatched]']
        cases=[dict(query=query,filters=filters) for query in queries for filters in ({},{'kind':'illustration'},{'format':'svg','themeable':True},{'transparent':True},{'kind':'background','transparent':False},{'category':self.rows[0]['category']})]
        script="const fs=require('fs'),search=require('./web/search.js'),input=JSON.parse(fs.readFileSync(0,'utf8')),prepared=search.prepare(input.rows,input.config);process.stdout.write(JSON.stringify(input.cases.map(({query,filters})=>{const result=search.rank(prepared,query,filters);return {ids:result.assets.map(a=>a.id),terms:result.terms};})));"
        result=subprocess.run([shutil.which('node'),'-e',script],cwd=ROOT,input=json.dumps(dict(rows=self.rows,config=self.config,cases=cases)).encode('utf-8'),capture_output=True,check=True)
        actual=json.loads(result.stdout)
        for case,browser in zip(cases,actual):
            with self.subTest(**case):
                ranked,terms=rank(self.prepared,case['query'],case['filters'])
                self.assertEqual(browser,dict(ids=[asset['id'] for asset in ranked],terms=terms))


if __name__=='__main__':unittest.main()
