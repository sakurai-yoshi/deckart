#!/usr/bin/env python3
"""Generate direct SVG/PNG assets, a compact AI index, sidecars and the offline gallery."""
import base64
import hashlib
import html
import json
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
from registry import ROOT, artwork, svg_document, metadata, project, asset_path
from themes import theme_contract, canonical_geometry


def packed_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')


def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))


def zip_entry(archive,name,data):
    info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.create_system=3;info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
    archive.writestr(info,data)


def browse_text(records):
    """Small complete inventory for an AI to read before loading candidate details."""
    kinds={'diagram':'図解','illustration':'イラスト','icon':'アイコン','chart':'グラフ','background':'背景','part':'説明パーツ'}
    lines=['DeckArt — 全素材のIDと題名 / All asset IDs and titles',
           '用途や種類を横断して選べます。候補の画像と詳細は catalog.json の preview_path / metadata_path から取得できます。','']
    for kind,title in kinds.items():
        items=sorted((a for a in records if a['kind']==kind),key=lambda a:a['id'])
        lines.append(f'[{kind} / {title}]')
        lines.extend(f'{a["id"]} | {a["title"]}' for a in items)
        lines.append('')
    return '\n'.join(lines)


def build():
    config=project();items=artwork();records=[];gallery=[]
    for a in items:
        meta=metadata(a)
        content=asset_path(a['source'],'media').read_bytes() if meta['format']=='png' else svg_document(a).encode('utf-8')
        meta['sha256']=hashlib.sha256(content).hexdigest();meta['size_bytes']=len(content)
        file=ROOT/meta['path'];file.parent.mkdir(parents=True,exist_ok=True)
        if meta['format']=='svg':file.write_bytes(content)
        if meta['preview_has_example_labels']:
            from library import add_labels
            preview,_=add_labels(content.decode('utf-8'),meta,{},include_examples=True)
            preview_file=ROOT/meta['preview_path'];preview_file.parent.mkdir(parents=True,exist_ok=True)
            preview_file.write_bytes(preview.encode('utf-8'))
        write_json(ROOT/meta['metadata_path'],meta)
        records.append(meta);gallery.append(dict(meta,**({'download':base64.b64encode(content).decode()} if meta['format']=='svg' else {})))
    # Both directories contain generated outputs only; remove superseded registered forms.
    expected={a['path'] for a in records}|{a['metadata_path'] for a in records}|{a['preview_path'] for a in records}
    for directory,suffix in [('assets','.svg'),('metadata','.json'),('previews','.svg')]:
        for file in (ROOT/directory).rglob('*'+suffix):
            if file.relative_to(ROOT).as_posix() not in expected:file.unlink()
        for directory_path in sorted((p for p in (ROOT/directory).rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
            if not any(directory_path.iterdir()):directory_path.rmdir()
    raw_base=f'https://raw.githubusercontent.com/{config["repository"]}/v{config["version"]}/'
    index=[]
    for a in records:
        row={k:a[k] for k in ('id','title','kind','category','format','mime_type','transparent','width','height','canvas','render','path','preview_path','preview_has_example_labels','metadata_path','sha256','size_bytes','keywords')}
        row.update(use_case=a['guidance']['use_case'],message=a['guidance']['message'],sample_data=bool(a.get('data',{}).get('is_sample')))
        if a.get('composition'):row['composition']=a['composition']
        index.append(row)
    catalog={**config,'raw_base':raw_base,'themes_path':'themes.json','asset_count':len(records),'assets':index}
    write_json(ROOT/'catalog.json',catalog)
    (ROOT/'catalog.txt').write_bytes(browse_text(records).encode('utf-8'))
    (ROOT/'catalog.ndjson').write_bytes(''.join(json.dumps(a,ensure_ascii=False)+'\n' for a in records).encode('utf-8'))
    themes=theme_contract();write_json(ROOT/'themes.json',themes)
    settings=dict(themes=themes,project=config,search=json.loads((ROOT/'search.json').read_text(encoding='utf-8')),assetLicense=(ROOT/'LICENSE-ASSETS').read_text(encoding='utf-8'))
    page=(ROOT/'web/page.html').read_text(encoding='utf-8').replace('@@LIBRARY@@',packed_json(gallery)).replace('@@SETTINGS@@',packed_json(settings))
    (ROOT/'index.html').write_bytes(page.encode('utf-8'))
    # The overview shows actual forms in the default theme, not recolor variants.
    chosen=[]
    for kind in ('diagram','icon','chart','part'):
        chosen.append(next(a for a in items if a['kind']==kind))
    preview=[]
    for i,a in enumerate(chosen):
        x=(i%2)*480;y=(i//2)*325;scale=min(440/a['width'],260/a['height']);tx=x+(480-a['width']*scale)/2;ty=y+(270-a['height']*scale)/2
        body=a['body']
        if a['kind'] in ('background','part'):
            from library import add_labels
            labeled,_=add_labels(svg_document(a),metadata(a),{},include_examples=True)
            body=''.join(ET.tostring(child,encoding='unicode') for child in ET.fromstring(labeled) if child.tag.split('}')[-1] not in ('title','desc'))
        preview.append(f'<g transform="translate({tx} {ty}) scale({scale})">{body}</g><text x="{x+240}" y="{y+298}" text-anchor="middle" fill="#153A6B" font-family="sans-serif" font-size="16">{html.escape(a["title"])}</text>')
    preview_svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 650" width="960" height="650"><rect width="960" height="650" fill="white"/>'+''.join(preview)+'</svg>'
    (ROOT/'preview.svg').write_bytes((ET.tostring(canonical_geometry(ET.fromstring(preview_svg)),encoding='unicode')+'\n').encode('utf-8'))
    package_files=[ROOT/p for a in records for p in (a['path'],a['metadata_path'])]
    package_files += [p for folder in ('scripts','web','examples','tests','sources','previews') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    package_files += [ROOT/p for p in ('README.md','llms.txt','project.json','request.schema.json','catalog.txt','catalog.json','catalog.ndjson','search.json','themes.json','LICENSE-ASSETS','LICENSE','preview.svg','index.html')]
    with zipfile.ZipFile(ROOT/'deckart.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(set(package_files),key=lambda p:p.relative_to(ROOT).as_posix()):zip_entry(archive,file.relative_to(ROOT).as_posix(),file.read_bytes())
    print(f'Built {len(records)} SVG/PNG assets, per-asset metadata, compact AI index and offline package.')


if __name__=='__main__':build()
