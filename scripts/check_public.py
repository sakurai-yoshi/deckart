#!/usr/bin/env python3
"""Reject accidental private identity, local paths and common credentials before sharing.

This targeted publication check complements the hosting provider's secret scanner.
Findings report a file or object ID and category, never the matching value.
"""
import argparse
from io import BytesIO
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
EMAIL=re.compile(r'(?<![A-Za-z0-9_])[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~\[\]-]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,63}')
LOCAL_PATH=re.compile(r'(?:/(?:Users|home)/[^\s/<>]+/|[A-Za-z]:\\Users\\[^\s\\<>]+\\)')
CREDENTIAL=re.compile(r'(?:\bgh[pousr]_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{40,}|\bAKIA[A-Z0-9]{16}\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')


def public_email(value):
    return bool(re.fullmatch(r'[^\s@]+@users\.noreply\.github\.com|noreply@github\.com',value))


def content_findings(data):
    text=data.decode('utf-8',errors='replace')
    findings=[]
    if any(not public_email(m.group().strip("'")) and m.group().split('@')[1] not in ('example.com','example.org','example.invalid') for m in EMAIL.finditer(text)):
        findings.append('non-public email address')
    if LOCAL_PATH.search(text):findings.append('personal filesystem path')
    if CREDENTIAL.search(text):findings.append('credential pattern')
    return findings


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def file_findings(name,data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        # Pixel compression can coincidentally contain address-like bytes. Accept only
        # our bounded PNG format with numeric color/density chunks and no text/EXIF.
        from registry import png_info
        try:png_info(data)
        except ValueError:return [f'{name}: invalid PNG or unsupported embedded metadata']
        return []
    issues=[] if name.endswith('.zip') else [f'{name}: {kind}' for kind in content_findings(data)]
    if name.endswith('.zip'):
        with zipfile.ZipFile(BytesIO(data)) as archive:
            for member in archive.infolist():
                if not member.is_dir():
                    issues.extend(file_findings(f'{name}:{member.filename}',archive.read(member)))
    return issues


def inspect_history():
    issues=[]
    for sha in git('log','--all','--format=%H').decode().splitlines():
        author_name,author,committer_name,committer,message=git('show','-s','--format=%an%x00%ae%x00%cn%x00%ce%x00%B',sha).decode().split('\0',4)
        if not public_email(author) or not public_email(committer):issues.append(f'{sha}: non-public commit identity')
        if any(content_findings(name.encode()) for name in (author_name,committer_name)):issues.append(f'{sha}: private commit identity name content')
        if content_findings(message.encode()):issues.append(f'{sha}: private commit message content')
    for ref in git('for-each-ref','--format=%(refname)','refs/tags').decode().splitlines():
        name,email,message=git('for-each-ref','--format=%(taggername)%00%(taggeremail:trim)%00%(contents)',ref).decode().split('\0',2)
        if email and not public_email(email):issues.append(f'{ref}: non-public tag identity')
        if content_findings(name.encode()):issues.append(f'{ref}: private tag identity name content')
        if content_findings(message.encode()):issues.append(f'{ref}: private tag message content')
    # A file removed from HEAD still becomes public when its commit is pushed.
    objects=[line.split(b' ',1)[0] for line in git('rev-list','--objects','--all').splitlines()]
    if objects:
        batch=['git','-C',str(ROOT),'cat-file']
        info=subprocess.check_output([*batch,'--batch-check=%(objectname) %(objecttype)'],input=b'\n'.join(objects)+b'\n')
        blobs=[line.split()[0] for line in info.splitlines() if line.endswith(b' blob')]
        if blobs:
            contents=subprocess.check_output([*batch,'--batch'],input=b'\n'.join(blobs)+b'\n');offset=0
            for sha in blobs:
                end=contents.index(b'\n',offset);header=contents[offset:end].split();size=int(header[2])
                assert header[:2]==[sha,b'blob']
                data=contents[end+1:end+1+size];offset=end+size+2
                name=sha.decode()+('.zip' if zipfile.is_zipfile(BytesIO(data)) else '')
                issues.extend(file_findings(name,data))
    return issues


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged',action='store_true',help='Inspect staged file contents instead of working files')
    parser.add_argument('--identity',action='store_true',help='Inspect the effective next commit identities')
    parser.add_argument('--history',action='store_true',help='Inspect all reachable file versions, identities and messages on all refs')
    args=parser.parse_args();issues=[]
    paths=git('ls-files','-z').decode().split('\0')
    for name in filter(None,paths):
        file=ROOT/name
        if not args.staged and not file.exists():continue
        data=git('show',':'+name) if args.staged else file.read_bytes()
        issues.extend(file_findings(name,data))
    if args.identity:
        for kind in ('GIT_AUTHOR_IDENT','GIT_COMMITTER_IDENT'):
            value=git('var',kind).decode();email=re.search(r'<([^<>]+)>',value)
            if not email or not public_email(email.group(1)):issues.append(f'{kind}: use a GitHub privacy address')
            if email and content_findings(value[:email.start()].encode()):issues.append(f'{kind}: private identity name content')
    if args.history:issues.extend(inspect_history())
    if issues:
        print('\n'.join(issues),file=sys.stderr);return 1
    print('PASS: public file contents'+('; reachable history' if args.history else '')+('; Git identities' if args.history or args.identity else ''))
    return 0


if __name__=='__main__':raise SystemExit(main())
