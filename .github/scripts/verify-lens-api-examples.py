#!/usr/bin/env python3
"""Verify that every Lens and Vega visualization API example in the docs still
creates a working visualization.

Background
----------
The chart pages under ``explore-analyze/visualize/charts/`` each embed one or
more API examples that POST to ``/api/visualizations``.  The Visualizations
API is in technical preview, so its schema can change between minor versions.
The Vega page (``explore-analyze/visualize/custom-visualizations-with-vega.md``)
embeds examples that POST to ``/api/vega``.
This script extracts every JSON payload from the Console tab of each dropdown,
strips docs-builder ``<n>`` callout markers, posts each one to a live Kibana,
asserts HTTP 201, then cleans up by deleting the created visualization.

The Vega API only validates the request envelope and accepts any spec, so a
201 alone doesn't prove the chart renders. For Vega payloads, the script also
reads the library item back and asserts the stored spec is the one it sent.
When the ``jsonschema`` package is installed, it also validates each JSON spec
against the Vega or Vega-Lite schema named in its ``$schema`` URL. Kibana
query objects in ``url`` (``%context%``, ``%type%: esql``, and so on) aren't
part of those schemas, so each one is replaced with a placeholder URL before
validation, and the ``config.kibana`` block is removed.

Usage
-----
Set ``KIBANA_URL`` and ``API_KEY`` (a Kibana API key with privileges to create
and delete visualizations) in your environment, then run::

    python3 .github/scripts/verify-lens-api-examples.py

To include the Vega schema check, install ``jsonschema`` first::

    pip install jsonschema

Optional flags::

    --keep          Do not delete test visualizations after verification.
    --file F        Only verify a single markdown file (path or basename).
    --skip-schema   Skip the Vega schema check even if jsonschema is installed.

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
5. **Vega spec schema error** — the spec doesn't match its Vega or Vega-Lite
   schema. The error lists the JSON path and the reason (for example,
   ``encoding.x.axis.title: False is not valid under any of the given
   schemas``).
6. **Vega read-back mismatch** — the API returned 201 but stored a different
   spec.
"""

from __future__ import annotations

import argparse
import copy
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
VEGA_FILE = REPO_ROOT / "explore-analyze" / "visualize" / "custom-visualizations-with-vega.md"
PLACEHOLDER_URL = "https://example.com/kibana-data.json"

_schema_cache: dict[str, dict] = {}


def extract_payloads(markdown_path: Path) -> list[tuple[str, str, dict]]:
    """Return (endpoint, title, parsed_payload) for every Console tab block.

    Extraction strategy
    -------------------
    Each API dropdown now contains a ``console`` code fence of the form::

        ```console
        POST kbn://api/visualizations
        {
          ...JSON...
        }
        ```

    The endpoint is ``visualizations`` or ``vega``. We locate every such
    block, strip ``<n>`` callout markers, then JSON-parse the body.  No
    shell-unescaping is needed because the Console tab carries plain JSON
    (unlike the curl tab which uses single-quote shell escaping).
    """
    text = markdown_path.read_text(encoding="utf-8")
    results = []

    pattern = re.compile(
        r"```console\nPOST kbn://api/(visualizations|vega)\n(\{.*?\n\})\n```",
        re.DOTALL,
    )

    for match in pattern.finditer(text):
        endpoint, raw = match.group(1), match.group(2)
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
        results.append((endpoint, title, payload))

    return results


def post_visualization(
    kibana_url: str, api_key: str, payload: dict, endpoint: str = "visualizations"
) -> str:
    """POST payload to /api/<endpoint>, return the new visualization ID."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}/api/{endpoint}",
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
            f"POST /api/{endpoint} HTTP {exc.code}: {detail}"
        ) from exc

    if status != 201:
        # Failure mode 4: unexpected success status.
        raise RuntimeError(f"Unexpected status {status}: {response_body}")

    data = json.loads(response_body)
    return data.get("id") or data.get("data", {}).get("id", "")


def strip_kibana_extensions(node):
    """Replace Kibana query objects in ``url`` and drop ``config.kibana``."""
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            if key == "url" and isinstance(value, dict):
                out[key] = PLACEHOLDER_URL
            elif key == "config" and isinstance(value, dict):
                out[key] = {
                    k: strip_kibana_extensions(v)
                    for k, v in value.items()
                    if k != "kibana"
                }
            else:
                out[key] = strip_kibana_extensions(value)
        return out
    if isinstance(node, list):
        return [strip_kibana_extensions(item) for item in node]
    return node


def validate_vega_spec(spec: dict) -> None:
    """Validate a JSON Vega spec against its ``$schema``. Failure mode 5."""
    import jsonschema

    if spec.get("format") != "json":
        return
    value = spec["value"]
    schema_url = value.get("$schema")
    if not schema_url:
        raise RuntimeError("Vega spec has no $schema, so it can't be validated")
    if schema_url not in _schema_cache:
        with urllib.request.urlopen(
            schema_url, context=ssl.create_default_context()
        ) as resp:
            _schema_cache[schema_url] = json.loads(resp.read().decode("utf-8"))
    schema = _schema_cache[schema_url]
    validator = jsonschema.validators.validator_for(schema)(schema)
    errors = list(
        validator.iter_errors(strip_kibana_extensions(copy.deepcopy(value)))
    )
    if errors:
        best = jsonschema.exceptions.best_match(errors)
        path = ".".join(str(p) for p in best.absolute_path) or "(root)"
        details = [f"       {path}: {best.message[:200]}"]
        details += [f"         {sub.message[:150]}" for sub in (best.context or [])[:3]]
        raise RuntimeError(f"Spec doesn't match {schema_url}:\n" + "\n".join(details))


def check_vega_readback(kibana_url: str, api_key: str, viz_id: str, spec: dict) -> None:
    """GET the Vega library item and compare its spec. Failure mode 6."""
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}/api/vega/{viz_id}",
        headers={"Authorization": f"ApiKey {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context()) as resp:
            stored = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GET /api/vega/{viz_id} HTTP {exc.code}: {detail}") from exc
    if stored.get("data", {}).get("spec") != spec:
        raise RuntimeError("The stored Vega spec differs from the spec that was sent")


def delete_visualization(
    kibana_url: str, api_key: str, viz_id: str, endpoint: str = "visualizations"
) -> None:
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}/api/{endpoint}/{viz_id}",
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
    parser.add_argument(
        "--skip-schema",
        action="store_true",
        help="Skip the Vega schema check even if jsonschema is installed.",
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

    check_schema = not args.skip_schema
    if check_schema:
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            check_schema = False
            print("jsonschema isn't installed, so Vega specs skip the schema check.")

    if args.file:
        p = Path(args.file)
        if p.is_absolute():
            files = [p]
        elif p.name == VEGA_FILE.name:
            files = [VEGA_FILE]
        else:
            files = [CHARTS_DIR / p.name]
    else:
        files = [CHARTS_DIR / f for f in CHART_FILES] + [VEGA_FILE]

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

        for endpoint, title, payload in payloads:
            total += 1
            try:
                if endpoint == "vega" and check_schema:
                    validate_vega_spec(payload.get("spec", {}))
                viz_id = post_visualization(kibana_url, api_key, payload, endpoint)
                if endpoint == "vega":
                    check_vega_readback(kibana_url, api_key, viz_id, payload.get("spec"))
                if not args.keep and viz_id:
                    delete_visualization(kibana_url, api_key, viz_id, endpoint)
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
