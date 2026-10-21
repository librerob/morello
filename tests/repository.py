"""Check source reproducibility, strict data parsing and local document links."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as XML
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, f'Duplicate JSON key: {key}'
        result[key] = value
    return result


def snapshot(root):
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob('*') if path.is_file() and '__pycache__' not in path.parts}


for path in ROOT.rglob('*.json'):
    json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=strict_object)
for path in (ROOT / 'assets').glob('*.svg'):
    XML.parse(path)
for path in ROOT.rglob('*.md'):
    content = path.read_text(encoding='utf-8')
    links = re.findall(r'\]\(([^)]+)\)', content) + re.findall(r'(?:src|srcset)="([^"]+)"', content)
    for link in links:
        if re.match(r'^[a-z]+:', link) or link.startswith('#'):
            continue
        destination = (path.parent / unquote(link.split('#', 1)[0].strip('<>'))).resolve()
        assert destination.is_relative_to(ROOT), f'Link escapes repository: {path}: {link}'
        assert destination.exists(), f'Broken local link: {path}: {link}'

with tempfile.TemporaryDirectory(prefix='morello-repro-') as directory:
    copy = Path(directory) / 'morello'
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('__pycache__', 'test-results', '.git'))
    before = snapshot(copy)
    for _ in range(2):
        for name in ('sync_ports.py', 'sync_extras.py', 'sync_vim.py', 'sync_apps.py', 'verify.py', 'verify_extras.py'):
            subprocess.run([sys.executable, str(copy / 'scripts' / name)], cwd=directory,
                           env=dict(os.environ, PYTHONUTF8='1'), capture_output=True, text=True, check=True)
        after = snapshot(copy)
        changed = sorted(key for key in before.keys() | after.keys() if before.get(key) != after.get(key))
        assert not changed, f'Regeneration changed committed files: {changed}'
print('Strict JSON, SVG, local document links, arbitrary working directory and repeat generation passed')
