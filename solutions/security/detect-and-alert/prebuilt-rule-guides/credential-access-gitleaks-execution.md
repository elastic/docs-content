---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Secret Scanning via Gitleaks" prebuilt detection rule.
---

# Potential Secret Scanning via Gitleaks

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Secret Scanning via Gitleaks

This alert fires when a host launches Gitleaks, a secret-scanning utility that hunts high-entropy strings and credentials in source code and repositories, signaling potential credential harvesting. An attacker may clone internal repos or traverse local workspace directories, drop a portable gitleaks binary in /tmp or %TEMP%, run recursive scans with wide rule sets and JSON output, then archive the results to exfiltrate tokens, API keys, and passwords for lateral movement and service impersonation.

### Possible investigation steps

- Review the full command line to identify --path/--repo/--report/--format flags, which reveal scope and whether results are being written for exfiltration.
- Examine parent and ancestry plus user session to determine if it was launched by CI/dev tooling versus an interactive shell, and note execution from temp or unusual directories suggesting a dropped portable binary.
- Locate and inspect newly created artifacts (gitleaks.json, .sarif, .csv, zip archives) near the event time, confirm the presence of secrets, and map their sensitivity to affected systems.
- Correlate with network and data movement around the event for clones to internal repos and outbound transfers to cloud storage, paste sites, or email, and capture repository URLs or destinations if present.
- Trace how the binary arrived by checking recent downloads and file writes (curl/wget, package managers, GitHub releases), verify the binary’s hash and signer, and compare against known-good sources.

### False positive analysis

- A developer or security team member intentionally runs gitleaks to audit internal code for secrets during routine hygiene, producing local report artifacts and showing normal parent processes without exfiltration behavior.
- A user invokes gitleaks with --version or --help to validate installation or review usage, which generates a process start event but performs no scanning or credential access.

### Response and remediation

- If the run was unauthorized or executed from /tmp, %TEMP%, or a user profile, terminate gitleaks.exe/gitleaks, isolate the host from the network, and capture the binary path and hash for forensics.
- Quarantine report artifacts produced by the run (gitleaks.json, .sarif, .csv, and any zip archives) by securing copies for evidence, removing world-readable permissions, and deleting residual copies from the working directory, Downloads, repo folders, and CI workspaces after collection.
- Eradicate tooling by removing the dropped gitleaks binary and any wrapper scripts or CI job steps that invoke it, and enforce execution blocking for gitleaks in user-writable paths via application control or EDR policy.
- Immediately revoke and rotate any secrets confirmed in the reports or repository (cloud API keys, service tokens, SSH keys, credentials), purge them from repo history (git filter-repo/BFG) if present, redeploy updated secrets from the vault, and force password resets for affected accounts.
- Review git activity and data movement around the event for repo clones and exports, and inspect outbound transfers of report files to cloud storage, paste sites, or email; escalate to Incident Response and Legal if any report left the device or if production/customer credentials are exposed.
- Harden going forward by enabling approved server-side and CI secret scanning, enforcing pre-commit hooks, prohibiting PATs with broad scopes, restricting egress to paste/file-sharing sites, and blocking execution of portable binaries from temp and user-writable locations.
