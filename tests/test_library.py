"""Regression checks for the AI-facing export boundary and semantic paint roles."""
from copy import deepcopy
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from library import render, export_files, search
from themes import resolve_theme, contrast, annotate_roles
from sets.metrics import render_chart, input_contract
from build import zip_entry


class ExportTests(unittest.TestCase):
    def test_zip_bytes_do_not_depend_on_host_platform(self):
        def package(platform):
            output=BytesIO()
            with patch.object(sys,'platform',platform):
                with zipfile.ZipFile(output,'w') as archive:zip_entry(archive,'asset.svg',b'<svg/>\n')
            return output.getvalue()
        self.assertEqual(package('linux'),package('win32'))

    def test_platform_tail_digits_produce_identical_svg(self):
        first='<svg xmlns="http://www.w3.org/2000/svg"><g transform="translate(249.52560554401657 489.5801025878342) scale(1.2272727272727273)"/></svg>'
        second=first.replace('249.52560554401657','249.52560554401663')
        self.assertEqual(annotate_roles(first),annotate_roles(second))

    def test_search_and_direct_export(self):
        result=search('承認 差戻し')
        self.assertIn('process/approval-return',[a['id'] for a in result['assets']])
        svg,meta=render({'id':'process/approval-return'})
        self.assertEqual(hashlib.sha256(svg.encode()).hexdigest(),meta['sha256'])
        self.assertIn('viewBox=',svg)

    def test_color_roles_preserve_signals_and_geometry(self):
        original,_=render({'id':'chart/waterfall'})
        changed,meta=render({'id':'chart/waterfall','accent':'#FFDD00'})
        self.assertTrue(meta['theme']['adjustments'])
        self.assertGreaterEqual(contrast(meta['theme']['colors']['accent']),4.5)
        a,b=ET.fromstring(original),ET.fromstring(changed)
        for left,right in zip(a.iter(),b.iter()):
            for attribute in ('d','x','y','width','height','transform','points'):
                self.assertEqual(left.get(attribute),right.get(attribute))
            for paint in ('fill','stroke'):
                if left.get('data-'+paint+'-role') in ('positive','negative','caution'):
                    self.assertEqual(left.get(paint),right.get(paint))

    def test_theme_extremes_remain_readable(self):
        for color in ('#FFFFFF','#000000','#FFFF00','#00FFFF','#FF00FF','#FF0000','#00FF00'):
            theme=resolve_theme(color)
            self.assertGreaterEqual(contrast(theme['colors']['accent']),4.5)
            self.assertGreaterEqual(contrast(theme['colors']['ink'],theme['colors']['mid']),4.5)
        with self.assertRaises(ValueError):resolve_theme('url(https://example.com)')

    def test_user_labels_escape_markup_and_reject_overflow(self):
        svg,meta=render({'id':'process/approval-return','labels':{'label-1':'<申請>'}})
        self.assertIn('&lt;申請&gt;',svg)
        self.assertEqual(meta['rendered_labels'],['label-1'])
        for labels in ({'unknown':'内容'},{'label-1':'長'*200}):
            with self.assertRaises(ValueError):render({'id':'process/approval-return','labels':labels})

    def test_wide_latin_and_invalid_xml_text_rejected(self):
        with self.assertRaises(ValueError):
            render({'id':'decision/current-target-bridge','labels':{'label-1':'WWWWWWWWWW'}})
        for text in ('\ufffe','\ud800','\x00'):
            with self.assertRaises(ValueError):render({'id':'process/approval-return','labels':{'label-1':text}})
            data=input_contract('horizontal_bar')['example'];data['categories'][0]=text
            with self.assertRaises(ValueError):render({'id':'chart/horizontal-bar','data':data})

    def test_categorical_roles_remain_distinct(self):
        for request in ({'monochrome':True},{'accent':'#153A6B'},{'accent':'#000000'}):
            _,meta=render({'id':'chart/pie',**request})
            colors=meta['theme']['colors']
            self.assertGreaterEqual(contrast(colors['accent'],colors['series_secondary']),1.5)
            self.assertGreaterEqual(contrast(colors['series_secondary']),4.5)

    def test_data_replaces_sample_and_updates_geometry(self):
        source,_=render({'id':'chart/progress-ring'})
        request=json.loads((ROOT/'examples/progress-data.json').read_text(encoding='utf-8'))
        changed,meta=render(request)
        self.assertNotEqual(source,changed)
        self.assertFalse(meta['data']['is_sample'])
        self.assertEqual(meta['data']['series'][0]['values'],[62,38])
        self.assertIn('62',json.dumps(meta['guidance'],ensure_ascii=False))

    def test_every_chart_accepts_its_documented_contract(self):
        index=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
        for a in index['assets']:
            if a['kind']!='chart':continue
            meta=json.loads((ROOT/a['metadata_path']).read_text(encoding='utf-8'))
            data=meta['data_input']['example']
            _,result=render({'id':a['id'],'data':data})
            self.assertFalse(result['data']['is_sample'])
            self.assertEqual(result['data']['categories'],data['categories'])

    def test_invalid_chart_data_cannot_be_silently_rendered(self):
        samples=[]
        base=input_contract('horizontal_bar')['example']
        bad=deepcopy(base);bad['series'][0]['values'][0]=float('nan');samples.append(('horizontal_bar',bad))
        bad=deepcopy(base);bad['series'][0]['values'].pop();samples.append(('horizontal_bar',bad))
        bad=deepcopy(base);bad['domain']=[0,1];samples.append(('horizontal_bar',bad))
        bad=deepcopy(base);bad['series'][0]['values'][0]=10**400;samples.append(('horizontal_bar',bad))
        bad=input_contract('waterfall')['example'];bad['series'][0]['values'][-1]+=1;samples.append(('waterfall',bad))
        for kind,data in samples:
            with self.assertRaises(ValueError):render_chart(kind,data)

    def test_unknown_fields_and_paths_rejected(self):
        for request in ({'id':'../catalog'},{'id':'icon/person','unknown':1},{'id':'icon/person','data':{}},{'id':'icon/person','monochrome':True,'accent':'#000000'}):
            with self.assertRaises(ValueError):render(request)

    def test_export_is_explicit_and_records_source(self):
        svg,meta=render({'id':'icon/person','accent':'#005BAC'})
        with tempfile.TemporaryDirectory() as directory:
            destination=Path(directory)/'person.svg'
            result=export_files(svg,meta,destination)
            saved=json.loads(destination.with_suffix('.json').read_text(encoding='utf-8'))
            self.assertEqual(saved['source']['id'],'icon/person')
            self.assertEqual(saved['sha256'],result['sha256'])
            self.assertEqual(hashlib.sha256(destination.read_bytes()).hexdigest(),saved['sha256'])
            with self.assertRaises(ValueError):export_files(svg,meta,destination)
            with self.assertRaises(ValueError):export_files(svg,meta,ROOT/'assets'/'unsafe.svg')

    def test_stdout_emits_exact_utf8_svg_bytes(self):
        svg,_=render({'id':'icon/person'})
        result=subprocess.run([sys.executable,str(ROOT/'scripts/library.py'),'export','icon/person','--stdout'],check=True,capture_output=True)
        self.assertEqual(result.stdout,svg.encode('utf-8'))

    def test_export_preview_resolves_to_the_saved_file(self):
        for request in ({'id':'process/approval-return','accent':'#005BAC'},
                        {'id':'process/approval-return','include_example_labels':True},
                        {'id':'chart/vertical-bar','data':input_contract('vertical_bar')['example']}):
            with self.subTest(request=request),tempfile.TemporaryDirectory() as directory:
                content,meta=render(request)
                destination=Path(directory)/'output.svg'
                export_files(content,meta,destination)
                saved=json.loads(destination.with_suffix('.json').read_text(encoding='utf-8'))
                self.assertEqual((destination.parent/saved['preview_path']).read_text(encoding='utf-8'),content)
                self.assertNotIn('preview_sha256',saved)
                self.assertFalse(saved['preview_has_example_labels'])
                original=(ROOT/saved['source']['preview_path']).read_bytes()
                self.assertEqual(hashlib.sha256(original).hexdigest(),saved['source']['preview_sha256'])

    def test_json_stdio_is_utf8_even_with_a_legacy_console_encoding(self):
        env={**os.environ,'PYTHONIOENCODING':'cp1252'}
        command=[sys.executable,str(ROOT/'scripts/library.py')]
        result=subprocess.run([*command,'show','icon/person'],env=env,capture_output=True,check=True)
        self.assertEqual(json.loads(result.stdout.decode('utf-8'))['id'],'icon/person')
        bad=subprocess.run([*command,'search','person','--不明'],env=env,capture_output=True)
        self.assertEqual(bad.returncode,2)
        self.assertIn('--不明',json.loads(bad.stderr.decode('utf-8'))['error'])

    def test_failed_sidecar_export_preserves_existing_svg(self):
        svg,meta=render({'id':'icon/person'})
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'person.svg';target.write_text('existing user content',encoding='utf-8')
            target.with_suffix('.json').mkdir()
            with self.assertRaises(ValueError):export_files(svg,meta,target,force=True)
            self.assertEqual(target.read_text(encoding='utf-8'),'existing user content')
            self.assertEqual(sorted(p.name for p in Path(directory).iterdir()),['person.json','person.svg'])


if __name__=='__main__':unittest.main()
