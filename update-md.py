#!/usr/bin/env python3
"""
Recursively walk a directory and, in every .md file:
  — if there’s a top‐level `products:` list in the YAML frontmatter,
    replace each
      <whitespace>- VALUE
    with
      <same whitespace>- id: VALUE

Usage:
    python update-md.py /path/to/markdown/root
"""

import sys
import os
import re

# matches the opening/closing of frontmatter
DELIM = re.compile(r'^---\s*$')
# matches the 'products:' line
PROD_KEY = re.compile(r'^(\s*)products:\s*$')
# matches a list item: captures leading whitespace, the value, and any trailing spaces
LIST_ITEM = re.compile(r'^(\s*)-\s*(.+?)(\s*)\n$')

def process_markdown(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # must start with '---'
    if not lines or not DELIM.match(lines[0]):
        return

    # find end of frontmatter
    try:
        end_idx = next(i for i, L in enumerate(lines[1:], start=1) if DELIM.match(L))
    except StopIteration:
        return

    changed = False
    # scan frontmatter for "products:" key
    i = 1
    while i < end_idx:
        m = PROD_KEY.match(lines[i])
        if m:
            # found products: at line i
            j = i + 1
            # for each immediately following "- ..." line, rewrite
            while j < end_idx:
                mi = LIST_ITEM.match(lines[j])
                if not mi:
                    break
                ws, val, trail = mi.groups()
                # skip if already "- id: ..."
                if not val.startswith('id:'):
                    lines[j] = f"{ws}- id: {val}{trail}\n"
                    changed = True
                j += 1
            break
        i += 1

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"✔ Updated products in {path}")

def main(root):
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith('.md'):
                process_markdown(os.path.join(dirpath, fn))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python update-md.py /path/to/markdown/root")
        sys.exit(1)
    main(sys.argv[1])
