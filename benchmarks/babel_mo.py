"""Compare MO output and benchmark writing translation catalogs."""

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

from benchmark_cpu import RotatingCores

from babel.messages import Catalog, mofile, pofile

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent / "babel"
BASE = "e2a17919f0eb988bfea2883b00793ca4d5d37c4f"
DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)
COUNTS = (1, 2, 10, 50, 100, 250, 500, 1000, 2500, 5000)
KINDS = ("UI labels", "help paragraphs", "context labels", "plural status", "mixed catalog")
FIXTURES = (
    ("Django German", "django/django", "dab0a5c47f159eb58472110dcbc10bd4a9b01adb",
     "django/conf/locale/de/LC_MESSAGES/django.po"),
    ("Wagtail German", "wagtail/wagtail", "e18fa1162b2fd352cefef345d9f558cc7fbdbcf3",
     "wagtail/admin/locale/de/LC_MESSAGES/django.po"),
    ("Wagtail French", "wagtail/wagtail", "e18fa1162b2fd352cefef345d9f558cc7fbdbcf3",
     "wagtail/admin/locale/fr/LC_MESSAGES/django.po"),
)


def methods():
    assert Path(mofile.__file__).resolve() == REPO / "babel/messages/mofile.py"
    source = subprocess.check_output(
        ["git", "show", f"{BASE}:babel/messages/mofile.py"],
        cwd=REPO, text=True, encoding="utf-8",
    )
    node = next(n for n in ast.parse(source).body
                if isinstance(n, ast.FunctionDef) and n.name == "write_mo")
    namespace = dict(vars(mofile))
    exec(compile(ast.Module(body=[node], type_ignores=[]), "<base write_mo>", "exec",
                 flags=__future__.annotations.compiler_flag), namespace)
    return {"base": namespace["write_mo"], "pr": mofile.write_mo}


def catalog_for(count, kind, charset="utf-8"):
    catalog = Catalog(locale="de", charset=charset, creation_date=DATE, revision_date=DATE)
    for index in range(count):
        selected = KINDS[index % 4] if kind == "mixed catalog" else kind
        context = None
        if selected == "UI labels":
            key, value = f"Save changes {index}", f"Änderungen speichern {index}"
        elif selected == "help paragraphs":
            key = ("Choose your account settings and save the changes. " * 6) + str(index)
            value = ("Wählen Sie Ihre Kontoeinstellungen und speichern Sie die Änderungen. " * 6) + str(index)
        elif selected == "context labels":
            key, value, context = "Open", "Öffnen", f"dialog_{index}"
        else:
            key = (f"One file {index}", f"Many files {index}")
            value = (f"Eine Datei {index}", f"Mehrere Dateien {index}")
        if kind == "mixed catalog" and index % 11 == 0:
            value = ("", "") if isinstance(key, tuple) else ""
        flags = ["fuzzy"] if index % 10 == 9 else []
        catalog.add(key, value, context=context, flags=flags)
    return catalog


def real_catalogs():
    directory = ROOT / "babel_mo_fixtures"
    directory.mkdir(exist_ok=True)
    catalogs, provenance = [], []
    for label, repository, ref, path in FIXTURES:
        url = f"https://raw.githubusercontent.com/{repository}/{ref}/{path}"
        target = directory / (label.replace(" ", "_").lower() + ".po")
        if not target.exists():
            with urlopen(url, timeout=30) as response:
                target.write_bytes(response.read())
        raw = target.read_bytes()
        catalog = pofile.read_po(BytesIO(raw), locale="fr" if "French" in label else "de")
        catalogs.append((label, catalog))
        provenance.append({"label": label, "url": url, "source_sha256": hashlib.sha256(raw).hexdigest()})
    return catalogs, provenance


def outcome(method, catalog, fuzzy, fail_write=False):
    calls = []

    class Output:
        def write(self, data):
            calls.append((type(data).__name__, bytes(data)))
            if fail_write:
                raise OSError("output unavailable")

    try:
        method(Output(), catalog, use_fuzzy=fuzzy)
    except Exception as error:
        return (type(error).__name__, str(error), calls)
    return (None, None, calls)


