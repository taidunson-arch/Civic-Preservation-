#!/usr/bin/env python3
"""Build an agency-only source ZIP. Requires completed TEST-RESULTS.txt in root."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
BASE = 'fb3eb3c80a95b076980f1ddc8697e1b965eac7be'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = Path(args.out).resolve()
    files = [ROOT / name for name in ('README.md', 'RELEASE-ASSESSMENT.md', 'requirements-tested.txt', 'civicpreserve.py', 'build_distribution.py', 'TEST-RESULTS.txt', 'Oregon_Affordable_Housing_Inventory_20261002.csv')]
    files += [p for p in (ROOT / 'skills/preservation-loan-book').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    entries = {}
    for path in sorted(files):
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            raise ValueError('distribution may not include linked/external files')
        entries[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    manifest = {'product': 'CivicPreserve', 'release': '0.1.0-pilot', 'base_commit': BASE,
                'scope': 'Agency-only source distribution; no production certification or license grant',
                'files': {name: hashlib.sha256(body).hexdigest() for name, body in entries.items()}}
    entries['RELEASE-FILES.json'] = json.dumps(manifest, indent=2, sort_keys=True).encode()
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, body in sorted(entries.items()):
            info = zipfile.ZipInfo('CivicPreserve/' + name, date_time=(2026, 10, 6, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, body)
    print(out)
    print('SHA256 ' + hashlib.sha256(out.read_bytes()).hexdigest())

if __name__ == '__main__':
    main()
