---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Notepad Markdown RCE Exploitation" prebuilt detection rule.'
---

# Potential Notepad Markdown RCE Exploitation

## Triage and analysis

### Investigating Potential Notepad Markdown RCE Exploitation

This rule detects a new child process launched by `notepad.exe` when Notepad was opened with a Markdown (`.md`) file.
This behavior can indicate exploitation of a Notepad remote code execution vulnerability where crafted Markdown content
triggers unintended process execution.

### Possible investigation steps

- Validate the parent-child relationship and confirm `notepad.exe` is the direct parent of the suspicious process.
- Review the full command line of both parent and child processes, including the Markdown file path in `process.parent.args`.
- Identify the Markdown file source (email attachment, browser download, chat client, removable media, or network share).
- Inspect process ancestry and descendants for additional payload execution, script interpreters, or LOLBIN activity.
- Correlate with file, registry, and network events around the same timestamp to identify follow-on behavior.
- Determine whether the child process and its execution path are expected in your environment.

### False positive analysis

- Legitimate automation or editor extensions may occasionally spawn helper processes from Notepad workflows.
- User-driven workflows that invoke external tools from Markdown previews can trigger this behavior.
- If benign, tune by excluding known-safe child process names, hashes, signed binaries, and approved file paths.

### Response and remediation

- Isolate affected endpoints until scope is understood.
- Terminate suspicious child and descendant processes initiated from `notepad.exe`.
- Quarantine and preserve the triggering Markdown file for forensic analysis.
- Run endpoint malware scans and collect volatile artifacts (running processes, network connections, autoruns).
- Patch Windows/Notepad to the latest security update level addressing the vulnerability.
- Hunt for the same parent-child pattern across other hosts to identify additional impacted systems.
