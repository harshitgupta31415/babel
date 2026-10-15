"""Run the same Babel tests with either PO generator implementation."""
import argparse
import json
from pathlib import Path

import pytest
from babel_po_locations import BASE, methods
from benchmark_cpu import RotatingCores

from babel.messages import pofile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base', action='store_true')
parser.add_argument('--targeted', action='store_true')
args = parser.parse_args()
if args.base:
    pofile.generate_po = methods()['base'].__globals__['generate_po']
cores = RotatingCores()


class Rotation:
    count = 0

    def pytest_runtest_setup(self, item):
        if self.count % 200 == 0:
            cores.rotate()
        self.count += 1


suite = ['tests/messages', '--doctest-modules', 'babel/messages/pofile.py'] if args.targeted else []
version = 'base' if args.base else 'pr'
suffix = '_targeted' if args.targeted else ''
result_file = Path(__file__).with_name(f'babel_po_{version}{suffix}_tests.xml')
try:
    result = pytest.main(['-q', '--tb=short', f'--junitxml={result_file}', *suite], plugins=[Rotation()])
finally:
    cores.restore()
Path(__file__).with_name('babel_po_last_test_run.json').write_text(json.dumps({
    'base': args.base, 'targeted': args.targeted, 'base_commit': BASE, 'exit_code': int(result),
    'report': result_file.name,
}), encoding='utf-8')
raise SystemExit(result)
