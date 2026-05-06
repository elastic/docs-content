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

Exit codes
----------
``0`` on success. Non-zero on any failure, with the reason printed to stderr.
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
        raise SystemExit(
            f"Could not find a curl POST example in {markdown_path}. "
            "Has the page structure changed?"
        )
    raw = match.group(1)
    cleaned = re.sub(r"\s*<\d+>", "", raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
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
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"POST /api/dashboards failed with HTTP {exc.code}: {detail}"
        ) from exc

    if status != 201:
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
        raise SystemExit(
            "KIBANA_URL and API_KEY must be set in the environment."
        )

    markdown_path = Path(args.markdown)
    payload = extract_payload(markdown_path)

    declared_panels = len(payload.get("panels", []))
    if declared_panels != EXPECTED_PANEL_COUNT:
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
        if not args.keep:
            delete_dashboard(kibana_url, api_key, dashboard_id)
        raise SystemExit(
            f"Server-created panel count ({created_panels}) does not match "
            f"the request ({declared_panels}). The schema may have changed."
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
