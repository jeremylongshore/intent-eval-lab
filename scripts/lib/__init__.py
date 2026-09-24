"""Shared helpers for the scripts/ deep-capture extractors.

Hyphenated script filenames are not importable, so cross-script reuse lives here
as a real package. Modules add their own directory to sys.path before importing
it (they run as `python3 scripts/<name>.py`, and pytest loads them by file path).
"""
