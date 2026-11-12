#!/usr/bin/env python3.11
"""Check examples/idn-hostname-formats.csv against the "idn-hostname" rules,
using python's "idna" library which seems to match expectations. The library
implements RFC 5891, RFC 5892
and RFC 5893 (including the CONTEXTJ, CONTEXTO and bidi rules).  The package
is used without UTS #46 mapping, so values that only become valid after
mapping (uppercase, full-width characters) are rejected.

Each case gives a value, whether it is valid for the "idn-hostname" format
attribute ("yes" or "no"), and a comment.  As the spec says, a value is valid
if it is a valid "hostname" (RFC 1123 labels, which may include "xn--" labels
that do not decode), or if it is an internationalized hostname under IDNA2008.
"""

import csv
import os
import re
import sys

import idna

base_dir = os.path.dirname(os.path.abspath(__file__))
cases_path = os.path.join(base_dir, "examples", "idn-hostname-formats.csv")

ldh_label = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")


def is_hostname(value):
    return (len(value) <= 253
            and all(ldh_label.fullmatch(label) for label in value.split(".")))


def is_idna_hostname(value):
    labels = value.split(".")
    if any(label == "" for label in labels):
        return False
    try:
        alabels = [idna.alabel(label) for label in labels]
    except idna.IDNAError:
        return False
    return len(b".".join(alabels)) <= 253


def is_idn_hostname(value):
    return is_hostname(value) or is_idna_hostname(value)


with open(cases_path, newline="", encoding="utf-8") as f:
    cases = list(csv.DictReader(f))

errors = []

for case in cases:
    value = case["value"]
    expected = case["valid"]
    if expected not in ("yes", "no"):
        print(f" ERROR {value!r}: valid must be 'yes' or 'no', got {expected!r}")
        errors.append(value)
        continue
    actual = "yes" if is_idn_hostname(value) else "no"
    if actual == expected:
        print(f" OK    {value!r} ({expected})")
    else:
        print(f" FAIL  {value!r}: expected {expected}, checker says {actual}"
              f" -- {case['comment']}")
        errors.append(value)

if errors:
    print(f"\n{len(errors)} of {len(cases)} case(s) failed.")
    sys.exit(1)
else:
    print(f"\nAll {len(cases)} cases match the idn-hostname rules.")
