#!/usr/bin/env python3
"""
Transform API dropdown blocks to include Console + curl tabs.

Each block of the form:
  :::...{dropdown} Create this chart using the API
  :applies_to: ...

  <intro>

  ```bash
  curl ... -d '{
    <JSON with callouts>
  }'
  ```

  1. callout 1
  2. callout 2

  For more information, refer to the [Visualizations API](...).
  :::...

Becomes:
  :::::::{dropdown} Create this chart using the API
  :applies_to: ...

  <intro>

  :::::{tab-set}

  :::{tab-item} Console
  :sync: api-console
  ```console
  POST kbn://api/visualizations
  {
    <JSON with callouts>
  }
  ```

  1. callout 1
  2. callout 2
  :::

  :::{tab-item} curl
  :sync: api-curl
  ```bash
  curl ... -d '{
    <JSON with callouts>
  }'
  ```

  1. callout 1
  2. callout 2
  :::

  :::::

  For more information, refer to the [Visualizations API](...).
  :::::::
"""

import re
import sys
from pathlib import Path


DROPDOWN_TITLE = "Create this chart using the API"

# Matches the opening fence: one or more colons followed by {dropdown}
OPEN_RE = re.compile(r"^(:{3,})\{dropdown\} " + re.escape(DROPDOWN_TITLE) + r"\s*$")


def transform_file(path: Path) -> str:
    text = path.read_text()
    lines = text.splitlines(keepends=True)

    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = OPEN_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue

        # Found a dropdown opening — collect the entire block
        open_colons = m.group(1)  # e.g. ":::" or "::::" or ":::::"
        close_fence = open_colons + "\n"

        block_lines = [line]
        i += 1
        while i < len(lines):
            block_lines.append(lines[i])
            if lines[i] == close_fence:
                i += 1
                break
            i += 1

        transformed = transform_block(block_lines)
        out.append(transformed)

    return "".join(out)


def transform_block(block_lines: list[str]) -> str:
    """Transform a single dropdown block."""
    raw = "".join(block_lines)

    # ---- Extract the :applies_to: option line (may be absent) ----
    applies_re = re.compile(r"^(:applies_to:.*)\n", re.MULTILINE)
    applies_m = applies_re.search(raw)
    applies_line = (applies_m.group(0) if applies_m else "")

    # ---- Split the block body into: intro | bash block | callout list | api link ----
    # Pattern: optional intro text, ```bash ... ```, numbered list, "For more..."
    bash_block_re = re.compile(
        r"(```bash\n.*?```\n)",
        re.DOTALL,
    )
    bash_m = bash_block_re.search(raw)
    if not bash_m:
        # No bash block found — return unchanged
        print(f"  WARNING: no bash block found, skipping block", file=sys.stderr)
        return raw

    bash_block = bash_m.group(1)

    # ---- Extract JSON from curl -d '{ ... }' ----
    # The payload sits between -d '{\n and \n}' (end of block)
    json_body = extract_json_from_curl(bash_block)
    if json_body is None:
        print(f"  WARNING: could not extract JSON from curl block, skipping", file=sys.stderr)
        return raw

    # ---- Extract numbered callout list ----
    # Everything between end of bash block and "For more information"
    after_bash = raw[bash_m.end():]
    for_more_re = re.compile(r"(For more information.*?\n)", re.DOTALL)
    for_more_m = for_more_re.search(after_bash)

    if for_more_m:
        callout_section = after_bash[: for_more_m.start()]
        for_more_line = for_more_m.group(1)
    else:
        # No "For more" line — treat remaining content (before closing fence) as callouts
        callout_section = after_bash
        for_more_line = ""

    # ---- Extract the intro text (between :applies_to: / opening line and ```bash) ----
    # intro = everything after the opening line (and optional :applies_to:) up to ```bash
    header_end = applies_m.end() if applies_m else raw.index("\n") + 1
    intro = raw[header_end : bash_m.start()]

    # ---- Build the Console JSON block ----
    console_block = f"```console\nPOST kbn://api/visualizations\n{{\n{json_body}\n}}\n```\n"

    # ---- Assemble the new block ----
    new_open = ":::::::" + "{dropdown} " + DROPDOWN_TITLE + "\n"
    new_close = ":::::::\n"
    tab_set_open = "\n:::::{tab-set}\n"
    tab_set_close = "\n:::::\n"
    # 4-colon tab-items so that any :::{note} (3 colons) inside content stays nested
    console_tab_open = "\n::::{tab-item} Console\n:sync: api-console\n"
    console_tab_close = "::::\n"
    curl_tab_open = "\n::::{tab-item} curl\n:sync: api-curl\n"
    curl_tab_close = "::::\n"

    result = (
        new_open
        + applies_line
        + intro
        + tab_set_open
        + console_tab_open
        + console_block
        + callout_section
        + console_tab_close
        + curl_tab_open
        + bash_block
        + callout_section
        + curl_tab_close
        + tab_set_close
        + "\n"
        + for_more_line
        + new_close
    )
    return result


def extract_json_from_curl(bash_block: str) -> str | None:
    """
    Extract the JSON body from a curl -d '{ ... }' block.
    Returns the lines between -d '{ and }' (exclusive), preserving indentation.
    """
    # Find -d '{\n
    start_re = re.compile(r"  -d '\{\n")
    start_m = start_re.search(bash_block)
    if not start_m:
        return None

    rest = bash_block[start_m.end():]

    # The JSON ends at a line that is exactly "}'\n" or "}'\n```"
    end_re = re.compile(r"\n\}'(\n|$)")
    end_m = end_re.search(rest)
    if not end_m:
        return None

    json_body = rest[: end_m.start()]
    # Convert shell single-quote escapes to literal characters so the Console
    # tab contains valid JSON (e.g. shift='\''1w'\'' → shift='1w').
    json_body = json_body.replace("'\\''", "'")
    json_body = json_body.replace("'''", "")
    return json_body


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Add Console tabs to API dropdowns")
    parser.add_argument("files", nargs="+", help="Markdown files to transform")
    parser.add_argument("--dry-run", action="store_true", help="Print output, don't write")
    args = parser.parse_args()

    for filepath in args.files:
        path = Path(filepath)
        if not path.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            continue

        print(f"Processing {path.name}...", file=sys.stderr)
        result = transform_file(path)

        if args.dry_run:
            print(result)
        else:
            path.write_text(result)
            print(f"  Written: {filepath}", file=sys.stderr)


if __name__ == "__main__":
    main()
