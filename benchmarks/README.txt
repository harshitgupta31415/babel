MO-file writing benchmark
=========================

This branch holds the runner and results separately from the proposed code
change, so the upstream PR only changes mofile.py and its tests.

Base commit: e2a17919f0eb988bfea2883b00793ca4d5d37c4f
Changed commit: 4cb2f4102ca18b7c48029b3d8b6ca55f8dc56fbb
Recorded run: Python 3.15.0 on Windows 11.

Files:
- babel_mo.py: the exact runner used for the recorded measurements.
- benchmark_cpu.py: Windows CPU affinity helper, allowing two physical cores
  at a time and rotating pairs between paired base/changed runs.
- babel_mo_results.json: every timing and peak-allocation sample, source
  hashes, fixture provenance, and output/error comparison totals.
- babel_mo_results.md: all 108 results, including slower cases and extra memory.

The first 100 cases are generated catalog examples. Two more are empty-catalog
controls. Six use unchanged public Django and Wagtail catalogs, with fuzzy
entries included or excluded. Their URLs are pinned to source commits in the
runner and their SHA256 hashes are recorded in the JSON.

The 414 additional comparisons check exact output bytes, output argument type,
number of output writes, and matching encoding/write errors. Of these, 336
produce matching output and 78 produce matching errors.

How to rerun on Windows
----------------------

Create this directory layout (the runner expects these sibling folders):

C:/mo-benchmark/
  babel/                 Babel checkout with the proposed change
  benchmarks/
    babel_mo.py
    benchmark_cpu.py

Download babel_mo.py and benchmark_cpu.py from this branch into benchmarks.
Clone the code branch into babel:

git clone --branch harshitgupta31415/speed-up-mo-file-writing https://github.com/harshitgupta31415/babel.git C:/mo-benchmark/babel
git -C C:/mo-benchmark/babel checkout 4cb2f4102ca18b7c48029b3d8b6ca55f8dc56fbb

From PowerShell, with Python 3.15.0 selected:

Set-Location C:/mo-benchmark/babel
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -e ".[dev]"
& ./.venv/Scripts/python.exe scripts/download_import_cldr.py
& ./.venv/Scripts/python.exe -X utf8 ../benchmarks/babel_mo.py

The runner needs at least two physical cores and Internet access for the first
fixture download. It reloads write_mo from the pinned base commit, compares it
with the checked-out function, and performs eight timing and eight separate
peak-allocation measurements per version. The terminal shows progress for
each sample and the reports update after each completed case.

Only the complete write_mo call is timed; catalog construction, PO parsing,
downloads and output comparisons are outside the timer. Each write uses a
fresh BytesIO. Timing runs do not use tracemalloc. Peak memory means newly
traced Python allocations during a write, not total process RAM. Both
versions use the same core pair within each repeat, and their order alternates.

To run just the 414 output/error comparisons:

& ./.venv/Scripts/python.exe -X utf8 ../benchmarks/babel_mo.py --verify-only

To run the messaging tests and writer doctests:

& ./.venv/Scripts/python.exe -X utf8 -m pytest -q tests/messages --doctest-modules babel/messages/mofile.py

The full-suite check on this PC gave the same result with both versions:
7,832 passed, two failed, nine skipped and two expected failures. Both failures
were the existing test_get_timezone_name_misc parametrizations, which compared
GMT+00:00 with GMT+05:30. The messaging tests and writer doctests passed (394).

Small timing differences can be noise. The large generated-catalog speedups
should not be treated as gains measured on collected production workloads.
