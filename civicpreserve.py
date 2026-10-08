#!/usr/bin/env python3
"""CivicPreserve local distribution entry point. Python 3.12 recommended."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / 'skills' / 'preservation-loan-book'
SCRIPTS = SKILL / 'scripts'

def run(script, *args):
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    if script == 'tests/run_tests.py' and (ROOT / 'Oregon_Affordable_Housing_Inventory_20261002.csv').is_file():
        env.setdefault('OHCS_CSV', str(ROOT / 'Oregon_Affordable_Housing_Inventory_20261002.csv'))
    subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], check=True, env=env)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    demo = commands.add_parser('demo', help='Run synthetic fixtures and export an offline review')
    demo.add_argument('--out', required=True, help='New directory; never overwrites an existing demo')
    commands.add_parser('doctor', help='Check runtime dependencies')
    tests = commands.add_parser('test', help='Run the bundled regression suite')
    commands.add_parser('pipeline', help='Forward arguments to the pipeline')
    commands.add_parser('review', help='Forward seal/verify/review arguments to review_run.py')
    commands.add_parser('cases', help='Forward arguments to the local case manager')
    commands.add_parser('acceptance', help='Forward arguments to agency acceptance validator')
    args, rest = parser.parse_known_args()
    if args.command in ('doctor', 'demo', 'test') and rest:
        parser.error('unrecognized arguments: ' + ' '.join(rest))
    try:
        if args.command == 'doctor':
            from importlib.metadata import version
            if sys.version_info < (3, 10):
                raise ValueError('Python 3.10+ required; distribution tested on 3.12')
            for package in ('pandas', 'openpyxl', 'PyYAML'):
                print(package + ' ' + version(package))
            print('Runtime available. This check does not establish agency acceptance.')
        elif args.command == 'demo':
            out = Path(args.out).resolve()
            out.mkdir(parents=True, exist_ok=False)
            fx = SCRIPTS / 'tests' / 'fixtures'
            cfg = {'market_id': 'SYNTHETIC-DEMO', 'pack': str(SKILL / 'references/sources/oregon-portland'),
                   'agency_profile': 'hfa', 'universe': 'all', 'geography_mode': 'metro_core',
                   'counties': ['41051', '41067', '41005'], 'as_of_date': '2026-10-04',
                   'servicing_extract': str(fx / 'agency_servicing_sample.csv'), 'book_coverage': 'full',
                   'book_crosswalk': str(fx / 'book_crosswalk_sample.csv'),
                   'local_datasets': [str(fx / name) for name in ('ohcs_sample.csv', 'reac_scores_sample.csv', 'ohcs_forecast_sample.csv')],
                   'pii_scope': 'organization', 'board_packet': True, 'out_dir': str(out / 'runs'),
                   'operations_db': str(out / 'agency.sqlite')}
            config = out / 'run_config.json'
            config.write_text(json.dumps(cfg, indent=2), encoding='utf-8')
            run('run_agency_pipeline.py', '--config', config)
            latest = json.loads((out / 'runs/2026-10-04/latest.json').read_text())
            run('review_run.py', 'seal', '--run-dir', latest['run_dir'])
            run('review_run.py', 'review', '--run-dir', latest['run_dir'], '--out', out / 'review.html', '--db', out / 'agency.sqlite', '--demo')
            print('Synthetic demo ready: ' + str(out / 'review.html'))
        elif args.command == 'test':
            run('tests/run_tests.py')
        else:
            run({'pipeline': 'run_agency_pipeline.py', 'review': 'review_run.py', 'cases': 'manage_cases.py', 'acceptance': 'validate_book.py'}[args.command], *rest)
    except (OSError, ValueError, subprocess.CalledProcessError, ImportError) as exc:
        parser.exit(2, f'Command failed: {exc}\n')

if __name__ == '__main__':
    main()
