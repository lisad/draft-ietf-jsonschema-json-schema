#!/usr/bin/env python3.11
"""Check examples/uri-formats.csv against parsers built from the RFC ABNF.

Each case gives a value, one of the "uri", "uri-reference", "iri" or
"iri-reference" format attributes, whether the value is valid for that
attribute ("yes" or "no"), and a comment.  The reference parsers come from
the abnf package, which parses using the ABNF rules of RFC 3986 and
RFC 3987 directly.  These cases document the generic syntax that the spec
refers to; they do not test any text in the spec itself.
"""

import csv
import os
import sys

from abnf import ParseError
from abnf.grammars import rfc3986, rfc3987

base_dir = os.path.dirname(os.path.abspath(__file__))
cases_path = os.path.join(base_dir, "examples", "uri-formats.csv")

rules = {
    "uri": rfc3986.Rule("URI"),
    "uri-reference": rfc3986.Rule("URI-reference"),
    "iri": rfc3987.Rule("IRI"),
    "iri-reference": rfc3987.Rule("IRI-reference"),
}


def parses(rule, value):
    try:
        rule.parse_all(value)
        return True
    except ParseError:
        return False


with open(cases_path, newline="", encoding="utf-8") as f:
    cases = list(csv.DictReader(f))

errors = []

for case in cases:
    value = case["value"]
    fmt = case["format"]
    expected = case["valid"]
    if fmt not in rules:
        print(" ERROR: format must be uri/iri/uri-reference/iri-reference")
        errors.append(value)

    elif expected not in ("yes", "no"):
        print(" ERROR: valid must be 'yes' or 'no'")
        errors.append(value)

    else:
        actual = "yes" if parses(rules[fmt], value) else "no"
        if actual == expected:
            print(f" OK    {fmt:13} {value!r} ({expected})")
        else:
            print(f" FAIL  {fmt:13} {value!r}: expected {expected}, parser says {actual}"
                  f" -- {case['comment']}")
            errors.append(value)

if errors:
    print(f"\n{len(errors)} of {len(cases)} case(s) failed.")
    sys.exit(1)
else:
    print(f"\nAll {len(cases)} cases match the RFC 3986 and RFC 3987 grammars.")
