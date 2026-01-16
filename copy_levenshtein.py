#!/usr/bin/env python3
import shutil
import os

src_file = "/Users/fefe/Downloads/levenshtein_pairs.csv"
dest_file = "/Users/fefe/albert-hod-101-2026-group-7/Information Retrieval/Assignement 1/part1/source/levenshtein_pairs.csv"

try:
    shutil.copy2(src_file, dest_file)
    print(f"✓ File copied successfully to: {dest_file}")
except FileNotFoundError:
    print(f"✗ Source file not found: {src_file}")
except Exception as e:
    print(f"✗ Error: {e}")
