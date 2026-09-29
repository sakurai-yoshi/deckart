#!/usr/bin/env python3
"""Validate the published retrieval contract, standalone SVG/PNG assets and release archive."""
import base64
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile
from registry import ROOT, KEY_RE, project, png_info, asset_path
from themes import theme_contract, resolve_theme, contrast, apply_theme

KINDS={'diagram','illustration','icon','chart','background','part'}
ALLOWED={'svg','title','desc','g','rect','circle','ellipse','line','path','polygon','polyline'}


def bounds(box,width,height):
    return 0<=box['x']<box['x']+box['width']<=width and 0<=box['y']<box['y']+box['height']<=height


def validate():
    catalog=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'));rows=catalog['assets']
    assert catalog['asset_count']==len(rows) and len({a['id'] for a in rows})==len(rows)
    assert catalog['version']==project()['version'] and catalog['license']=='CC0-1.0'
    assert catalog['raw_base']==f'https://raw.githubusercontent.com/{catalog["repository"]}/v{catalog["version"]}/'
    # Bound retrieval overhead per asset while allowing the library to grow.
    assert len(json.dumps(catalog,ensure_ascii=False).encode())<=1024*len(rows),'Keep the AI index compact per asset'
    records=[json.loads(asset_path(a['metadata_path'],'metadata').read_text(encoding='utf-8')) for a in rows]
    assert {a['path'] for a in records}=={p.relative_to(ROOT).as_posix() for folder,pattern in [('assets','*.svg'),('media','*.png')] for p in (ROOT/folder).rglob(pattern)},'Unregistered asset'
    assert {a['metadata_path'] for a in records}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'metadata').rglob('*.json')},'Unregistered metadata'
    assert {a['kind'] for a in records}==KINDS
    default=resolve_theme();colors=default['colors']
    assert json.loads((ROOT/'themes.json').read_text(encoding='utf-8'))==theme_contract()
    for color in ('#2864F0','#005BAC','#FFDD00','#FFFFFF','#000000','#00FF00'):
        theme=resolve_theme(color)
        assert contrast(theme['colors']['accent'])>=4.5
        assert contrast(theme['colors']['ink'],theme['colors']['mid'])>=4.5
        assert all(theme['colors'][role]==colors[role] for role in ('positive','negative','caution'))
    for a,row in zip(records,rows):
        file=asset_path(a['path'],'media' if a['format']=='png' else 'assets');content=file.read_bytes()
        assert KEY_RE.fullmatch(a['id']) and a['id']==row['id']
        assert a['format'] in ('svg','png')
        assert a['path']==f'{"media" if a["format"]=="png" else "assets"}/{a["id"]}.{a["format"]}' and a['metadata_path']==f'metadata/{a["id"]}.json'
        assert hashlib.sha256(content).hexdigest()==a['sha256']==row['sha256'],file
        assert len(content)==a['size_bytes']==row['size_bytes'],file
        assert a['name'] and a['description'] and len(a['keywords'])>=3 and a['search_text'],file
        assert a['schema_version']==2 and a['license']=='CC0-1.0'
        guide=a['guidance'];assert set(guide)=={'use_case','message','reading','avoid'}
        assert all(isinstance(guide[k],str) and guide[k] for k in ('use_case','message')),file
        assert 1<=len(guide['reading'])<=4 and all(guide['reading']),file
        assert row['use_case']==guide['use_case'] and row['message']==guide['message'],file
        assert a['format']==('png' if a['kind'] in ('illustration','background') else 'svg'),file
        assert all(row[field]==a[field] for field in ('format','mime_type','transparent','canvas','render')),file
        if a['format']=='png':
            info=png_info(content)
            assert (a['width'],a['height'],a['transparent'])==(info['width'],info['height'],info['transparent']),file
            assert a['mime_type']=='image/png' and a['render']==dict(theme=False,labels=False,data=False) and not a['labels'],file
            assert set(a['generation'])=={'method','definition_path'} and a['generation']['method']=='image-generation',file
            definitions=json.loads(asset_path(a['generation']['definition_path'],'sources').read_text(encoding='utf-8'))
            declaration=next(item for item in definitions if item['key']==a['id'])
            assert declaration['generation']['method']=='image-generation' and declaration['generation']['prompt'],file
            if a['kind']=='illustration':assert a['transparent'] is True and info['alpha_min']==0,file
            else:assert a['transparent'] is False,file
            if a.get('preview_path'):
                preview=asset_path(a['preview_path'],'previews');small=png_info(preview.read_bytes())
                assert max(small['width'],small['height'])<=768 and abs(small['width']/small['height']-a['width']/a['height'])<.02,file
        else:
            assert a['mime_type']=='image/svg+xml' and a['render']['theme'],file
            tree=ET.fromstring(content)
            assert tree.attrib['viewBox']==f'0 0 {a["width"]} {a["height"]}',file
            for el in tree.iter():
                assert el.tag.split('}')[-1] in ALLOWED,file
                assert not any(k.lower().startswith('on') or 'href' in k.lower() or k=='style' for k in el.attrib),file
                assert not any('url(' in v.lower() or re.search(r'\b(?:nan|infinity)\b',v,re.I) for v in el.attrib.values()),file
                for paint in ('fill','stroke'):
                    value=el.get(paint);role=el.get('data-'+paint+'-role')
                    if value and value!='none':assert role in colors and value==colors[role],(file,value,role)
                for name in ('width','height','r','rx','ry','stroke-width'):
                    if name in el.attrib:assert math.isfinite(float(el.attrib[name])) and float(el.attrib[name])>=0,(file,name)
        if a.get('placement'):
            placement=a['placement']
            assert placement==row['placement'] and placement['framing'] in ('waist-up','full-body','object'),file
            assert placement['facing'] in ('left','right','front','inward','down'),file
            if 'people_count' in placement:assert type(placement['people_count']) is int and 0<=placement['people_count']<=10,file
            size=placement['recommended_width_cm'];assert len(size)==2 and 0<size[0]<=size[1]<=34,file
        for i,label in enumerate(a['labels']):
            assert label['id']==f'label-{i+1}' and bounds(label,a['width'],a['height']),(file,label)
            assert label['text'] and label['role'] and label['align'] in ('left','center')
            assert label['font_size']>0 and label['max_lines']>0 and label['max_fullwidth_chars']>0
            assert label['color']==colors[label['color_role']]
        if a['labels']:
            from library import add_labels
            add_labels(content.decode(),deepcopy(a),{},include_examples=True)
        if a['kind']=='background':
            canvas=a['canvas'];assert canvas['width']/canvas['height']==16/9 and abs(a['width']/a['height']-16/9)<.005,file
            areas=a['content_areas'];assert areas and len({area['id'] for area in areas})==len(areas),file
            for i,area in enumerate(areas):
                assert re.fullmatch(r'[a-z][a-z0-9-]*',area['id']) and area['role'] and area['purpose'],file
                assert bounds(area,canvas['width'],canvas['height']),(file,area)
                for other in areas[i+1:]:
                    overlap=min(area['x']+area['width'],other['x']+other['width'])>max(area['x'],other['x']) and min(area['y']+area['height'],other['y']+other['height'])>max(area['y'],other['y'])
                    assert not overlap,(file,'Overlapping content areas',area['id'],other['id'])
        if a['kind']=='chart':
            data=a['data'];assert data['is_sample'] is True and '作例' in a['name'] and data['unit']
            assert a['data_input']['category_count']==len(data['categories'])
            assert all(len(s['values'])==len(data['categories']) for s in data['series'])
        if a['format']=='svg':
            for theme in (resolve_theme('#005BAC'),resolve_theme(monochrome=True)):ET.fromstring(apply_theme(content.decode(),theme))
    assert [json.loads(line) for line in (ROOT/'catalog.ndjson').read_text(encoding='utf-8').splitlines()]==records
    page=(ROOT/'index.html').read_text(encoding='utf-8')
    embedded=json.loads(re.search(r'<script id="library" type="application/json">(.*?)</script>',page,re.S).group(1))
    assert [{k:v for k,v in a.items() if k!='download'} for a in embedded]==records,'Gallery metadata mismatch'
    for a in embedded:
        if a['format']=='svg':assert base64.b64decode(a['download'])==(ROOT/a['path']).read_bytes(),a['id']
        else:assert 'download' not in a,a['id']
    with zipfile.ZipFile(ROOT/'deckart.zip') as archive:
        assert archive.testzip() is None
        names=archive.namelist();assert len(names)==len(set(names))
        assert names==sorted(names),'Release ZIP entries must use identical path ordering on every OS'
        assert all(info.create_system==3 for info in archive.infolist()),'Release ZIP metadata must be independent of the build host'
        assert {'index.html','web/themes.js','web/catalog.js','llms.txt','scripts/library.py','catalog.json','request.schema.json'}<=set(names)
        for name in names:
            assert not Path(name).is_absolute() and '..' not in Path(name).parts,name
            assert archive.read(name)==(ROOT/name).read_bytes(),name
        assert {a['path'] for a in records}<=set(names)
    from check_charts import validate_charts
    validate_charts(ROOT,records)
    print(f'PASS: {len(rows)} SVG/PNG assets; AI index and sidecars; paint roles; placement bounds; chart geometry; offline archive')


if __name__=='__main__':validate()
