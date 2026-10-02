#!/usr/bin/env python3.11
"""Test the email regex included in the spec against examples/email-formats.csv.

The regex in email-format.regex is wrapped across lines so it fits in the
draft; line breaks are removed before use, as the spec text instructs.

Each case has a status: "valid" or "invalid" means a full "email" format
implementation and this deliberately simple regex agree on the result;
"special" means they differ, with the description explaining why.  Special
cases are reported but not tested.
"""

import csv
import os
import re
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
regex_path = os.path.join(base_dir, "email-format.regex")
cases_path = os.path.join(base_dir, "examples", "email-formats.csv")

with open(regex_path, encoding="utf-8") as f:
    email_re = re.compile(f.read().replace("\n", ""))

with open(cases_path, newline="", encoding="utf-8") as f:
    cases = list(csv.DictReader(f))

errors = []
special = []

for case in cases:
    address = case["address"]
    status = case["status"]
    if status == "special":
        print(f" SPCL  {address!r} -- {case['description']}")
        special.append(address)
        continue
    if status not in ("valid", "invalid"):
        print(f" ERROR {address!r}: status must be 'valid', 'invalid' or 'special',"
              f" got {status!r}")
        errors.append(address)
        continue
    actual = "valid" if email_re.fullmatch(address) else "invalid"
    if actual == status:
        print(f" OK    {address!r} ({status})")
    else:
        print(f" FAIL  {address!r}: expected {status}, regex says {actual}"
              f" -- {case['description']}")
        errors.append(address)

tested = len(cases) - len(special)

if errors:
    print(f"\n{len(errors)} of {tested} tested case(s) failed"
          f" ({len(special)} special case(s) not tested).")
    sys.exit(1)
else:
    print(f"\nAll {tested} tested cases match the email regex"
          f" ({len(special)} special case(s) not tested).")
