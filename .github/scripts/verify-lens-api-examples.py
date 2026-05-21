#!/usr/bin/env python3
"""Verify that every Lens visualization API example in the chart docs still
creates a working visualization.

Background
----------
The chart pages under ``explore-analyze/visualize/charts/`` each embed one or
more API examples that POST to ``/api/visualizations``.  The Visualizations
API is in technical preview, so its schema can change between minor versions.
This script extracts every JSON payload from the Console tab of each dropdown,
strips docs-builder ``<n>`` callout markers, posts each one to a live Kibana,
asserts HTTP 201, then cleans up by deleting the created visualization.

Usage
-----
Set ``KIBANA_URL`` and ``API_KEY`` (a Kibana API key with privileges to create
and delete visualizations) in your environment, then run::

    python3 .github/scripts/verify-lens-api-examples.py

Optional flags::

    --keep        Do not delete test visualizations after verification.
    --file F      Only verify a single markdown file (path or basename).

Failure modes
-------------
The script exits ``0`` on success and non-zero when any payload fails, with
the reason printed to stderr. Failure paths:

1. **Environment not set** — ``KIBANA_URL`` or ``API_KEY`` missing.
2. **JSON parse error** — a docs edit broke the JSON inside a curl block
   (stray comma, unbalanced brace, smart quote). The error includes the
   character offset to look at.
3. **API rejected the request (HTTP 4xx/5xx)** — Kibana's response body is
   printed verbatim and includes the field path and reason (for example,
   ``layers.0.breakdown_by: field 'fields' is required``).
4. **Non-201 success status** — the request didn't error but didn't return
   201. Rare; usually a redirect or proxy quirk.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHARTS_DIR = REPO_ROOT / "explore-analyze" / "visualize" / "charts"
CHART_FILES = [
    "area-charts.md",
    "bar-charts.md",
    "gauge-charts.md",
    "heat-map-charts.md",
    "line-charts.md",
    "metric-charts.md",
    "mosaic-charts.md",
    "pie-charts.md",
    "region-map-charts.md",
    "tables.md",
    "tag-cloud-charts.md",
    "treemap-charts.md",
    "waffle-charts.md",
]


def extract_payloads(markdown_path: Path) -> list[tuple[str, dict]]:
    """Return (title, parsed_payload) for every Console tab block in the file.

    Extraction strategy
    -------------------
    Each API dropdown now contains a ``console`` code fence of the form::

        ```console
        POST kbn://api/visualizations
        {
          ...JSON...
        }
        ```

    We locate every such block, strip ``<n>`` callout markers, then
    JSON-parse the body.  No shell-unescaping is needed because the Console
    tab carries plain JSON (unlike the curl tab which uses single-quote
    shell escaping).
    """
    text = markdown_path.read_text(encoding="utf-8")
    results = []

    pattern = re.compile(
        r"```console\nPOST kbn://api/visualizations\n(\{.*?\n\})\n```",
        re.DOTALL,
    )

    for match in pattern.finditer(text):
        raw = match.group(1)
        # Strip callout markers e.g.  <1>  <2>
        cleaned = re.sub(r"\s*<\d+>", "", raw)

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            context_start = max(0, exc.pos - 120)
            context_end = min(len(cleaned), exc.pos + 120)
            snippet = cleaned[context_start:context_end].replace("\n", "↵")
            print(
                f"  ✗ JSON parse error in {markdown_path.name}: {exc}\n"
                f"    ...{snippet}...",
                file=sys.stderr,
            )
            continue

        title = payload.get("title", "(untitled)")
        results.append((title, payload))

    return results


def post_visualization(kibana_url: str, api_key: str, payload: dict) -> str:
    """POST payload to /api/visualizations, return the new visualization ID."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}/api/visualizations",
        data=body,
        method="POST",
        headers={
            "Authorization": f"ApiKey {api_key}",
            "kbn-xsrf": "true",
            "Content-Type": "application/json",
        },
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            status = resp.status
            response_body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        # Failure mode 3: API rejected the payload.
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"POST /api/visualizations HTTP {exc.code}: {detail}"
        ) from exc

    if status != 201:
        # Failure mode 4: unexpected success status.
        raise RuntimeError(f"Unexpected status {status}: {response_body}")

    data = json.loads(response_body)
    return data.get("id") or data.get("data", {}).get("id", "")


def delete_visualization(kibana_url: str, api_key: str, viz_id: str) -> None:
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}/api/visualizations/{viz_id}",
        method="DELETE",
        headers={
            "Authorization": f"ApiKey {api_key}",
            "kbn-xsrf": "true",
        },
    )
    ctx = ssl.create_default_context()
    try:
        urllib.request.urlopen(req, context=ssl.create_default_context())
    except urllib.error.HTTPError as exc:
        print(
            f"  Warning: cleanup DELETE failed with HTTP {exc.code}",
            file=sys.stderr,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Do not delete test visualizations after verification.",
    )
    parser.add_argument(
        "--file",
        help="Only verify a specific markdown file (path or basename).",
    )
    args = parser.parse_args()

    kibana_url = os.environ.get("KIBANA_URL")
    api_key = os.environ.get("API_KEY")
    if not kibana_url or not api_key:
        # Failure mode 1.
        raise SystemExit(
            "KIBANA_URL and API_KEY must be set in the environment.\n"
            "Example:\n"
            "  export KIBANA_URL=https://my-kibana.example.com\n"
            "  export API_KEY=<base64-encoded-api-key>"
        )

    if args.file:
        p = Path(args.file)
        files = [p if p.is_absolute() else CHARTS_DIR / p.name]
    else:
        files = [CHARTS_DIR / f for f in CHART_FILES]

    total = passed = failed = 0

    for md_file in files:
        if not md_file.exists():
            print(f"⚠ File not found: {md_file}", file=sys.stderr)
            continue

        payloads = extract_payloads(md_file)
        if not payloads:
            print(f"{md_file.name}: no payloads found — skipping")
            continue

        print(f"\n{md_file.name}  ({len(payloads)} payload{'s' if len(payloads) != 1 else ''})")

        for title, payload in payloads:
            total += 1
            try:
                viz_id = post_visualization(kibana_url, api_key, payload)
                if not args.keep and viz_id:
                    delete_visualization(kibana_url, api_key, viz_id)
                status_str = "(kept)" if args.keep else "(deleted)"
                print(f"  ✓  {title}  {status_str}")
                passed += 1
            except RuntimeError as exc:
                print(f"  ✗  {title}\n     {exc}", file=sys.stderr)
                failed += 1

    print(f"\n{'─' * 50}")
    print(f"Results: {passed}/{total} passed", end="")
    if failed:
        print(f", {failed} FAILED")
    else:
        print(" — all OK")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
