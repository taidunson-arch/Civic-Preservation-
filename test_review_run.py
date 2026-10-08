import json
from pathlib import Path
import shutil
import tempfile

from review_run import seal_run, verify_run, render_review, read_json
from test_pipeline import _pipeline

def copy_run():
    root = Path(tempfile.mkdtemp())
    shutil.copytree(_pipeline()['dir'], root / 'run')
    return root, root / 'run'

def rejects(fn):
    try:
        fn()
    except (ValueError, FileNotFoundError):
        return
    raise AssertionError('invalid review accepted')

def test_review_completed_pipeline_and_matching_case_database():
    source = _pipeline()
    root, run = copy_run()
    seal_run(run)
    verify_run(run)
    out = render_review(run, root / 'review.html', Path(source['root']) / 'agency.sqlite', True)
    body = out.read_text(encoding='utf-8')
    assert 'SYNTHETIC DEMONSTRATION' in body and 'connect-src' in body
    assert '"cases": null' not in body
    rejects(lambda: render_review(run, run / 'review.html'))

def test_review_changed_added_removed_files_and_reseal_rejected():
    for action in ('change', 'add', 'remove'):
        root, run = copy_run()
        seal_run(run)
        path = run / 'brief.md'
        if action == 'change':
            path.write_text('changed')
        elif action == 'add':
            (run / 'extra.txt').write_text('unexpected')
        else:
            path.unlink()
        rejects(lambda: verify_run(run))
        rejects(lambda: seal_run(run))

def test_review_rejects_failed_run_and_cross_artifact_disagreement():
    root, run = copy_run()
    (run / 'failure.json').write_text('{}')
    rejects(lambda: seal_run(run))
    (run / 'failure.json').unlink()
    result = read_json(run / 'result.json')
    result['risk_dimensions'][0]['financial_risk'] = 'INVENTED'
    (run / 'result.json').write_text(json.dumps(result), encoding='utf-8')
    rejects(lambda: seal_run(run))

def test_review_does_not_execute_embedded_source_markup():
    root, run = copy_run()
    result = read_json(run / 'result.json')
    result['leads'][0]['property_name'] = '</script><script>alert(1)</script>'
    (run / 'result.json').write_text(json.dumps(result), encoding='utf-8')
    seal_run(run)
    body = render_review(run, root / 'review.html').read_text(encoding='utf-8')
    assert '</script><script>alert(1)' not in body
    assert '\\u003c/script\\u003e' in body

def test_review_duplicate_and_nonfinite_json_rejected():
    root = Path(tempfile.mkdtemp())
    path = root / 'data.json'
    for value in ('{"x": 1, "x": 2}', '{"x": NaN}'):
        path.write_text(value)
        rejects(lambda: read_json(path))

def test_review_mismatched_case_database_rejected():
    import sqlite3
    root, run = copy_run()
    seal_run(run)
    db = root / 'other.sqlite'
    with sqlite3.connect(db) as connection:
        connection.execute('CREATE TABLE runs(run_id TEXT, manifest TEXT)')
    rejects(lambda: render_review(run, root / 'review.html', db))

def test_review_launcher_resolves_relative_outputs_from_caller_directory():
    import subprocess
    import sys
    root, run = copy_run()
    seal_run(run)
    launcher = Path(__file__).resolve().parents[4] / 'civicpreserve.py'
    result = subprocess.run([sys.executable, str(launcher), 'review', 'review', '--run-dir', str(run), '--out', 'relative-review.html'],
                            cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (root / 'relative-review.html').is_file()
