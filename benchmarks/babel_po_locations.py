"""Compare PO output and measure location lookup costs."""
from __future__ import annotations
import __future__

import argparse
import ast
import gc
import hashlib
import json
import platform
import subprocess
import time
import tracemalloc
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from statistics import median
from urllib.request import urlopen

from babel_mo import real_catalogs
from benchmark_cpu import RotatingCores

from babel.messages import Catalog, pofile

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent / "babel"
BASE = "e2a17919f0eb988bfea2883b00793ca4d5d37c4f"
DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)
COUNTS = (1, 2, 5, 10, 20, 50, 100, 250, 500, 1000)
KINDS = ("shared label across files", "shared label within one file", "app labels across files",
         "app labels within modules", "filenames with spaces and Unicode")


def input_catalogs():
    catalogs, provenance = real_catalogs()
    url = ('https://raw.githubusercontent.com/odoo/odoo/'
           'e1ed4fe077ba98ce7ac6802a43bb68242081dee9/addons/account/i18n/account.pot')
    path = ROOT / 'babel_mo_fixtures' / 'odoo_account.pot'
    if not path.exists():
        with urlopen(url, timeout=30) as response:
            path.write_bytes(response.read())
    raw = path.read_bytes()
    catalogs.append(('Odoo account template', pofile.read_po(BytesIO(raw))))
    provenance.append({'label': 'Odoo account template', 'url': url,
                       'source_sha256': hashlib.sha256(raw).hexdigest()})
    return catalogs, provenance


def methods():
    assert Path(pofile.__file__).resolve() == REPO / "babel/messages/pofile.py"
    source = subprocess.check_output(["git", "show", f"{BASE}:babel/messages/pofile.py"],
                                     cwd=REPO, text=True, encoding="utf-8")
    tree = ast.parse(source)
    nodes = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    namespace = dict(vars(pofile))
    exec(compile(ast.Module(body=[nodes["generate_po"]], type_ignores=[]), "<base generate_po>", "exec",
                 flags=__future__.annotations.compiler_flag), namespace)
    generators = {"base": namespace["generate_po"], "pr": pofile.generate_po}
    writers = {}
    for label, generator in generators.items():
        writer_namespace = dict(vars(pofile))
        writer_namespace["generate_po"] = generator
        exec(compile(ast.Module(body=[nodes["write_po"]], type_ignores=[]), "<write_po>", "exec",
                     flags=__future__.annotations.compiler_flag), writer_namespace)
        writers[label] = writer_namespace["write_po"]
    return writers


