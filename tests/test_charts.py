"""Numerical and layout regressions for user-supplied quantitative artwork."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from chart_inputs import normalize, input_contract
from sets.metrics import render_chart, make_assets
from registry import metadata, svg_document
from library import add_labels
from check_charts import CHECKS, Drawing

NEW=('dot','actual_target','range','diverging_bar','pareto','scatter')


class ChartTests(unittest.TestCase):
    def test_all_exported_samples_have_numerically_correct_geometry(self):
        samples=make_assets()
        self.assertEqual({a['data']['chart_type'] for a in samples},set(CHECKS))
        for a in samples:
            with self.subTest(kind=a['data']['chart_type']):
                CHECKS[a['data']['chart_type']](Drawing(ET.fromstring(svg_document(a))),a['data'])

    def test_new_geometry_audit_rejects_distorted_values(self):
        for kind in NEW:
            a=render_chart(kind,input_contract(kind)['example']);root=ET.fromstring(svg_document(a));drawing=Drawing(root)
            CHECKS[kind](drawing,a['data'])
            if kind in ('actual_target','diverging_bar','pareto'):
                mark=drawing.tags('rect')[0];mark.set('width',str(float(mark.get('width'))+10))
            else:
                mark=drawing.tags('circle')[0];mark.set('cx',str(float(mark.get('cx'))+10))
            with self.assertRaises(AssertionError,msg=kind):CHECKS[kind](Drawing(root),a['data'])

    def test_samples_and_real_data_have_valid_readable_labels(self):
        for example in make_assets():
            kind=example['data']['chart_type']
            for a in (example,render_chart(kind,input_contract(kind)['example'])):
                meta=metadata(a);svg,_=add_labels(svg_document(a),meta,{},True);ET.fromstring(svg)
                minimum=20 if a['width']<=600 else 24
                for label in meta['labels']:
                    self.assertGreaterEqual(label['font_size'],minimum,(kind,label['text']))
                    self.assertGreaterEqual(label['x'],0);self.assertGreaterEqual(label['y'],0)
                    self.assertLessEqual(label['x']+label['width'],a['width'])
                    self.assertLessEqual(label['y']+label['height'],a['height'])

    def test_short_months_remain_compact_and_complete(self):
        for kind in ('vertical_bar','line'):
            data=input_contract(kind)['example'];data['categories']=[f'{i+1}月' for i in range(12)];data['series'][0]['values']=[20+i*3 for i in range(12)]
            a=render_chart(kind,data);meta=metadata(a);add_labels(svg_document(a),meta,{},True)
            self.assertLessEqual(a['width'],1500)
            self.assertEqual(a['height'],720)
            self.assertEqual([l['text'].replace('\n','') for l in a['labels'][1:]],data['categories'])
            self.assertTrue(all(l['font_size']>=24 for l in meta['labels']))

    def test_variable_names_expand_without_losing_values(self):
        for kind,count in (('horizontal_bar',9),('vertical_bar',7),('line',7),('grouped_bar',6),('stacked_percent_bar',8),('waterfall',9)):
            data=input_contract(kind)['example'];data['categories']=['工程条件の確認'+str(i+1) for i in range(count)]
            for j,s in enumerate(data['series']):s['values']=[20+j*10+i for i in range(count)]
            if kind=='stacked_percent_bar':
                for j,s in enumerate(data['series']):s['values']=[(30,40,30)[j]]*count
            if kind=='waterfall':data['series'][0]['values']=[100,5,-4,2,7,-2,10,-3,115]
            a=render_chart(kind,data);meta=metadata(a);add_labels(svg_document(a),meta,{},True)
            self.assertEqual(a['data']['categories'],data['categories'])
            self.assertEqual(a['data']['series'],data['series'])
            self.assertTrue(all(l['font_size']>=24 for l in meta['labels']))

    def test_range_ordering_is_checked_and_endpoints_map_to_axis(self):
        data=input_contract('range')['example'];data['series'][0]['values'][1]=68
        with self.assertRaises(ValueError):render_chart('range',data)
        data=input_contract('range')['example'];data['series'][0]['values'][0]=data['series'][1]['values'][0]=data['series'][2]['values'][0]=50
        a=render_chart('range',data);m=a['data']['marks'][0];p=a['data']['plot']
        self.assertEqual(m['lower_x'],m['representative_x']);self.assertEqual(m['representative_x'],m['upper_x'])
        self.assertAlmostEqual(m['lower_x'],p['x']+p['width']/2)
        self.assertIn('r="10"',a['body'])

    def test_actual_target_handles_exceeding_and_zero_targets(self):
        data=input_contract('actual_target')['example'];data['series'][0]['values']=[0,100,60];data['series'][1]['values']=[0,70,80]
        a=render_chart('actual_target',data);marks=a['data']['marks'];p=a['data']['plot']
        self.assertEqual(marks[0]['actual_x'],p['x']);self.assertEqual(marks[0]['target_x'],p['x'])
        self.assertEqual(marks[1]['actual_x'],p['x']+p['width']);self.assertGreater(marks[1]['actual_x'],marks[1]['target_x'])
        self.assertLess(marks[2]['actual_x'],marks[2]['target_x'])

    def test_signed_values_extend_in_the_correct_direction(self):
        data=input_contract('diverging_bar')['example'];data['series'][0]['values']=[-40,0,20,40]
        a=render_chart('diverging_bar',data);m=a['data']['marks'];p=a['data']['plot']
        self.assertEqual(m[0]['x'],p['x']);self.assertEqual(m[1]['width'],0)
        self.assertEqual(m[3]['x'],p['x']+p['width']);self.assertEqual(m[0]['width'],m[3]['width'])
        self.assertIn('-40から40',str(a['guidance']))
        bad=deepcopy(data);bad['domain']=[-30,40]
        with self.assertRaises(ValueError):render_chart('diverging_bar',bad)

    def test_pareto_sorts_geometry_preserves_input_and_ends_at_100(self):
        data=dict(categories=['A','B','C'],series=[dict(label='件数',values=[30,60,10])],unit='件')
        a=render_chart('pareto',data);d=a['data']
        self.assertEqual(d['sorted_indices'],[1,0,2]);self.assertEqual(d['ordered_categories'],['B','A','C'])
        self.assertEqual(d['cumulative_percent'],[60,90,100]);self.assertEqual(d['series'],data['series']);self.assertEqual(d['categories'],data['categories'])
        root=ET.fromstring('<svg>'+a['body']+'</svg>');bars=[e for e in root if e.tag=='rect' and e.get('fill')=='#79A7ED']
        self.assertEqual(len(bars),3);self.assertGreater(float(bars[0].get('height')),float(bars[1].get('height')))
        self.assertAlmostEqual(float(bars[0].get('height'))/float(bars[2].get('height')),6)
        bad=deepcopy(data);bad['series'][0]['values']=[0,0,0]
        with self.assertRaises(ValueError):render_chart('pareto',bad)

    def test_scatter_axes_are_independent_and_signed(self):
        data=dict(categories=['A','B','C'],series=[dict(label='温度差',values=[-10,0,10]),dict(label='変化',values=[30,10,-10])],x_unit='度',unit='件',x_domain=[-10,10],domain=[-10,30])
        a=render_chart('scatter',data);d=a['data'];p=d['plot'];points=d['points']
        self.assertEqual(points[0]['x'],p['x']);self.assertEqual(points[0]['y'],p['y'])
        self.assertEqual(points[-1]['x'],p['x']+p['width']);self.assertEqual(points[-1]['y'],p['y']+p['height'])
        self.assertEqual(points[1]['x'],p['x']+p['width']/2);self.assertEqual(points[1]['y'],p['y']+p['height']/2)
        self.assertEqual(d['x_unit'],'度');self.assertEqual(d['unit'],'件')
        bad=deepcopy(data);bad['x_domain']=[0,10]
        with self.assertRaises(ValueError):render_chart('scatter',bad)
        bad=deepcopy(data);bad.pop('x_unit')
        with self.assertRaises(ValueError):render_chart('scatter',bad)

    def test_new_contracts_reject_nonfinite_or_misaligned_series(self):
        for kind in NEW:
            data=input_contract(kind)['example'];data['series'][0]['values'][0]=float('nan')
            with self.assertRaises(ValueError,msg=kind):render_chart(kind,data)
            data=input_contract(kind)['example'];data['series'][0]['values'].pop()
            with self.assertRaises(ValueError,msg=kind):render_chart(kind,data)

    def test_existing_bar_geometry_uses_the_supplied_values(self):
        data=input_contract('vertical_bar')['example'];data['series'][0]['values']=[0,25,50,100]
        a=render_chart('vertical_bar',data);root=ET.fromstring('<svg>'+a['body']+'</svg>');bars=[e for e in root if e.tag=='rect' and e.get('fill')=='#2864F0']
        self.assertEqual([float(e.get('height')) for e in bars],[0,105,210,420])
        self.assertEqual([float(e.get('y'))+float(e.get('height')) for e in bars],[566]*4)
        self.assertEqual(normalize('waterfall')['series'][0]['values'][-1],130)


if __name__=='__main__':unittest.main()
