#!/usr/bin/env python3
"""Verify that every Vega API example in the Vega docs still creates a working
Vega library item.

Background
----------
The Vega page at ``explore-analyze/visualize/custom-visualizations-with-vega.md``
embeds API examples that POST to ``/api/vega``. The Vega API only validates the
request envelope (``title`` and ``spec.format`` plus ``spec.value``). It accepts
any spec content, so a 201 alone doesn't prove the chart renders. This script
runs three checks on every Console payload:

1. **Spec schema**: Validates the spec against the Vega or Vega-Lite JSON
   schema named in its ``$schema`` URL. Kibana query objects in ``url`` (for
   example ``%context%`` or ``%type%: esql``) are not part of those schemas, so
   each one is replaced with a placeholder URL before validation. The
   ``config.kibana`` block is removed for the same reason.
2. **Create**: POSTs the payload to a live Kibana and asserts HTTP 201.
3. **Read back**: GETs the new library item and asserts the stored spec is the
   one that was sent.

The script then deletes the library item.

Usage
-----
Install the dependencies, set ``KIBANA_URL`` and ``API_KEY`` (a Kibana API key
with privileges to create and delete Vega visualizations) in your environment,
then run::

    pip install jsonschema hjson
    python3 .github/scripts/verify-vega-api-examples.py

Optional flags::

    --keep          Do not delete test library items after verification.
    --skip-schema   Skip the JSON schema validation (no network access to
                    vega.github.io, for example).
    --file F        Verify a different markdown file.

Failure modes
-------------
The script exits ``0`` on success and non-zero when any payload fails, with
the reason printed to stderr. Failure paths:

1. **Environment not set**: ``KIBANA_URL`` or ``API_KEY`` missing.
2. **JSON parse error**: A docs edit broke the JSON inside a Console block
   (stray comma, unbalanced brace, smart quote).
3. **Spec schema error**: The spec doesn't match its Vega or Vega-Lite schema.
   The error lists the JSON path and the reason (for example,
   ``encoding.x.type: 'time' is not one of [...]``).
4. **API rejected the request (HTTP 4xx/5xx)**: Kibana's response body is
   printed verbatim and includes the field path and reason.
5. **Read-back mismatch**: The API returned 201 but stored a different spec.
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
DEFAULT_FILE = (
    REPO_ROOT / "explore-analyze" / "visualize" / "custom-visualizations-with-vega.md"
)
PLACEHOLDER_URL = "https://example.com/kibana-data.json"

_schema_cache: dict[str, dict] = {}


def extract_payloads(markdown_path: Path) -> list[tuple[str, dict]]:
    """Return (title, parsed_payload) for every ``POST kbn://api/vega`` block."""
    text = markdown_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"```console\nPOST kbn://api/vega\n(\{.*?\n\})\n```",
        re.DOTALL,
    )
    results = []
    for match in pattern.finditer(text):
        cleaned = re.sub(r"\s*<\d+>", "", match.group(1))
        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            start = max(0, exc.pos - 120)
            snippet = cleaned[start : exc.pos + 120].replace("\n", "↵")
            print(
                f"  ✗ JSON parse error in {markdown_path.name}: {exc}\n"
                f"    ...{snippet}...",
                file=sys.stderr,
            )
            continue
        results.append((payload.get("title", "(untitled)"), payload))
    return results


def spec_as_object(spec: dict) -> dict:
    """Return the Vega spec as a dict, whatever its ``format``."""
    value = spec.get("value")
    if spec.get("format") == "json":
        return value
    import hjson  # Imported here so JSON-only payloads don't need it.

    return json.loads(json.dumps(hjson.loads(value)))


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


def load_schema(url: str) -> dict:
    if url not in _schema_cache:
        with urllib.request.urlopen(url, context=ssl.create_default_context()) as resp:
            _schema_cache[url] = json.loads(resp.read().decode("utf-8"))
    return _schema_cache[url]


def validate_spec(spec_obj: dict) -> None:
    import jsonschema

    schema_url = spec_obj.get("$schema")
    if not schema_url:
        raise RuntimeError("Spec has no $schema, so it can't be validated")
    schema = load_schema(schema_url)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema)
    errors = list(
        validator.iter_errors(strip_kibana_extensions(copy.deepcopy(spec_obj)))
    )
    if errors:
        best = jsonschema.exceptions.best_match(errors)
        path = ".".join(str(p) for p in best.absolute_path) or "(root)"
        details = [f"       {path}: {best.message[:200]}"]
        details += [f"         {sub.message[:150]}" for sub in (best.context or [])[:3]]
        raise RuntimeError(f"Spec doesn't match {schema_url}:\n" + "\n".join(details))


def request(kibana_url: str, api_key: str, method: str, path: str, payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        f"{kibana_url.rstrip('/')}{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"ApiKey {api_key}",
            "kbn-xsrf": "true",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context()) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", action="store_true")
    parser.add_argument("--skip-schema", action="store_true")
    parser.add_argument("--file", help="Markdown file to verify.")
    args = parser.parse_args()

    kibana_url = os.environ.get("KIBANA_URL")
    api_key = os.environ.get("API_KEY")
    if not kibana_url or not api_key:
        raise SystemExit("KIBANA_URL and API_KEY must be set in the environment.")

    if not args.skip_schema:
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            raise SystemExit(
                "The jsonschema package is required: pip install jsonschema hjson\n"
                "Or run with --skip-schema."
            )

    md_file = Path(args.file) if args.file else DEFAULT_FILE
    payloads = extract_payloads(md_file)
    if not payloads:
        print(f"{md_file.name}: no payloads found", file=sys.stderr)
        return 1

    print(f"\n{md_file.name}  ({len(payloads)} payload{'s' if len(payloads) != 1 else ''})")
    passed = failed = 0
    for title, payload in payloads:
        try:
            sent_spec = spec_as_object(payload["spec"])
            if not args.skip_schema:
                validate_spec(sent_spec)

            status, created = request(kibana_url, api_key, "POST", "/api/vega", payload)
            if status != 201:
                raise RuntimeError(f"Unexpected status {status}: {created}")
            item_id = created.get("id")

            _, stored = request(kibana_url, api_key, "GET", f"/api/vega/{item_id}")
            stored_spec = spec_as_object(stored["data"]["spec"])
            if stored_spec != sent_spec:
                raise RuntimeError("The stored spec differs from the spec that was sent")

            if not args.keep:
                request(kibana_url, api_key, "DELETE", f"/api/vega/{item_id}")
            print(f"  ✓  {title}  {'(kept)' if args.keep else '(deleted)'}")
            passed += 1
        except (RuntimeError, KeyError, ValueError) as exc:
            print(f"  ✗  {title}\n     {exc}", file=sys.stderr)
            failed += 1

    total = passed + failed
    print(f"\n{'─' * 50}")
    print(f"Results: {passed}/{total} passed" + (f", {failed} FAILED" if failed else " — all OK"))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