def catalog_for(count, kind):
    catalog = Catalog(locale="de", creation_date=DATE, revision_date=DATE)
    messages = min(25, max(1, 5000 // max(count, 1))) if kind.startswith("app labels") else 1
    if count == 0:
        messages = 0
    for index in range(messages):
        locations = []
        for reference in range(count):
            if kind == "shared label within one file":
                filename = "app/views/accounts.py"
            elif kind == "app labels within modules":
                filename = f"app/module_{reference % 4}/views.py"
            elif kind == "filenames with spaces and Unicode":
                filename = f"app/account settings/Übersicht_{reference}.py"
            else:
                filename = f"app/views/view_{reference}.py"
            locations.append((filename, reference * 3 + index + 1))
        catalog.add(f"Save changes {index}", f"Änderungen speichern {index}", locations=locations)
    return catalog


def outcome(method, catalog, options, fail_at=0):
    calls = []

    class Output:
        def write(self, data):
            calls.append((type(data).__name__, bytes(data)))
            if fail_at and len(calls) == fail_at:
                raise OSError("output unavailable")

    try:
        method(Output(), catalog, **options)
    except Exception as error:
        return type(error).__name__, str(error), calls
    return None, None, calls


def verify(pair, real):
    cores = RotatingCores()
    compared, errors, differences = 0, 0, []

    def check(label, catalog, options, fail_at=0):
        nonlocal compared, errors
        before = outcome(pair["base"], catalog, options, fail_at)
        after = outcome(pair["pr"], catalog, options, fail_at)
        compared += 1
        errors += before[0] is not None
        if before != after:
            differences.append(label)

    try:
        for count in (0, 1, 2, 3, 5, 10, 20, 32, 50, 100):
            cores.rotate()
            for kind in KINDS:
                catalog = catalog_for(count, kind)
                original = [(message.id, message.locations[:]) for message in catalog]
                for lines in (False, True):
                    for no_location in (False, True):
                        for width in (0, 40, 76):
                            options = {"include_lineno": lines, "no_location": no_location, "width": width}
                            check([count, kind, options], catalog, options)
                assert original == [(message.id, message.locations[:]) for message in catalog]
        for label, catalog in real:
            cores.rotate()
            for lines in (False, True):
                for width in (0, 40, 76):
                    for fail_at in (0, 1, 3):
                        check([label, lines, width, fail_at], catalog,
                              {"include_lineno": lines, "width": width}, fail_at)
        for locations in ([('a.py', None), ('a.py', 0), ('a.py', -1), ('a.py', True)],
                          [('a.py', 'bad')], [(None, 3)], [(42, 3)],
                          [('dir\\view.py', 1), ('dir/view.py', 1)]):
            catalog = Catalog(creation_date=DATE, revision_date=DATE)
            catalog.add('Save', 'Speichern', locations=locations)
            for lines in (False, True):
                for no_location in (False, True):
                    check([str(locations), lines, no_location], catalog,
                          {"include_lineno": lines, "no_location": no_location})
    finally:
        cores.restore()
    result = {"comparisons": compared, "matching_error_cases": errors, "differences": differences}
    print("Output/error verification:", result, flush=True)
    assert not differences
    return result


def timing(method, catalog, options, number, expected):
    outputs = [BytesIO() for _ in range(number)]
    gc.collect()
    enabled = gc.isenabled()
    gc.disable()
    try:
        start = time.perf_counter_ns()
        for output in outputs:
            method(output, catalog, **options)
        elapsed = time.perf_counter_ns() - start
    finally:
        if enabled:
            gc.enable()
    assert all(output.getvalue() == expected for output in outputs)
    return elapsed / number


def peak(method, catalog, options, expected):
    output = BytesIO()
    gc.collect()
    tracemalloc.start()
    try:
        method(output, catalog, **options)
        _, high = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert output.getvalue() == expected
    return high


def ratio(before, after, speed=True):
    if before == after:
        return "same"
    if speed:
        return f"{before / after:.3f}× faster" if before > after else f"{after / before:.3f}× slower"
    return f"{after / before:.3f}× more" if after > before else f"{before / after:.3f}× less"


def save(report):
    destination = ROOT / "babel_po_locations_results"
    destination.with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    metadata, results = report['metadata'], report['results']
    lines = ['# PO-location benchmark', '',
             f"Python {metadata['python']}; base {BASE}; changed source SHA256 {metadata['changed_source_sha256']}.",
             f"Median of {metadata['repeats']} timing and {metadata['repeats']} separate memory runs per version.",
             'The complete write_po call is timed, including sorting, formatting, encoding and writes to a fresh BytesIO.',
             'The two writer functions have identical code; only their generate_po global differs (base or changed).',
             'Catalog construction, PO parsing and output/error checks are outside the timer.',
             'Memory is peak newly traced Python allocations during a write, not total process RAM.',
             'One process is restricted to two physical cores at a time. Pairs rotate, paired versions use the same cores, and order alternates.',
             '100 cases are generated project-like examples; two are empty controls, eight use unchanged public catalogs, and two disable location output.',
             'Generated examples are not collected production workloads. Small timing differences may be noise; slower results and extra memory are retained.',
             f"Completed: {len(results)}/{metadata['planned_cases']}; output/error comparisons: {report['verification']['comparisons']}.", '',
             '<details>', f'<summary>Show all {len(results)} benchmark cases</summary>', '',
             '| Messages | Source references | Catalog | Line numbers | Locations enabled | Base time | PR time | Speed | Base peak | PR peak | Memory |',
             '|---:|---:|---|:---:|:---:|---:|---:|---|---:|---:|---|']
    for row in sorted(results, key=lambda r: (r['messages'], r['references'], r['label'], r['options']['include_lineno'])):
        base, changed = row['base'], row['pr']
        bt, pt = median(base['time_ns']), median(changed['time_ns'])
        bm, pm = median(base['peak_bytes']), median(changed['peak_bytes'])
        lines.append(f"| {row['messages']} | {row['references']} | {row['label']} | "
                     f"{'yes' if row['options']['include_lineno'] else 'no'} | {'no' if row['options'].get('no_location') else 'yes'} | "
                     f"{bt / 1e6:.4f} ms | {pt / 1e6:.4f} ms | {ratio(bt, pt)} | {bm / 1024:.2f} KiB | {pm / 1024:.2f} KiB | {ratio(bm, pm, False)} |")
    lines += ['', '</details>', '', 'Public catalog sources:', '']
    lines += [f"- [{fixture['label']}]({fixture['url']}) (unchanged contents; SHA256 in JSON)."
              for fixture in metadata['fixtures']]
    destination.with_suffix('.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats', type=int, default=8)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    assert args.repeats >= 5
    pair = methods()
    real, provenance = input_catalogs()
    verification = verify(pair, real)
    if args.verify_only:
        return
    cases = [('empty catalog', (0, KINDS[0]), {'include_lineno': lines}) for lines in (False, True)]
    cases += [(f'generated: {kind}', (count, kind), {'include_lineno': lines})
              for count in COUNTS for kind in KINDS for lines in (False, True)]
    cases += [(label, catalog, {'include_lineno': lines}) for label, catalog in real for lines in (False, True)]
    cases += [('locations disabled control', (1000, KINDS[0]), {'include_lineno': lines, 'no_location': True})
              for lines in (False, True)]
    cores = RotatingCores()
    report = {'metadata': {'python': platform.python_version(), 'platform': platform.platform(),
                           'base_commit': BASE, 'repeats': args.repeats, 'planned_cases': len(cases),
                           'changed_source_sha256': hashlib.sha256((REPO / 'babel/messages/pofile.py').read_bytes()).hexdigest(),
                           'benchmark_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           'fixtures': provenance, 'core_masks': [hex(mask) for mask in cores.pairs],
                           'started_utc': datetime.now(timezone.utc).isoformat()},
              'verification': verification, 'results': []}
    save(report)
    completed, total = 0, len(cases) * args.repeats * 4
    try:
        for index, (label, input_data, options) in enumerate(cases, 1):
            cores.rotate()
            catalog = catalog_for(*input_data) if isinstance(input_data, tuple) else input_data
            warmups, elapsed = [BytesIO(), BytesIO()], []
            for output, method in zip(warmups, pair.values()):
                start = time.perf_counter_ns()
                method(output, catalog, **options)
                elapsed.append(time.perf_counter_ns() - start)
            expected = warmups[0].getvalue()
            assert warmups[1].getvalue() == expected
            number = min(100, max(1, int(10_000_000 / max(elapsed))))
            row = {'label': label, 'messages': len(catalog), 'references': sum(len(m.locations) for m in catalog),
                   'options': options, 'number': number, 'output_bytes': len(expected),
                   'output_sha256': hashlib.sha256(expected).hexdigest(), 'masks': [],
                   'base': {'time_ns': [], 'peak_bytes': []}, 'pr': {'time_ns': [], 'peak_bytes': []}}
            for repeat in range(args.repeats):
                mask = cores.rotate()
                row['masks'].append(mask)
                order = ('base', 'pr') if repeat % 2 == 0 else ('pr', 'base')
                for mode in ('time_ns', 'peak_bytes'):
                    for name in order:
                        value = (timing(pair[name], catalog, options, number, expected) if mode == 'time_ns'
                                 else peak(pair[name], catalog, options, expected))
                        row[name][mode].append(value)
                        completed += 1
                        print(f"#{index}/{len(cases)} {label} | {name} {mode} {repeat + 1}/{args.repeats} | "
                              f"{completed / total:.1%} complete | cores {mask}", flush=True)
            report['results'].append(row)
            save(report)
    finally:
        cores.restore()
    report['metadata']['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save(report)
    print(f"Finished {len(cases)} cases; every measured output matched. {ROOT / 'babel_po_locations_results.md'}", flush=True)


if __name__ == '__main__':
    main()
