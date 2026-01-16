#!/usr/bin/env python3
import shutil
import os

base_path = "/Users/fefe/albert-hod-101-2026-group-7/Information Retrieval/Assignement 1"
old_path = os.path.join(base_path, "part1", "source")
new_path = os.path.join(base_path, "source")

try:
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
        print(f"✓ Moved: {old_path} -> {new_path}")
    else:
        print(f"✗ Source folder not found: {old_path}")
except Exception as e:
    print(f"✗ Error: {e}")
