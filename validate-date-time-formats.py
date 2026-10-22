#!/usr/bin/env python3.11
"""Test examples/date-time-formats.csv against the jsonschema library.

Each case gives a value, one of the "date-time", "date", "time" or
"duration" format attributes, whether the value is valid for that
attribute ("yes" or "no"), and a comment.  The checks are the 2020-12
format checkers in the jsonschema library, which need the library's
"format-nongpl" extra installed.

A case marked "skip" is one where the library does not do what RFC 3339
requires; the comment gives the correct result.  Skipped cases are
reported but not tested.
"""

import csv
import os
import sys

from jsonschema import Draft202012Validator

base_dir = os.path.dirname(os.path.abspath(__file__))
cases_path = os.path.join(base_dir, "examples", "date-time-formats.csv")

checker = Draft202012Validator.FORMAT_CHECKER
formats = ("date-time", "date", "time", "duration")

with open(cases_path, newline="", encoding="utf-8") as f:
    cases = list(csv.DictReader(f))

errors = []
skipped = []

for case in cases:
    value = case["value"]
    fmt = case["format"]
    expected = case["valid"]

    if expected == "skip":
        print(f" SKIP  {fmt:9} {value!r} -- {case['comment']}")
        skipped.append(value)

    elif expected not in ("yes", "no"):
        print(f" ERROR {value!r}: valid must be 'yes', 'no' or 'skip'")
        errors.append(value)

    else:
        actual = "yes" if checker.conforms(value, fmt) else "no"
        if actual == expected:
            print(f" OK    {fmt:9} {value!r} ({expected})")
        else:
            print(f" FAIL  {fmt:9} {value!r}: expected {expected}, jsonschema library says {actual}"
                  f" -- {case['comment']}")
            errors.append(value)

tested = len(cases) - len(skipped)
if errors:
    print(f"\n{len(errors)} of {tested} case(s) failed ({len(skipped)} skipped).")
    sys.exit(1)
else:
    print(f"\nAll {tested} cases pass ({len(skipped)} skipped).")