def verify(methods, real):
    cores = RotatingCores()
    cases, failures, differences = 0, 0, []
    try:
        for count in (0, 1, 2, 3, 10, 32, 64, 100, 128, 256):
            cores.rotate()
            for kind in KINDS:
                for charset in ("utf-8", "iso-8859-1", "ascii", "utf-16"):
                    catalog = catalog_for(count, kind, charset)
                    for fuzzy in (False, True):
                        base = outcome(methods["base"], catalog, fuzzy)
                        changed = outcome(methods["pr"], catalog, fuzzy)
                        cases += 1
                        failures += base[0] is not None
                        if changed != base:
                            differences.append([count, kind, charset, fuzzy])
        for label, catalog in real:
            cores.rotate()
            for fuzzy in (False, True):
                for fail_write in (False, True):
                    base = outcome(methods["base"], catalog, fuzzy, fail_write)
                    changed = outcome(methods["pr"], catalog, fuzzy, fail_write)
                    cases += 1
                    failures += base[0] is not None
                    if changed != base:
                        differences.append([label, fuzzy, fail_write])
        for charset in ("invalid-charset", "ascii"):
            catalog = catalog_for(2, "UI labels", charset)
            base = outcome(methods["base"], catalog, False)
            changed = outcome(methods["pr"], catalog, False)
            cases += 1
            failures += base[0] is not None
            if base != changed:
                differences.append([charset])
    finally:
        cores.restore()
    result = {"comparisons": cases, "matching_error_cases": failures, "differences": differences}
    print("Output/error verification:", result, flush=True)
    assert not differences
    return result


def timing(method, catalog, fuzzy, number, expected):
    outputs = [BytesIO() for _ in range(number)]
    gc.collect()
    enabled = gc.isenabled()
    gc.disable()
    try:
        start = time.perf_counter_ns()
        for output in outputs:
            method(output, catalog, use_fuzzy=fuzzy)
        elapsed = time.perf_counter_ns() - start
    finally:
        if enabled:
            gc.enable()
    assert all(output.getvalue() == expected for output in outputs)
    return elapsed / number


def peak(method, catalog, fuzzy, expected):
    output = BytesIO()
    gc.collect()
    tracemalloc.start()
    try:
        method(output, catalog, use_fuzzy=fuzzy)
        _, high = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert output.getvalue() == expected
    return high


def ratio(base, changed, speed=True):
    if base == changed:
        return "same"
    if speed:
        return f"{base / changed:.3f}× faster" if base > changed else f"{changed / base:.3f}× slower"
    return f"{changed / base:.3f}× more" if changed > base else f"{base / changed:.3f}× less"


