#!/usr/bin/env python3
import json
import sys

def flatten_json(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            yield from flatten_json(v, new_prefix)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_prefix = f"{prefix}[{i}]"
            yield from flatten_json(v, new_prefix)
    else:
        yield prefix, obj

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    for path, value in flatten_json(data):
        print(f"{path}: {value}")

if __name__ == "__main__":
    main()

