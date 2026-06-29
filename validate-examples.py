#!/usr/bin/env python3.11
"""Validate all JSON files in examples/ against the JSON Schema 2020-12 meta-schema."""

import json
import os
import sys

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

examples_dir = os.path.join(os.path.dirname(__file__), "examples")
files = sorted(f for f in os.listdir(examples_dir) if f.endswith(".json"))
errors = []

for filename in files:
    path = os.path.join(examples_dir, filename)
    with open(path) as f:
        schema = json.load(f)
    try:
        Draft202012Validator.check_schema(schema)
        print(f" OK    {filename}")
    except SchemaError as e:
        print(f" FAIL  {filename}: {e.message}")
        errors.append(filename)

if errors:
    print(f"\n{len(errors)} file(s) failed meta-schema validation.")
    sys.exit(1)
else:
    print(f"\nAll {len(files)} schemas are valid against the 2020-12 meta-schema.")
