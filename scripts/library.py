#!/usr/bin/env python3
"""Search, inspect and export business SVG and PNG assets without third-party packages."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
from registry import ROOT, KEY_RE, metadata, project, svg_document, asset_path
from search import prepare, rank
from themes import SVG_NS, DEFAULT_ACCENT, apply_theme, resolve_theme


def read_json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'),parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f'Invalid numeric value: {value}')))
    except (OSError,json.JSONDecodeError) as error:raise ValueError(f'Cannot read JSON: {path}: {error}') from error


def load_asset(asset_id):
    if not KEY_RE.fullmatch(asset_id):raise ValueError('id must be an exact catalog id such as process/approval-return')
    index=read_json(ROOT/'catalog.json')
    row=next((a for a in index['assets'] if a['id']==asset_id),None)
    if row is None:raise ValueError(f'Unknown asset id: {asset_id}')
    expected=f'metadata/{asset_id}.json'
    if row['metadata_path']!=expected:raise ValueError('Metadata path does not match asset id')
    meta=read_json(asset_path(row['metadata_path'],'metadata'))
    format=meta.get('format')
    if format not in ('svg','png') or meta['id']!=asset_id or meta['path']!=f'{"media" if format=="png" else "assets"}/{asset_id}.{format}' or row['path']!=meta['path']:raise ValueError('Asset path or format does not match catalog')
    content=asset_path(meta['path'],'media' if format=='png' else 'assets').read_bytes()
    actual=hashlib.sha256(content).hexdigest()
    if row.get('format')!=format or row['sha256']!=actual or meta['sha256']!=actual:raise ValueError('Source asset hash mismatch; use a consistent repository revision')
    return meta,content.decode('utf-8') if format=='svg' else content


def search(query,kind=None,limit=20,format=None,transparent=None,themeable=None,offset=0,category=None):
    if not isinstance(query,str):raise ValueError('query must be text')
    if type(limit) is not int or limit<0:raise ValueError('limit must be a nonnegative integer; 0 returns all matches')
    if type(offset) is not int or offset<0:raise ValueError('offset must be a nonnegative integer')
    filters={key:value for key,value in dict(kind=kind,format=format,category=category).items() if value}
    filters.update({key:value for key,value in dict(transparent=transparent,themeable=themeable).items() if value is not None})
    config=read_json(Path(__file__).resolve().parents[1]/'search.json')
    ranked,terms=rank(prepare(read_json(ROOT/'catalog.json')['assets'],config),query,filters)
    assets=ranked[offset:offset+limit] if limit else ranked[offset:]
    next_offset=offset+len(assets) if offset+len(assets)<len(ranked) else None
    return dict(query=query,total=len(ranked),returned=len(assets),offset=offset,limit=limit,next_offset=next_offset,filters=filters,matched_terms=terms,assets=assets)


def text_units(text):
    # Conservative advance estimate. Explicit line breaks keep layout predictable.
    return sum(0 if unicodedata.combining(c) else 1 for c in text)


def validate_strings(value):
    if isinstance(value,str):
        if any(not (c=='\n' or 0x20<=ord(c)<=0xD7FF or 0xE000<=ord(c)<=0xFFFD or 0x10000<=ord(c)<=0x10FFFF) for c in value):
            raise ValueError('Text contains a control character or invalid XML character')
    elif isinstance(value,dict):
        for key,item in value.items():validate_strings(key);validate_strings(item)
    elif isinstance(value,list):
        for item in value:validate_strings(item)


def add_labels(svg,meta,overrides,include_examples=False):
    if not isinstance(overrides,dict):raise ValueError('labels must be an object keyed by label id')
    known={l['id'] for l in meta['labels']}
    if set(overrides)-known:raise ValueError('Unknown label ids: '+', '.join(sorted(set(overrides)-known)))
    root=ET.fromstring(svg);group=ET.SubElement(root,f'{{{SVG_NS}}}g',{'data-labels':'true'})
    actual=[]
    for label in meta['labels']:
        if label['id'] not in overrides and not include_examples:continue
        value=overrides.get(label['id'],label['text'])
        if not isinstance(value,str) or not value.strip():raise ValueError(f'{label["id"]}: text must be a nonempty string')
        if any(ord(c)<32 and c!='\n' for c in value):raise ValueError(f'{label["id"]}: control characters are not allowed')
        lines=value.split('\n');size=label['font_size']
        if len(lines)>label['max_lines']:raise ValueError(f'{label["id"]}: at most {label["max_lines"]} lines')
        if any(text_units(line)*size*1.06>label['width'] for line in lines):
            raise ValueError(f'{label["id"]}: shorten text to about {label["max_fullwidth_chars"]} fullwidth characters per line')
        x=label['x'] if label['align']=='left' else label['x']+label['width']/2
        text=ET.SubElement(group,f'{{{SVG_NS}}}text',{'font-family':'Noto Sans CJK JP, Yu Gothic, Hiragino Kaku Gothic ProN, Meiryo, sans-serif','font-size':str(size),'font-weight':'500','text-anchor':'start' if label['align']=='left' else 'middle','fill':label['color'],'data-fill-role':label['color_role']})
        for i,line in enumerate(lines):
            y=label['y']+label['height']/2+(i-(len(lines)-1)/2)*size*1.4+size*.35
            ET.SubElement(text,f'{{{SVG_NS}}}tspan',{'x':str(x),'y':str(round(y,3))}).text=line
        label['text']=value;actual.append(label['id'])
    return ET.tostring(root,encoding='unicode')+'\n',actual


def render(request):
    if not isinstance(request,dict):raise ValueError('Request must be a JSON object')
    validate_strings(request)
    allowed={'id','format','accent','monochrome','labels','include_example_labels','data'}
    if set(request)-allowed:raise ValueError('Unknown request fields: '+', '.join(sorted(set(request)-allowed)))
    asset_id=request.get('id')
    if not isinstance(asset_id,str):raise ValueError('id is required')
    for name in ('monochrome','include_example_labels'):
        if name in request and not isinstance(request[name],bool):raise ValueError(name+' must be a boolean')
    for name in ('labels','data'):
        if name in request and not isinstance(request[name],dict):raise ValueError(name+' must be an object')
    if request.get('monochrome') and 'accent' in request:raise ValueError('Choose an accent or monochrome, not both')
    meta,svg=load_asset(asset_id);meta=deepcopy(meta)
    if 'format' in request and request['format']!=meta['format']:raise ValueError('Requested format is unavailable; use metadata.format')
    config=project()
    source={'id':asset_id,'version':config['version'],'raw_base':f'https://raw.githubusercontent.com/{config["repository"]}/v{config["version"]}/','path':meta['path'],'sha256':meta['sha256']}
    if meta['format']=='png':
        unsupported={name for name in ('accent','data') if name in request}
        unsupported.update(name for name in ('monochrome','labels','include_example_labels') if request.get(name))
        if unsupported:raise ValueError('PNG is a fixed image; unsupported options: '+', '.join(sorted(unsupported)))
        meta['source']=source
        return svg,meta
    if 'data' in request:
        if meta['kind']!='chart':raise ValueError('This asset does not accept data')
        from sets.metrics import render_chart
        generated=render_chart(meta['data']['chart_type'],request['data'])
        generated['key']=asset_id;generated['kind']='chart'
        svg=svg_document(generated);meta=metadata(generated)
        minimum=24 if meta['width']>=1000 else 20
        if any(label['font_size']<minimum for label in meta['labels']):
            raise ValueError('Data labels exceed this layout. Shorten category, series or unit names.')
    theme=resolve_theme(request.get('accent',DEFAULT_ACCENT),request.get('monochrome',False))
    rendered_labels=[]
    if 'labels' in request or request.get('include_example_labels'):
        svg,rendered_labels=add_labels(svg,meta,request.get('labels',{}),request.get('include_example_labels',False))
    svg=apply_theme(svg,theme)
    meta['theme']=theme;meta['source']=source;meta['rendered_labels']=rendered_labels
    for label in meta['labels']:label['color']=theme['colors'][label['color_role']]
    meta['sha256']=hashlib.sha256(svg.encode()).hexdigest();meta['size_bytes']=len(svg.encode('utf-8'))
    if rendered_labels:meta['text_rendering']='SVG text uses the listed system-font fallbacks; geometry-only exports are font-independent.'
    return svg,meta


def export_files(svg,meta,destination,force=False):
    destination=Path(destination)
    if destination.is_symlink():raise ValueError('Output must not be a symbolic link')
    destination=destination.resolve()
    if destination.suffix.lower()!='.'+meta['format']:raise ValueError('Output must end in .'+meta['format'])
    sidecar=destination.with_suffix('.json')
    for target in (destination,sidecar.resolve()):
        if target.is_relative_to(ROOT.resolve()) and not target.is_relative_to(ROOT.resolve()/'exports'):
            raise ValueError('Choose an output under exports/ or outside the repository')
    if not force and (destination.exists() or sidecar.exists()):raise ValueError('Output already exists; choose another path or use --force')
    if any(p.exists() and (not p.is_file() or p.is_symlink()) for p in (destination,sidecar)):
        raise ValueError('Both output paths must be regular files or new paths')
    destination.parent.mkdir(parents=True,exist_ok=True)
    output_meta=dict(meta,path=destination.name,metadata_path=sidecar.name)
    original=destination.read_bytes() if destination.exists() else None
    with tempfile.TemporaryDirectory(prefix='.asset-export-',dir=destination.parent) as temporary:
        staged_svg=Path(temporary)/('asset.'+meta['format']);staged_json=Path(temporary)/'asset.json'
        staged_svg.write_bytes(svg.encode('utf-8') if isinstance(svg,str) else svg)
        staged_json.write_bytes((json.dumps(output_meta,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
        os.replace(staged_svg,destination)
        try:os.replace(staged_json,sidecar)
        except OSError:
            if original is None:destination.unlink()
            else:
                staged_svg.write_bytes(original);os.replace(staged_svg,destination)
            raise
    return {'file':str(destination),'format':meta['format'],'mime_type':meta['mime_type'],'metadata':str(sidecar),'sha256':meta['sha256'],'render':meta['render'],'theme':meta.get('theme'),'sample_data':bool(meta.get('data',{}).get('is_sample'))}


def emit_json(value,error=False):
    stream=sys.stderr if error else sys.stdout
    stream.buffer.write((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self,message):
        emit_json({'error':message,'code':'invalid_input'},error=True)
        raise SystemExit(2)


def main():
    parser=JsonArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    find=commands.add_parser('search');find.add_argument('query',nargs='?',default='');find.add_argument('--kind',choices=['diagram','illustration','icon','chart','background','part']);find.add_argument('--limit',type=int,default=20,help='Results per page; 0 returns all matches');find.add_argument('--offset',type=int,default=0);find.add_argument('--category');find.add_argument('--format',choices=['svg','png']);find.add_argument('--transparent',action='store_true',default=None);find.add_argument('--themeable',action='store_true',default=None)
    show=commands.add_parser('show');show.add_argument('id')
    export=commands.add_parser('export');export.add_argument('id',nargs='?');export.add_argument('--request',type=Path);export.add_argument('--output',type=Path);export.add_argument('--stdout',action='store_true');export.add_argument('--force',action='store_true')
    export.add_argument('--format',choices=['svg','png']);export.add_argument('--accent');export.add_argument('--monochrome',action='store_true');export.add_argument('--labels',type=Path);export.add_argument('--data',type=Path);export.add_argument('--example-labels',action='store_true')
    args=parser.parse_args()
    try:
        if args.command=='search':
            result=search(args.query,args.kind,args.limit,args.format,args.transparent,args.themeable,args.offset,args.category)
        elif args.command=='show':result=load_asset(args.id)[0]
        else:
            if bool(args.output)==bool(args.stdout):raise ValueError('Choose exactly one of --output and --stdout')
            if args.request:
                if any((args.id,args.format,args.accent,args.monochrome,args.labels,args.data,args.example_labels)):raise ValueError('Request JSON cannot be combined with inline rendering options')
                request=read_json(args.request)
            else:
                request={'id':args.id}
                for name in ('format','accent','monochrome'):
                    if getattr(args,name):request[name]=getattr(args,name)
                for name in ('labels','data'):
                    if getattr(args,name):request[name]=read_json(getattr(args,name))
                if args.example_labels:request['include_example_labels']=True
            svg,meta=render(request)
            if args.stdout:
                sys.stdout.buffer.write(svg.encode('utf-8') if isinstance(svg,str) else svg)
                for adjustment in meta.get('theme',{}).get('adjustments',[]):print(adjustment,file=sys.stderr)
                return
            result=export_files(svg,meta,args.output,args.force)
        emit_json(result)
    except (ValueError,OSError,KeyError,TypeError) as error:
        emit_json({'error':str(error),'code':'invalid_input'},error=True)
        raise SystemExit(2)


if __name__=='__main__':main()
