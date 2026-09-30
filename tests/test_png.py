"""Synthetic pixel fixtures exercise transport and validation, never production artwork."""
from contextlib import ExitStack
from copy import deepcopy
import hashlib
from io import BytesIO
import json
from pathlib import Path
import struct
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zlib

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import library
import registry


def chunk(kind,payload):
    return struct.pack('>I',len(payload))+kind+payload+struct.pack('>I',zlib.crc32(kind+payload)&0xffffffff)


def png(pixels,width=3,height=2,channels=4,filter_type=0,extra=b''):
    """Tiny explicit pixels are test data only."""
    stride=width*channels;encoded=[];previous=bytes(stride)
    for y in range(height):
        row=bytes(pixels[y*stride:(y+1)*stride]);filtered=bytearray(row)
        for x,value in enumerate(row):
            left=row[x-channels] if x>=channels else 0;up=previous[x];upper_left=previous[x-channels] if x>=channels else 0
            predictor=0
            if filter_type==1:predictor=left
            elif filter_type==2:predictor=up
            elif filter_type==3:predictor=(left+up)//2
            elif filter_type==4:
                p=left+up-upper_left;pa=abs(p-left);pb=abs(p-up);pc=abs(p-upper_left)
                predictor=left if pa<=pb and pa<=pc else up if pb<=pc else upper_left
            filtered[x]=(value-predictor)&255
        encoded.append(bytes([filter_type])+filtered);previous=row
    header=struct.pack('>IIBBBBB',width,height,8,6 if channels==4 else 2,0,0,0)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',header)+extra+chunk(b'IDAT',zlib.compress(b''.join(encoded)))+chunk(b'IEND',b'')


def sample_png():
    return png([0,0,0,0,21,58,107,255,255,255,255,128,30,40,50,254,60,70,80,0,90,100,110,255])


class PNGInspectionTests(unittest.TestCase):
    def test_all_png_filter_types_preserve_real_alpha(self):
        pixels=[0,0,0,0,21,58,107,255,255,255,255,128,30,40,50,254,60,70,80,0,90,100,110,255]
        for method in range(5):
            with self.subTest(filter=method):
                self.assertEqual(registry.png_info(png(pixels,filter_type=method)),dict(width=3,height=2,transparent=True,alpha_min=0,alpha_max=255))

    def test_partial_alpha_is_not_classified_as_opaque(self):
        content=png([20,40,60,128]*6)
        info=registry.png_info(content)
        self.assertTrue(info['transparent']);self.assertEqual(info['alpha_min'],128)
        self.assertEqual(registry.png_info(png([20,40,60]*6,channels=3))['transparent'],False)
        with self.assertRaisesRegex(ValueError,'entirely transparent'):registry.png_info(png([0,0,0,0]*6))

    def test_metadata_crc_truncation_and_trailing_bytes_rejected(self):
        for kind in (b'tEXt',b'iTXt',b'eXIf',b'acTL'):
            with self.subTest(chunk=kind):
                with self.assertRaises(ValueError):registry.png_info(png([20,40,60,255]*6,extra=chunk(kind,b'not public image metadata')))
        original=sample_png();bad=bytearray(original);bad[-1]^=1
        for data in (bytes(bad),original[:-1],original+b'junk',b'not a PNG'):
            with self.assertRaises(ValueError):registry.png_info(data)

    def test_external_paths_and_symlinked_media_directory_rejected(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as external:
            root=Path(temp)
            with patch.object(registry,'ROOT',root):
                for value in ('../outside.png','/absolute.png','media/../outside.png','media\\x.png','sources/file.png'):
                    with self.assertRaises(ValueError):registry.asset_path(value,'media')
                try:(root/'media').symlink_to(external,target_is_directory=True)
                except OSError:self.skipTest('Directory symlink unavailable on this host')
                with self.assertRaises(ValueError):registry.asset_path('media/outside.png','media')

    def test_malformed_public_ancillary_chunks_rejected(self):
        for kind,payload in ((b'pHYs',b'x'),(b'sRGB',bytes([4])),(b'gAMA',bytes(4)),(b'cHRM',bytes(31)),(b'pHYs',bytes(8)+bytes([2]))):
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):registry.png_info(png([20,40,60,255]*6,extra=chunk(kind,payload)))


