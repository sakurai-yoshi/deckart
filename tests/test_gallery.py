"""Browser-independent checks for card save state and downloadable ZIP contents."""
import base64
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from themes import apply_theme, resolve_theme


@unittest.skipUnless(shutil.which('node'),'Node is needed for gallery export checks')
class GalleryExportTests(unittest.TestCase):
    def run_js(self,body,data):
        # Evaluate the actual save functions with explicit rendering inputs. No
        # browser, Blob URL, network, or download interception is used here.
        prelude=r"""
const fs=require('fs'),vm=require('vm'),input=JSON.parse(fs.readFileSync(0,'utf8'));
const source=fs.readFileSync('web/catalog.js','utf8');
function declaration(name,next){return source.slice(source.indexOf('function '+name+'('),source.indexOf('function '+next+'(')).replace(/^function /,name==='packAsset'||name==='pngBytes'?'async function ':'function ').trim().replace(/\nasync\s*$/,'');}
const code=[source.match(/^function fileName\(.*$/m)[0],declaration('updateCardDownload','setHash'),source.match(/^function indexEntry\(.*$/m)[0],declaration('packAsset','pngBytes'),declaration('pngBytes','saveBlob')].join('\n');
const settings={project:input.project},localMedia=new Map();let checked=true,mode='blue',theme=input.theme;
const $=()=>({checked});
const artURL=(a,full,labels)=>'test:'+a.id+':'+labels;
const svgFor=(a,resolved)=>input.rendered[a.id][resolved.mode+':'+resolved.colors.accent].geometry;
const labeledSVG=(a,resolved)=>input.rendered[a.id][resolved.mode+':'+resolved.colors.accent].preview;
const window={};vm.runInNewContext(fs.readFileSync('web/zip.js','utf8'),{window,TextEncoder,Blob,Uint32Array,Uint8Array,DataView});
eval(code);
"""
        process=subprocess.run([shutil.which('node'),'-e',prelude+body],cwd=ROOT,input=json.dumps(data).encode(),capture_output=True)
        self.assertEqual(process.returncode,0,process.stderr.decode())
        return json.loads(process.stdout)

    @classmethod
    def setUpClass(cls):
        rows=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))['assets']
        cls.assets=[json.loads((ROOT/next(a for a in rows if a['kind']==kind)['metadata_path']).read_text(encoding='utf-8')) for kind in ('diagram','part','chart','icon','illustration')]
        cls.themes=[resolve_theme(),resolve_theme('#005BAC'),resolve_theme(monochrome=True)]
        cls.rendered={}
        for a in cls.assets:
            if a['format']=='svg':
                cls.rendered[a['id']]={}
                for t in cls.themes:
                    key=t['mode']+':'+t['colors']['accent']
                    cls.rendered[a['id']][key]=dict(geometry=apply_theme((ROOT/a['path']).read_text(encoding='utf-8'),t),preview=apply_theme((ROOT/a['preview_path']).read_text(encoding='utf-8'),t))
        cls.input=dict(project=json.loads((ROOT/'project.json').read_text(encoding='utf-8')),assets=cls.assets,themes=cls.themes,theme=cls.themes[0],rendered=cls.rendered)

    def test_card_save_follows_visible_labels_and_names_the_result(self):
        result=self.run_js(r"""
const results=[];
for(const a of input.assets){const link={dataset:{labels:'false'},setAttribute(name,value){this[name]=value;}};for(const value of [true,false,true]){checked=value;updateCardDownload(link,a);results.push({id:a.id,checked:value,labels:link.dataset.labels,text:link.textContent,aria:link['aria-label'],download:link.download});}}
process.stdout.write(JSON.stringify(results));
""",self.input)
        for result in result:
            a=next(a for a in self.assets if a['id']==result['id'])
            expected=bool(a['format']=='svg' and a['labels'] and result['checked'])
            self.assertEqual(result['labels'],str(expected).lower())
            self.assertIn(a['title'],result['aria'])
            if a['labels']:
                self.assertEqual(result['text'],'文字入りSVG保存' if expected else '図形のみSVG保存')
                self.assertEqual('--labels.svg' in result['download'],expected)
            else:self.assertEqual(result['text'],a['format'].upper()+'保存')

    def test_zip_contains_both_svg_forms_with_matching_hashes_and_source(self):
        data=dict(self.input,png={a['path']:base64.b64encode((ROOT/a['path']).read_bytes()).decode() for a in self.assets if a['format']=='png'})
        result=self.run_js(r"""
(async()=>{for(const [path,value] of Object.entries(input.png))localMedia.set(path,Uint8Array.from(Buffer.from(value,'base64')));const results=[];
for(let i=0;i<input.themes.length;i++){const resolved=input.themes[i],selectedMode=['blue','brand','mono'][i],prepared=await Promise.all(input.assets.map(a=>packAsset(a,resolved,selectedMode))),records=prepared.map(a=>a.record),files=prepared.flatMap(a=>a.files);files.push({name:'catalog.json',data:JSON.stringify({assets:records.map(indexEntry)})});const bytes=Buffer.from(await window.makeZip(files).arrayBuffer());results.push({theme:resolved,zip:bytes.toString('base64')});}
const png=input.assets.find(a=>a.format==='png');localMedia.set(png.path,new Uint8Array([0]));let rejected=false;try{await packAsset(png);}catch{rejected=true;}process.stdout.write(JSON.stringify({results,rejected}));})();
""",data)
        self.assertTrue(result['rejected'],'PNG hash mismatches must still be rejected')
        for output in result['results']:
            theme=output['theme'];key=theme['mode']+':'+theme['colors']['accent']
            with zipfile.ZipFile(io.BytesIO(base64.b64decode(output['zip']))) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(len(archive.namelist()),len(set(archive.namelist())))
                rows=json.loads(archive.read('catalog.json'))['assets']
                self.assertEqual(len(rows),len(self.assets))
                for row,a in zip(rows,self.assets):
                    meta=json.loads(archive.read(row['metadata_path']));payload=archive.read(row['path'])
                    self.assertEqual(meta['source']['path'],a['path']);self.assertEqual(meta['source']['sha256'],a['sha256'])
                    self.assertEqual(meta['sha256'],hashlib.sha256(payload).hexdigest())
                    self.assertEqual(meta['sha256'],row['sha256']);self.assertEqual(meta['size_bytes'],len(payload))
                    if a['labels']:
                        preview=archive.read(row['preview_path'])
                        self.assertNotEqual(row['path'],row['preview_path'])
                        self.assertTrue(meta['preview_has_example_labels']);self.assertTrue(row['preview_has_example_labels'])
                        self.assertEqual(meta['preview_sha256'],hashlib.sha256(preview).hexdigest());self.assertEqual(meta['preview_sha256'],row['preview_sha256'])
                        self.assertEqual(meta['source']['preview_sha256'],a['preview_sha256'])
                        self.assertEqual(preview.decode(),self.rendered[a['id']][key]['preview'])
                        self.assertEqual(payload.decode(),self.rendered[a['id']][key]['geometry'])
                        for label in meta['labels']:self.assertEqual(label['color'],theme['colors'][label['color_role']])
                    else:
                        self.assertEqual(row['preview_path'],row['path']);self.assertFalse(meta['preview_has_example_labels'])
                        self.assertNotIn('preview_sha256',meta);self.assertNotIn('preview_sha256',row)
                    if a['format']=='png':self.assertEqual(payload,(ROOT/a['path']).read_bytes())


if __name__=='__main__':unittest.main()
