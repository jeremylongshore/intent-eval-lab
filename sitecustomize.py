"""sitecustomize.py — auto-initialize coverage in every Python subprocess.

When COVERAGE_PROCESS_START is set in the environment, coverage.process_startup()
reads the path it points to, registers itself, and traces the subprocess. The
result lands as .coverage.<pid>.<hostname>.<random> files that `coverage combine`
merges before report.

Without this file, smoke tests that invoke runners via `subprocess.run(...)`
would show 0% coverage for the runner modules (the parent's coverage doesn't
trace into child processes).

Activated by:
    export COVERAGE_PROCESS_START=/path/to/pyproject.toml
    python3 -m pytest ...

CI sets COVERAGE_PROCESS_START in .github/workflows/python-tests.yml. Local dev
can use the same export or just `coverage run -m pytest ...`.

Reference: https://coverage.readthedocs.io/en/latest/subprocess.html
"""

try:
    import coverage
except ImportError:
    pass
else:
    coverage.process_startup()
