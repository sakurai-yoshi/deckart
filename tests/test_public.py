"""Publication privacy checks must reject sensitive patterns without echoing them."""
from contextlib import redirect_stderr, redirect_stdout
from io import BytesIO, StringIO
from pathlib import Path
import os
import subprocess
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_public import content_findings, file_findings, public_email
import check_public


class PublicTests(unittest.TestCase):
    def test_only_privacy_identities_are_accepted(self):
        self.assertTrue(public_email('123+contributor@users.noreply.github.com'))
        self.assertTrue(public_email('noreply@github.com'))
        self.assertFalse(public_email('contributor@example.com'))
        self.assertFalse(public_email('user'+'@'+'users.noreply.github.com.evil.invalid'))

    def test_private_values_are_detected_without_disclosure(self):
        address='person'+'@'+'private.invalid'
        local='/'+'Users'+'/example/work'
        credential='gh'+'p_'+'x'*36
        for value in (address,local,credential):
            findings=file_findings('sample.txt',value.encode())
            self.assertTrue(findings)
            self.assertNotIn(value,'\n'.join(findings))
        self.assertFalse(content_findings(b'contact@example.com'))

    def test_zip_members_are_inspected(self):
        stream=BytesIO()
        with zipfile.ZipFile(stream,'w') as archive:
            archive.writestr('private.txt',('person'+'@'+'private.invalid').encode())
        self.assertEqual(file_findings('pack.zip',stream.getvalue()),['pack.zip:private.txt: non-public email address'])

    def test_png_pixels_are_distinct_from_embedded_private_metadata(self):
        address=('person'+'@'+'private.invalid').encode()
        pixels=(address+b'\x00\x00')[:len(address)//3*3]
        def chunk(kind,payload):
            return struct.pack('>I',len(payload))+kind+payload+struct.pack('>I',zlib.crc32(kind+payload)&0xffffffff)
        header=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',len(pixels)//3,1,8,2,0,0,0))
        image=header+chunk(b'IDAT',zlib.compress(b'\x00'+pixels,0))+chunk(b'IEND',b'')
        self.assertTrue(content_findings(image))
        self.assertEqual(file_findings('pixels.png',image),[])
        private=header+chunk(b'tEXt',address)+image[len(header):]
        self.assertTrue(file_findings('private.png',private))
        stream=BytesIO()
        with zipfile.ZipFile(stream,'w') as archive:archive.writestr('private.png',private)
        self.assertTrue(file_findings('pack.zip',stream.getvalue()))

    def test_commit_and_tag_privacy_checks_inspect_real_git_objects(self):
        with tempfile.TemporaryDirectory() as directory:
            repo=Path(directory)
            env={**os.environ,'GIT_AUTHOR_NAME':'Test contributor','GIT_COMMITTER_NAME':'Test contributor',
                 'GIT_AUTHOR_EMAIL':'123+contributor@users.noreply.github.com',
                 'GIT_COMMITTER_EMAIL':'123+contributor@users.noreply.github.com'}
            def run(*args):
                subprocess.run(['git','-c','commit.gpgsign=false','-c','tag.gpgsign=false',*args],cwd=repo,env=env,check=True,capture_output=True)
            run('init');run('commit','--allow-empty','-m','Public root')
            with patch.object(check_public,'ROOT',repo):
                self.assertEqual(check_public.inspect_history(),[])
                env['GIT_COMMITTER_EMAIL']='committer@example.invalid'
                run('commit','--allow-empty','-m','Identity probe')
                env['GIT_COMMITTER_EMAIL']='123+contributor@users.noreply.github.com'
                private='person'+'@'+'private.invalid'
                run('tag','-a','v0.0.0','-m',private)
                issues=check_public.inspect_history()
                self.assertTrue(any('non-public commit identity' in item for item in issues))
                self.assertTrue(any('private tag message content' in item for item in issues))
                self.assertNotIn(private,'\n'.join(issues))

    def test_removed_private_files_are_still_rejected_from_history(self):
        with tempfile.TemporaryDirectory() as directory:
            repo=Path(directory)
            env={**os.environ,'GIT_AUTHOR_NAME':'Test contributor','GIT_COMMITTER_NAME':'Test contributor',
                 'GIT_AUTHOR_EMAIL':'123+contributor@users.noreply.github.com',
                 'GIT_COMMITTER_EMAIL':'123+contributor@users.noreply.github.com'}
            def run(*args):
                subprocess.run(['git','-c','commit.gpgsign=false',*args],cwd=repo,env=env,check=True,capture_output=True)
            run('init');private='/'+'Users'+'/example/work'
            (repo/'note.txt').write_text(private,encoding='utf-8')
            run('add','note.txt');run('commit','-m','First version')
            run('rm','note.txt');run('commit','-m','Remove note')
            with patch.object(check_public,'ROOT',repo):
                issues=check_public.inspect_history()
                self.assertTrue(any('personal filesystem path' in item for item in issues))
                self.assertNotIn(private,'\n'.join(issues))

    def test_detached_pr_merge_identity_is_checked_with_its_parents(self):
        with tempfile.TemporaryDirectory() as directory:
            repo=Path(directory)
            env={**os.environ,'GIT_AUTHOR_NAME':'Test contributor','GIT_COMMITTER_NAME':'Test contributor',
                 'GIT_AUTHOR_EMAIL':'123+contributor@users.noreply.github.com',
                 'GIT_COMMITTER_EMAIL':'noreply@github.com'}
            def run(*args):
                return subprocess.check_output(['git','-c','commit.gpgsign=false',*args],cwd=repo,env=env,stderr=subprocess.DEVNULL).decode().strip()
            run('init','-b','main');run('commit','--allow-empty','-m','Public root')
            run('switch','-c','topic');run('commit','--allow-empty','-m','Public contribution')
            run('switch','--detach','main')
            private='merge-author'+'@'+'example.invalid'
            env['GIT_AUTHOR_EMAIL']=private
            run('merge','--no-ff','topic','-m','PR integration')
            merge=run('rev-parse','HEAD')
            with patch.object(check_public,'ROOT',repo):
                issues=check_public.inspect_history()
                self.assertIn(f'{merge}: non-public commit identity',issues)
                self.assertNotIn(private,'\n'.join(issues))
                env['GIT_AUTHOR_EMAIL']='123+contributor@users.noreply.github.com'
                run('commit','--amend','--reset-author','--no-edit')
                self.assertEqual(check_public.inspect_history(),[])

    def test_detached_head_only_checks_both_parents_and_merge_committer(self):
        with tempfile.TemporaryDirectory() as directory:
            repo=Path(directory)
            env={**os.environ,'GIT_AUTHOR_NAME':'Test contributor','GIT_COMMITTER_NAME':'Test contributor',
                 'GIT_AUTHOR_EMAIL':'123+contributor@users.noreply.github.com',
                 'GIT_COMMITTER_EMAIL':'noreply@github.com'}
            def run(*args,changes=None,input=None):
                return subprocess.check_output(['git','-c','commit.gpgsign=false',*args],cwd=repo,
                    env={**env,**(changes or {})},input=input,stderr=subprocess.DEVNULL).decode().strip()
            run('init','-b','main');tree=run('mktree',input=b'')
            base=run('commit-tree',tree,'-m','Public root')
            private='identity'+'@'+'private.invalid'
            left=run('commit-tree',tree,'-p',base,'-m','Left parent',changes={'GIT_AUTHOR_EMAIL':private})
            right=run('commit-tree',tree,'-p',base,'-m','Right parent',changes={'GIT_COMMITTER_EMAIL':private})
            merge=run('commit-tree',tree,'-p',left,'-p',right,'-m','PR integration',changes={'GIT_COMMITTER_EMAIL':private})
            run('checkout','--detach',merge)
            self.assertEqual(run('for-each-ref','--format=%(refname)'),'')
            with patch.object(check_public,'ROOT',repo):
                issues=check_public.inspect_history()
                self.assertCountEqual(issues,[f'{sha}: non-public commit identity' for sha in (left,right,merge)])
                self.assertNotIn(private,'\n'.join(issues))

    def test_commit_tagger_and_next_identity_names_are_inspected(self):
        with tempfile.TemporaryDirectory() as directory:
            repo=Path(directory)
            env={**os.environ,'GIT_AUTHOR_NAME':'Test contributor','GIT_COMMITTER_NAME':'Test contributor',
                 'GIT_AUTHOR_EMAIL':'123+contributor@users.noreply.github.com',
                 'GIT_COMMITTER_EMAIL':'123+contributor@users.noreply.github.com'}
            def run(*args,changes=None):
                return subprocess.check_output(['git','-c','commit.gpgsign=false','-c','tag.gpgsign=false',*args],cwd=repo,
                    env={**env,**(changes or {})},stderr=subprocess.DEVNULL).decode().strip()
            run('init','-b','main')
            private='name-field'+'@'+'private.invalid'
            run('commit','--allow-empty','-m','Author name probe',changes={'GIT_AUTHOR_NAME':private})
            author=run('rev-parse','HEAD')
            run('commit','--allow-empty','-m','Committer name probe',changes={'GIT_COMMITTER_NAME':private})
            committer=run('rev-parse','HEAD')
            run('tag','-a','v0.0.0','-m','Public tag message',changes={'GIT_COMMITTER_NAME':private})
            with patch.object(check_public,'ROOT',repo):
                issues=check_public.inspect_history()
                for sha in (author,committer):self.assertIn(f'{sha}: private commit identity name content',issues)
                self.assertIn('refs/tags/v0.0.0: private tag identity name content',issues)
                self.assertNotIn(private,'\n'.join(issues))
                output=StringIO();errors=StringIO()
                with patch.dict(os.environ,{**env,'GIT_AUTHOR_NAME':private,'GIT_COMMITTER_NAME':private}), \
                     patch.object(sys,'argv',['check_public.py','--identity']),redirect_stdout(output),redirect_stderr(errors):
                    self.assertEqual(check_public.main(),1)
                for kind in ('GIT_AUTHOR_IDENT','GIT_COMMITTER_IDENT'):
                    self.assertIn(f'{kind}: private identity name content',errors.getvalue())
                self.assertNotIn(private,output.getvalue()+errors.getvalue())


if __name__=='__main__':unittest.main()
