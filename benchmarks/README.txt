PO location lookup benchmarks
=============================

These are the runner and results for the PO location lookup change. The
upstream PR only changes pofile.py and its tests; these files stay in this
separate branch so they do not add to that diff.

Tested code: 622716125a23cf108c5ef4788fcbcca8d427d0c4
Base code: e2a17919f0eb988bfea2883b00793ca4d5d37c4f
Recorded environment: Python 3.15.0, Windows 11.

The table includes all 112 cases, including slower results. Most inputs are
generated examples, not production workloads. Django and Wagtail files have
no source references and are controls. The Odoo file has source references,
but was slower in this run. See the JSON for every sample and fixture hash.

How to run again (PowerShell on Windows)
---------------------------------------

Keep the folders side by side:

  C:/po-benchmark/babel/       code checkout
  C:/po-benchmark/benchmarks/  files from this directory

Copy babel_po_locations.py, babel_mo.py and benchmark_cpu.py into the
benchmarks folder. babel_mo.py provides the shared public-catalog loader;
importing it does not run the MO benchmarks. Public fixtures are downloaded
from pinned commits on the first run. Internet access is needed for that.

git clone --branch harshitgupta31415/speed-up-po-location-lookups https://github.com/harshitgupta31415/babel.git C:/po-benchmark/babel
git -C C:/po-benchmark/babel checkout 622716125a23cf108c5ef4788fcbcca8d427d0c4
Set-Location C:/po-benchmark/babel
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -e '.[dev]'
& ./.venv/Scripts/python.exe scripts/download_import_cldr.py
& ./.venv/Scripts/python.exe -X utf8 ../benchmarks/babel_po_locations.py

Use Python 3.15.0 to match the recorded version. The runner checks that it
imports Babel from the sibling checkout. It loads the original generator
from the pinned base commit and compares it with the changed generator.
Two otherwise identical write_po functions call those generators. The
complete write_po call is timed; setup and output checks are not.

Each version gets eight timing runs and eight separate allocation runs.
The table uses medians. Peak means newly traced Python allocations during
one write, not total RAM. There is one process, restricted to two physical
cores at a time, with rotating pairs. Both versions use the same pair in
each repeat and their order alternates. This is not a parallel writer.

The runner overwrites its local result files. Keep the recorded JSON/MD
elsewhere if you want to compare a new run with this one.

Output and error checks only:
& ./.venv/Scripts/python.exe -X utf8 ../benchmarks/babel_po_locations.py --verify-only

For the test runs, also copy run_babel_po_tests.py into benchmarks:
& ./.venv/Scripts/python.exe -X utf8 ../benchmarks/run_babel_po_tests.py --targeted
& ./.venv/Scripts/python.exe -X utf8 ../benchmarks/run_babel_po_tests.py --base --targeted

Drop --targeted to run the full suite. In the recorded environment both
full-suite runs had 7,836 passes and the same two timezone-name failures
(GMT+00:00 versus GMT+05:30), plus nine skips and two expected failures.
The targeted runs both had 408 passes.