def save(report):
    destination = ROOT / "babel_mo_results"
    destination.with_suffix(".json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    meta, results = report["metadata"], report["results"]
    lines = ["# MO-file writing benchmark", "",
             f"Python {meta['python']}; base {BASE}; changed-source SHA256 {meta['changed_source_sha256']}.",
             f"Median of {meta['repeats']} timing and {meta['repeats']} separate peak-memory runs per version.",
             "The complete write_mo() call is timed, including sorting and writing to a fresh BytesIO.",
             "Catalog construction, PO parsing, fixture downloads and output comparisons are excluded.",
             "Memory is peak newly traced Python allocations during one write, not total RAM.",
             "Paired versions use the same two physical cores; pairs rotate between repeats. Version order alternates.",
             "100 cases are generated examples, not collected production workloads; two are empty-catalog controls. Six use unchanged public project catalogs.",
             "Small differences may be measurement noise. Slower cases and extra memory are retained.",
             f"Completed: {len(results)}/{meta['planned_cases']} cases. Output/error comparisons: {report['verification']['comparisons']}.", "",
             "<details>", f"<summary>Show all {len(results)} measured cases</summary>", "",
             "| Messages | Catalog | Include fuzzy | Base time | PR time | Speed | Base peak | PR peak | Memory |",
             "|---:|---|:---:|---:|---:|---|---:|---:|---|"]
    for row in sorted(results, key=lambda r: (r["messages"], r["label"], r["fuzzy"])):
        base, changed = row["base"], row["pr"]
        bt, pt = median(base["time_ns"]), median(changed["time_ns"])
        bm, pm = median(base["peak_bytes"]), median(changed["peak_bytes"])
        lines.append(f"| {row['messages']} | {row['label']} | {'yes' if row['fuzzy'] else 'no'} | "
                     f"{bt / 1e6:.4f} ms | {pt / 1e6:.4f} ms | {ratio(bt, pt)} | "
                     f"{bm / 1024:.2f} KiB | {pm / 1024:.2f} KiB | {ratio(bm, pm, False)} |")
    lines += ["", "</details>", "", "Public fixture sources:", ""]
    lines += [f"- [{item['label']}]({item['url']}) (unchanged contents; source SHA256 in JSON)."
              for item in meta["fixtures"]]
    destination.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=8)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    assert args.repeats >= 5
    pair = methods()
    real, provenance = real_catalogs()
    verification = verify(pair, real)
    if args.verify_only:
        return
    cases = [(f"generated: {kind}", (count, kind), fuzzy)
             for count in COUNTS for kind in KINDS for fuzzy in (False, True)]
    cases = [("empty-catalog control", (0, "UI labels"), fuzzy) for fuzzy in (False, True)] + cases
    cases += [(label, catalog, fuzzy) for label, catalog in real for fuzzy in (False, True)]
    cores = RotatingCores()
    report = {"metadata": {"python": platform.python_version(), "platform": platform.platform(),
                           "base_commit": BASE, "repeats": args.repeats,
                           "benchmark_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           "changed_source_sha256": hashlib.sha256((REPO / 'babel/messages/mofile.py').read_bytes()).hexdigest(),
                           "planned_cases": len(cases), "fixtures": provenance,
                           "core_masks": [hex(mask) for mask in cores.pairs],
                           "started_utc": datetime.now(timezone.utc).isoformat()},
              "verification": verification, "results": []}
    completed, total = 0, len(cases) * args.repeats * 4
    save(report)
    try:
        for case_number, (label, input_data, fuzzy) in enumerate(cases, 1):
            cores.rotate()
            catalog = catalog_for(*input_data) if isinstance(input_data, tuple) else input_data
            warmups = [BytesIO(), BytesIO()]
            elapsed = []
            for output, method in zip(warmups, pair.values()):
                start = time.perf_counter_ns()
                method(output, catalog, use_fuzzy=fuzzy)
                elapsed.append(time.perf_counter_ns() - start)
            expected = warmups[0].getvalue()
            assert warmups[1].getvalue() == expected
            number = min(200, max(1, int(15_000_000 / max(elapsed))))
            row = {"label": label, "messages": len(catalog), "fuzzy": fuzzy,
                   "number": number, "output_bytes": len(expected),
                   "output_sha256": hashlib.sha256(expected).hexdigest(), "masks": [],
                   "base": {"time_ns": [], "peak_bytes": []}, "pr": {"time_ns": [], "peak_bytes": []}}
            for repeat in range(args.repeats):
                mask = cores.rotate()
                row["masks"].append(mask)
                order = ("base", "pr") if repeat % 2 == 0 else ("pr", "base")
                for mode in ("time_ns", "peak_bytes"):
                    for name in order:
                        value = (timing(pair[name], catalog, fuzzy, number, expected) if mode == "time_ns"
                                 else peak(pair[name], catalog, fuzzy, expected))
                        row[name][mode].append(value)
                        completed += 1
                        print(f"#{case_number}/{len(cases)} {label}, {len(catalog)} messages, fuzzy={fuzzy} | "
                              f"{name} {mode} {repeat + 1}/{args.repeats} | {completed / total:.1%} | cores {mask}", flush=True)
            report["results"].append(row)
            save(report)
    finally:
        cores.restore()
    report["metadata"]["finished_utc"] = datetime.now(timezone.utc).isoformat()
    save(report)
    print(f"Finished: {len(cases)} cases; all outputs match. {ROOT / 'babel_mo_results.md'}", flush=True)


if __name__ == "__main__":
    main()
