#!/usr/bin/env python3
"""Verify that the embedded Dashboards API example in the Kibana data
exploration learning tutorial still creates a working dashboard.

Background
----------
The tutorial page at ``explore-analyze/kibana-data-exploration-learning-tutorial.md``
embeds a single ``curl`` example that POSTs to ``/api/dashboards`` and recreates
the dashboard built throughout the tutorial. The Dashboards API is in technical
preview, so its schema can change between minor versions. This script extracts
that JSON payload from the markdown, strips docs-builder ``<n>`` callout
markers, posts it to a live Kibana, and asserts the dashboard creates
successfully with the expected number of panels.

Usage
-----
Set ``KIBANA_URL`` and ``API_KEY`` (a Kibana API key with privileges to create
dashboards) in your environment, then run::

    python3 .github/scripts/verify-dashboards-api-example.py

Optional flags::

    --keep        Do not delete the test dashboard after verification.
    --markdown F  Point at a different markdown file (default: the tutorial).

Failure modes
-------------
The script exits ``0`` on success and non-zero on any failure, with the
reason printed to stderr. Each failure path is annotated inline below;
this is the index:

1. **Environment not set** — ``KIBANA_URL`` or ``API_KEY`` missing. Setup
   problem, not an API problem. Source your ``.env`` and re-run.
2. **Curl block not found in markdown** — the regex couldn't locate the
   ``curl`` POST example. The dropdown was removed, restructured, or the
   code fence was reformatted. Open the markdown and confirm the example
   is still present in the expected shape.
3. **Extracted JSON is invalid** — a docs edit broke the JSON inside the
   curl block (stray comma, unbalanced brace, smart quote). The error
   includes the line/column reported by the JSON parser.
4. **Panel count drift in the source** — the payload no longer declares
   ``EXPECTED_PANEL_COUNT`` panels. Either the example was edited
   intentionally (update the constant) or panels were lost.
5. **API rejected the request (HTTP 4xx/5xx)** — the most informative
   failure mode for schema drift. Kibana's response body is printed
   verbatim and includes the field path and reason
   (for example, ``panels.5.config.layers.0.breakdown_by: field 'fields' is required``).
6. **Non-201 success status** — the request didn't error but didn't
   return 201 either. Rare; usually a redirect or proxy quirk.
7. **Panel count mismatch on the server** — POST returned 201 but the
   stored dashboard has fewer (or more) panels than we sent. Means the
   API silently dropped a panel rather than rejecting the whole request.
   The script identifies the missing panels by their ``grid`` position
   and prints ``type``/``config.type`` for each so you know which
   visualization to look at.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MARKDOWN = (
    REPO_ROOT
    / "explore-analyze"
    / "kibana-data-exploration-learning-tutorial.md"
)
EXPECTED_PANEL_COUNT = 11


def extract_payload(markdown_path: Path) -> dict:
    """Return the parsed JSON payload from the curl example in the markdown."""
    text = markdown_path.read_text(encoding="utf-8")
    match = re.search(
        r"curl[^\n]*\n(?:[^\n]*\n)*?\s*-d '(\{.*?\})'\n```",
        text,
        re.DOTALL,
    )
    if not match:
        # Failure mode 2: the regex couldn't find a curl block matching our
        # expected shape. The page has been restructured, the dropdown was
        # removed, or the fence/indent changed. Inspect the markdown to
        # confirm the example still exists.
        raise SystemExit(
            f"Could not find a curl POST example in {markdown_path}. "
            "Has the page structure changed?"
        )
    raw = match.group(1)
    cleaned = re.sub(r"\s*<\d+>", "", raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        # Failure mode 3: a docs edit produced syntactically invalid JSON
        # inside the curl block. The parser reports the line/column to look
        # at; also worth checking for smart quotes or trailing commas.
        raise SystemExit(f"Extracted JSON is not valid: {exc}") from exc


def post_dashboard(kibana_url: str, api_key: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}/api/dashboards",
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
        # Failure mode 5: the API rejected the payload. `detail` is Kibana's
        # full response body, which for schema rejections includes the field
        # path and reason. This is the failure that tells you exactly what
        # the API now expects vs. what the example sends.
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"POST /api/dashboards failed with HTTP {exc.code}: {detail}"
        ) from exc

    if status != 201:
        # Failure mode 6: 2xx but not 201. Rare. Usually a proxy or redirect
        # in front of Kibana; double-check `KIBANA_URL`.
        raise SystemExit(f"Unexpected status code {status}: {response_body}")
    return json.loads(response_body)


def delete_dashboard(kibana_url: str, api_key: str, dashboard_id: str) -> None:
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}/api/dashboards/{dashboard_id}",
        method="DELETE",
        headers={
            "Authorization": f"ApiKey {api_key}",
            "kbn-xsrf": "true",
        },
    )
    ctx = ssl.create_default_context()
    try:
        urllib.request.urlopen(req, context=ctx)
    except urllib.error.HTTPError as exc:
        print(
            f"Warning: cleanup DELETE failed with HTTP {exc.code}",
            file=sys.stderr,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--markdown",
        default=str(DEFAULT_MARKDOWN),
        help=f"Markdown file to verify (default: {DEFAULT_MARKDOWN})",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Do not delete the dashboard after verification.",
    )
    args = parser.parse_args()

    kibana_url = os.environ.get("KIBANA_URL")
    api_key = os.environ.get("API_KEY")
    if not kibana_url or not api_key:
        # Failure mode 1: missing credentials. Source the .env file or
        # export both variables before re-running.
        raise SystemExit(
            "KIBANA_URL and API_KEY must be set in the environment."
        )

    markdown_path = Path(args.markdown)
    payload = extract_payload(markdown_path)

    declared_panels = len(payload.get("panels", []))
    if declared_panels != EXPECTED_PANEL_COUNT:
        # Failure mode 4: the example no longer matches what this script
        # was designed to verify. If the change is intentional (a panel was
        # added or removed in the docs), update EXPECTED_PANEL_COUNT above.
        raise SystemExit(
            f"Payload declares {declared_panels} panels but the verifier "
            f"expects {EXPECTED_PANEL_COUNT}. Update EXPECTED_PANEL_COUNT "
            "if this change is intentional."
        )

    today = dt.date.today().isoformat()
    payload["title"] = f"{today} verify-dashboards-api-example (test run)"

    print(
        f"Posting payload extracted from {markdown_path.name} "
        f"({declared_panels} panels) to {kibana_url}..."
    )
    response = post_dashboard(kibana_url, api_key, payload)
    dashboard_id = response.get("id")
    created_panels = len(response.get("data", {}).get("panels", []))
    print(f"Created dashboard {dashboard_id} with {created_panels} panels.")

    if created_panels != declared_panels:
        # Failure mode 7: the API accepted the request (201) but stored a
        # different number of panels than we sent. Identify the missing
        # panels by their grid position, which is stable across the
        # request/response roundtrip, so the editor knows which panel
        # config the API silently dropped.
        returned_grids = {
            (p.get("grid", {}).get("x"), p.get("grid", {}).get("y"))
            for p in response.get("data", {}).get("panels", [])
        }
        missing = [
            p
            for p in payload.get("panels", [])
            if (p.get("grid", {}).get("x"), p.get("grid", {}).get("y"))
            not in returned_grids
        ]
        if missing:
            missing_lines = "\n".join(
                f"  - grid x={p['grid']['x']}, y={p['grid']['y']} "
                f"(type={p.get('type')}, "
                f"config.type={p.get('config', {}).get('type')})"
                for p in missing
            )
            detail = f"\nMissing panels:\n{missing_lines}"
        else:
            detail = ""
        if not args.keep:
            delete_dashboard(kibana_url, api_key, dashboard_id)
        raise SystemExit(
            f"Server-created panel count ({created_panels}) does not match "
            f"the request ({declared_panels}). The schema may have changed."
            f"{detail}"
        )

    if args.keep:
        print("Skipping cleanup (--keep).")
    else:
        delete_dashboard(kibana_url, api_key, dashboard_id)
        print("Deleted test dashboard.")

    print("OK: example payload still creates a valid dashboard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