class PNGExportTests(unittest.TestCase):
    def setUp(self):
        self.stack=ExitStack();self.addCleanup(self.stack.close)
        self.root=Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.stack.enter_context(patch.object(registry,'ROOT',self.root));self.stack.enter_context(patch.object(library,'ROOT',self.root))
        self.content=sample_png()
        declaration=dict(key='illustration/explaining',id='説明を伝える',title='説明',kind='illustration',category='06-業務イラスト',width=3,height=2,format='png',transparent=True,labels=[],description='相手に説明する',keywords=['説明','案内','共有'],guidance=dict(use_case='会議で説明する',message='相手に伝える',reading=['人物が説明する','手が内容へ向く']),composition=dict(framing='waist-up',facing='right',people_count=1))
        self.declaration={**declaration,'name':declaration['id'],'source':'media/illustration/explaining.png','generation':{'method':'image-generation','prompt':'Synthetic transport test only.'}}
        del self.declaration['id']
        self.meta=registry.metadata(declaration);self.meta['sha256']=hashlib.sha256(self.content).hexdigest();self.meta['size_bytes']=len(self.content)
        row={**self.meta,'use_case':self.meta['guidance']['use_case'],'message':self.meta['guidance']['message']}
        self.write('catalog.json',dict(assets=[row]));self.write('project.json',dict(version='2.0.0',repository='example/deckart'))
        self.write(self.meta['metadata_path'],self.meta)
        source=self.root/self.meta['path'];source.parent.mkdir(parents=True);source.write_bytes(self.content)

    def write(self,path,value):
        file=self.root/path;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(json.dumps(value,ensure_ascii=False).encode('utf-8'))

    def test_authoring_keeps_prompt_once_and_requires_cutout_alpha(self):
        self.write('sources/test.json',[self.declaration])
        with patch.object(registry,'MODULES',()):
            item=registry.artwork()[0];meta=registry.metadata(item)
            self.assertEqual(meta['generation'],{'method':'image-generation','definition_path':'sources/test.json'})
            self.assertNotIn('Synthetic transport',json.dumps(meta))
            (self.root/self.meta['path']).write_bytes(png([20,40,60,128]*6))
            with self.assertRaisesRegex(ValueError,'real alpha transparency'):registry.artwork()
            opaque=deepcopy(self.declaration);opaque.update(key='background/test',source='media/background/test.png',kind='background')
            self.write('sources/test.json',[opaque]);image=self.root/opaque['source'];image.parent.mkdir();image.write_bytes(png([20,40,60,128]*6))
            with self.assertRaisesRegex(ValueError,'fully opaque'):registry.artwork()

    def test_search_format_alpha_capabilities_and_facing(self):
        self.assertEqual(library.search('説明',format='png',transparent=True)['total'],1)
        self.assertEqual(library.search('右向き',kind='illustration')['total'],1)
        self.assertEqual(library.search('',themeable=True)['total'],0)
        self.assertEqual(library.search('',format='svg')['total'],0)

    def test_png_export_copies_exact_bytes_and_generic_result(self):
        content,meta=library.render({'id':'illustration/explaining','format':'png'})
        self.assertEqual(content,self.content);self.assertEqual(meta['source']['path'],self.meta['path'])
        destination=self.root/'exports'/'explanation.png'
        result=library.export_files(content,meta,destination)
        self.assertEqual(destination.read_bytes(),self.content);self.assertEqual(result['file'],str(destination.resolve()))
        self.assertEqual(result['format'],'png');self.assertIsNone(result['theme']);self.assertNotIn('svg',result)
        saved=json.loads(destination.with_suffix('.json').read_text(encoding='utf-8'))
        self.assertEqual(saved['sha256'],hashlib.sha256(destination.read_bytes()).hexdigest())
        self.assertEqual(saved['source']['id'],'illustration/explaining')
        with self.assertRaises(ValueError):library.export_files(content,meta,destination)
        with self.assertRaises(ValueError):library.export_files(content,meta,self.root/'exports'/'wrong.svg')

    def test_png_accepts_disabled_options_without_changing_pixels(self):
        content,meta=library.render({'id':'illustration/explaining','monochrome':False,'include_example_labels':False,'labels':{}})
        self.assertEqual(content,self.content)
        self.assertEqual(meta['sha256'],hashlib.sha256(content).hexdigest())

    def test_png_rejects_actual_transforms_and_malformed_options(self):
        for option,value in [('accent','#005BAC'),('monochrome',True),('labels',{'label-1':'新しい文字'}),('include_example_labels',True),('data',{}),('format','svg'),('labels',[]),('labels',None),('data',[]),('monochrome',0),('include_example_labels','false')]:
            with self.subTest(option=option):
                with self.assertRaises(ValueError):library.render({'id':'illustration/explaining',option:value})

    def test_png_stdout_is_binary_only(self):
        output=BytesIO()
        with patch.object(sys,'argv',['library.py','export','illustration/explaining','--stdout']),patch.object(sys,'stdout',SimpleNamespace(buffer=output)):
            library.main()
        self.assertEqual(output.getvalue(),self.content)

    def test_modified_image_or_traversing_metadata_rejected(self):
        source=self.root/self.meta['path'];source.write_bytes(self.content+b'changed')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):library.load_asset('illustration/explaining')
        source.write_bytes(self.content);meta=deepcopy(self.meta);meta['path']='../outside.png';self.write(meta['metadata_path'],meta)
        with self.assertRaises(ValueError):library.load_asset('illustration/explaining')

    def test_sidecar_failure_restores_existing_png(self):
        content,meta=library.render({'id':'illustration/explaining'})
        destination=self.root/'exports'/'explanation.png';destination.parent.mkdir();destination.write_bytes(b'original user content')
        original_replace=library.os.replace
        def fail_sidecar(source,target):
            if Path(target).suffix=='.json':raise OSError('simulated write failure')
            return original_replace(source,target)
        with patch.object(library.os,'replace',side_effect=fail_sidecar):
            with self.assertRaises(OSError):library.export_files(content,meta,destination,force=True)
        self.assertEqual(destination.read_bytes(),b'original user content')
        self.assertFalse(destination.with_suffix('.json').exists())


if __name__=='__main__':unittest.main()
