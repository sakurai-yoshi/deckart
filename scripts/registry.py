"""Authoring registry and the public, per-asset metadata contract."""
import html
import math
from pathlib import Path
import json
import re
import struct
import zlib
from themes import SOURCE_ROLES, resolve_theme, annotate_roles, apply_theme

ROOT=Path(__file__).resolve().parents[1]
MODULES=('process','strategy','illustration_icons','pictograms','business_icons','frameworks','metrics','parts','operations','planning','technology')
KEY_RE=re.compile(r'[a-z][a-z0-9-]*/[a-z][a-z0-9-]*\Z')



def asset_path(value,folder):
    """Reject paths that escape the public package, including symlink targets."""
    if not isinstance(value,str) or not value or '\\' in value:raise ValueError('Expected a relative POSIX asset path')
    path=Path(value)
    if path.is_absolute() or '..' in path.parts or not value.startswith(folder+'/'):raise ValueError('Invalid asset path')
    resolved=(ROOT/path).resolve()
    if not resolved.is_relative_to(ROOT.resolve()/folder):raise ValueError('Asset path escapes its directory')
    return resolved


def png_info(content):
    """Inspect RGB/RGBA PNGs and alpha without image dependencies or metadata leakage."""
    if len(content)>64000000:raise ValueError('PNG file exceeds size limit')
    if not content.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid PNG signature')
    offset=8;chunks=[];compressed=[];seen_end=False
    allowed={b'IHDR',b'IDAT',b'IEND',b'sRGB',b'gAMA',b'cHRM',b'pHYs'}
    while offset<len(content):
        if offset+12>len(content):raise ValueError('Truncated PNG chunk')
        size=struct.unpack('>I',content[offset:offset+4])[0];kind=content[offset+4:offset+8]
        payload=content[offset+8:offset+8+size];end=offset+12+size
        if end>len(content):raise ValueError('Truncated PNG data')
        if zlib.crc32(kind+payload)&0xffffffff!=struct.unpack('>I',content[end-4:end])[0]:raise ValueError('PNG CRC mismatch')
        if kind not in allowed:raise ValueError('PNG contains unsupported or private metadata chunk: '+kind.decode('ascii',errors='replace'))
        ancillary_lengths={b'sRGB':1,b'gAMA':4,b'cHRM':32,b'pHYs':9}
        if kind in ancillary_lengths and size!=ancillary_lengths[kind]:raise ValueError('Invalid PNG ancillary chunk length')
        if kind==b'sRGB' and payload[0]>3:raise ValueError('Invalid PNG rendering intent')
        if kind==b'pHYs' and payload[8]>1:raise ValueError('Invalid PNG pixel density unit')
        if kind==b'gAMA' and payload==b'\x00\x00\x00\x00':raise ValueError('Invalid PNG gamma')
        chunks.append(kind)
        if kind==b'IHDR':
            if len(chunks)!=1 or size!=13:raise ValueError('Invalid PNG header')
            width,height,depth,color,compression,filter_method,interlace=struct.unpack('>IIBBBBB',payload)
            if not 1<=width<=8192 or not 1<=height<=8192 or width*height>24000000:raise ValueError('PNG dimensions exceed limits')
            if depth!=8 or color not in (2,6) or compression or filter_method or interlace:raise ValueError('PNG must be non-interlaced 8-bit RGB or RGBA')
        elif kind==b'IDAT':compressed.append(payload)
        elif kind==b'IEND':
            if payload or end!=len(content):raise ValueError('Unexpected PNG trailing data')
            seen_end=True
        offset=end
    if not seen_end or not chunks or chunks[0]!=b'IHDR' or chunks.count(b'IHDR')!=1 or not compressed:raise ValueError('Incomplete PNG')
    channels=4 if color==6 else 3;stride=width*channels;expected=height*(stride+1)
    decoder=zlib.decompressobj()
    try:raw=decoder.decompress(b''.join(compressed),expected+1)
    except zlib.error as error:raise ValueError('Invalid PNG compressed data') from error
    if len(raw)!=expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:raise ValueError('Invalid PNG pixel data')
    alpha_min=255;alpha_max=0 if color==6 else 255;previous=bytearray(stride)
    for y in range(height):
        start=y*(stride+1);method=raw[start];row=bytearray(raw[start+1:start+1+stride])
        if method>4:raise ValueError('Invalid PNG filter')
        for x in range(3,stride,4) if color==6 else ():
            left=row[x-channels] if x>=channels else 0;up=previous[x];upper_left=previous[x-channels] if x>=channels else 0
            if method==1:row[x]=(row[x]+left)&255
            elif method==2:row[x]=(row[x]+up)&255
            elif method==3:row[x]=(row[x]+(left+up)//2)&255
            elif method==4:
                p=left+up-upper_left;pa=abs(p-left);pb=abs(p-up);pc=abs(p-upper_left)
                row[x]=(row[x]+(left if pa<=pb and pa<=pc else up if pb<=pc else upper_left))&255
        if color==6:
            alpha=row[3::4];alpha_min=min(alpha_min,min(alpha));alpha_max=max(alpha_max,max(alpha))
        previous=row
    if alpha_max==0:raise ValueError('PNG is entirely transparent')
    return dict(width=width,height=height,transparent=alpha_min<255,alpha_min=alpha_min,alpha_max=alpha_max)


def composition_text(composition):
    words={'waist-up':'上半身 腰上','full-body':'全身','object':'物 道具','left':'左向き','right':'右向き','front':'正面','inward':'向かい合う 対話','down':'下向き 手元を見る'}
    return ' '.join(str(value)+' '+words.get(str(value),'') for key,value in composition.items() if key in ('framing','facing'))


def artwork():
    from importlib import import_module
    items=[]
    for module in MODULES:items.extend(import_module('sets.'+module).make_assets())
    for declaration in sorted((ROOT/'sources').glob('*.json')):
        definitions=json.loads(declaration.read_text(encoding='utf-8'))
        if not isinstance(definitions,list):raise ValueError('Source declarations must contain a list')
        for definition in definitions:
            a=dict(definition);a['id']=a.pop('name');a.setdefault('description',a['guidance']['message']);a.setdefault('labels',[])
            if a['kind'] not in ('illustration','background'):raise ValueError('PNG declarations must be illustrations or backgrounds')
            if not a['key'].startswith(a['kind']+'/'):raise ValueError('PNG key must match its kind')
            if a['source']!=f'media/{a["key"]}.png':raise ValueError('PNG source path must match asset id')
            source=asset_path(a['source'],'media')
            info=png_info(source.read_bytes())
            if (a['width'],a['height'])!=(info['width'],info['height']):raise ValueError(f'PNG dimensions differ: {a["key"]}')
            if a['kind']=='illustration' and info['alpha_min']!=0:raise ValueError('Illustrations require real alpha transparency')
            if a['kind']=='background' and info['transparent']:raise ValueError('Background PNGs must be fully opaque')
            generation=a['generation']
            if generation['method']!='image-generation' or not isinstance(generation.get('prompt'),str) or not generation['prompt'].strip():raise ValueError('PNG declaration needs its generation prompt')
            a['generation']={'method':generation['method'],'definition_path':declaration.relative_to(ROOT).as_posix()}
            if a.get('labels'):raise ValueError('PNG labels belong in presentation text, not the raster export')
            if a.get('preview_path'):
                if a['preview_path']!=f'previews/{a["key"]}.png':raise ValueError('Preview path must match asset id')
                asset_path(a['preview_path'],'previews')
            a.update(format='png',mime_type='image/png',transparent=info['transparent'])
            a.setdefault('canvas',dict(width=a['width'],height=a['height']))
            items.append(a)
    for a in items:
        assert KEY_RE.fullmatch(a['key']),a.get('key')
        a.setdefault('kind','illustration' if a['category'].startswith('06-') else 'part' if a['category'].startswith('07-') else 'diagram')
    assert len({a['key'] for a in items})==len(items),'Duplicate stable ids'
    assert len({a['id'] for a in items})==len(items),'Duplicate descriptive names'
    return sorted(items,key=lambda a:(a['category'],a['key']))


def svg_document(a):
    guide=a['guidance'];description=f"{guide['use_case']} {guide['message']}"
    if a.get('data',{}).get('is_sample'):description+=' 数値は作例です。実績や調査結果ではありません。'
    content=f'<svg xmlns="http://www.w3.org/2000/svg" width="{a["width"]}" height="{a["height"]}" viewBox="0 0 {a["width"]} {a["height"]}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(a["title"])}</title><desc id="desc">{html.escape(description)}</desc>{a["body"]}</svg>'
    return apply_theme(annotate_roles(content),resolve_theme())


def metadata(a):
    format=a.get('format','svg')
    meta={k:v for k,v in a.items() if k not in ('body','id','key','source')}
    meta.update(schema_version=3,id=a['key'],name=a['id'],license='CC0-1.0',format=format,mime_type='image/png' if format=='png' else 'image/svg+xml',transparent=a.get('transparent'),canvas=a.get('canvas',dict(width=a['width'],height=a['height'])),path=f'{"media" if format=="png" else "assets"}/{a["key"]}.{format}',metadata_path=f'metadata/{a["key"]}.json')
    meta.setdefault('preview_path',meta['path'])
    labels=[]
    for i,source in enumerate(a['labels']):
        label=dict(source);lines=label['text'].split('\n')
        recommended=min(label.get('font_size',46 if a['kind']=='background' else 30 if a['kind']=='part' else 27),label['height']/(len(lines)*1.4),label['width']/max(map(len,lines))*.92)
        label.update(id=f'label-{i+1}',font_size=round(recommended,3),color_role=SOURCE_ROLES[label['color'].upper()],max_lines=max(1,math.floor(label['height']/(recommended*1.4))),max_fullwidth_chars=max(1,math.floor(label['width']/(recommended*1.06))))
        label['color']=resolve_theme()['colors'][label['color_role']]
        labels.append(label)
    meta['labels']=labels
    meta['preview_has_example_labels']=bool(format=='svg' and labels)
    if meta['preview_has_example_labels']:meta['preview_path']=f'previews/{a["key"]}.svg'
    guide=a['guidance']
    meta['search_text']='\n'.join([a['key'],a['id'],a['title'],guide['use_case'],guide['message'],*guide['reading'],' '.join(a['keywords'])])
    if a.get('composition'):meta['search_text']+='\n'+composition_text(a['composition'])
    meta['render']={'theme':format=='svg','labels':format=='svg' and bool(labels),'data':a['kind']=='chart'}
    if a['kind']=='chart':
        from sets.metrics import input_contract
        meta['data_input']=input_contract(a['data']['chart_type'])
    return meta


def project():
    return json.loads((ROOT/'project.json').read_text(encoding='utf-8'))
