#!/usr/bin/env python3
"""
Sync prebuilt detection rules from elastic/detection-rules to CSV files.

Downloads the latest tarball from the detection-rules repo, parses TOML
rule files, and generates CSV files organized by MITRE ATT&CK tactic
for inclusion in docs via the csv-include directive.
"""

import argparse
import csv
import io
import os
import re
import sys
import tarfile
from collections import defaultdict
from typing import Any, Dict, List, Optional

import requests
import toml


TARBALL_URL = "https://api.github.com/repos/elastic/detection-rules/tarball"

RULE_PATH_PATTERNS = [
    re.compile(r"^[^/]+/rules/.*\.toml$"),
    re.compile(r"^[^/]+/rules_building_block/.*\.toml$"),
]
DEPRECATED_PATTERN = re.compile(r"/_deprecated/")

RULE_TYPE_LABELS = {
    "eql": "EQL",
    "query": "Custom Query",
    "saved_query": "Custom Query",
    "threshold": "Threshold",
    "threat_match": "Indicator Match",
    "new_terms": "New Terms",
    "esql": "ES|QL",
    "machine_learning": "Machine Learning",
}

TACTIC_ORDER = [
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact",
]

CSV_COLUMNS = ["Name", "Technique", "Rule Type", "Severity", "Source"]


def tactic_to_filename(tactic: str) -> str:
    return tactic.lower().replace(" ", "-").replace("&", "and") + ".csv"


def derive_rule_type(rule: Dict[str, Any]) -> str:
    if rule.get("type") == "machine_learning":
        return "Machine Learning"
    if rule.get("language") == "esql":
        return "ES|QL"
    return RULE_TYPE_LABELS.get(rule.get("type", ""), "Unknown")


def extract_techniques(threats: List[Dict]) -> str:
    ids = set()
    for threat_entry in threats:
        for tech in threat_entry.get("technique", []):
            tid = tech.get("id", "")
            if tid:
                ids.add(tid)
            for sub in tech.get("subtechnique", []):
                sid = sub.get("id", "")
                if sid:
                    ids.add(sid)
    return ", ".join(sorted(ids))


def extract_tactics(threats: List[Dict]) -> List[str]:
    tactics = []
    for threat_entry in threats:
        name = threat_entry.get("tactic", {}).get("name", "")
        if name and name not in tactics:
            tactics.append(name)
    return tactics if tactics else ["Other"]


def truncate_description(desc: str, max_len: int = 160) -> str:
    if not desc:
        return ""
    cleaned = re.sub(r"\s+", " ", desc.replace("\n", " ").replace("\r", " ")).strip()
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 3].rsplit(" ", 1)[0] + "..."


def github_relative_path(entry_path: str) -> str:
    match = re.match(r"^[^/]+/(.*)", entry_path)
    return match.group(1) if match else entry_path


def fetch_and_parse_rules(verbose: bool = False) -> List[Dict[str, Any]]:
    """Download the detection-rules tarball and parse all TOML rule files."""
    if verbose:
        print(f"Fetching tarball from {TARBALL_URL}...")

    resp = requests.get(TARBALL_URL, stream=True, timeout=120)
    resp.raise_for_status()

    rules = []
    skipped = 0

    with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue

            path = member.name
            if DEPRECATED_PATTERN.search(path):
                continue
            if not any(p.match(path) for p in RULE_PATH_PATTERNS):
                continue

            try:
                f = tar.extractfile(member)
                if f is None:
                    continue
                content = f.read().decode("utf-8")
                parsed = toml.loads(content)
            except Exception as e:
                if verbose:
                    print(f"  Skipping {path}: {e}")
                skipped += 1
                continue

            rule = parsed.get("rule", {})
            if not rule.get("name"):
                skipped += 1
                continue

            threats = rule.get("threat", [])

            rules.append({
                "name": rule["name"],
                "description": truncate_description(rule.get("description", "")),
                "tactics": extract_tactics(threats),
                "techniques": extract_techniques(threats),
                "rule_type": derive_rule_type(rule),
                "severity": (rule.get("severity") or "unknown").capitalize(),
                "github_path": github_relative_path(path),
            })

    if verbose:
        print(f"Parsed {len(rules)} rules ({skipped} skipped)")
    return rules


def write_csv_file(filepath: str, rows: List[Dict], verbose: bool = False):
    """Write a sorted CSV file for a set of rules."""
    sorted_rows = sorted(rows, key=lambda r: r["name"].lower())

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        for r in sorted_rows:
            source = (
                f"[GitHub ↗](https://github.com/elastic/detection-rules"
                f"/blob/main/{r['github_path']})"
            )
            writer.writerow([
                r["name"],
                r["techniques"],
                r["rule_type"],
                r["severity"],
                source,
            ])

    if verbose:
        print(f"  Wrote {len(sorted_rows):>4} rules → {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Sync detection rules to CSV")
    parser.add_argument(
        "--output-dir",
        default=os.path.join(
            "solutions", "security", "detect-and-alert", "prebuilt-rule-catalog"
        ),
        help="Output directory for CSV files",
    )
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    args = parser.parse_args()

    rules = fetch_and_parse_rules(verbose=args.verbose)

    if not rules:
        print("ERROR: No rules found. Aborting.", file=sys.stderr)
        sys.exit(1)

    by_tactic = defaultdict(list)
    for rule in rules:
        for tactic in rule["tactics"]:
            by_tactic[tactic].append(rule)

    ordered_tactics = list(TACTIC_ORDER)
    for tactic in sorted(by_tactic.keys()):
        if tactic not in ordered_tactics:
            ordered_tactics.append(tactic)

    generated = []
    for tactic in ordered_tactics:
        entries = by_tactic.get(tactic)
        if not entries:
            continue
        filename = tactic_to_filename(tactic)
        filepath = os.path.join(args.output_dir, filename)
        write_csv_file(filepath, entries, verbose=args.verbose)
        generated.append(filepath)

    all_path = os.path.join(args.output_dir, "_all-rules.csv")
    write_csv_file(all_path, rules, verbose=args.verbose)
    generated.append(all_path)

    print(f"\n✓ Generated {len(generated)} CSV files ({len(rules)} total rules)")
    for tactic in ordered_tactics:
        count = len(by_tactic.get(tactic, []))
        if count:
            print(f"  {tactic}: {count}")

    for p in generated:
        print(f"OUTPUT_CSV_PATH={p}")


if __name__ == "__main__":
    main()
